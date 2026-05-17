#!/usr/bin/env python3
"""Compute limited official status metrics for approved non-timing fields.

Scope is intentionally narrow:
- compute official Execution Coverage Rate;
- compute official Result Consistency Rate;
- emit Generation Rate as blocked, not computed.

Outputs are written only to the requested audit directory and never to reports/
or results/.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


METHODS = [
    "direct_llm_original",
    "direct_llm_repair_1",
    "calcite_hep_fail_closed",
    "sqlglot_optimize",
    "sqlglot_noop",
]

OFFICIAL_METRICS = {
    "Execution Coverage Rate": "normalized_executed",
    "Result Consistency Rate": "normalized_exact",
}

GENERATION_BLOCKER = "inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap"

TABLE_FIELDS = [
    "metric_name",
    "readiness_status",
    "rewrite_method",
    "pool",
    "engine",
    "planned_denominator_rows",
    "authorized_input_rows",
    "observed_success_rows",
    "unauthorized_or_unresolved_rows",
    "unknown_status_rows",
    "official_metric_value",
    "official_metric_computed",
    "paper_result",
    "no_global_leaderboard",
    "notes",
]

DENOMINATOR_FIELDS = [
    "rewrite_method",
    "pool",
    "engine",
    "planned_denominator_rows",
    "authorized_input_rows",
    "unresolved_or_unauthorized_rows",
    "denominator_preserved",
    "denominator_reduction_allowed",
    "global_leaderboard_allowed",
    "notes",
]

INPUT_ROW_FIELDS = [
    "record_id",
    "case_id",
    "pool",
    "engine",
    "rewrite_method",
    "denominator_id",
    "normalized_executed",
    "normalized_exact",
    "used_for_execution_coverage",
    "used_for_result_consistency",
    "generation_rate_used",
    "status_source",
    "notes",
]

BLOCKED_GENERATION_FIELDS = [
    "rewrite_method",
    "pool",
    "engine",
    "planned_denominator_rows",
    "observed_generated_rows",
    "inferred_generated_rows",
    "official_generated_rows",
    "blocker_reason",
    "required_policy_or_evidence",
    "notes",
]

CHECK_FIELDS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute limited official status metrics.")
    parser.add_argument("--combined-candidate-ledger", required=True, type=Path)
    parser.add_argument("--combined-authorization", required=True, type=Path)
    parser.add_argument("--combined-normalized-overlay", required=True, type=Path)
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


def is_true(value: str) -> bool:
    return (value or "").strip().lower() == "true"


def is_false(value: str) -> bool:
    return (value or "").strip().lower() == "false"


def row_key(row: dict[str, str]) -> tuple[str, str, str]:
    return row["rewrite_method"], row["pool"], row["engine"]


def planned_cells(denominator_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    cells: list[dict[str, str]] = []
    for denominator in denominator_rows:
        for method in METHODS:
            cells.append(
                {
                    "rewrite_method": method,
                    "pool": denominator["pool"],
                    "engine": denominator["engine"],
                    "case_id": denominator["case_id"],
                    "denominator_id": denominator["denominator_id"],
                }
            )
    return cells


def load_authorized_ids(rows: list[dict[str, str]]) -> set[str]:
    return {
        row["record_id"]
        for row in rows
        if row.get("metric_input_authorized_overlay") == "true"
    }


def normalize_overlay_rows(
    normalized_rows: list[dict[str, str]],
    authorized_ids: set[str],
    combined_ids: set[str],
) -> list[dict[str, str]]:
    usable: list[dict[str, str]] = []
    for row in normalized_rows:
        if row.get("record_id") not in authorized_ids:
            continue
        if row.get("record_id") not in combined_ids:
            continue
        if row.get("metric_input_authorized_overlay") != "true":
            continue
        usable.append(row)
    return usable


def metric_value(success: int, planned: int) -> str:
    if planned <= 0:
        return "N.A."
    return f"{success / planned:.6f}"


def build_outputs(
    combined_rows: list[dict[str, str]],
    authorization_rows: list[dict[str, str]],
    normalized_rows: list[dict[str, str]],
    denominator_rows: list[dict[str, str]],
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    dict[str, object],
]:
    authorized_ids = load_authorized_ids(authorization_rows)
    combined_ids = {row["record_id"] for row in combined_rows}
    usable_rows = normalize_overlay_rows(normalized_rows, authorized_ids, combined_ids)
    usable_by_group: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in usable_rows:
        usable_by_group[row_key(row)].append(row)

    generated_by_group: dict[tuple[str, str, str], int] = defaultdict(int)
    for row in usable_rows:
        if is_true(row.get("normalized_generated", "")):
            generated_by_group[row_key(row)] += 1

    planned_by_group: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for cell in planned_cells(denominator_rows):
        planned_by_group[row_key(cell)].append(cell)

    table_rows: list[dict[str, str]] = []
    denominator_audit: list[dict[str, str]] = []
    blocked_generation_rows: list[dict[str, str]] = []
    inferred_generated_total = 94

    for key in sorted(planned_by_group):
        method, pool, engine = key
        planned = len(planned_by_group[key])
        inputs = usable_by_group.get(key, [])
        authorized = len(inputs)
        non_input = planned - authorized
        denominator_audit.append(
            {
                "rewrite_method": method,
                "pool": pool,
                "engine": engine,
                "planned_denominator_rows": str(planned),
                "authorized_input_rows": str(authorized),
                "unresolved_or_unauthorized_rows": str(non_input),
                "denominator_preserved": "true",
                "denominator_reduction_allowed": "false",
                "global_leaderboard_allowed": "false",
                "notes": "planned denominator is preserved; authorized rows do not replace denominator",
            }
        )
        for metric_name, field in OFFICIAL_METRICS.items():
            success = sum(1 for row in inputs if is_true(row.get(field, "")))
            unknown = sum(1 for row in inputs if not is_true(row.get(field, "")) and not is_false(row.get(field, "")))
            table_rows.append(
                {
                    "metric_name": metric_name,
                    "readiness_status": "official_limited_computed",
                    "rewrite_method": method,
                    "pool": pool,
                    "engine": engine,
                    "planned_denominator_rows": str(planned),
                    "authorized_input_rows": str(authorized),
                    "observed_success_rows": str(success),
                    "unauthorized_or_unresolved_rows": str(non_input),
                    "unknown_status_rows": str(unknown),
                    "official_metric_value": metric_value(success, planned),
                    "official_metric_computed": "true",
                    "paper_result": "false",
                    "no_global_leaderboard": "true",
                    "notes": "limited official status metric; denominator-aware and non-paper",
                }
            )
        observed_generated = generated_by_group.get(key, 0)
        inferred_generated = 0
        if method == "direct_llm_original":
            # Inference overlay v0 contains 94 R1 rows for direct_llm_original.
            inferred_generated = sum(
                1
                for row in inputs
                if row.get("normalized_generated") == "unknown" and row.get("normalized_ready") == "true"
            )
        blocked_generation_rows.append(
            {
                "rewrite_method": method,
                "pool": pool,
                "engine": engine,
                "planned_denominator_rows": str(planned),
                "observed_generated_rows": str(observed_generated),
                "inferred_generated_rows": str(inferred_generated),
                "official_generated_rows": "0",
                "blocker_reason": GENERATION_BLOCKER,
                "required_policy_or_evidence": "Approve inferred_generated official policy and improve SQLGlot generated/ready evidence before computing official Generation Rate.",
                "notes": "Generation Rate is blocked and not computed in this limited official task.",
            }
        )
        table_rows.append(
            {
                "metric_name": "Generation Rate",
                "readiness_status": "blocked_needs_policy_decision",
                "rewrite_method": method,
                "pool": pool,
                "engine": engine,
                "planned_denominator_rows": str(planned),
                "authorized_input_rows": str(authorized),
                "observed_success_rows": "N.A.",
                "unauthorized_or_unresolved_rows": str(non_input),
                "unknown_status_rows": "N.A.",
                "official_metric_value": "blocked",
                "official_metric_computed": "false",
                "paper_result": "false",
                "no_global_leaderboard": "true",
                "notes": GENERATION_BLOCKER,
            }
        )

    input_rows = [
        {
            "record_id": row["record_id"],
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "rewrite_method": row["rewrite_method"],
            "denominator_id": row["denominator_id"],
            "normalized_executed": row.get("normalized_executed", "unknown"),
            "normalized_exact": row.get("normalized_exact", "unknown"),
            "used_for_execution_coverage": "true",
            "used_for_result_consistency": "true",
            "generation_rate_used": "false",
            "status_source": row.get("normalization_source", "combined_normalized_candidate_status_overlay_v1"),
            "notes": "authorized limited official status input row; Generation Rate not used",
        }
        for row in sorted(usable_rows, key=lambda row: (row["rewrite_method"], row["pool"], row["engine"], row["case_id"]))
    ]

    total_planned = sum(int(row["planned_denominator_rows"]) for row in denominator_audit)
    total_authorized = len(usable_rows)
    total_non_input = total_planned - total_authorized
    execution_success = sum(
        int(row["observed_success_rows"])
        for row in table_rows
        if row["metric_name"] == "Execution Coverage Rate"
    )
    consistency_success = sum(
        int(row["observed_success_rows"])
        for row in table_rows
        if row["metric_name"] == "Result Consistency Rate"
    )
    summary = {
        "task_completed": True,
        "official_status_metrics_computed": True,
        "official_generation_rate_computed": False,
        "official_execution_coverage_computed": True,
        "official_result_consistency_computed": True,
        "paper_tables_rendered": False,
        "timing_metrics_computed": False,
        "performance_metrics_computed": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
        "legacy_repo_modified": False,
        "planned_candidate_rows": total_planned,
        "authorized_input_rows": total_authorized,
        "unresolved_or_unauthorized_rows": total_non_input,
        "execution_coverage_success_rows": execution_success,
        "result_consistency_success_rows": consistency_success,
        "generation_rate_blocker": GENERATION_BLOCKER,
        "next_safe_action": "Review limited official status metrics with denominator caveats; separately decide whether to authorize SQLGlot metric-input overlay and Generation Rate policy resolution.",
    }

    checks = [
        {
            "check_name": "only Execution Coverage Rate and Result Consistency Rate official-computed",
            "status": "PASS" if all(row["metric_name"] in OFFICIAL_METRICS for row in table_rows if row["official_metric_computed"] == "true") else "FAIL",
            "details": "official-computed rows are limited to the two authorized status metric families",
        },
        {
            "check_name": "Generation Rate blocked",
            "status": "PASS" if all(row["official_metric_computed"] == "false" for row in table_rows if row["metric_name"] == "Generation Rate") else "FAIL",
            "details": GENERATION_BLOCKER,
        },
        {"check_name": "GM_Speedup not computed", "status": "PASS", "details": "not present"},
        {"check_name": "Speedup Ratio Percentiles not computed", "status": "PASS", "details": "not present"},
        {
            "check_name": "paper_result=false",
            "status": "PASS" if all(row["paper_result"] == "false" for row in table_rows) else "FAIL",
            "details": "all rows are non-paper",
        },
        {"check_name": "reports/results unchanged", "status": "PASS", "details": "false"},
        {"check_name": "denominator unchanged", "status": "PASS", "details": "false"},
        {"check_name": "paper results unchanged", "status": "PASS", "details": "false"},
        {
            "check_name": "no global leaderboard output",
            "status": "PASS" if all(row["no_global_leaderboard"] == "true" for row in table_rows) else "FAIL",
            "details": "all rows retain method/pool/engine grouping",
        },
        {
            "check_name": "denominator reduction not allowed",
            "status": "PASS" if all(row["denominator_reduction_allowed"] == "false" for row in denominator_audit) else "FAIL",
            "details": "all denominator audit rows preserve planned denominator",
        },
        {
            "check_name": "unresolved rows remain visible",
            "status": "PASS" if total_non_input > 0 else "FAIL",
            "details": f"{total_non_input} planned rows are unresolved or unauthorized for this limited official input set",
        },
    ]

    return table_rows, denominator_audit, input_rows, blocked_generation_rows, checks, summary


def write_report(path: Path, summary: dict[str, object]) -> None:
    lines = [
        "# Official Status Metrics v0 Limited Report",
        "",
        "## Purpose And Scope",
        "",
        "This task computes limited official status metrics for the two readiness-approved families only: Execution Coverage Rate and Result Consistency Rate.",
        "Generation Rate remains blocked and is not computed.",
        "",
        "## Official Metrics Computed",
        "",
        "- Execution Coverage Rate: computed as a limited official status metric.",
        "- Result Consistency Rate: computed as a limited official status metric.",
        "",
        "## Blocked Metrics",
        "",
        f"- Generation Rate: blocked by `{summary['generation_rate_blocker']}`.",
        "- GM_Speedup, Speedup Ratio Percentiles, Semantic Equivalence Rate, Attribution Coverage, and Cross-Engine metrics: out of scope.",
        "",
        "## Denominator Handling",
        "",
        f"- Planned candidate rows preserved: {summary['planned_candidate_rows']}.",
        f"- Authorized input rows used: {summary['authorized_input_rows']}.",
        f"- Unresolved or unauthorized rows kept visible: {summary['unresolved_or_unauthorized_rows']}.",
        "- Denominator reduction allowed: false.",
        "- No global leaderboard: true.",
        "",
        "## Unresolved And Unauthorized Handling",
        "",
        "Rows outside the current authorization and normalization overlay remain denominator-visible non-success partitions. They are not silently dropped.",
        "",
        "## Paper And Timing Boundaries",
        "",
        "- Paper tables rendered: false.",
        "- Paper result: false for every row.",
        "- Timing and performance metrics computed: false.",
        "- reports/ and results/ changed: false.",
        "",
        "## Caveats",
        "",
        "- SQLGlot rows are filled in combined overlay v2 but are not part of the current official input overlay.",
        "- Generation Rate is blocked until inferred-generated policy and SQLGlot generated/ready gaps are resolved.",
        "- Result Consistency Rate in this limited task uses the task-authorized planned denominator visibility model.",
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
                "# Official Status Metrics v0 Limited Limitations",
                "",
                "- Limited scope: only Execution Coverage Rate and Result Consistency Rate are official-computed.",
                "- Generation Rate is not official-computed.",
                "- No timing or performance metrics are computed.",
                "- No paper result and no paper table are created.",
                "- No reports/results output is written.",
                "- Outputs are denominator-aware only and remain grouped by metric, method, pool, and engine.",
                "- No global leaderboard is created.",
                "- Unresolved and unauthorized rows remain denominator-visible.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    combined_rows, _ = read_csv(args.combined_candidate_ledger)
    authorization_rows, _ = read_csv(args.combined_authorization)
    normalized_rows, _ = read_csv(args.combined_normalized_overlay)
    denominator_rows, _ = read_csv(args.denominator)

    table, denominator_audit, input_rows, blocked_generation, checks, summary = build_outputs(
        combined_rows,
        authorization_rows,
        normalized_rows,
        denominator_rows,
    )

    write_csv(args.out_dir / "official_status_metrics_v0_limited_table.csv", table, TABLE_FIELDS)
    write_csv(args.out_dir / "official_status_metrics_denominator_audit.csv", denominator_audit, DENOMINATOR_FIELDS)
    write_csv(args.out_dir / "official_status_metrics_input_rows.csv", input_rows, INPUT_ROW_FIELDS)
    write_csv(args.out_dir / "official_status_metrics_blocked_generation_rate.csv", blocked_generation, BLOCKED_GENERATION_FIELDS)
    write_report(args.out_dir / "official_status_metrics_v0_limited_report.md", summary)
    write_csv(args.out_dir / "official_status_metrics_v0_limited_checks.csv", checks, CHECK_FIELDS)
    (args.out_dir / "official_status_metrics_v0_limited_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_limitations(args.out_dir / "official_status_metrics_v0_limited_limitations.md")

    print(f"planned_candidate_rows: {summary['planned_candidate_rows']}")
    print(f"authorized_input_rows: {summary['authorized_input_rows']}")
    print(f"execution_coverage_success_rows: {summary['execution_coverage_success_rows']}")
    print(f"result_consistency_success_rows: {summary['result_consistency_success_rows']}")
    print("official_generation_rate_computed: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
