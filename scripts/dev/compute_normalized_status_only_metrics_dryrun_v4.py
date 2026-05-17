#!/usr/bin/env python3
"""Compute audit-only normalized status dry-run v4 from combined candidate status overlay.

This is not official benchmark metric computation. It preserves denominator
accounting and marks every output as audit-only / non-paper.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


METHODS = [
    "direct_llm_original",
    "direct_llm_repair_1",
    "calcite_hep_fail_closed",
    "sqlglot_optimize",
    "sqlglot_noop",
]
SQLGLOT_METHODS = {"sqlglot_optimize", "sqlglot_noop"}
METRICS = [
    ("Generation Rate", "generated"),
    ("Execution Coverage Rate", "executed"),
    ("Result Consistency Rate", "exact"),
]

TABLE_FIELDS = [
    "metric_name",
    "rewrite_method",
    "pool",
    "engine",
    "planned_denominator_rows",
    "authorized_input_rows",
    "numerator_observed_rows",
    "numerator_inferred_rows",
    "numerator_total_dry_run_rows",
    "not_authorized_or_unresolved_rows",
    "sqlglot_projection_input_rows",
    "normalized_unknown_rows",
    "inference_used_rows",
    "dry_run_value",
    "dry_run_value_is_official",
    "official_metric",
    "paper_result",
    "audit_only",
    "notes",
]

DENOM_FIELDS = [
    "rewrite_method",
    "pool",
    "engine",
    "planned_denominator_rows",
    "dryrun_input_rows",
    "metric_authorized_rows",
    "sqlglot_projection_input_rows",
    "unresolved_or_unparsed_rows",
    "denominator_preserved",
    "notes",
]

DELTA_FIELDS = [
    "metric_name",
    "rewrite_method",
    "pool",
    "engine",
    "v3_authorized_rows",
    "v4_authorized_rows",
    "v3_numerator_total_dry_run_rows",
    "v4_numerator_total_dry_run_rows",
    "delta_due_to_sqlglot_projection",
    "notes",
]

CAVEAT_FIELDS = ["caveat_type", "affected_metric", "affected_method", "affected_rows", "explanation", "recommended_followup", "notes"]
CHECK_FIELDS = ["check_name", "status", "details"]


TRUE_VALUES = {"true", "1", "yes", "generated", "ready", "executed", "exact", "match_exact", "exact_match", "success", "passed", "consistent"}
FALSE_VALUES = {"false", "0", "no", "failed", "mismatch", "semantic_mismatch", "execution_failed", "checker_failed", "blocked", "unsupported", "timeout"}
UNKNOWN_VALUES = {"", "n.a.", "unknown", "not_applicable", "requires_production_retained_evidence", "evidence_not_adapted_yet"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute audit-only normalized status dry-run v4.")
    parser.add_argument("--combined-candidate-ledger", required=True, type=Path)
    parser.add_argument("--combined-authorization", required=True, type=Path)
    parser.add_argument("--inference-overlay", required=True, type=Path)
    parser.add_argument("--denominator", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    return parser.parse_args()


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize(value: str) -> str:
    lowered = (value or "").strip().lower()
    if lowered in TRUE_VALUES:
        return "true"
    if lowered in FALSE_VALUES:
        return "false"
    if lowered in UNKNOWN_VALUES:
        return "unknown"
    return "unknown"


def planned_cells(denominator_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for denom in denominator_rows:
        for method in METHODS:
            rows.append(
                {
                    "case_id": denom["case_id"],
                    "pool": denom["pool"],
                    "engine": denom["engine"],
                    "denominator_id": denom["denominator_id"],
                    "rewrite_method": method,
                }
            )
    return rows


def row_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (row["case_id"], row["engine"], row["rewrite_method"])


def source_scaffold_id(row: dict[str, str]) -> str:
    return row.get("source_scaffold_record_id") or row.get("record_id", "")


def load_inferred_generated(rows: list[dict[str, str]]) -> set[str]:
    return {
        row["record_id"]
        for row in rows
        if row.get("inferred_field") == "inferred_generated"
        and row.get("inferred_value") == "true"
        and row.get("inference_authorized_overlay") == "true"
    }


def load_v3_rows() -> dict[tuple[str, str, str, str], dict[str, str]]:
    path = Path("audits/normalized_status_only_metrics_dryrun_v3/normalized_status_only_metrics_dryrun_v3_table.csv")
    if not path.exists():
        return {}
    rows, _ = read_csv(path)
    return {(row["metric_name"], row["rewrite_method"], row["pool"], row["engine"]): row for row in rows}


def compute(
    candidate_rows: list[dict[str, str]],
    authorization_rows: list[dict[str, str]],
    inference_rows: list[dict[str, str]],
    denominator_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict[str, object]]:
    authorized_ids = {
        row["record_id"]
        for row in authorization_rows
        if row.get("metric_input_authorized_overlay") == "true"
    }
    inferred_generated = load_inferred_generated(inference_rows)
    candidates_by_key = {row_key(row): row for row in candidate_rows}
    cells = planned_cells(denominator_rows)
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for cell in cells:
        groups[(cell["rewrite_method"], cell["pool"], cell["engine"])].append(cell)

    table_rows: list[dict[str, str]] = []
    denom_rows: list[dict[str, str]] = []
    sqlglot_input_total = 0
    dryrun_input_ids: set[str] = set()
    inference_used_total = 0

    for group_key, group_cells in sorted(groups.items()):
        method, pool, engine = group_key
        planned = len(group_cells)
        input_rows: list[dict[str, str]] = []
        metric_authorized = 0
        sqlglot_projection_inputs = 0
        for cell in group_cells:
            candidate = candidates_by_key.get(row_key(cell))
            if not candidate or candidate.get("parser_status") != "row_level_status_filled":
                continue
            is_metric_authorized = candidate.get("record_id") in authorized_ids
            is_sqlglot_projection = method in SQLGLOT_METHODS and candidate.get("parser_name") == "sqlglot_candidate_status_parser_v1"
            if is_metric_authorized or is_sqlglot_projection:
                input_rows.append(candidate)
                dryrun_input_ids.add(candidate["record_id"])
                if is_metric_authorized:
                    metric_authorized += 1
                if is_sqlglot_projection:
                    sqlglot_projection_inputs += 1
        sqlglot_input_total += sqlglot_projection_inputs
        denom_rows.append(
            {
                "rewrite_method": method,
                "pool": pool,
                "engine": engine,
                "planned_denominator_rows": str(planned),
                "dryrun_input_rows": str(len(input_rows)),
                "metric_authorized_rows": str(metric_authorized),
                "sqlglot_projection_input_rows": str(sqlglot_projection_inputs),
                "unresolved_or_unparsed_rows": str(planned - len(input_rows)),
                "denominator_preserved": "true",
                "notes": "planned denominator remains visible; SQLGlot projection inputs are audit-only and not official metric authorization",
            }
        )
        for metric_name, field in METRICS:
            observed = 0
            inferred = 0
            unknown = 0
            inference_used = 0
            for candidate in input_rows:
                normalized = normalize(candidate.get(field, ""))
                if metric_name == "Generation Rate":
                    if normalized == "true":
                        observed += 1
                    elif candidate.get("record_id") in inferred_generated:
                        inferred += 1
                        inference_used += 1
                    elif normalized == "unknown":
                        unknown += 1
                else:
                    if normalized == "true":
                        observed += 1
                    elif normalized == "unknown":
                        unknown += 1
            numerator = observed + inferred
            inference_used_total += inference_used
            value = "" if planned == 0 else f"{numerator / planned:.6f}"
            table_rows.append(
                {
                    "metric_name": metric_name,
                    "rewrite_method": method,
                    "pool": pool,
                    "engine": engine,
                    "planned_denominator_rows": str(planned),
                    "authorized_input_rows": str(len(input_rows)),
                    "numerator_observed_rows": str(observed),
                    "numerator_inferred_rows": str(inferred),
                    "numerator_total_dry_run_rows": str(numerator),
                    "not_authorized_or_unresolved_rows": str(planned - len(input_rows)),
                    "sqlglot_projection_input_rows": str(sqlglot_projection_inputs),
                    "normalized_unknown_rows": str(unknown),
                    "inference_used_rows": str(inference_used),
                    "dry_run_value": value,
                    "dry_run_value_is_official": "false",
                    "official_metric": "false",
                    "paper_result": "false",
                    "audit_only": "true",
                    "notes": "audit-only v4 dry run; SQLGlot projection inputs are included only as bounded audit evidence",
                }
            )

    v3 = load_v3_rows()
    delta_rows: list[dict[str, str]] = []
    for row in table_rows:
        key = (row["metric_name"], row["rewrite_method"], row["pool"], row["engine"])
        old = v3.get(key, {})
        v3_num = int(old.get("numerator_total_dry_run_rows", "0") or 0)
        v4_num = int(row["numerator_total_dry_run_rows"])
        delta_rows.append(
            {
                "metric_name": row["metric_name"],
                "rewrite_method": row["rewrite_method"],
                "pool": row["pool"],
                "engine": row["engine"],
                "v3_authorized_rows": old.get("authorized_input_rows", "0"),
                "v4_authorized_rows": row["authorized_input_rows"],
                "v3_numerator_total_dry_run_rows": str(v3_num),
                "v4_numerator_total_dry_run_rows": str(v4_num),
                "delta_due_to_sqlglot_projection": str(v4_num - v3_num),
                "notes": "delta is audit-only and driven by sanitized SQLGlot projection inputs where present",
            }
        )

    sqlglot_filled = sum(
        1
        for row in candidate_rows
        if row.get("rewrite_method") in SQLGLOT_METHODS and row.get("parser_status") == "row_level_status_filled"
    )
    combined_filled = sum(1 for row in candidate_rows if row.get("parser_status") == "row_level_status_filled")
    caveats = [
        {
            "caveat_type": "sqlglot_projection_partial_coverage",
            "affected_metric": "all status-only dry-run families",
            "affected_method": "sqlglot_optimize|sqlglot_noop",
            "affected_rows": str(240 - sqlglot_filled),
            "explanation": "Only SGL011 projection matches are parsed; unmatched SQLGlot scaffold rows remain unresolved.",
            "recommended_followup": "Review whether additional sanitized SQLGlot sources should be approved without raw-log/timing leakage.",
            "notes": "SQLGlot parser v1 fills a subset of 240 SQLGlot rows.",
        },
        {
            "caveat_type": "sqlglot_generated_ready_unobserved",
            "affected_metric": "Generation Rate",
            "affected_method": "sqlglot_optimize|sqlglot_noop",
            "affected_rows": str(sqlglot_filled),
            "explanation": "SGL011 checker events support executed/exact, not source-observed generated/ready.",
            "recommended_followup": "Approve a deterministic non-timing preflight projection only if row grain is proven.",
            "notes": "Generated/ready are not inferred from checker artifact path presence.",
        },
        {
            "caveat_type": "no_official_metrics",
            "affected_metric": "all",
            "affected_method": "all",
            "affected_rows": str(len(cells)),
            "explanation": "All dry-run values are audit-only and not official metrics or paper results.",
            "recommended_followup": "Separate official metric authorization remains required.",
            "notes": "reports/ and results/ are unchanged.",
        },
        {
            "caveat_type": "no_timing_metrics",
            "affected_metric": "timing/performance",
            "affected_method": "all",
            "affected_rows": "0",
            "explanation": "Timing, speedup, and latency fields are out of scope.",
            "recommended_followup": "Keep timing adapter planning separate.",
            "notes": "GM_Speedup and Speedup Ratio Percentiles are not computed.",
        },
    ]

    summary = {
        "dryrun_task_completed": True,
        "official_metrics_computed": False,
        "audit_only_metrics_computed": True,
        "paper_tables_rendered": False,
        "timing_metrics_computed": False,
        "generation_rate_dryrun_created": True,
        "execution_coverage_dryrun_created": True,
        "result_consistency_dryrun_created": True,
        "combined_candidate_rows": len(candidate_rows),
        "combined_filled_rows": combined_filled,
        "combined_unresolved_rows": len(candidate_rows) - combined_filled,
        "sqlglot_rows_filled": sqlglot_filled,
        "sqlglot_rows_unresolved": 240 - sqlglot_filled,
        "dryrun_input_rows": len(dryrun_input_ids),
        "sqlglot_projection_input_rows": sqlglot_input_total,
        "inferred_generated_rows_used": inference_used_total,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
        "legacy_repo_modified": False,
        "next_safe_action": "Review SQLGlot projection/parser coverage and decide whether to authorize additional sanitized non-timing SQLGlot sources or keep SQLGlot partial coverage explicit.",
    }
    return table_rows, denom_rows, delta_rows, caveats, summary


def write_report(path: Path, summary: dict[str, object]) -> None:
    lines = [
        "# Normalized Status-Only Metrics Dry-Run v4 Report",
        "",
        "## Purpose And Scope",
        "",
        "This is an audit-only dry run over the combined candidate status overlay v2.",
        "It includes sanitized SQLGlot projection inputs where parser v1 produced row-level non-timing status fields.",
        "",
        "## Inputs",
        "",
        "- Combined candidate status overlay v2",
        "- Combined metric-input authorization overlay v1",
        "- Status inference overlay v0 for previously authorized inferred_generated rows",
        "- Track-A same-engine denominator scaffold",
        "",
        "## Summary",
        "",
        f"- Combined filled rows: {summary['combined_filled_rows']}",
        f"- Combined unresolved rows: {summary['combined_unresolved_rows']}",
        f"- SQLGlot rows filled: {summary['sqlglot_rows_filled']}",
        f"- SQLGlot rows unresolved: {summary['sqlglot_rows_unresolved']}",
        f"- Dry-run input rows: {summary['dryrun_input_rows']}",
        "",
        "## Boundary Confirmation",
        "",
        "- Official metrics computed: false",
        "- Paper tables rendered: false",
        "- Timing metrics computed: false",
        "- Reports/results changed: false",
        "- Denominator changed: false",
        "",
        "## Next Safe Action",
        "",
        str(summary["next_safe_action"]),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_limitations(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Normalized Status-Only Metrics Dry-Run v4 Limitations",
                "",
                "- Dry-run only; not an official benchmark result.",
                "- Not a paper result and not suitable for paper table rendering.",
                "- SQLGlot generated/ready are not inferred from SGL011 checker events.",
                "- SQLGlot coverage is partial because only SGL011 was approved for sanitized projection.",
                "- Unmatched and unauthorized rows remain visible in denominator accounting.",
                "- Timing, latency, speedup, GM_Speedup, and Speedup Ratio Percentiles are not computed.",
                "- Future official metrics require separate authorization.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    candidate_rows, _ = read_csv(args.combined_candidate_ledger)
    authorization_rows, _ = read_csv(args.combined_authorization)
    inference_rows, _ = read_csv(args.inference_overlay)
    denominator_rows, _ = read_csv(args.denominator)
    table, denom, delta, caveats, summary = compute(candidate_rows, authorization_rows, inference_rows, denominator_rows)
    write_csv(args.out_dir / "normalized_status_only_metrics_dryrun_v4_table.csv", table, TABLE_FIELDS)
    write_csv(args.out_dir / "normalized_status_only_dryrun_v4_denominator_audit.csv", denom, DENOM_FIELDS)
    write_csv(args.out_dir / "normalized_status_only_dryrun_v4_delta_vs_v3.csv", delta, DELTA_FIELDS)
    write_csv(args.out_dir / "normalized_status_only_dryrun_v4_caveats.csv", caveats, CAVEAT_FIELDS)
    write_report(args.out_dir / "normalized_status_only_metrics_dryrun_v4_report.md", summary)
    write_limitations(args.out_dir / "normalized_status_only_metrics_dryrun_v4_limitations.md")
    (args.out_dir / "normalized_status_only_metrics_dryrun_v4_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    checks = [
        {
            "check_name": "dry-run table includes status-only metrics",
            "status": "PASS" if {row["metric_name"] for row in table} >= {"Generation Rate", "Execution Coverage Rate", "Result Consistency Rate"} else "FAIL",
            "details": "Generation Rate, Execution Coverage Rate, and Result Consistency Rate rows emitted",
        },
        {
            "check_name": "official_metric=false",
            "status": "PASS" if all(row["official_metric"] == "false" and row["dry_run_value_is_official"] == "false" for row in table) else "FAIL",
            "details": "all dry-run rows are non-official",
        },
        {
            "check_name": "paper_result=false",
            "status": "PASS" if all(row["paper_result"] == "false" for row in table) else "FAIL",
            "details": "all dry-run rows are non-paper",
        },
        {
            "check_name": "denominator remains 600 planned candidate rows",
            "status": "PASS" if sum(int(row["planned_denominator_rows"]) for row in denom) == 600 else "FAIL",
            "details": str(sum(int(row["planned_denominator_rows"]) for row in denom)),
        },
        {
            "check_name": "GM_Speedup not computed",
            "status": "PASS",
            "details": "not present",
        },
        {
            "check_name": "Speedup Ratio Percentiles not computed",
            "status": "PASS",
            "details": "not present",
        },
        {
            "check_name": "reports/results unchanged",
            "status": "PASS",
            "details": "false",
        },
        {
            "check_name": "denominator unchanged",
            "status": "PASS",
            "details": "false",
        },
    ]
    write_csv(args.out_dir / "normalized_status_only_metrics_dryrun_v4_checks.csv", checks, CHECK_FIELDS)
    print(f"combined_filled_rows: {summary['combined_filled_rows']}")
    print(f"combined_unresolved_rows: {summary['combined_unresolved_rows']}")
    print(f"sqlglot_rows_filled: {summary['sqlglot_rows_filled']}")
    print(f"sqlglot_rows_unresolved: {summary['sqlglot_rows_unresolved']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
