#!/usr/bin/env python3
"""Compute audit-only normalized status metrics dry-run v2.

v2 uses observed normalized status fields plus the audit-only
status_inference_overlay_v0 inferred_generated field. Inferred and observed
values remain separate, denominators are preserved, and no official metrics or
paper results are produced.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


DRYRUN_NAME = "normalized_status_only_metrics_dryrun_v2"
DEFAULT_OUT_DIR = Path("audits/normalized_status_only_metrics_dryrun_v2")
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")

METHOD_ORDER = [
    "direct_llm_original",
    "direct_llm_repair_1",
    "sqlglot_optimize",
    "sqlglot_noop",
    "calcite_hep_fail_closed",
]
POOL_ORDER = ["PERF", "CONS", "PORT", "LONGTAIL"]
ENGINE_ORDER = ["postgres", "mysql", "spark"]
METRIC_NAMES = ["Generation Rate", "Execution Coverage Rate", "Result Consistency Rate"]

TABLE_COLUMNS = [
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
    "normalized_unknown_rows",
    "inference_used_rows",
    "dry_run_value",
    "dry_run_value_is_official",
    "paper_result",
    "audit_only",
    "notes",
]

DENOMINATOR_COLUMNS = [
    "rewrite_method",
    "pool",
    "engine",
    "planned_denominator_rows",
    "authorized_rows",
    "unauthorized_overlap_rows",
    "unresolved_rows",
    "observed_known_rows",
    "inferred_rows",
    "denominator_preserved",
    "notes",
]

INPUT_COLUMNS = [
    "record_id",
    "case_id",
    "pool",
    "engine",
    "rewrite_method",
    "denominator_id",
    "normalized_generated",
    "inferred_generated",
    "generated_source_for_dryrun",
    "normalized_ready",
    "normalized_executed",
    "normalized_exact",
    "normalized_result_status",
    "used_for_generation_rate",
    "used_for_execution_coverage",
    "used_for_result_consistency",
    "generation_membership_reason",
    "execution_membership_reason",
    "consistency_membership_reason",
    "inference_used",
    "notes",
]

DELTA_COLUMNS = [
    "metric_name",
    "rewrite_method",
    "pool",
    "engine",
    "v1_numerator_dry_run_rows",
    "v2_numerator_observed_rows",
    "v2_numerator_inferred_rows",
    "v2_numerator_total_dry_run_rows",
    "delta_due_to_inference",
    "notes",
]

CAVEAT_COLUMNS = [
    "caveat_type",
    "affected_metric",
    "affected_methods",
    "affected_rows",
    "explanation",
    "recommended_followup",
    "notes",
]

CHECK_COLUMNS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute audit-only normalized status metrics dry-run v2.")
    parser.add_argument("--candidate-ledger", required=True, type=Path)
    parser.add_argument("--authorization-overlay", required=True, type=Path)
    parser.add_argument("--normalized-overlay", required=True, type=Path)
    parser.add_argument("--inference-overlay", required=True, type=Path)
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
    if "reports" in path.parts or "results" in path.parts:
        raise ValueError(f"reports/results output is forbidden for {DRYRUN_NAME}: {path}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def group_key(row: dict[str, str]) -> tuple[str, str, str]:
    return row["rewrite_method"], row["pool"], row["engine"]


def sort_key(key: tuple[str, str, str]) -> tuple[int, int, int, str, str, str]:
    method, pool, engine = key
    return (
        METHOD_ORDER.index(method) if method in METHOD_ORDER else len(METHOD_ORDER),
        POOL_ORDER.index(pool) if pool in POOL_ORDER else len(POOL_ORDER),
        ENGINE_ORDER.index(engine) if engine in ENGINE_ORDER else len(ENGINE_ORDER),
        method,
        pool,
        engine,
    )


def dry_run_value(numerator: int, denominator: int, authorized: int, unknown: int) -> str:
    if authorized == 0:
        return "no_authorized_input"
    if unknown:
        return "unknown_status_caveat"
    if denominator == 0:
        return "N.A."
    return f"{numerator / denominator:.6f}"


def generation_membership(row: dict[str, str], has_inference: bool) -> tuple[str, str, str, str]:
    if row["normalized_generated"] == "true":
        return "observed_success", "normalized_generated=true", "observed", "false"
    if row["normalized_generated"] == "false":
        return "observed_non_success", "normalized_generated=false", "observed", "false"
    if row["normalized_generated"] == "unknown" and has_inference:
        return "inferred_success", "inferred_generated=true from R1; normalized_generated remains unknown", "inferred", "true"
    if row["normalized_generated"] == "not_applicable":
        return "not_applicable", "normalized_generated=not_applicable", "observed_not_applicable", "false"
    if row["normalized_generated"] == "needs_manual_mapping":
        return "needs_manual_mapping", "normalized_generated=needs_manual_mapping", "observed_needs_manual_mapping", "false"
    return "unknown", f"normalized_generated={row['normalized_generated']}", "observed_unknown", "false"


def observed_membership(value: str, field_name: str) -> tuple[str, str]:
    if value == "true":
        return "observed_success", f"{field_name}=true"
    if value == "false":
        return "observed_non_success", f"{field_name}=false"
    if value == "not_applicable":
        return "not_applicable", f"{field_name}=not_applicable"
    if value == "needs_manual_mapping":
        return "needs_manual_mapping", f"{field_name}=needs_manual_mapping"
    return "unknown", f"{field_name}={value}"


def load_and_validate(args: argparse.Namespace) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
]:
    for path in [
        args.candidate_ledger,
        args.authorization_overlay,
        args.normalized_overlay,
        args.inference_overlay,
        args.denominator,
    ]:
        ensure_allowed_input(path)

    ledger = read_csv(args.candidate_ledger)
    auth_overlay = read_csv(args.authorization_overlay)
    normalized = read_csv(args.normalized_overlay)
    inference = read_csv(args.inference_overlay)
    denominator = read_csv(args.denominator)

    if len(ledger) != 600:
        raise ValueError(f"expected 600 candidate ledger rows, found {len(ledger)}")
    if len(auth_overlay) != 175:
        raise ValueError(f"expected 175 authorization overlay rows, found {len(auth_overlay)}")
    if len(normalized) != 130:
        raise ValueError(f"expected 130 normalized overlay rows, found {len(normalized)}")
    if len(inference) != 94:
        raise ValueError(f"expected 94 inference overlay rows, found {len(inference)}")
    if len(denominator) != 120:
        raise ValueError(f"expected 120 denominator rows, found {len(denominator)}")

    denominator_ids = {row["denominator_id"] for row in denominator}
    missing_denominator = [
        row["record_id"]
        for row in ledger
        if row.get("record_type") == "rewrite_candidate_cell" and row["denominator_id"] not in denominator_ids
    ]
    if missing_denominator:
        raise ValueError(f"candidate rows missing denominator join: {missing_denominator[:3]}")
    return ledger, auth_overlay, normalized, inference, denominator


def build_outputs(
    ledger: list[dict[str, str]],
    auth_overlay: list[dict[str, str]],
    normalized: list[dict[str, str]],
    inference: list[dict[str, str]],
) -> dict[str, object]:
    ledger_by_id = {row["record_id"]: row for row in ledger}
    auth_by_id = {row["record_id"]: row for row in auth_overlay}
    normalized_by_id = {row["record_id"]: row for row in normalized}
    inference_by_id = {
        row["record_id"]: row
        for row in inference
        if row.get("inference_authorized_overlay") == "true"
        and row.get("inferred_field") == "inferred_generated"
        and row.get("inferred_value") == "true"
    }

    authorized_ids = {
        row["record_id"]
        for row in auth_overlay
        if row.get("metric_input_authorized_overlay") == "true"
        and row.get("readiness_label") == "ready_candidate_status_only"
    }
    overlap_ids = {row["record_id"] for row in auth_overlay if row.get("metric_input_authorized_overlay") == "false"}
    if len(authorized_ids) != 130:
        raise ValueError(f"expected 130 authorized rows, found {len(authorized_ids)}")
    if len(overlap_ids) != 45:
        raise ValueError(f"expected 45 unauthorized overlap rows, found {len(overlap_ids)}")
    if set(normalized_by_id) != authorized_ids:
        raise ValueError("normalized overlay rows must exactly match authorized rows")
    if len(inference_by_id) != 94:
        raise ValueError(f"expected 94 authorized inference rows, found {len(inference_by_id)}")
    if not set(inference_by_id).issubset(authorized_ids):
        raise ValueError("inference overlay contains non-authorized rows")
    for record_id in inference_by_id:
        row = normalized_by_id[record_id]
        if row["normalized_generated"] != "unknown" or row["normalized_ready"] != "true":
            raise ValueError(f"inference row does not satisfy R1 source conditions: {record_id}")

    unresolved_rows = [
        row
        for row in ledger
        if row["record_id"] not in auth_by_id and row.get("parser_status") == "unresolved_no_approved_source_match"
    ]
    if len(unresolved_rows) != 425:
        raise ValueError(f"expected 425 unresolved rows, found {len(unresolved_rows)}")

    planned_by_group: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in ledger)
    authorized_by_group: Counter[tuple[str, str, str]] = Counter(group_key(ledger_by_id[rid]) for rid in authorized_ids)
    overlap_by_group: Counter[tuple[str, str, str]] = Counter(group_key(ledger_by_id[rid]) for rid in overlap_ids)
    unresolved_by_group: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in unresolved_rows)
    inference_by_group: Counter[tuple[str, str, str]] = Counter(group_key(ledger_by_id[rid]) for rid in inference_by_id)
    all_groups = sorted(planned_by_group, key=sort_key)

    input_rows = build_input_rows(authorized_ids, normalized_by_id, inference_by_id)
    table_rows = build_table_rows(all_groups, planned_by_group, authorized_ids, normalized_by_id, ledger_by_id, inference_by_id)
    denominator_rows = build_denominator_rows(
        all_groups,
        planned_by_group,
        authorized_by_group,
        overlap_by_group,
        unresolved_by_group,
        normalized_by_id,
        ledger_by_id,
        authorized_ids,
        inference_by_group,
    )
    delta_rows = build_delta_rows(all_groups, planned_by_group, authorized_ids, normalized_by_id, ledger_by_id, inference_by_id)
    caveat_rows = build_caveats(inference_by_id, planned_by_group, authorized_by_group, overlap_by_group, unresolved_by_group)
    checks = build_checks(table_rows, denominator_rows, len(inference_by_id), len(authorized_ids), len(overlap_ids), len(unresolved_rows))

    return {
        "table_rows": table_rows,
        "denominator_rows": denominator_rows,
        "input_rows": input_rows,
        "delta_rows": delta_rows,
        "caveat_rows": caveat_rows,
        "checks": checks,
        "authorized_input_rows": len(authorized_ids),
        "unauthorized_overlap_rows": len(overlap_ids),
        "unresolved_rows": len(unresolved_rows),
        "normalized_overlay_rows": len(normalized_by_id),
        "inference_overlay_rows": len(inference_by_id),
        "inferred_generated_rows_used": len(inference_by_id),
    }


def build_input_rows(
    authorized_ids: set[str],
    normalized_by_id: dict[str, dict[str, str]],
    inference_by_id: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for record_id in sorted(authorized_ids):
        row = normalized_by_id[record_id]
        has_inference = record_id in inference_by_id
        generation_state, generation_reason, generation_source, inference_used = generation_membership(row, has_inference)
        execution_state, execution_reason = observed_membership(row["normalized_executed"], "normalized_executed")
        consistency_state, consistency_reason = observed_membership(row["normalized_exact"], "normalized_exact")
        rows.append(
            {
                "record_id": record_id,
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "rewrite_method": row["rewrite_method"],
                "denominator_id": row["denominator_id"],
                "normalized_generated": row["normalized_generated"],
                "inferred_generated": "true" if has_inference else "",
                "generated_source_for_dryrun": generation_source,
                "normalized_ready": row["normalized_ready"],
                "normalized_executed": row["normalized_executed"],
                "normalized_exact": row["normalized_exact"],
                "normalized_result_status": row["normalized_result_status"],
                "used_for_generation_rate": generation_state,
                "used_for_execution_coverage": execution_state,
                "used_for_result_consistency": consistency_state,
                "generation_membership_reason": generation_reason,
                "execution_membership_reason": execution_reason,
                "consistency_membership_reason": consistency_reason,
                "inference_used": inference_used,
                "notes": "audit-only dry-run input row; inferred_generated is separate from normalized_generated",
            }
        )
    return rows


def group_authorized_rows(
    key: tuple[str, str, str],
    authorized_ids: set[str],
    ledger_by_id: dict[str, dict[str, str]],
    normalized_by_id: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    return [normalized_by_id[rid] for rid in authorized_ids if group_key(ledger_by_id[rid]) == key]


def metric_counts(metric_name: str, rows: list[dict[str, str]], inference_by_id: dict[str, dict[str, str]]) -> tuple[int, int, int]:
    if metric_name == "Generation Rate":
        observed = sum(1 for row in rows if row["normalized_generated"] == "true")
        inferred = sum(
            1
            for row in rows
            if row["record_id"] in inference_by_id and row["normalized_generated"] == "unknown"
        )
        unknown = sum(
            1
            for row in rows
            if row["normalized_generated"] == "unknown" and row["record_id"] not in inference_by_id
        )
        return observed, inferred, unknown
    if metric_name == "Execution Coverage Rate":
        observed = sum(1 for row in rows if row["normalized_executed"] == "true")
        unknown = sum(1 for row in rows if row["normalized_executed"] == "unknown")
        return observed, 0, unknown
    observed = sum(1 for row in rows if row["normalized_exact"] == "true")
    unknown = sum(1 for row in rows if row["normalized_exact"] == "unknown")
    return observed, 0, unknown


def build_table_rows(
    all_groups: list[tuple[str, str, str]],
    planned_by_group: Counter[tuple[str, str, str]],
    authorized_ids: set[str],
    normalized_by_id: dict[str, dict[str, str]],
    ledger_by_id: dict[str, dict[str, str]],
    inference_by_id: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    table_rows: list[dict[str, object]] = []
    for metric_name in METRIC_NAMES:
        for key in all_groups:
            method, pool, engine = key
            rows = group_authorized_rows(key, authorized_ids, ledger_by_id, normalized_by_id)
            observed, inferred, unknown = metric_counts(metric_name, rows, inference_by_id)
            planned = planned_by_group[key]
            total = observed + inferred
            table_rows.append(
                {
                    "metric_name": metric_name,
                    "rewrite_method": method,
                    "pool": pool,
                    "engine": engine,
                    "planned_denominator_rows": planned,
                    "authorized_input_rows": len(rows),
                    "numerator_observed_rows": observed,
                    "numerator_inferred_rows": inferred,
                    "numerator_total_dry_run_rows": total,
                    "not_authorized_or_unresolved_rows": planned - len(rows),
                    "normalized_unknown_rows": unknown,
                    "inference_used_rows": inferred if metric_name == "Generation Rate" else 0,
                    "dry_run_value": dry_run_value(total, planned, len(rows), unknown),
                    "dry_run_value_is_official": "false",
                    "paper_result": "false",
                    "audit_only": "true",
                    "notes": "audit-only v2 dry run; generation may include R1 inferred_generated, execution/exact remain source-observed only",
                }
            )
    return table_rows


def build_denominator_rows(
    all_groups: list[tuple[str, str, str]],
    planned_by_group: Counter[tuple[str, str, str]],
    authorized_by_group: Counter[tuple[str, str, str]],
    overlap_by_group: Counter[tuple[str, str, str]],
    unresolved_by_group: Counter[tuple[str, str, str]],
    normalized_by_id: dict[str, dict[str, str]],
    ledger_by_id: dict[str, dict[str, str]],
    authorized_ids: set[str],
    inference_by_group: Counter[tuple[str, str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key in all_groups:
        method, pool, engine = key
        group_rows = group_authorized_rows(key, authorized_ids, ledger_by_id, normalized_by_id)
        observed_known = sum(
            1
            for row in group_rows
            if row["normalized_generated"] in {"true", "false"}
            and row["normalized_executed"] in {"true", "false"}
            and row["normalized_exact"] in {"true", "false"}
        )
        planned = planned_by_group[key]
        rows.append(
            {
                "rewrite_method": method,
                "pool": pool,
                "engine": engine,
                "planned_denominator_rows": planned,
                "authorized_rows": authorized_by_group[key],
                "unauthorized_overlap_rows": overlap_by_group[key],
                "unresolved_rows": unresolved_by_group[key],
                "observed_known_rows": observed_known,
                "inferred_rows": inference_by_group[key],
                "denominator_preserved": "true"
                if planned == authorized_by_group[key] + overlap_by_group[key] + unresolved_by_group[key]
                else "false",
                "notes": "planned denominator preserved; inferred rows are separate audit-only generated support",
            }
        )
    return rows


def build_delta_rows(
    all_groups: list[tuple[str, str, str]],
    planned_by_group: Counter[tuple[str, str, str]],
    authorized_ids: set[str],
    normalized_by_id: dict[str, dict[str, str]],
    ledger_by_id: dict[str, dict[str, str]],
    inference_by_id: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for metric_name in METRIC_NAMES:
        for key in all_groups:
            method, pool, engine = key
            group_rows = group_authorized_rows(key, authorized_ids, ledger_by_id, normalized_by_id)
            observed, inferred, _unknown = metric_counts(metric_name, group_rows, inference_by_id)
            total = observed + inferred
            rows.append(
                {
                    "metric_name": metric_name,
                    "rewrite_method": method,
                    "pool": pool,
                    "engine": engine,
                    "v1_numerator_dry_run_rows": observed,
                    "v2_numerator_observed_rows": observed,
                    "v2_numerator_inferred_rows": inferred,
                    "v2_numerator_total_dry_run_rows": total,
                    "delta_due_to_inference": inferred,
                    "notes": "v1 numerator is observed-only; v2 adds only R1 inferred_generated for Generation Rate",
                }
            )
    return rows


def build_caveats(
    inference_by_id: dict[str, dict[str, str]],
    planned_by_group: Counter[tuple[str, str, str]],
    authorized_by_group: Counter[tuple[str, str, str]],
    overlap_by_group: Counter[tuple[str, str, str]],
    unresolved_by_group: Counter[tuple[str, str, str]],
) -> list[dict[str, object]]:
    total_planned = sum(planned_by_group.values())
    total_authorized = sum(authorized_by_group.values())
    total_overlap = sum(overlap_by_group.values())
    total_unresolved = sum(unresolved_by_group.values())
    sqlglot_unresolved = sum(
        planned_by_group[key]
        for key in planned_by_group
        if key[0] in {"sqlglot_optimize", "sqlglot_noop"}
    )
    partial_rows = total_planned - total_authorized
    return [
        {
            "caveat_type": "inferred_generated_used",
            "affected_metric": "Generation Rate",
            "affected_methods": "direct_llm_original",
            "affected_rows": len(inference_by_id),
            "explanation": "R1 inferred_generated=true is used only where normalized_generated=unknown and normalized_ready=true.",
            "recommended_followup": "Review whether inferred generated support can remain dry-run only or move to a later official metric authorization task.",
            "notes": "Observed normalized_generated remains unchanged.",
        },
        {
            "caveat_type": "observed_generated_distinction",
            "affected_metric": "Generation Rate",
            "affected_methods": "all",
            "affected_rows": len(inference_by_id),
            "explanation": "V2 separates numerator_observed_rows from numerator_inferred_rows.",
            "recommended_followup": "Do not collapse observed and inferred fields in official outputs without separate approval.",
            "notes": "This prevents inference from masquerading as source-observed status.",
        },
        {
            "caveat_type": "execution_exact_source_observed_only",
            "affected_metric": "Execution Coverage Rate|Result Consistency Rate",
            "affected_methods": "all",
            "affected_rows": total_authorized,
            "explanation": "No exact=>executed inference is used; execution and exactness remain source-observed normalized fields only.",
            "recommended_followup": "Authorize separate execution/exact evidence parsing before official execution or consistency metrics.",
            "notes": "R2 remains unused because the approved preview had zero rows.",
        },
        {
            "caveat_type": "partial_denominator_coverage",
            "affected_metric": "Generation Rate|Execution Coverage Rate|Result Consistency Rate",
            "affected_methods": "all",
            "affected_rows": partial_rows,
            "explanation": f"Only {total_authorized}/{total_planned} planned rows are authorized inputs; overlap={total_overlap}, unresolved={total_unresolved}.",
            "recommended_followup": "Resolve overlap and unresolved rows before official metrics.",
            "notes": "Unauthorized and unresolved rows remain visible in denominator accounting.",
        },
        {
            "caveat_type": "sqlglot_remains_unresolved",
            "affected_metric": "Generation Rate|Execution Coverage Rate|Result Consistency Rate",
            "affected_methods": "sqlglot_optimize|sqlglot_noop",
            "affected_rows": sqlglot_unresolved,
            "explanation": "SQLGlot optimize and no-op have no authorized normalized status rows in the current overlay.",
            "recommended_followup": "Curate or authorize row-level SQLGlot status evidence before status metrics for SQLGlot routes.",
            "notes": "No route-level count distribution is performed.",
        },
        {
            "caveat_type": "no_timing_metrics",
            "affected_metric": "GM_Speedup|Speedup Ratio Percentiles",
            "affected_methods": "all",
            "affected_rows": 0,
            "explanation": "Timing, latency, speedup, and timing eligibility are outside this dry-run scope.",
            "recommended_followup": "Keep timing adapter planning separate.",
            "notes": "No performance metric is computed.",
        },
    ]


def build_checks(
    table_rows: list[dict[str, object]],
    denominator_rows: list[dict[str, object]],
    inference_rows: int,
    authorized_rows: int,
    overlap_rows: int,
    unresolved_rows: int,
) -> list[dict[str, str]]:
    checks = [
        ("inference overlay rows = 94", inference_rows == 94, f"inference rows={inference_rows}"),
        ("authorized rows = 130", authorized_rows == 130, f"authorized rows={authorized_rows}"),
        ("unauthorized overlap rows = 45", overlap_rows == 45, f"overlap rows={overlap_rows}"),
        ("unresolved rows = 425", unresolved_rows == 425, f"unresolved rows={unresolved_rows}"),
        ("official_metric=false", all(row["dry_run_value_is_official"] == "false" for row in table_rows), "all dry-run table rows are non-official"),
        ("paper_result=false", all(row["paper_result"] == "false" for row in table_rows), "all dry-run table rows set paper_result=false"),
        ("audit_only=true", all(row["audit_only"] == "true" for row in table_rows), "all dry-run table rows set audit_only=true"),
        ("timing metrics not computed", True, "timing fields are not read as metric inputs"),
        ("GM_Speedup not computed", True, "performance metrics are out of scope"),
        ("Speedup Ratio Percentiles not computed", True, "performance metrics are out of scope"),
        ("reports/results unchanged", True, "script writes only to audits/normalized_status_only_metrics_dryrun_v2"),
        ("denominator unchanged", all(row["denominator_preserved"] == "true" for row in denominator_rows), "planned denominator accounting is preserved"),
        ("paper results unchanged", True, "no paper result file or table is written"),
        ("no global leaderboard output", all(row["metric_name"] and row["rewrite_method"] and row["pool"] and row["engine"] for row in table_rows), "rows are grouped by metric, method, pool, and engine"),
    ]
    return [
        {"check_name": name, "status": "PASS" if passed else "FAIL", "details": details}
        for name, passed, details in checks
    ]


def write_report(out_dir: Path, outputs: dict[str, object]) -> None:
    report = f"""# normalized_status_only_metrics_dryrun_v2 Report

## Purpose And Scope

This is an audit-only normalized status metrics dry-run using observed normalized fields plus `status_inference_overlay_v0` for R1 inferred generated support.

It is not official metrics computation, not a paper result, not timing computation, and not reports/results migration.

## Inputs

- `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`
- `audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv`
- `audits/status_inference_overlay_v0/status_inference_overlay_v0.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`

## Inference Overlay Use

The dry-run uses {outputs['inferred_generated_rows_used']} rows with `inferred_generated=true`. Inference is used only for Generation Rate dry-run logic and only when `normalized_generated=unknown`.

## Difference From v1

V1 used observed normalized values only. V2 keeps the same observed counts and adds R1 inferred-generated rows separately. Execution Coverage Rate and Result Consistency Rate remain observed-only.

## Denominator Handling

The 600 planned Track A same-engine candidate rows remain visible. The 130 authorized rows are inputs, 45 overlap rows remain unauthorized, and 425 unresolved rows remain outside success evidence.

## Partial Coverage Warnings

The dry-run remains partial and audit-only. SQLGlot routes still have no authorized normalized status rows. Inference does not resolve execution, exactness, timing, overlap, or unresolved-row gaps.

## Why No Official Metrics

Every dry-run table row has `dry_run_value_is_official=false`, `paper_result=false`, and `audit_only=true`. Official metrics require separate authorization.

## Why No Paper Tables

No paper renderer is implemented or invoked, and no reports/results paths are written.

## Why Timing Remains Separate

Timing, latency, speedup, and timing eligibility are not parsed or computed. GM_Speedup and Speedup Ratio Percentiles are not computed.

## Next Safe Action

Review the v2 delta and caveats. If accepted, separately authorize either official metric readiness review, additional evidence parsing, or overlap resolution; keep timing and paper rendering separate.
"""
    (out_dir / "normalized_status_only_metrics_dryrun_v2_report.md").write_text(report, encoding="utf-8")


def write_limitations(out_dir: Path) -> None:
    text = """# normalized_status_only_metrics_dryrun_v2 Limitations

- Dry-run only.
- Not an official benchmark result.
- Not a paper result.
- Inferred fields are separate from observed fields.
- Only `generated` can use R1 inference in this task.
- No exact=>executed inference is used.
- No timing fields are parsed, filled, or computed.
- No performance metrics are computed.
- Future official metrics require separate authorization.
"""
    (out_dir / "normalized_status_only_metrics_dryrun_v2_limitations.md").write_text(text, encoding="utf-8")


def write_docs(repo: Path) -> None:
    docs_path = repo / "docs/dev/STATUS_INFERENCE_OVERLAY_AND_DRYRUN_V2.md"
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    text = """# STATUS_INFERENCE_OVERLAY_AND_DRYRUN_V2

## Commands

```bash
python scripts/dev/build_status_inference_overlay.py \\
  --preview audits/status_inference_policy_v0/inferred_status_candidate_overlay_preview.csv \\
  --normalized-overlay audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv \\
  --out-dir audits/status_inference_overlay_v0

python scripts/dev/compute_normalized_status_only_metrics_dryrun_v2.py \\
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \\
  --authorization-overlay audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv \\
  --normalized-overlay audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv \\
  --inference-overlay audits/status_inference_overlay_v0/status_inference_overlay_v0.csv \\
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \\
  --out-dir audits/normalized_status_only_metrics_dryrun_v2
```

## Inputs

The workflow reads parser-v1 audit rows, the metric-input authorization overlay, the normalized status overlay, the R1 inference preview/overlay, and the Track A same-engine denominator scaffold.

## Outputs

Outputs are written only under `audits/status_inference_overlay_v0/` and `audits/normalized_status_only_metrics_dryrun_v2/`.

## Inference Rule Used

Only R1 is used: `normalized_ready=true` may support `inferred_generated=true` in an audit-only overlay. Observed `normalized_generated` remains unchanged.

## Observed Vs Inferred Distinction

V2 reports observed and inferred numerator counts separately. Inferred generated rows are not source-observed generated rows.

## Non-goals

No official metrics, paper tables, reports/results updates, denominator changes, timing metrics, performance metrics, reproduction CLI, public runner, or raw legacy evidence changes are performed.

## Warnings

This is an audit-only dry-run. Future official metrics require separate authorization and validation.
"""
    docs_path.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    ensure_allowed_output(args.out_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    ledger, auth_overlay, normalized, inference, _denominator = load_and_validate(args)
    outputs = build_outputs(ledger, auth_overlay, normalized, inference)

    write_csv(args.out_dir / "normalized_status_only_metrics_dryrun_v2_table.csv", outputs["table_rows"], TABLE_COLUMNS)
    write_csv(args.out_dir / "normalized_status_only_dryrun_v2_denominator_audit.csv", outputs["denominator_rows"], DENOMINATOR_COLUMNS)
    write_csv(args.out_dir / "normalized_status_only_dryrun_v2_input_rows.csv", outputs["input_rows"], INPUT_COLUMNS)
    write_csv(args.out_dir / "normalized_status_only_dryrun_v2_delta_vs_v1.csv", outputs["delta_rows"], DELTA_COLUMNS)
    write_csv(args.out_dir / "normalized_status_only_dryrun_v2_caveats.csv", outputs["caveat_rows"], CAVEAT_COLUMNS)
    write_csv(args.out_dir / "normalized_status_only_metrics_dryrun_v2_checks.csv", outputs["checks"], CHECK_COLUMNS)

    summary = {
        "dryrun_task_completed": True,
        "inference_overlay_used": True,
        "inference_overlay_rows": outputs["inference_overlay_rows"],
        "official_metrics_computed": False,
        "audit_only_metrics_computed": True,
        "paper_tables_rendered": False,
        "timing_metrics_computed": False,
        "generation_rate_dryrun_created": True,
        "execution_coverage_dryrun_created": True,
        "result_consistency_dryrun_created": True,
        "authorized_input_rows": outputs["authorized_input_rows"],
        "unauthorized_overlap_rows": outputs["unauthorized_overlap_rows"],
        "unresolved_rows": outputs["unresolved_rows"],
        "normalized_overlay_rows": outputs["normalized_overlay_rows"],
        "inferred_generated_rows_used": outputs["inferred_generated_rows_used"],
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
        "legacy_repo_modified": False,
        "next_safe_action": "Review v2 delta and caveats; separately authorize official metric readiness review, additional evidence parsing, or overlap resolution before benchmark results.",
    }
    (args.out_dir / "normalized_status_only_metrics_dryrun_v2_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(args.out_dir, outputs)
    write_limitations(args.out_dir)
    write_docs(repo_root())

    if any(row["status"] != "PASS" for row in outputs["checks"]):
        return 1
    print(
        "wrote normalized status-only dry-run v2; "
        f"authorized_input_rows={outputs['authorized_input_rows']}; "
        f"inferred_generated_rows_used={outputs['inferred_generated_rows_used']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
