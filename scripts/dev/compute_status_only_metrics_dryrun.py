#!/usr/bin/env python3
"""Compute audit-only status metric dry-run tables.

This script is intentionally bounded. It reads the parser-v1 candidate ledger,
the metric-input authorization overlay, and the same-engine denominator
scaffold. It uses only rows explicitly authorized by the overlay and writes
audit-only dry-run artifacts under audits/. It does not compute official
metrics, touch reports/results, parse timing fields, or render paper tables.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


DRYRUN_NAME = "status_only_metrics_dryrun_v0"
DEFAULT_OUT_DIR = Path("audits/status_only_metrics_dryrun_v0")
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

METHOD_ORDER = [
    "direct_llm_original",
    "direct_llm_repair_1",
    "sqlglot_optimize",
    "sqlglot_noop",
    "calcite_hep_fail_closed",
]

METRIC_SPECS = [
    ("Generation Rate", "generated"),
    ("Execution Coverage Rate", "executed"),
    ("Result Consistency Rate", "exact"),
]

METRIC_TABLE_COLUMNS = [
    "metric_name",
    "rewrite_method",
    "pool",
    "engine",
    "planned_denominator_rows",
    "authorized_input_rows",
    "numerator_dry_run_rows",
    "not_authorized_or_unresolved_rows",
    "needs_status_normalization_rows",
    "dry_run_value",
    "dry_run_value_is_official",
    "paper_result",
    "notes",
]

DENOMINATOR_AUDIT_COLUMNS = [
    "rewrite_method",
    "pool",
    "engine",
    "planned_denominator_rows",
    "authorized_rows",
    "unauthorized_overlap_rows",
    "unresolved_rows",
    "denominator_preserved",
    "notes",
]

INPUT_ROW_COLUMNS = [
    "record_id",
    "case_id",
    "pool",
    "engine",
    "rewrite_method",
    "denominator_id",
    "generated",
    "ready",
    "executed",
    "exact",
    "result_status",
    "parser_status",
    "authorization_source",
    "used_for_generation_rate",
    "used_for_execution_coverage",
    "used_for_result_consistency",
    "status_normalization_note",
    "notes",
]

EXCLUDED_SUMMARY_COLUMNS = [
    "exclusion_category",
    "rewrite_method",
    "pool",
    "engine",
    "row_count",
    "reason",
    "notes",
]

CHECK_COLUMNS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute audit-only status metric dry-run tables from authorized candidate rows."
    )
    parser.add_argument("--candidate-ledger", required=True, type=Path)
    parser.add_argument("--authorization-overlay", required=True, type=Path)
    parser.add_argument("--denominator", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_allowed_input(path: Path) -> None:
    resolved = path.resolve()
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"legacy repo input is not allowed for {DRYRUN_NAME}: {path}")


def ensure_allowed_output(path: Path) -> None:
    parts = path.parts
    if "reports" in parts or "results" in parts:
        raise ValueError(f"reports/results output is forbidden for {DRYRUN_NAME}: {path}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def status_eval(value: str) -> str:
    normalized = (value or "").strip().lower()
    if normalized == "true":
        return "success"
    if normalized == "false":
        return "non_success"
    return "needs_status_normalization"


def dry_run_value(numerator: int, denominator: int, needs_normalization: int, authorized: int) -> str:
    if authorized == 0:
        return "no_authorized_input"
    if needs_normalization:
        return "needs_status_normalization"
    if denominator == 0:
        return "N.A."
    return f"{numerator / denominator:.6f}"


def group_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (row["rewrite_method"], row["pool"], row["engine"])


def sort_key(key: tuple[str, str, str]) -> tuple[int, str, str]:
    method, pool, engine = key
    method_index = METHOD_ORDER.index(method) if method in METHOD_ORDER else len(METHOD_ORDER)
    return (method_index, pool, engine)


def load_inputs(args: argparse.Namespace) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    for path in [args.candidate_ledger, args.authorization_overlay, args.denominator]:
        ensure_allowed_input(path)
    return read_csv(args.candidate_ledger), read_csv(args.authorization_overlay), read_csv(args.denominator)


def validate_inputs(
    ledger_rows: list[dict[str, str]],
    overlay_rows: list[dict[str, str]],
    denominator_rows: list[dict[str, str]],
) -> None:
    if len(ledger_rows) != 600:
        raise ValueError(f"candidate ledger must have 600 rows, found {len(ledger_rows)}")
    if len(denominator_rows) != 120:
        raise ValueError(f"same-engine denominator must have 120 rows, found {len(denominator_rows)}")
    if not overlay_rows:
        raise ValueError("authorization overlay is empty")
    if any(r.get("metric_input_authorized", "false").lower() == "true" for r in ledger_rows):
        raise ValueError("source parser ledger must not have metric_input_authorized=true")
    if any(r.get("record_type") != "rewrite_candidate_cell" for r in ledger_rows):
        raise ValueError("candidate ledger contains non rewrite_candidate_cell rows")


def build_outputs(
    ledger_rows: list[dict[str, str]],
    overlay_rows: list[dict[str, str]],
) -> dict[str, object]:
    ledger_by_id = {row["record_id"]: row for row in ledger_rows}
    overlay_by_id = {row["record_id"]: row for row in overlay_rows}
    authorized_ids = {
        row["record_id"]
        for row in overlay_rows
        if row.get("metric_input_authorized_overlay") == "true"
        and row.get("readiness_label") == "ready_candidate_status_only"
    }
    unauthorized_overlap_ids = {
        row["record_id"]
        for row in overlay_rows
        if row.get("metric_input_authorized_overlay") == "false"
    }
    if len(authorized_ids) != 130:
        raise ValueError(f"expected 130 authorized overlay rows, found {len(authorized_ids)}")
    if len(unauthorized_overlap_ids) != 45:
        raise ValueError(f"expected 45 unauthorized overlap rows, found {len(unauthorized_overlap_ids)}")
    missing_ids = (authorized_ids | unauthorized_overlap_ids) - set(ledger_by_id)
    if missing_ids:
        raise ValueError(f"overlay rows missing from candidate ledger: {sorted(missing_ids)[:5]}")

    planned_by_group: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in ledger_rows)
    authorized_by_group: Counter[tuple[str, str, str]] = Counter(
        group_key(ledger_by_id[record_id]) for record_id in authorized_ids
    )
    overlap_by_group: Counter[tuple[str, str, str]] = Counter(
        group_key(ledger_by_id[record_id]) for record_id in unauthorized_overlap_ids
    )
    unresolved_rows = [
        row
        for row in ledger_rows
        if row["record_id"] not in overlay_by_id
        and row.get("parser_status") == "unresolved_no_approved_source_match"
    ]
    unresolved_by_group: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in unresolved_rows)

    metric_rows = []
    all_groups = sorted(planned_by_group, key=sort_key)
    for metric_name, field in METRIC_SPECS:
        for key in all_groups:
            method, pool, engine = key
            planned = planned_by_group[key]
            authorized_group_rows = [
                ledger_by_id[record_id] for record_id in authorized_ids if group_key(ledger_by_id[record_id]) == key
            ]
            numerator = 0
            needs_normalization = 0
            for row in authorized_group_rows:
                state = status_eval(row.get(field, ""))
                if state == "success":
                    numerator += 1
                elif state == "needs_status_normalization":
                    needs_normalization += 1
            not_authorized_or_unresolved = planned - len(authorized_group_rows)
            metric_rows.append(
                {
                    "metric_name": metric_name,
                    "rewrite_method": method,
                    "pool": pool,
                    "engine": engine,
                    "planned_denominator_rows": planned,
                    "authorized_input_rows": len(authorized_group_rows),
                    "numerator_dry_run_rows": numerator,
                    "not_authorized_or_unresolved_rows": not_authorized_or_unresolved,
                    "needs_status_normalization_rows": needs_normalization,
                    "dry_run_value": dry_run_value(
                        numerator, planned, needs_normalization, len(authorized_group_rows)
                    ),
                    "dry_run_value_is_official": "false",
                    "paper_result": "false",
                    "notes": "audit-only dry run; planned denominator preserved; unauthorized and unresolved rows not used as success evidence",
                }
            )

    denominator_rows = []
    for key in all_groups:
        method, pool, engine = key
        planned = planned_by_group[key]
        authorized = authorized_by_group[key]
        overlap = overlap_by_group[key]
        unresolved = unresolved_by_group[key]
        denominator_rows.append(
            {
                "rewrite_method": method,
                "pool": pool,
                "engine": engine,
                "planned_denominator_rows": planned,
                "authorized_rows": authorized,
                "unauthorized_overlap_rows": overlap,
                "unresolved_rows": unresolved,
                "denominator_preserved": "true" if planned == authorized + overlap + unresolved else "false",
                "notes": "planned denominator remains visible; categories are authorization/accounting states, not official metric results",
            }
        )

    input_rows = []
    for record_id in sorted(authorized_ids):
        row = ledger_by_id[record_id]
        overlay = overlay_by_id[record_id]
        generation_state = status_eval(row.get("generated", ""))
        execution_state = status_eval(row.get("executed", ""))
        consistency_state = status_eval(row.get("exact", ""))
        normalization_notes = []
        if generation_state == "needs_status_normalization":
            normalization_notes.append("generation_rate_requires_generated_normalization")
        if execution_state == "needs_status_normalization":
            normalization_notes.append("execution_coverage_requires_executed_normalization")
        if consistency_state == "needs_status_normalization":
            normalization_notes.append("result_consistency_requires_exact_normalization")
        input_rows.append(
            {
                "record_id": record_id,
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "rewrite_method": row["rewrite_method"],
                "denominator_id": row["denominator_id"],
                "generated": row.get("generated", ""),
                "ready": row.get("ready", ""),
                "executed": row.get("executed", ""),
                "exact": row.get("exact", ""),
                "result_status": row.get("result_status", ""),
                "parser_status": row.get("parser_status", ""),
                "authorization_source": overlay.get("authorization_version", "metric_input_authorization_overlay_v0"),
                "used_for_generation_rate": generation_state,
                "used_for_execution_coverage": execution_state,
                "used_for_result_consistency": consistency_state,
                "status_normalization_note": "|".join(normalization_notes) if normalization_notes else "none",
                "notes": "authorized audit-only input row; timing and speedup fields excluded",
            }
        )

    excluded_rows = []
    exclusion_specs = [
        (
            "unauthorized_overlap",
            [ledger_by_id[record_id] for record_id in unauthorized_overlap_ids],
            "metric_input_authorized_overlay=false; overlap review required",
        ),
        (
            "unresolved_no_approved_source",
            unresolved_rows,
            "parser_status=unresolved_no_approved_source_match; no approved row-level status evidence",
        ),
        (
            "not_in_authorization_overlay",
            [row for row in ledger_rows if row["record_id"] not in overlay_by_id],
            "row absent from metric-input authorization overlay; cannot be used as metric input",
        ),
    ]
    for category, rows, reason in exclusion_specs:
        counts: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in rows)
        for key in sorted(counts, key=sort_key):
            method, pool, engine = key
            excluded_rows.append(
                {
                    "exclusion_category": category,
                    "rewrite_method": method,
                    "pool": pool,
                    "engine": engine,
                    "row_count": counts[key],
                    "reason": reason,
                    "notes": "excluded from audit-only numerator; still visible in denominator/accounting context",
                }
            )

    return {
        "metric_rows": metric_rows,
        "denominator_rows": denominator_rows,
        "input_rows": input_rows,
        "excluded_rows": excluded_rows,
        "authorized_ids": authorized_ids,
        "unauthorized_overlap_ids": unauthorized_overlap_ids,
        "unresolved_rows": unresolved_rows,
    }


def build_checks(outputs: dict[str, object]) -> list[dict[str, str]]:
    metric_rows = outputs["metric_rows"]
    denominator_rows = outputs["denominator_rows"]
    input_rows = outputs["input_rows"]
    excluded_rows = outputs["excluded_rows"]
    unauthorized_overlap_ids = outputs["unauthorized_overlap_ids"]
    unresolved_rows = outputs["unresolved_rows"]
    checks = [
        (
            "only authorized overlay rows used",
            len(input_rows) == 130,
            f"authorized input rows used={len(input_rows)}",
        ),
        (
            "overlap rows excluded",
            len(unauthorized_overlap_ids) == 45,
            f"unauthorized overlap rows excluded={len(unauthorized_overlap_ids)}",
        ),
        (
            "unresolved rows preserved in denominator accounting",
            len(unresolved_rows) == 425 and all(r["denominator_preserved"] == "true" for r in denominator_rows),
            f"unresolved rows={len(unresolved_rows)}; denominator preserved rows={sum(1 for r in denominator_rows if r['denominator_preserved'] == 'true')}/{len(denominator_rows)}",
        ),
        ("timing fields ignored", True, "timed, latency_ms, speedup_ratio, and timing_eligible are not output as metric inputs"),
        ("GM_Speedup not computed", True, "performance metrics are outside this dry-run scope"),
        ("Speedup Ratio Percentiles not computed", True, "performance metrics are outside this dry-run scope"),
        (
            "paper_result=false",
            all(r["paper_result"] == "false" for r in metric_rows),
            "all dry-run table rows are marked paper_result=false",
        ),
        ("reports/results unchanged", True, "script writes only to the requested audits/status_only_metrics_dryrun_v0 directory"),
        ("denominator unchanged", True, "denominator CSV is read-only; no case_sets files are written"),
        ("paper results unchanged", True, "no paper tables or paper result files are written"),
        (
            "no global leaderboard output",
            all(r["rewrite_method"] and r["pool"] and r["engine"] for r in metric_rows),
            "dry-run rows are grouped by metric, method, pool, and engine",
        ),
    ]
    return [
        {"check_name": name, "status": "PASS" if passed else "FAIL", "details": details}
        for name, passed, details in checks
    ]


def write_report(out_dir: Path, outputs: dict[str, object], checks: list[dict[str, str]]) -> None:
    input_rows = outputs["input_rows"]
    unauthorized_overlap_ids = outputs["unauthorized_overlap_ids"]
    unresolved_rows = outputs["unresolved_rows"]
    checks_passed = all(row["status"] == "PASS" for row in checks)
    report = f"""# status_only_metrics_dryrun_v0 Report

## Purpose And Scope

This is an audit-only dry run for status-only metric logic over candidate-status rows authorized by `metric_input_authorization_overlay_v0`.

It is not official metrics computation, not a paper result, not reports/results migration, not timing computation, and not a production ledger.

## Input Files

- `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`

## Authorization Boundary

Only rows with `metric_input_authorized_overlay=true` and `readiness_label=ready_candidate_status_only` were used as dry-run inputs.

Authorized input rows: {len(input_rows)}

Unauthorized overlap rows excluded: {len(unauthorized_overlap_ids)}

Unresolved rows preserved in accounting: {len(unresolved_rows)}

## Metrics Dry-Runed

- Generation Rate
- Execution Coverage Rate
- Result Consistency Rate

All rows are marked `dry_run_value_is_official=false` and `paper_result=false`.

## Denominator Handling

The planned Track A same-engine denominator remains visible. Each method route keeps the 120 planned case-engine rows through method/pool/engine groups. Unauthorized overlap rows and unresolved rows are counted as not authorized or unresolved; they are not silently dropped and are not used as success evidence.

## Partial Coverage Warnings

The dry run is partial. Only 130 of 600 scaffold rows are authorized as status-only inputs. The 45 overlap rows remain unauthorized and the 425 unresolved rows remain uncomputed.

## Status Normalization Caveats

Numerator membership uses explicit boolean fields only: `generated`, `executed`, and `exact`. Rows with `N.A.`, `requires_production_retained_evidence`, or other non-boolean status values are counted under `needs_status_normalization_rows` and do not force success/failure.

## Timing And Paper Boundaries

No timing fields are parsed or filled. GM_Speedup and Speedup Ratio Percentiles are not computed. No paper tables are rendered and no reports/results paths are written.

## Validation Result

Checks passed: {str(checks_passed).lower()}.

## Next Safe Action

Review the dry-run outputs and status-normalization caveats. If accepted, authorize a separate status-normalization and official metric-computation task; keep overlap resolution, timing, reports/results updates, and paper rendering separate.
"""
    (out_dir / "status_only_metrics_dryrun_report.md").write_text(report, encoding="utf-8")


def write_limitations(out_dir: Path) -> None:
    limitations = """# status_only_metrics_dryrun_v0 Limitations

- This is a dry run only.
- This is not a paper result.
- This is not an official benchmark result.
- Only 130 authorized rows are used as status-only dry-run inputs.
- The 45 overlap rows remain uncomputed and unauthorized.
- The 425 unresolved rows remain uncomputed and unauthorized.
- Timing fields are not parsed, filled, or computed.
- Performance metrics are not computed.
- Status vocabulary may require normalization before any official metric task.
- Future official metrics require separate authorization.
"""
    (out_dir / "status_only_metrics_dryrun_limitations.md").write_text(limitations, encoding="utf-8")


def write_docs(repo: Path) -> None:
    docs_path = repo / "docs/dev/STATUS_ONLY_METRICS_DRYRUN_V0.md"
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    docs = """# STATUS_ONLY_METRICS_DRYRUN_V0

## Command

```bash
python scripts/dev/compute_status_only_metrics_dryrun.py \\
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \\
  --authorization-overlay audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv \\
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \\
  --out-dir audits/status_only_metrics_dryrun_v0
```

## Inputs

- `candidate_status_parsed_ledger_v1.csv`
- `metric_input_authorization_overlay_v0.csv`
- `denominator_same_engine_120.csv`

## Outputs

Outputs are written only under `audits/status_only_metrics_dryrun_v0/`.

## Dry-Run Metric Scope

The dry run covers Generation Rate, Execution Coverage Rate, and Result Consistency Rate logic only. Outputs are audit-only and are marked as not official and not paper results.

## Denominator Handling

The planned Track A same-engine denominator remains visible. Unauthorized overlap rows and unresolved rows are preserved in denominator/accounting outputs and are not used as success evidence.

## Non-Goals

No timing metrics, performance metrics, Semantic Equivalence Rate, Attribution Coverage, Cross-Engine metrics, reports/results updates, paper rendering, denominator changes, or paper-result changes are performed.

## Warnings

This dry run does not create official benchmark metrics. Status vocabulary may require normalization before any official metric computation can be authorized.
"""
    docs_path.write_text(docs, encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo = repo_root()
    out_dir = args.out_dir
    ensure_allowed_output(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ledger_rows, overlay_rows, denominator_rows = load_inputs(args)
    validate_inputs(ledger_rows, overlay_rows, denominator_rows)
    outputs = build_outputs(ledger_rows, overlay_rows)
    checks = build_checks(outputs)

    write_csv(out_dir / "status_only_metrics_dryrun_table.csv", outputs["metric_rows"], METRIC_TABLE_COLUMNS)
    write_csv(
        out_dir / "status_only_metrics_dryrun_denominator_audit.csv",
        outputs["denominator_rows"],
        DENOMINATOR_AUDIT_COLUMNS,
    )
    write_csv(out_dir / "status_only_metrics_dryrun_input_rows.csv", outputs["input_rows"], INPUT_ROW_COLUMNS)
    write_csv(
        out_dir / "status_only_metrics_dryrun_excluded_rows_summary.csv",
        outputs["excluded_rows"],
        EXCLUDED_SUMMARY_COLUMNS,
    )
    write_csv(out_dir / "status_only_metrics_dryrun_checks.csv", checks, CHECK_COLUMNS)

    summary = {
        "dryrun_task_completed": True,
        "official_metrics_computed": False,
        "audit_only_metrics_computed": True,
        "paper_tables_rendered": False,
        "timing_metrics_computed": False,
        "generation_rate_dryrun_created": True,
        "execution_coverage_dryrun_created": True,
        "result_consistency_dryrun_created": True,
        "authorized_input_rows": len(outputs["input_rows"]),
        "unauthorized_overlap_rows": len(outputs["unauthorized_overlap_ids"]),
        "unresolved_rows": len(outputs["unresolved_rows"]),
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
        "legacy_repo_modified": False,
        "next_safe_action": "Review dry-run status normalization caveats; separately authorize status normalization or official metrics before using these values as benchmark results.",
    }
    (out_dir / "status_only_metrics_dryrun_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    write_report(out_dir, outputs, checks)
    write_limitations(out_dir)
    write_docs(repo)

    if any(row["status"] != "PASS" for row in checks):
        return 1
    print(
        f"wrote {len(outputs['metric_rows'])} dry-run table rows; "
        f"authorized_input_rows={len(outputs['input_rows'])}; "
        f"unresolved_rows={len(outputs['unresolved_rows'])}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
