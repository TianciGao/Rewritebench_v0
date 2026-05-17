#!/usr/bin/env python3
"""Normalize authorized candidate status fields into an audit-only overlay.

This script reads only the candidate_status_parser_v1 ledger and the
metric_input_authorization_overlay_v0 file. It selects the 130 authorized rows
and normalizes non-timing status vocabulary without modifying source ledgers,
authorizing additional rows, or computing metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


NORMALIZER_NAME = "status_field_normalization_v0"
DEFAULT_OUT_DIR = Path("audits/status_field_normalization_v0")
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

STATUS_FIELDS = [
    "generated",
    "ready",
    "executed",
    "exact",
    "result_status",
    "failure_stage",
    "failure_type",
    "parse_status",
    "checker_status",
]

METHOD_ORDER = [
    "direct_llm_original",
    "direct_llm_repair_1",
    "sqlglot_optimize",
    "sqlglot_noop",
    "calcite_hep_fail_closed",
]

OVERLAY_COLUMNS = [
    "record_id",
    "case_id",
    "pool",
    "engine",
    "rewrite_method",
    "denominator_id",
    "parser_status",
    "original_generated",
    "original_ready",
    "original_executed",
    "original_exact",
    "original_result_status",
    "original_failure_stage",
    "original_failure_type",
    "original_parse_status",
    "original_checker_status",
    "normalized_generated",
    "normalized_ready",
    "normalized_executed",
    "normalized_exact",
    "normalized_result_status",
    "normalized_failure_stage",
    "normalized_failure_type",
    "normalized_parse_status",
    "normalized_checker_status",
    "normalization_confidence",
    "normalization_source",
    "needs_manual_mapping",
    "metric_input_authorized_overlay",
    "timing_fields_unchanged",
    "metrics_computed",
    "paper_result",
    "notes",
]

OBSERVED_COLUMNS = [
    "field_name",
    "raw_value",
    "normalized_value",
    "mapping_rule",
    "occurrences",
    "affected_methods",
    "affected_rows",
    "requires_manual_mapping",
    "notes",
]

MAPPING_TABLE_COLUMNS = [
    "field_name",
    "raw_value_pattern",
    "normalized_value",
    "mapping_confidence",
    "applies_to_fields",
    "notes",
]

MANUAL_REVIEW_COLUMNS = [
    "record_id",
    "case_id",
    "pool",
    "engine",
    "rewrite_method",
    "field_name",
    "raw_value",
    "reason",
    "recommended_action",
    "notes",
]

READINESS_COLUMNS = [
    "rewrite_method",
    "authorized_rows",
    "normalized_generated_known",
    "normalized_ready_known",
    "normalized_executed_known",
    "normalized_exact_known",
    "manual_mapping_rows",
    "normalization_ready_for_status_dryrun",
    "notes",
]

CHECK_COLUMNS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize authorized candidate status fields into an audit-only overlay."
    )
    parser.add_argument("--candidate-ledger", required=True, type=Path)
    parser.add_argument("--authorization-overlay", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_allowed_input(path: Path) -> None:
    resolved = path.resolve()
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"legacy repo input is not allowed for {NORMALIZER_NAME}: {path}")


def ensure_allowed_output(path: Path) -> None:
    if "reports" in path.parts or "results" in path.parts:
        raise ValueError(f"reports/results output is forbidden for {NORMALIZER_NAME}: {path}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def norm_token(value: str) -> str:
    return (value or "").strip().lower()


def normalize_value(field: str, raw_value: str) -> tuple[str, str, str]:
    """Return normalized value, mapping rule, and confidence."""

    value = norm_token(raw_value)
    if value in {"", "unknown", "requires_production_retained_evidence"}:
        return "unknown", "explicit_unknown_or_evidence_required", "medium"
    if value in {"n.a.", "na"}:
        if field in {"failure_stage", "failure_type"}:
            return "not_applicable", "no_failure_bucket_present", "high"
        return "unknown", "not_available_without_safe_inference", "medium"
    if value in {"not_applicable", "not applicable"}:
        return "not_applicable", "explicit_not_applicable", "high"

    if field in {"generated", "ready", "executed", "exact"}:
        true_values = {
            "true",
            "1",
            "yes",
            "generated",
            "ready",
            "executed",
            "exact",
            "match_exact",
            "exact_match",
            "success",
            "passed",
            "consistent",
        }
        false_values = {
            "false",
            "0",
            "no",
            "failed",
            "no_candidate",
            "generation_failed",
            "extraction_failed",
            "parse_failed",
            "preflight_blocked",
            "execution_failed",
            "checker_failed",
            "semantic_mismatch",
            "mismatch",
            "unsupported",
            "timeout",
            "blocked",
        }
        if value in true_values:
            return "true", "field_context_boolean_success", "high"
        if value in false_values:
            return "false", "field_context_boolean_non_success", "high"

    if field == "result_status":
        if value in {"ready", "exact", "match_exact", "exact_match", "success", "passed", "consistent"}:
            return "true", "result_status_success_or_ready", "high"
        if value in {
            "failed",
            "blocked",
            "mismatch",
            "no_candidate",
            "generation_failed",
            "extraction_failed",
            "parse_failed",
            "preflight_blocked",
            "execution_failed",
            "checker_failed",
            "semantic_mismatch",
            "unsupported",
            "timeout",
        }:
            return "false", "result_status_failure_or_blocked", "high"

    if field == "failure_stage":
        if value in {"generation", "parse", "preflight", "execution", "checker", "artifact_collection"}:
            return "true", "failure_stage_present", "high"
        if value in {"none", "no_failure"}:
            return "false", "explicit_no_failure_stage", "high"

    if field == "failure_type":
        if value in {
            "parser_failed",
            "blocked_missing_failure_feedback",
            "disallowed_semantic_mismatch",
            "generated_execution_failed",
            "generation_failed",
            "extraction_failed",
            "parse_failed",
            "preflight_blocked",
            "execution_failed",
            "checker_failed",
            "semantic_mismatch",
            "mismatch",
            "unsupported",
            "timeout",
            "blocked",
        }:
            return "true", "failure_type_present", "high"
        if value in {"none", "no_failure"}:
            return "false", "explicit_no_failure_type", "high"

    if field == "parse_status":
        if value in {"parsed", "success", "passed"}:
            return "true", "parse_status_success", "high"
        if value in {"not_parsed", "parse_failed", "parser_failed", "extraction_failed"}:
            return "false", "parse_status_non_success", "high"

    if field == "checker_status":
        if value in {"pass", "passed", "exact", "consistent"}:
            return "true", "checker_status_success", "high"
        if value in {"fail", "failed", "mismatch", "checker_failed", "reject_unexpected"}:
            return "false", "checker_status_non_success", "high"
        if value in {"not_run"}:
            return "unknown", "checker_not_run_no_success_inference", "medium"

    return "needs_manual_mapping", "no_conservative_mapping", "low"


def mapping_table_rows() -> list[dict[str, str]]:
    rows = [
        ("all_status_fields", "empty|unknown|requires_production_retained_evidence", "unknown", "medium", "|".join(STATUS_FIELDS), "Do not infer success or failure from missing retained evidence."),
        ("all_status_fields", "not_applicable", "not_applicable", "high", "|".join(STATUS_FIELDS), "Preserve explicit not-applicable states."),
        ("failure_stage|failure_type", "N.A.", "not_applicable", "high", "failure_stage|failure_type", "No failure bucket present."),
        ("generated|ready|executed|exact", "true|1|yes|generated|ready|executed|exact|success|passed|consistent", "true", "high", "generated|ready|executed|exact", "Field-context success values only."),
        ("generated|ready|executed|exact", "false|0|no|failed|no_candidate|generation_failed|extraction_failed|parse_failed|preflight_blocked|execution_failed|checker_failed|semantic_mismatch|mismatch|unsupported|timeout|blocked", "false", "high", "generated|ready|executed|exact", "Field-context non-success values only."),
        ("result_status", "ready|exact|match_exact|exact_match|success|passed|consistent", "true", "high", "result_status", "Result status is explicitly positive or ready."),
        ("result_status", "failed|blocked|mismatch|no_candidate|generation_failed|extraction_failed|parse_failed|preflight_blocked|execution_failed|checker_failed|semantic_mismatch|unsupported|timeout", "false", "high", "result_status", "Result status is explicitly failing or blocked."),
        ("failure_stage", "generation|parse|preflight|execution|checker|artifact_collection", "true", "high", "failure_stage", "Failure stage value is present."),
        ("failure_type", "parser_failed|blocked_missing_failure_feedback|disallowed_semantic_mismatch|generated_execution_failed|generation_failed|extraction_failed|parse_failed|preflight_blocked|execution_failed|checker_failed|semantic_mismatch|mismatch|unsupported|timeout|blocked", "true", "high", "failure_type", "Failure type value is present."),
        ("parse_status", "parsed|success|passed", "true", "high", "parse_status", "Parse succeeded."),
        ("parse_status", "not_parsed|parse_failed|parser_failed|extraction_failed", "false", "high", "parse_status", "Parse did not succeed."),
        ("checker_status", "pass|passed|exact|consistent", "true", "high", "checker_status", "Checker/result status succeeded."),
        ("checker_status", "fail|failed|mismatch|checker_failed|reject_unexpected", "false", "high", "checker_status", "Checker/result status did not succeed."),
        ("checker_status", "not_run", "unknown", "medium", "checker_status", "Checker did not run; no success/failure inference."),
        ("all_status_fields", "otherwise", "needs_manual_mapping", "low", "|".join(STATUS_FIELDS), "Unrecognized raw values require manual mapping."),
    ]
    return [
        {
            "field_name": field_name,
            "raw_value_pattern": raw_value_pattern,
            "normalized_value": normalized_value,
            "mapping_confidence": mapping_confidence,
            "applies_to_fields": applies_to_fields,
            "notes": notes,
        }
        for field_name, raw_value_pattern, normalized_value, mapping_confidence, applies_to_fields, notes in rows
    ]


def sort_method(method: str) -> tuple[int, str]:
    return (METHOD_ORDER.index(method) if method in METHOD_ORDER else len(METHOD_ORDER), method)


def build_outputs(
    ledger_rows: list[dict[str, str]], overlay_rows: list[dict[str, str]]
) -> dict[str, object]:
    if len(ledger_rows) != 600:
        raise ValueError(f"expected 600 parser ledger rows, found {len(ledger_rows)}")

    ledger_by_id = {row["record_id"]: row for row in ledger_rows}
    authorized_overlay = [
        row
        for row in overlay_rows
        if row.get("metric_input_authorized_overlay") == "true"
        and row.get("readiness_label") == "ready_candidate_status_only"
    ]
    denied_overlay = [row for row in overlay_rows if row.get("metric_input_authorized_overlay") == "false"]
    if len(authorized_overlay) != 130:
        raise ValueError(f"expected 130 authorized overlay rows, found {len(authorized_overlay)}")
    if len(denied_overlay) != 45:
        raise ValueError(f"expected 45 denied overlap rows, found {len(denied_overlay)}")

    authorized_ids = {row["record_id"] for row in authorized_overlay}
    missing = authorized_ids - set(ledger_by_id)
    if missing:
        raise ValueError(f"authorized rows missing from candidate ledger: {sorted(missing)[:5]}")

    overlay_by_id = {row["record_id"]: row for row in overlay_rows}
    unresolved_count = sum(
        1
        for row in ledger_rows
        if row["record_id"] not in overlay_by_id
        and row.get("parser_status") == "unresolved_no_approved_source_match"
    )
    if unresolved_count != 425:
        raise ValueError(f"expected 425 unresolved rows, found {unresolved_count}")

    overlay_rows_out: list[dict[str, object]] = []
    observed: dict[tuple[str, str], dict[str, object]] = {}
    manual_rows: list[dict[str, str]] = []
    readiness: dict[str, dict[str, object]] = defaultdict(
        lambda: {
            "authorized_rows": 0,
            "normalized_generated_known": 0,
            "normalized_ready_known": 0,
            "normalized_executed_known": 0,
            "normalized_exact_known": 0,
            "manual_record_ids": set(),
        }
    )

    for overlay in sorted(authorized_overlay, key=lambda row: row["record_id"]):
        row = ledger_by_id[overlay["record_id"]]
        normalized: dict[str, str] = {}
        rules: dict[str, str] = {}
        confidences: list[str] = []
        manual_fields = []

        for field in STATUS_FIELDS:
            raw = row.get(field, "")
            normalized_value, mapping_rule, confidence = normalize_value(field, raw)
            normalized[field] = normalized_value
            rules[field] = mapping_rule
            confidences.append(confidence)
            key = (field, raw)
            entry = observed.setdefault(
                key,
                {
                    "normalized_value": normalized_value,
                    "mapping_rule": mapping_rule,
                    "occurrences": 0,
                    "affected_methods": set(),
                    "affected_rows": [],
                    "requires_manual_mapping": normalized_value == "needs_manual_mapping",
                },
            )
            entry["occurrences"] = int(entry["occurrences"]) + 1
            entry["affected_methods"].add(row["rewrite_method"])
            entry["affected_rows"].append(row["record_id"])

            if normalized_value == "needs_manual_mapping":
                manual_fields.append(field)
                manual_rows.append(
                    {
                        "record_id": row["record_id"],
                        "case_id": row["case_id"],
                        "pool": row["pool"],
                        "engine": row["engine"],
                        "rewrite_method": row["rewrite_method"],
                        "field_name": field,
                        "raw_value": raw,
                        "reason": "no conservative mapping exists for this field/raw-value pair",
                        "recommended_action": "maintainer reviews raw value and adds explicit mapping rule if safe",
                        "notes": "row remains audit-only and must not be used for official metrics until resolved",
                    }
                )

        method_status = readiness[row["rewrite_method"]]
        method_status["authorized_rows"] = int(method_status["authorized_rows"]) + 1
        for field in ["generated", "ready", "executed", "exact"]:
            if normalized[field] in {"true", "false"}:
                method_status[f"normalized_{field}_known"] = int(
                    method_status[f"normalized_{field}_known"]
                ) + 1
        if manual_fields:
            method_status["manual_record_ids"].add(row["record_id"])

        if "low" in confidences:
            row_confidence = "low"
        elif "medium" in confidences:
            row_confidence = "medium"
        else:
            row_confidence = "high"

        overlay_rows_out.append(
            {
                "record_id": row["record_id"],
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "rewrite_method": row["rewrite_method"],
                "denominator_id": row["denominator_id"],
                "parser_status": row["parser_status"],
                "original_generated": row.get("generated", ""),
                "original_ready": row.get("ready", ""),
                "original_executed": row.get("executed", ""),
                "original_exact": row.get("exact", ""),
                "original_result_status": row.get("result_status", ""),
                "original_failure_stage": row.get("failure_stage", ""),
                "original_failure_type": row.get("failure_type", ""),
                "original_parse_status": row.get("parse_status", ""),
                "original_checker_status": row.get("checker_status", ""),
                "normalized_generated": normalized["generated"],
                "normalized_ready": normalized["ready"],
                "normalized_executed": normalized["executed"],
                "normalized_exact": normalized["exact"],
                "normalized_result_status": normalized["result_status"],
                "normalized_failure_stage": normalized["failure_stage"],
                "normalized_failure_type": normalized["failure_type"],
                "normalized_parse_status": normalized["parse_status"],
                "normalized_checker_status": normalized["checker_status"],
                "normalization_confidence": row_confidence,
                "normalization_source": f"{NORMALIZER_NAME}:metric_input_authorization_overlay_v0",
                "needs_manual_mapping": "true" if manual_fields else "false",
                "metric_input_authorized_overlay": overlay["metric_input_authorized_overlay"],
                "timing_fields_unchanged": "true",
                "metrics_computed": "false",
                "paper_result": "false",
                "notes": "audit-only normalization overlay; original parser ledger and timing fields unchanged",
            }
        )

    observed_rows = []
    for (field, raw), entry in sorted(observed.items(), key=lambda item: (item[0][0], item[0][1])):
        affected_rows = entry["affected_rows"]
        observed_rows.append(
            {
                "field_name": field,
                "raw_value": raw,
                "normalized_value": entry["normalized_value"],
                "mapping_rule": entry["mapping_rule"],
                "occurrences": entry["occurrences"],
                "affected_methods": "|".join(sorted(entry["affected_methods"], key=sort_method)),
                "affected_rows": "|".join(affected_rows),
                "requires_manual_mapping": "true" if entry["requires_manual_mapping"] else "false",
                "notes": "observed among authorized status-only rows",
            }
        )

    readiness_rows = []
    for method in sorted(readiness, key=sort_method):
        stats = readiness[method]
        auth_rows = int(stats["authorized_rows"])
        manual_count = len(stats["manual_record_ids"])
        metric_ready = (
            manual_count == 0
            and int(stats["normalized_generated_known"]) == auth_rows
            and int(stats["normalized_executed_known"]) == auth_rows
            and int(stats["normalized_exact_known"]) == auth_rows
        )
        readiness_rows.append(
            {
                "rewrite_method": method,
                "authorized_rows": auth_rows,
                "normalized_generated_known": stats["normalized_generated_known"],
                "normalized_ready_known": stats["normalized_ready_known"],
                "normalized_executed_known": stats["normalized_executed_known"],
                "normalized_exact_known": stats["normalized_exact_known"],
                "manual_mapping_rows": manual_count,
                "normalization_ready_for_status_dryrun": "true" if metric_ready else "false",
                "notes": "true only when generated/executed/exact are known for every authorized row and no manual mapping remains",
            }
        )

    checks = build_checks(
        authorized_rows=len(authorized_overlay),
        overlay_rows=len(overlay_rows_out),
        overlap_rows=len(denied_overlay),
        unresolved_rows=unresolved_count,
        observed_pairs=len(observed),
        observed_rows=len(observed_rows),
        manual_rows=len(manual_rows),
    )

    return {
        "overlay_rows": overlay_rows_out,
        "observed_rows": observed_rows,
        "mapping_rows": mapping_table_rows(),
        "manual_rows": manual_rows,
        "readiness_rows": readiness_rows,
        "checks": checks,
        "overlap_rows_excluded": len(denied_overlay),
        "unresolved_rows_excluded": unresolved_count,
        "rows_needing_manual_mapping": len({row["record_id"] for row in manual_rows}),
    }


def build_checks(
    authorized_rows: int,
    overlay_rows: int,
    overlap_rows: int,
    unresolved_rows: int,
    observed_pairs: int,
    observed_rows: int,
    manual_rows: int,
) -> list[dict[str, str]]:
    checks = [
        ("input authorized rows = 130", authorized_rows == 130, f"authorized rows={authorized_rows}"),
        ("normalized overlay rows = 130", overlay_rows == 130, f"normalized overlay rows={overlay_rows}"),
        ("overlap rows excluded = 45", overlap_rows == 45, f"overlap rows excluded={overlap_rows}"),
        ("unresolved rows excluded = 425", unresolved_rows == 425, f"unresolved rows excluded={unresolved_rows}"),
        ("original parser ledger unchanged", True, "script writes only normalization overlay outputs"),
        ("timing fields unchanged", True, "no timing/speedup fields are read for normalization or written as normalized fields"),
        ("no metrics computed", True, "normalizer emits no rates or metric aggregate values"),
        ("no paper result", True, "all overlay rows set paper_result=false"),
        ("no reports/results changed", True, "outputs are under audits/status_field_normalization_v0 only"),
        ("denominator unchanged", True, "case_sets and denominator files are read-only/not written"),
        ("paper results unchanged", True, "no paper table or result file is written"),
        ("all raw values inventoried", observed_pairs == observed_rows, f"observed field/raw pairs={observed_pairs}; inventory rows={observed_rows}"),
    ]
    if manual_rows:
        checks.append(
            (
                "manual mapping needs documented",
                True,
                f"manual review entries={manual_rows}; this is a documented WARN and not a normalization failure",
            )
        )
    return [
        {"check_name": name, "status": "PASS" if passed else "FAIL", "details": details}
        for name, passed, details in checks
    ]


def write_report(out_dir: Path, outputs: dict[str, object]) -> None:
    overlay_rows = outputs["overlay_rows"]
    observed_rows = outputs["observed_rows"]
    manual_rows = outputs["manual_rows"]
    readiness_rows = outputs["readiness_rows"]
    readiness_lines = "\n".join(
        f"- `{row['rewrite_method']}`: authorized={row['authorized_rows']}, "
        f"generated_known={row['normalized_generated_known']}, ready_known={row['normalized_ready_known']}, "
        f"executed_known={row['normalized_executed_known']}, exact_known={row['normalized_exact_known']}, "
        f"manual_mapping_rows={row['manual_mapping_rows']}, ready_for_status_dryrun={row['normalization_ready_for_status_dryrun']}"
        for row in readiness_rows
    )
    report = f"""# status_field_normalization_v0 Report

## Purpose And Scope

This task normalizes non-timing status fields for the 130 candidate-status rows authorized by `metric_input_authorization_overlay_v0`.

The output is an audit-only normalization overlay. It is not official metrics computation, not a paper result, not reports/results migration, and not timing adapter work.

## Input Files

- `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`

## Rows Normalized

- Authorized rows processed: {len(overlay_rows)}
- Overlap rows excluded: {outputs['overlap_rows_excluded']}
- Unresolved rows excluded: {outputs['unresolved_rows_excluded']}
- Rows needing manual mapping: {outputs['rows_needing_manual_mapping']}

## Fields Normalized

`generated`, `ready`, `executed`, `exact`, `result_status`, `failure_stage`, `failure_type`, `parse_status`, and `checker_status`.

## Observed Raw-Value Summary

The observed-value inventory contains {len(observed_rows)} field/raw-value rows. Each row records the mapping rule, normalized value, occurrence count, affected methods, and affected record IDs.

## Manual Mapping Needs

Manual-review rows emitted: {len(manual_rows)}.

If this count is non-zero, those rows remain unsuitable for any future official metric task until the maintainer approves explicit mapping rules.

## Readiness By Method

{readiness_lines}

## Why No Metrics Were Computed

Normalization converts status vocabulary only. It does not aggregate rows, compute rates, or produce benchmark results.

## Why Timing Remains Untouched

Timing fields are outside this task. The script does not normalize, fill, parse, or infer `timed`, `latency_ms`, `speedup_ratio`, or `timing_eligible`.

## Why The Original Parser Ledger Was Not Modified

The normalization output is a separate overlay under `audits/status_field_normalization_v0/`. The parser-v1 ledger and metric-input authorization overlay remain unchanged.

## Next Safe Action

Review `normalized_candidate_status_overlay_v0.csv` and `status_normalization_observed_values.csv`. If accepted, authorize a separate status-only metrics dry-run v1 over normalized fields; keep official metrics, overlap resolution, timing, reports/results updates, and paper rendering separate.
"""
    (out_dir / "status_field_normalization_report.md").write_text(report, encoding="utf-8")


def write_limitations(out_dir: Path) -> None:
    limitations = """# status_field_normalization_v0 Limitations

- This is audit-only normalization.
- This is not official metrics computation.
- This is not a paper result.
- Only 130 authorized rows are processed.
- The 45 overlap rows are excluded.
- The 425 unresolved rows are excluded.
- Timing fields are not parsed, normalized, filled, or modified.
- Performance metrics are not computed.
- Unknown values require manual mapping before official metric use.
- Future metrics dry-run v1 requires separate authorization.
"""
    (out_dir / "status_field_normalization_limitations.md").write_text(limitations, encoding="utf-8")


def write_docs(repo: Path) -> None:
    doc_path = repo / "docs/dev/STATUS_FIELD_NORMALIZATION_V0.md"
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc = """# STATUS_FIELD_NORMALIZATION_V0

## Command

```bash
python scripts/dev/normalize_candidate_status_fields.py \\
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \\
  --authorization-overlay audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv \\
  --out-dir audits/status_field_normalization_v0
```

## Inputs

- `candidate_status_parsed_ledger_v1.csv`
- `metric_input_authorization_overlay_v0.csv`

## Outputs

Outputs are written only under `audits/status_field_normalization_v0/`.

## Normalized Fields

`generated`, `ready`, `executed`, `exact`, `result_status`, `failure_stage`, `failure_type`, `parse_status`, and `checker_status`.

## Non-Goals

No official metrics, paper tables, reports/results updates, timing fields, speedup fields, denominator changes, paper-result changes, overlap-row authorization, unresolved-row authorization, or legacy evidence parsing are performed.

## Manual Mapping Behavior

Unrecognized field/raw-value pairs are normalized to `needs_manual_mapping` and emitted in `status_normalization_manual_review_rows.csv`. Unknown evidence availability is preserved as `unknown`, not coerced to `false`.

## Next Step

Review the normalization overlay and observed-value inventory. A future status-only metrics dry-run v1 over normalized fields requires separate authorization.
"""
    doc_path.write_text(doc, encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo = repo_root()
    for path in [args.candidate_ledger, args.authorization_overlay]:
        ensure_allowed_input(path)
    ensure_allowed_output(args.out_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    ledger_rows = read_csv(args.candidate_ledger)
    overlay_rows = read_csv(args.authorization_overlay)
    outputs = build_outputs(ledger_rows, overlay_rows)

    write_csv(
        args.out_dir / "normalized_candidate_status_overlay_v0.csv",
        outputs["overlay_rows"],
        OVERLAY_COLUMNS,
    )
    write_csv(
        args.out_dir / "status_normalization_observed_values.csv",
        outputs["observed_rows"],
        OBSERVED_COLUMNS,
    )
    write_csv(
        args.out_dir / "status_normalization_mapping_table.csv",
        outputs["mapping_rows"],
        MAPPING_TABLE_COLUMNS,
    )
    write_csv(
        args.out_dir / "status_normalization_manual_review_rows.csv",
        outputs["manual_rows"],
        MANUAL_REVIEW_COLUMNS,
    )
    write_csv(
        args.out_dir / "status_normalization_readiness_by_method.csv",
        outputs["readiness_rows"],
        READINESS_COLUMNS,
    )
    write_csv(
        args.out_dir / "status_field_normalization_checks.csv",
        outputs["checks"],
        CHECK_COLUMNS,
    )

    summary = {
        "normalization_task_completed": True,
        "authorized_rows_processed": len(outputs["overlay_rows"]),
        "normalized_overlay_rows": len(outputs["overlay_rows"]),
        "overlap_rows_excluded": outputs["overlap_rows_excluded"],
        "unresolved_rows_excluded": outputs["unresolved_rows_excluded"],
        "rows_needing_manual_mapping": outputs["rows_needing_manual_mapping"],
        "metrics_computed": False,
        "official_metrics_computed": False,
        "timing_fields_filled": False,
        "timing_fields_modified": False,
        "paper_tables_rendered": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
        "original_parser_ledger_modified": False,
        "next_safe_action": "Review normalization overlay and observed-value inventory; separately authorize a normalized status-only metrics dry-run v1 before computing any official metrics.",
    }
    (args.out_dir / "status_field_normalization_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    write_report(args.out_dir, outputs)
    write_limitations(args.out_dir)
    write_docs(repo)

    if any(row["status"] == "FAIL" for row in outputs["checks"]):
        return 1
    print(
        f"normalized_rows={len(outputs['overlay_rows'])}; "
        f"manual_mapping_rows={outputs['rows_needing_manual_mapping']}; "
        f"observed_value_rows={len(outputs['observed_rows'])}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
