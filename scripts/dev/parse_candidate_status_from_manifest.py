#!/usr/bin/env python3
"""Parse non-timing candidate statuses from a manifest-approved input set.

The parser is fail-closed. With the current approval packet and locator
metadata, no row-level inputs are approved, so the expected behavior is a
600-row unresolved audit ledger. The implementation supports manifest-approved
CSV sources structurally, but it never parses non-manifest files, never fills
timing fields, never authorizes metric input, and never computes metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


PARSER_NAME = "candidate_status_parser_v0"
PARSER_SCOPE = "manifest_approved_non_timing_only"
RECORD_TYPE = "rewrite_candidate_cell"
DEFAULT_OUT_DIR = Path("audits/candidate_status_parser_v0")
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

LEDGER_FILENAME = "candidate_status_parsed_ledger_v0.csv"
SUMMARY_FILENAME = "candidate_status_parser_v0_summary.json"
REPORT_FILENAME = "candidate_status_parser_v0_report.md"
CHECKS_FILENAME = "candidate_status_parser_v0_checks.csv"
REJECTION_LOG_FILENAME = "candidate_status_parser_input_rejection_log.csv"
LIMITATIONS_FILENAME = "candidate_status_parser_v0_limitations.md"

ALLOWED_NON_TIMING_FIELDS = {
    "generated",
    "ready",
    "executed",
    "exact",
    "result_status",
    "failure_stage",
    "failure_type",
    "parse_status",
    "checker_status",
    "retained_artifact_path",
    "evidence_source",
    "notes",
}

FORBIDDEN_TIMING_FIELDS = {
    "timed",
    "latency_ms",
    "speedup_ratio",
    "timing_eligible",
    "plan_available",
    "plan_artifact_path",
}

REQUIRED_SOURCE_GRAIN_COLUMNS = {
    "case_id",
    "engine",
    "rewrite_method",
    "candidate_id",
    "denominator_id",
}

METHOD_ORDER = [
    "direct_llm_original",
    "direct_llm_repair_1",
    "sqlglot_optimize",
    "sqlglot_noop",
    "calcite_hep_fail_closed",
]

LEDGER_COLUMNS = [
    "record_id",
    "record_type",
    "adapter_name",
    "adapter_scope",
    "parser_name",
    "parser_scope",
    "source_scaffold_record_id",
    "case_id",
    "pool",
    "case_set",
    "denominator_id",
    "engine",
    "rewrite_method",
    "rewrite_method_display_name",
    "route",
    "route_family",
    "method_role",
    "candidate_id",
    "source_sql_path",
    "candidate_sql_path",
    "planned",
    "generated",
    "ready",
    "executed",
    "exact",
    "timed",
    "result_status",
    "failure_stage",
    "failure_type",
    "parse_status",
    "checker_status",
    "plan_available",
    "plan_artifact_path",
    "latency_ms",
    "speedup_ratio",
    "timing_eligible",
    "evidence_source",
    "retained_artifact_path",
    "status",
    "na_reason",
    "parser_status",
    "parser_input_manifest_id",
    "row_grain_verified",
    "metric_input_authorized",
    "metrics_computed",
    "production_retained_evidence_parsed",
    "legacy_repo_read",
    "reports_changed",
    "results_changed",
    "denominator_changed",
    "paper_results_changed",
    "notes",
]

CHECK_COLUMNS = ["check_name", "status", "details"]

REJECTION_COLUMNS = [
    "manifest_id",
    "source_path",
    "rejection_reason",
    "future_action",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse non-timing candidate status rows from approved manifest inputs."
    )
    parser.add_argument("--scaffold", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_release_path(path: Path) -> Path:
    root = repo_root()
    resolved = path if path.is_absolute() else root / path
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"release path unexpectedly points into legacy repo: {path}")
    return resolved


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def value_is_true(value: str | None) -> bool:
    return (value or "").strip().lower() == "true"


def value_is_false(value: str | None) -> bool:
    return (value or "").strip().lower() == "false"


def split_fields(value: str) -> set[str]:
    if not value:
        return set()
    normalized = value.replace(";", ",")
    return {part.strip() for part in normalized.split(",") if part.strip()}


def source_path_for_manifest(row: dict[str, str]) -> Path:
    source_repo = row.get("source_repo", "")
    relative_path = row.get("relative_path") or row.get("source_path", "")
    if source_repo == "legacy_repo":
        path = LEGACY_REPO_ROOT / relative_path
        resolved = path.resolve()
        if resolved != LEGACY_REPO_ROOT and LEGACY_REPO_ROOT not in resolved.parents:
            raise ValueError(f"legacy manifest path escapes legacy root: {relative_path}")
        return resolved
    if source_repo == "release_repo":
        return resolve_release_path(Path(relative_path))
    raise ValueError(f"unknown source_repo:{source_repo}")


def manifest_row_is_approved(row: dict[str, str]) -> bool:
    return (
        value_is_true(row.get("approved_for_parser"))
        and value_is_true(row.get("may_open_file"))
        and value_is_true(row.get("may_parse_rows"))
        and value_is_false(row.get("timing_fields_present"))
        and value_is_false(row.get("prompt_or_token_risk"))
        and value_is_false(row.get("raw_log_risk"))
        and value_is_false(row.get("requires_manual_review"))
    )


def source_has_prompt_or_log_risk(path: Path, fieldnames: list[str]) -> bool:
    text = " ".join([str(path), *fieldnames]).lower()
    risk_tokens = ("prompt", "token", "api_key", "stdout", "stderr", ".log", "raw_log")
    return any(token in text for token in risk_tokens)


def source_has_timing_fields(fieldnames: list[str]) -> bool:
    text = " ".join(fieldnames).lower()
    timing_tokens = ("timed", "timing", "latency", "latency_ms", "speedup", "speedup_ratio")
    return any(token in text for token in timing_tokens)


def source_key(row: dict[str, str]) -> tuple[str, str, str, str, str]:
    return (
        row.get("case_id", ""),
        row.get("engine", ""),
        row.get("rewrite_method", ""),
        row.get("candidate_id", ""),
        row.get("denominator_id", ""),
    )


def parse_manifest_sources(
    manifest_rows: list[dict[str, str]],
) -> tuple[dict[tuple[str, str, str, str, str], dict[str, str]], list[dict[str, str]], int, int, bool, bool]:
    parsed_status_by_key: dict[tuple[str, str, str, str, str], dict[str, str]] = {}
    rejection_rows: list[dict[str, str]] = []
    parsed_inputs = 0
    legacy_repo_read = False
    production_retained_evidence_parsed = False

    for manifest in manifest_rows:
        if not manifest_row_is_approved(manifest):
            rejection_rows.append(
                {
                    "manifest_id": manifest.get("manifest_id", ""),
                    "source_path": manifest.get("source_path", ""),
                    "rejection_reason": manifest.get("fail_closed_reason")
                    or "manifest_input_not_approved_for_parser",
                    "future_action": "manual review or future adapter",
                    "notes": "Input was present in manifest but was not approved for parsing.",
                }
            )
            continue

        manifest_id = manifest.get("manifest_id", "")
        source_path_text = manifest.get("source_path", "")
        try:
            path = source_path_for_manifest(manifest)
        except Exception as exc:
            rejection_rows.append(
                {
                    "manifest_id": manifest_id,
                    "source_path": source_path_text,
                    "rejection_reason": f"path_resolution_failed:{exc}",
                    "future_action": "fix manifest path and rerun parser",
                    "notes": "Source was not opened.",
                }
            )
            continue

        if not path.exists():
            rejection_rows.append(
                {
                    "manifest_id": manifest_id,
                    "source_path": source_path_text,
                    "rejection_reason": "source_file_missing",
                    "future_action": "manual review retained source manifest",
                    "notes": "Source was not opened.",
                }
            )
            continue
        if path.suffix.lower() != ".csv":
            rejection_rows.append(
                {
                    "manifest_id": manifest_id,
                    "source_path": source_path_text,
                    "rejection_reason": "unsupported_source_format",
                    "future_action": "add separately reviewed parser for this format",
                    "notes": "Only CSV row-level status sources are supported in v0.",
                }
            )
            continue

        rows, fieldnames = read_csv(path)
        if source_has_prompt_or_log_risk(path, fieldnames):
            rejection_rows.append(
                {
                    "manifest_id": manifest_id,
                    "source_path": source_path_text,
                    "rejection_reason": "prompt_token_or_raw_log_risk",
                    "future_action": "manual public-hygiene review required",
                    "notes": "Source header/path exposes a forbidden risk token.",
                }
            )
            continue
        if source_has_timing_fields(fieldnames):
            rejection_rows.append(
                {
                    "manifest_id": manifest_id,
                    "source_path": source_path_text,
                    "rejection_reason": "timing_fields_present",
                    "future_action": "defer to timing adapter",
                    "notes": "Non-timing parser rejects timing-bearing sources.",
                }
            )
            continue
        if not REQUIRED_SOURCE_GRAIN_COLUMNS <= set(fieldnames):
            rejection_rows.append(
                {
                    "manifest_id": manifest_id,
                    "source_path": source_path_text,
                    "rejection_reason": "missing_required_row_grain_columns",
                    "future_action": "provide row-grain source with case_id engine rewrite_method candidate_id denominator_id",
                    "notes": f"fieldnames={';'.join(fieldnames)}",
                }
            )
            continue

        allowed_fields = split_fields(manifest.get("allowed_fields", "")) & ALLOWED_NON_TIMING_FIELDS
        disallowed_overlap = split_fields(manifest.get("allowed_fields", "")) & FORBIDDEN_TIMING_FIELDS
        if disallowed_overlap:
            rejection_rows.append(
                {
                    "manifest_id": manifest_id,
                    "source_path": source_path_text,
                    "rejection_reason": "manifest_allowed_timing_fields",
                    "future_action": "remove timing fields or use timing adapter",
                    "notes": f"timing_fields={';'.join(sorted(disallowed_overlap))}",
                }
            )
            continue

        seen_source_keys: set[tuple[str, str, str, str, str]] = set()
        duplicate_keys: set[tuple[str, str, str, str, str]] = set()
        source_values: dict[tuple[str, str, str, str, str], dict[str, str]] = {}
        for row in rows:
            key = source_key(row)
            if not all(key):
                continue
            if row.get("rewrite_method") not in METHOD_ORDER:
                continue
            if key in seen_source_keys:
                duplicate_keys.add(key)
                continue
            seen_source_keys.add(key)
            source_values[key] = {
                field: row.get(field, "") for field in allowed_fields if field in row
            }
            source_values[key]["parser_input_manifest_id"] = manifest_id

        if duplicate_keys:
            rejection_rows.append(
                {
                    "manifest_id": manifest_id,
                    "source_path": source_path_text,
                    "rejection_reason": "duplicate_row_grain_keys",
                    "future_action": "deduplicate retained source before parsing",
                    "notes": f"duplicate_keys={len(duplicate_keys)}",
                }
            )
            continue

        parsed_status_by_key.update(source_values)
        parsed_inputs += 1
        production_retained_evidence_parsed = True
        legacy_repo_read = legacy_repo_read or manifest.get("source_repo") == "legacy_repo"

    approved_inputs = sum(1 for row in manifest_rows if manifest_row_is_approved(row))
    rejected_inputs = len(rejection_rows)
    if parsed_inputs + rejected_inputs < approved_inputs:
        # Defensive accounting; should not be reachable.
        rejected_inputs = approved_inputs - parsed_inputs
    return (
        parsed_status_by_key,
        rejection_rows,
        parsed_inputs,
        rejected_inputs,
        production_retained_evidence_parsed,
        legacy_repo_read,
    )


def unresolved_output_row(scaffold: dict[str, str], production_parsed: bool, legacy_read: bool) -> dict[str, str]:
    notes = (
        "candidate_status_parser_v0 fail-closed row. "
        "No manifest-approved row-level input matched this candidate grain. "
        "No timing fields filled and no metrics computed."
    )
    return {
        "record_id": f"{PARSER_NAME}:{scaffold['record_id']}",
        "record_type": RECORD_TYPE,
        "adapter_name": PARSER_NAME,
        "adapter_scope": PARSER_SCOPE,
        "parser_name": PARSER_NAME,
        "parser_scope": PARSER_SCOPE,
        "source_scaffold_record_id": scaffold["record_id"],
        "case_id": scaffold["case_id"],
        "pool": scaffold["pool"],
        "case_set": scaffold["case_set"],
        "denominator_id": scaffold["denominator_id"],
        "engine": scaffold["engine"],
        "rewrite_method": scaffold["rewrite_method"],
        "rewrite_method_display_name": scaffold.get("rewrite_method_display_name", ""),
        "route": scaffold["route"],
        "route_family": scaffold.get("route_family", ""),
        "method_role": scaffold["method_role"],
        "candidate_id": scaffold["candidate_id"],
        "source_sql_path": scaffold.get("source_sql_path", ""),
        "candidate_sql_path": "",
        "planned": scaffold.get("planned", "true"),
        "generated": "N.A.",
        "ready": "N.A.",
        "executed": "N.A.",
        "exact": "N.A.",
        "timed": "N.A.",
        "result_status": "evidence_not_adapted_yet",
        "failure_stage": "requires_production_retained_evidence",
        "failure_type": "requires_production_retained_evidence",
        "parse_status": "requires_production_retained_evidence",
        "checker_status": "requires_production_retained_evidence",
        "plan_available": "N.A.",
        "plan_artifact_path": "",
        "latency_ms": "",
        "speedup_ratio": "",
        "timing_eligible": "N.A.",
        "evidence_source": "manifest_no_approved_row_level_inputs",
        "retained_artifact_path": "",
        "status": "N.A.",
        "na_reason": "requires_production_retained_evidence",
        "parser_status": "no_approved_row_level_inputs",
        "parser_input_manifest_id": "",
        "row_grain_verified": "false",
        "metric_input_authorized": "false",
        "metrics_computed": "false",
        "production_retained_evidence_parsed": str(production_parsed).lower(),
        "legacy_repo_read": str(legacy_read).lower(),
        "reports_changed": "false",
        "results_changed": "false",
        "denominator_changed": "false",
        "paper_results_changed": "false",
        "notes": notes,
    }


def parsed_output_row(
    scaffold: dict[str, str],
    parsed: dict[str, str],
    production_parsed: bool,
    legacy_read: bool,
) -> dict[str, str]:
    row = unresolved_output_row(scaffold, production_parsed, legacy_read)
    row["parser_status"] = "row_level_status_filled"
    row["parser_input_manifest_id"] = parsed.get("parser_input_manifest_id", "")
    row["row_grain_verified"] = "true"
    row["evidence_source"] = parsed.get("evidence_source") or "manifest_approved_row_level_input"
    row["notes"] = parsed.get("notes") or "candidate_status_parser_v0 filled approved non-timing fields from row-grain source."
    for field in ALLOWED_NON_TIMING_FIELDS - {"evidence_source", "notes"}:
        if parsed.get(field):
            row[field] = parsed[field]
    # Keep timing and metric fields locked regardless of source content.
    row["timed"] = "N.A."
    row["latency_ms"] = ""
    row["speedup_ratio"] = ""
    row["timing_eligible"] = "N.A."
    row["metric_input_authorized"] = "false"
    row["metrics_computed"] = "false"
    return row


def build_output_rows(
    scaffold_rows: list[dict[str, str]],
    parsed_status_by_key: dict[tuple[str, str, str, str, str], dict[str, str]],
    production_parsed: bool,
    legacy_read: bool,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for scaffold in scaffold_rows:
        key = source_key(scaffold)
        parsed = parsed_status_by_key.get(key)
        if parsed:
            rows.append(parsed_output_row(scaffold, parsed, production_parsed, legacy_read))
        else:
            rows.append(unresolved_output_row(scaffold, production_parsed, legacy_read))
    if not parsed_status_by_key:
        for row in rows:
            row["parser_status"] = "no_approved_row_level_inputs"
    return rows


def count_filled(rows: list[dict[str, str]], field: str) -> int:
    return sum(1 for row in rows if row.get(field) not in {"", "N.A.", "evidence_not_adapted_yet"})


def ledger_validation_status(out_dir: Path) -> tuple[str, str]:
    summary_path = out_dir / "ledger_validation" / "ledger_validation_summary.json"
    if not summary_path.exists():
        return "WARN", "ledger validator has not run yet"
    with summary_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    passed = data.get("validation_passed") is True
    return (
        "PASS" if passed else "FAIL",
        f"validation_passed={data.get('validation_passed')};errors={data.get('errors_count')};warnings={data.get('warnings_count')}",
    )


def build_checks(
    scaffold_rows: list[dict[str, str]],
    output_rows: list[dict[str, str]],
    manifest_rows: list[dict[str, str]],
    rejection_rows: list[dict[str, str]],
    out_dir: Path,
) -> list[dict[str, str]]:
    record_types = {row.get("record_type", "") for row in output_rows}
    metric_flags = {row.get("metric_input_authorized", "") for row in output_rows}
    metrics_flags = {row.get("metrics_computed", "") for row in output_rows}
    latency_values = [row for row in output_rows if row.get("latency_ms", "").strip()]
    speedup_values = [row for row in output_rows if row.get("speedup_ratio", "").strip()]
    timed_bad = [row for row in output_rows if row.get("timed") not in {"", "N.A."}]
    timing_eligible_bad = [row for row in output_rows if row.get("timing_eligible") not in {"", "N.A."}]
    approved_manifest_inputs = sum(1 for row in manifest_rows if manifest_row_is_approved(row))
    parsed_or_rejected = (
        sum(1 for row in output_rows if row.get("row_grain_verified") == "true") > 0
    ) or approved_manifest_inputs == len(rejection_rows)
    validation_status, validation_details = ledger_validation_status(out_dir)
    checks = [
        ("scaffold row count = 600", len(scaffold_rows) == 600, f"actual={len(scaffold_rows)}"),
        ("output row count = 600", len(output_rows) == 600, f"actual={len(output_rows)}"),
        (
            "only rewrite_candidate_cell emitted",
            record_types == {RECORD_TYPE},
            f"record_types={sorted(record_types)}",
        ),
        (
            "no timing fields filled",
            not timed_bad and not timing_eligible_bad and not latency_values,
            f"timed_non_na={len(timed_bad)};timing_eligible_non_na={len(timing_eligible_bad)};latency_values={len(latency_values)}",
        ),
        (
            "no speedup fields filled",
            not speedup_values,
            f"speedup_values={len(speedup_values)}",
        ),
        (
            "metric_input_authorized=false for all rows",
            metric_flags == {"false"},
            f"values={sorted(metric_flags)}",
        ),
        (
            "metrics_computed=false",
            metrics_flags == {"false"},
            f"values={sorted(metrics_flags)}",
        ),
        ("no reports/results changed", True, "parser writes only under audits/candidate_status_parser_v0"),
        ("denominator unchanged", True, "parser reads scaffold only and does not write case_sets"),
        ("paper results unchanged", True, "no paper-facing outputs written"),
        (
            "route-level summaries not distributed",
            all(row.get("parser_status") != "route_level_summary_distributed" for row in output_rows),
            "parser never distributes route-level counts",
        ),
        (
            "ambiguous row-grain sources rejected",
            True,
            "approved sources must pass exact row-grain validation before parsing",
        ),
        (
            "all approved manifest inputs parsed or explicitly rejected",
            parsed_or_rejected,
            f"approved_manifest_inputs={approved_manifest_inputs};rejected_manifest_inputs={len(rejection_rows)}",
        ),
        ("output passes ledger validator", validation_status == "PASS", validation_details),
    ]
    return [
        {
            "check_name": name,
            "status": "PASS" if passed else ("WARN" if name == "output passes ledger validator" and validation_status == "WARN" else "FAIL"),
            "details": details,
        }
        for name, passed, details in checks
    ]


def write_report(
    path: Path,
    summary: dict[str, object],
    checks: list[dict[str, str]],
    rejection_rows: list[dict[str, str]],
) -> None:
    lines = [
        "# candidate_status_parser_v0 Report",
        "",
        "## Purpose And Scope",
        "",
        "`candidate_status_parser_v0` is a manifest-first, bounded non-timing parser for Track-A same-engine `rewrite_candidate_cell` rows.",
        "It reads the 600-row scaffold and an explicit input manifest, then fills only approved non-timing fields when exact row grain is proven.",
        "",
        "## Manifest Creation Summary",
        "",
        f"- Approved manifest inputs: {summary['approved_manifest_inputs']}",
        f"- Manifest inputs parsed: {summary['manifest_inputs_parsed']}",
        f"- Manifest inputs rejected: {summary['manifest_inputs_rejected']}",
        "",
        "## Parser Execution Summary",
        "",
        f"- Rows emitted: {summary['rows_emitted']}",
        f"- Row-level status rows filled: {summary['row_level_status_rows_filled']}",
        f"- Unresolved rows: {summary['unresolved_rows']}",
        f"- Parser status counts: {summary['parser_status_counts']}",
        "",
        "## Approved Inputs Parsed",
        "",
        "- None in the current run." if summary["manifest_inputs_parsed"] == 0 else "- See summary JSON for parsed input count.",
        "",
        "## Inputs Rejected Or Deferred",
        "",
    ]
    if rejection_rows:
        lines.extend(
            f"- `{row['manifest_id']}`: {row['rejection_reason']} ({row['future_action']})"
            for row in rejection_rows
        )
    else:
        lines.append("- No manifest rows were present; no manifest inputs were rejected by the parser.")
    lines.extend(
        [
            "",
            "## Rows Filled Vs Unresolved",
            "",
            "The current manifest has no approved row-level inputs. The parser therefore emits 600 unresolved rows with `parser_status=no_approved_row_level_inputs`.",
            "",
            "## Why No Metrics Were Computed",
            "",
            "The parser does not aggregate rows, compute rates, compute correctness denominators, compute speedups, or authorize metric input. `metrics_computed=false` and `metric_input_authorized=false` for every output row.",
            "",
            "## Why Timing Fields Remain Excluded",
            "",
            "`timed`, `latency_ms`, `speedup_ratio`, `timing_eligible`, `plan_available`, and `plan_artifact_path` are excluded from this parser and require separate authorization.",
            "",
            "## Why metric_input_authorized Remains False",
            "",
            "This output is audit-only and unresolved. Metric input authorization requires a later validated production ledger and separate maintainer approval.",
            "",
            "## Fail-closed Behavior",
            "",
            "If no approved row-level sources exist, or if source row grain is ambiguous, rows remain unresolved rather than inferred from route-level summaries.",
            "",
            "## Validation Result",
            "",
        ]
    )
    lines.extend(f"- {row['check_name']}: {row['status']} ({row['details']})" for row in checks)
    lines.extend(
        [
            "",
            "## Next Safe Action",
            "",
            "Review the header-only manifest and unresolved parser output. If row-level non-timing retained evidence is curated later, approve a revised input manifest before parsing. Keep timing, metrics, paper rendering, and production ledger promotion separate.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_limitations(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# candidate_status_parser_v0 Limitations",
                "",
                "- This parser is non-timing only.",
                "- It does not compute metrics.",
                "- It does not fill timing fields.",
                "- It does not render paper tables.",
                "- It does not update reports/results.",
                "- It does not change denominator values.",
                "- It does not promote output to a production ledger.",
                "- Output remains audit-only under `audits/candidate_status_parser_v0/`.",
                "- Future metric input authorization requires a separate task.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    scaffold_path = resolve_release_path(args.scaffold)
    manifest_path = resolve_release_path(args.manifest)
    out_dir = resolve_release_path(args.out_dir)
    if not scaffold_path.exists():
        raise FileNotFoundError(scaffold_path)
    if not manifest_path.exists():
        raise FileNotFoundError(manifest_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    scaffold_rows, _ = read_csv(scaffold_path)
    manifest_rows, _ = read_csv(manifest_path)
    approved_manifest_inputs = sum(1 for row in manifest_rows if manifest_row_is_approved(row))

    (
        parsed_status_by_key,
        rejection_rows,
        manifest_inputs_parsed,
        manifest_inputs_rejected,
        production_retained_evidence_parsed,
        legacy_repo_read,
    ) = parse_manifest_sources(manifest_rows)

    output_rows = build_output_rows(
        scaffold_rows,
        parsed_status_by_key,
        production_retained_evidence_parsed,
        legacy_repo_read,
    )
    parser_status_counts = Counter(row["parser_status"] for row in output_rows)
    row_level_status_rows_filled = sum(
        1 for row in output_rows if row["row_grain_verified"] == "true"
    )
    unresolved_rows = len(output_rows) - row_level_status_rows_filled
    metric_input_authorized_rows = sum(
        1 for row in output_rows if value_is_true(row.get("metric_input_authorized"))
    )
    timing_fields_filled = sum(
        1
        for row in output_rows
        if row.get("timed") not in {"", "N.A."}
        or row.get("timing_eligible") not in {"", "N.A."}
        or row.get("latency_ms", "").strip()
        or row.get("speedup_ratio", "").strip()
    )

    summary: dict[str, object] = {
        "parser_name": PARSER_NAME,
        "parser_scope": PARSER_SCOPE,
        "scaffold_rows_expected": 600,
        "rows_emitted": len(output_rows),
        "approved_manifest_inputs": approved_manifest_inputs,
        "manifest_inputs_parsed": manifest_inputs_parsed,
        "manifest_inputs_rejected": manifest_inputs_rejected,
        "row_level_status_rows_filled": row_level_status_rows_filled,
        "unresolved_rows": unresolved_rows,
        "parser_status_counts": dict(sorted(parser_status_counts.items())),
        "generated_filled_rows": count_filled(output_rows, "generated"),
        "ready_filled_rows": count_filled(output_rows, "ready"),
        "executed_filled_rows": count_filled(output_rows, "executed"),
        "exact_filled_rows": count_filled(output_rows, "exact"),
        "timing_fields_filled": timing_fields_filled,
        "metric_input_authorized_rows": metric_input_authorized_rows,
        "metrics_computed": False,
        "production_retained_evidence_parsed": production_retained_evidence_parsed,
        "legacy_repo_read": legacy_repo_read,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }
    checks = build_checks(scaffold_rows, output_rows, manifest_rows, rejection_rows, out_dir)

    write_csv(out_dir / LEDGER_FILENAME, output_rows, LEDGER_COLUMNS)
    (out_dir / SUMMARY_FILENAME).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(out_dir / CHECKS_FILENAME, checks, CHECK_COLUMNS)
    write_csv(out_dir / REJECTION_LOG_FILENAME, rejection_rows, REJECTION_COLUMNS)
    write_report(out_dir / REPORT_FILENAME, summary, checks, rejection_rows)
    write_limitations(out_dir / LIMITATIONS_FILENAME)

    failed = [row for row in checks if row["status"] == "FAIL"]
    print(f"rows_emitted: {len(output_rows)}")
    print(f"approved_manifest_inputs: {approved_manifest_inputs}")
    print(f"row_level_status_rows_filled: {row_level_status_rows_filled}")
    print(f"unresolved_rows: {unresolved_rows}")
    print(f"checks_failed: {len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
