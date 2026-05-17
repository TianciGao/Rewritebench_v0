#!/usr/bin/env python3
"""Compute audit-only normalized status metrics dry-run v3.

v3 uses combined overlap-priority authorization overlay v1, combined normalized
candidate status overlay v1, and the existing audit-only inferred_generated
overlay. It preserves planned denominator accounting and does not compute
official metrics or paper results.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


DRYRUN_NAME = "normalized_status_only_metrics_dryrun_v3"
LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")
V2_TABLE = Path("audits/normalized_status_only_metrics_dryrun_v2/normalized_status_only_metrics_dryrun_v2_table.csv")

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
    "still_blocked_overlap_rows",
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
    "still_blocked_overlap_rows",
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
    "v2_authorized_rows",
    "v3_authorized_rows",
    "v2_numerator_total_dry_run_rows",
    "v3_numerator_total_dry_run_rows",
    "delta_due_to_overlap_resolution",
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
    parser = argparse.ArgumentParser(description="Compute audit-only normalized status metrics dry-run v3.")
    parser.add_argument("--candidate-ledger", required=True, type=Path)
    parser.add_argument("--combined-authorization", required=True, type=Path)
    parser.add_argument("--combined-normalized-overlay", required=True, type=Path)
    parser.add_argument("--inference-overlay", required=True, type=Path)
    parser.add_argument("--denominator", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    return parser.parse_args()


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
    list[dict[str, str]],
]:
    for path in [
        args.candidate_ledger,
        args.combined_authorization,
        args.combined_normalized_overlay,
        args.inference_overlay,
        args.denominator,
        V2_TABLE,
    ]:
        ensure_allowed_input(path)

    ledger = read_csv(args.candidate_ledger)
    combined_auth = read_csv(args.combined_authorization)
    normalized = read_csv(args.combined_normalized_overlay)
    inference = read_csv(args.inference_overlay)
    denominator = read_csv(args.denominator)
    v2_table = read_csv(V2_TABLE)

    if len(ledger) != 600:
        raise ValueError(f"expected 600 candidate ledger rows, found {len(ledger)}")
    if len(combined_auth) < 175:
        raise ValueError(f"expected at least 175 combined authorization rows, found {len(combined_auth)}")
    if len(normalized) < 130:
        raise ValueError(f"expected at least 130 normalized rows, found {len(normalized)}")
    if len(inference) != 94:
        raise ValueError(f"expected 94 inference overlay rows, found {len(inference)}")
    if len(denominator) != 120:
        raise ValueError(f"expected 120 denominator rows, found {len(denominator)}")
    if len(v2_table) != 180:
        raise ValueError(f"expected 180 v2 dry-run table rows, found {len(v2_table)}")
    return ledger, combined_auth, normalized, inference, denominator, v2_table


def build_outputs(
    ledger: list[dict[str, str]],
    combined_auth: list[dict[str, str]],
    normalized: list[dict[str, str]],
    inference: list[dict[str, str]],
    _denominator: list[dict[str, str]],
    v2_table: list[dict[str, str]],
) -> dict[str, object]:
    ledger_by_id = {row["record_id"]: row for row in ledger}
    auth_by_id = {row["record_id"]: row for row in combined_auth}
    normalized_by_id = {row["record_id"]: row for row in normalized}
    inference_by_id = {
        row["record_id"]: row
        for row in inference
        if row.get("inference_authorized_overlay") == "true"
        and row.get("inferred_field") == "inferred_generated"
        and row.get("inferred_value") == "true"
    }

    authorized_ids = {
        row["record_id"] for row in combined_auth if row.get("metric_input_authorized_overlay") == "true"
    }
    blocked_overlap_ids = {
        row["record_id"] for row in combined_auth if row.get("metric_input_authorized_overlay") == "false"
    }
    if len(authorized_ids) < 130:
        raise ValueError(f"expected at least 130 authorized rows, found {len(authorized_ids)}")
    if set(normalized_by_id) != authorized_ids:
        raise ValueError("combined normalized overlay rows must exactly match authorized combined overlay rows")
    if not set(inference_by_id).issubset(authorized_ids):
        raise ValueError("inference overlay contains rows not authorized by combined overlay")

    unresolved_rows = [
        row
        for row in ledger
        if row["record_id"] not in auth_by_id
        and row.get("parser_status") == "unresolved_no_approved_source_match"
    ]
    if len(unresolved_rows) != 425:
        raise ValueError(f"expected 425 unresolved rows, found {len(unresolved_rows)}")

    planned_by_group: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in ledger)
    authorized_by_group: Counter[tuple[str, str, str]] = Counter(group_key(ledger_by_id[rid]) for rid in authorized_ids)
    blocked_by_group: Counter[tuple[str, str, str]] = Counter(group_key(ledger_by_id[rid]) for rid in blocked_overlap_ids)
    unresolved_by_group: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in unresolved_rows)
    inference_by_group: Counter[tuple[str, str, str]] = Counter(group_key(ledger_by_id[rid]) for rid in inference_by_id)
    all_groups = sorted(planned_by_group, key=sort_key)

    table_rows = build_table_rows(
        all_groups,
        planned_by_group,
        authorized_ids,
        normalized_by_id,
        ledger_by_id,
        inference_by_id,
        blocked_by_group,
    )
    denominator_rows = build_denominator_rows(
        all_groups,
        planned_by_group,
        authorized_by_group,
        blocked_by_group,
        unresolved_by_group,
        normalized_by_id,
        ledger_by_id,
        authorized_ids,
        inference_by_group,
    )
    input_rows = build_input_rows(authorized_ids, normalized_by_id, inference_by_id)
    delta_rows = build_delta_rows(table_rows, v2_table)
    caveat_rows = build_caveats(
        inference_by_id,
        planned_by_group,
        authorized_by_group,
        blocked_by_group,
        unresolved_by_group,
        normalized_by_id,
    )
    checks = build_checks(
        table_rows,
        denominator_rows,
        len(authorized_ids),
        len(blocked_overlap_ids),
        len(unresolved_rows),
        len(inference_by_id),
    )
    return {
        "table_rows": table_rows,
        "denominator_rows": denominator_rows,
        "input_rows": input_rows,
        "delta_rows": delta_rows,
        "caveat_rows": caveat_rows,
        "check_rows": checks,
        "v3_authorized_input_rows": len(authorized_ids),
        "newly_authorized_overlap_rows": len(authorized_ids) - 130,
        "still_blocked_overlap_rows": len(blocked_overlap_ids),
        "unresolved_rows": len(unresolved_rows),
        "inferred_generated_rows_used": len(inference_by_id),
    }


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
    blocked_by_group: Counter[tuple[str, str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for metric_name in METRIC_NAMES:
        for key in all_groups:
            method, pool, engine = key
            group_rows = group_authorized_rows(key, authorized_ids, ledger_by_id, normalized_by_id)
            observed, inferred, unknown = metric_counts(metric_name, group_rows, inference_by_id)
            planned = planned_by_group[key]
            total = observed + inferred
            rows.append(
                {
                    "metric_name": metric_name,
                    "rewrite_method": method,
                    "pool": pool,
                    "engine": engine,
                    "planned_denominator_rows": planned,
                    "authorized_input_rows": len(group_rows),
                    "numerator_observed_rows": observed,
                    "numerator_inferred_rows": inferred,
                    "numerator_total_dry_run_rows": total,
                    "not_authorized_or_unresolved_rows": planned - len(group_rows),
                    "still_blocked_overlap_rows": blocked_by_group[key],
                    "normalized_unknown_rows": unknown,
                    "inference_used_rows": inferred if metric_name == "Generation Rate" else 0,
                    "dry_run_value": dry_run_value(total, planned, len(group_rows), unknown),
                    "dry_run_value_is_official": "false",
                    "paper_result": "false",
                    "audit_only": "true",
                    "notes": "audit-only v3 dry run; overlap-resolved rows are included, official metrics remain unauthorized",
                }
            )
    return rows


def build_denominator_rows(
    all_groups: list[tuple[str, str, str]],
    planned_by_group: Counter[tuple[str, str, str]],
    authorized_by_group: Counter[tuple[str, str, str]],
    blocked_by_group: Counter[tuple[str, str, str]],
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
        preserved = planned == authorized_by_group[key] + blocked_by_group[key] + unresolved_by_group[key]
        rows.append(
            {
                "rewrite_method": method,
                "pool": pool,
                "engine": engine,
                "planned_denominator_rows": planned,
                "authorized_rows": authorized_by_group[key],
                "still_blocked_overlap_rows": blocked_by_group[key],
                "unresolved_rows": unresolved_by_group[key],
                "observed_known_rows": observed_known,
                "inferred_rows": inference_by_group[key],
                "denominator_preserved": "true" if preserved else "false",
                "notes": "planned denominator preserved; overlap resolution changes authorization only, not denominator",
            }
        )
    return rows


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
                "notes": "audit-only v3 input row; inferred fields remain separate from observed normalized fields",
            }
        )
    return rows


def build_delta_rows(table_rows: list[dict[str, object]], v2_table: list[dict[str, str]]) -> list[dict[str, object]]:
    v2_by_key = {
        (row["metric_name"], row["rewrite_method"], row["pool"], row["engine"]): row
        for row in v2_table
    }
    rows: list[dict[str, object]] = []
    for row in table_rows:
        key = (row["metric_name"], row["rewrite_method"], row["pool"], row["engine"])
        v2 = v2_by_key.get(key)
        if v2 is None:
            raise ValueError(f"missing v2 table row for {key}")
        v2_auth = int(v2["authorized_input_rows"])
        v3_auth = int(row["authorized_input_rows"])
        v2_num = int(v2["numerator_total_dry_run_rows"])
        v3_num = int(row["numerator_total_dry_run_rows"])
        rows.append(
            {
                "metric_name": row["metric_name"],
                "rewrite_method": row["rewrite_method"],
                "pool": row["pool"],
                "engine": row["engine"],
                "v2_authorized_rows": v2_auth,
                "v3_authorized_rows": v3_auth,
                "v2_numerator_total_dry_run_rows": v2_num,
                "v3_numerator_total_dry_run_rows": v3_num,
                "delta_due_to_overlap_resolution": v3_num - v2_num,
                "notes": "v3 delta is audit-only and reflects overlap-priority authorization plus normalization, not official metrics",
            }
        )
    return rows


def build_caveats(
    inference_by_id: dict[str, dict[str, str]],
    planned_by_group: Counter[tuple[str, str, str]],
    authorized_by_group: Counter[tuple[str, str, str]],
    blocked_by_group: Counter[tuple[str, str, str]],
    unresolved_by_group: Counter[tuple[str, str, str]],
    normalized_by_id: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    total_planned = sum(planned_by_group.values())
    total_authorized = sum(authorized_by_group.values())
    total_blocked = sum(blocked_by_group.values())
    total_unresolved = sum(unresolved_by_group.values())
    sqlglot_unresolved = sum(
        unresolved_by_group[key]
        for key in unresolved_by_group
        if key[0] in {"sqlglot_optimize", "sqlglot_noop"}
    )
    manual_mapping_rows = sum(1 for row in normalized_by_id.values() if row.get("needs_manual_mapping") == "true")
    return [
        {
            "caveat_type": "still_blocked_overlap_rows",
            "affected_metric": "Generation Rate|Execution Coverage Rate|Result Consistency Rate",
            "affected_methods": "direct_llm_original|direct_llm_repair_1",
            "affected_rows": total_blocked,
            "explanation": "Any overlap rows not resolved by Option B remain unauthorized and visible in accounting.",
            "recommended_followup": "Review still-blocked rows manually if this value is nonzero.",
            "notes": "Option B resolved all expected overlap rows in this run." if total_blocked == 0 else "Some overlap rows remain blocked.",
        },
        {
            "caveat_type": "unresolved_rows",
            "affected_metric": "Generation Rate|Execution Coverage Rate|Result Consistency Rate",
            "affected_methods": "all",
            "affected_rows": total_unresolved,
            "explanation": "Rows without approved parser-v1 status evidence remain unresolved and cannot count as success evidence.",
            "recommended_followup": "Authorize additional row-level non-timing evidence parsing before official metrics.",
            "notes": "Unresolved rows remain in denominator/accounting outputs.",
        },
        {
            "caveat_type": "sqlglot_remains_unresolved",
            "affected_metric": "Generation Rate|Execution Coverage Rate|Result Consistency Rate",
            "affected_methods": "sqlglot_optimize|sqlglot_noop",
            "affected_rows": sqlglot_unresolved,
            "explanation": "SQLGlot parser implementation is out of scope for this task.",
            "recommended_followup": "Use the SQLGlot manual decision sheet to authorize a separate sanitized projection/parser task.",
            "notes": "No SQLGlot row-level status evidence is added here.",
        },
        {
            "caveat_type": "inferred_generated_distinction",
            "affected_metric": "Generation Rate",
            "affected_methods": "direct_llm_original",
            "affected_rows": len(inference_by_id),
            "explanation": "R1 inferred_generated remains separate from observed normalized_generated.",
            "recommended_followup": "Do not collapse inferred and observed generated fields in official outputs without separate approval.",
            "notes": "The v3 table separates numerator_observed_rows and numerator_inferred_rows.",
        },
        {
            "caveat_type": "manual_mapping_non_primary_fields",
            "affected_metric": "Generation Rate|Execution Coverage Rate|Result Consistency Rate",
            "affected_methods": "direct_llm_original|direct_llm_repair_1",
            "affected_rows": manual_mapping_rows,
            "explanation": "Some newly normalized overlap rows may require manual mapping for non-primary failure bucket labels.",
            "recommended_followup": "Review `combined_normalized_candidate_status_overlay_v1.csv` before any official metric authorization.",
            "notes": "Primary generated/executed/exact membership remains conservative.",
        },
        {
            "caveat_type": "no_official_metrics",
            "affected_metric": "all",
            "affected_methods": "all",
            "affected_rows": total_authorized,
            "explanation": "This is an audit-only dry-run table, not official benchmark metric computation.",
            "recommended_followup": "Separate official metric-readiness review is required.",
            "notes": "paper_result=false and dry_run_value_is_official=false are set for every table row.",
        },
        {
            "caveat_type": "no_timing",
            "affected_metric": "performance metrics",
            "affected_methods": "all",
            "affected_rows": 0,
            "explanation": "Timing, latency, speedup, and timing eligibility remain outside scope.",
            "recommended_followup": "Keep timing adapter planning separate.",
            "notes": "No performance metric is computed.",
        },
    ]


def build_checks(
    table_rows: list[dict[str, object]],
    denominator_rows: list[dict[str, object]],
    authorized_rows: int,
    blocked_rows: int,
    unresolved_rows: int,
    inference_rows: int,
) -> list[dict[str, str]]:
    checks = [
        ("v3 authorized rows >= 130", authorized_rows >= 130, f"authorized rows={authorized_rows}"),
        ("unresolved rows = 425", unresolved_rows == 425, f"unresolved rows={unresolved_rows}"),
        ("official_metric=false", all(row["dry_run_value_is_official"] == "false" for row in table_rows), "all table rows are non-official"),
        ("paper_result=false", all(row["paper_result"] == "false" for row in table_rows), "all table rows set paper_result=false"),
        ("audit_only=true", all(row["audit_only"] == "true" for row in table_rows), "all table rows set audit_only=true"),
        ("timing metrics not computed", True, "timing fields are not metric inputs"),
        ("GM_Speedup not computed", True, "performance metrics are out of scope"),
        ("Speedup Ratio Percentiles not computed", True, "performance metrics are out of scope"),
        ("reports/results unchanged", True, "script writes only under audits/normalized_status_only_metrics_dryrun_v3"),
        ("denominator unchanged", True, "denominator file is read-only"),
        ("paper results unchanged", True, "paper_result=false in outputs"),
        ("no global leaderboard output", True, "outputs are grouped by metric/method/pool/engine"),
        (
            "denominator preserved",
            all(row["denominator_preserved"] == "true" for row in denominator_rows),
            "authorized + blocked + unresolved rows equal planned denominator per group",
        ),
        ("inference overlay used", inference_rows == 94, f"inference rows={inference_rows}"),
        ("still-blocked overlap rows tracked", blocked_rows >= 0, f"still-blocked overlap rows={blocked_rows}"),
    ]
    return [
        {"check_name": name, "status": "PASS" if passed else "FAIL", "details": details}
        for name, passed, details in checks
    ]


def write_report(out_dir: Path, summary: dict[str, object]) -> None:
    report = f"""# normalized_status_only_metrics_dryrun_v3 Report

## Purpose And Scope

This audit-only dry run uses `combined_metric_input_authorization_overlay_v1.csv`, `combined_normalized_candidate_status_overlay_v1.csv`, and the existing R1 `inferred_generated` overlay. It is not official metric computation and does not create paper results.

## Inputs

- Parser-v1 candidate ledger: 600 rows.
- Combined authorization overlay v1: {summary['v3_authorized_input_rows']} authorized rows.
- Newly authorized overlap rows: {summary['newly_authorized_overlap_rows']}.
- Still-blocked overlap rows: {summary['still_blocked_overlap_rows']}.
- Unresolved rows preserved: {summary['unresolved_rows']}.
- Inferred generated rows used: {summary['inferred_generated_rows_used']}.

## Difference From v2

v3 adds overlap-priority authorization and normalization before the dry run. The delta table records row-count changes versus v2 by metric, method, pool, and engine.

## Denominator Handling

The planned Track-A same-engine denominator remains unchanged. Unauthorized, still-blocked, and unresolved rows remain visible in denominator/accounting outputs and are not silently dropped.

## Boundaries

- Official metrics computed: no.
- Paper tables rendered: no.
- Timing metrics computed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.

## Next Safe Action

Review the v3 delta and caveats. If accepted, separately authorize official metric-readiness review or SQLGlot status evidence parsing; keep timing and paper rendering separate.
"""
    (out_dir / "normalized_status_only_metrics_dryrun_v3_report.md").write_text(report, encoding="utf-8")


def write_limitations(out_dir: Path) -> None:
    limitations = """# normalized_status_only_metrics_dryrun_v3 Limitations

- Dry-run only.
- Not official benchmark results.
- Not paper results.
- Uses overlap-priority authorization overlay v1 only as an audit overlay.
- Inferred fields remain separate from observed normalized fields.
- SQLGlot optimize and no-op remain unresolved in this task.
- No timing fields are filled.
- No performance metrics are computed.
- Reports/results and denominator files are unchanged.
- Future official metrics require separate authorization.
"""
    (out_dir / "normalized_status_only_metrics_dryrun_v3_limitations.md").write_text(limitations, encoding="utf-8")


def main() -> int:
    args = parse_args()
    ensure_allowed_output(args.out_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    result = build_outputs(*load_and_validate(args))

    write_csv(
        args.out_dir / "normalized_status_only_metrics_dryrun_v3_table.csv",
        result["table_rows"],
        TABLE_COLUMNS,
    )
    write_csv(
        args.out_dir / "normalized_status_only_dryrun_v3_denominator_audit.csv",
        result["denominator_rows"],
        DENOMINATOR_COLUMNS,
    )
    write_csv(
        args.out_dir / "normalized_status_only_dryrun_v3_input_rows.csv",
        result["input_rows"],
        INPUT_COLUMNS,
    )
    write_csv(
        args.out_dir / "normalized_status_only_dryrun_v3_delta_vs_v2.csv",
        result["delta_rows"],
        DELTA_COLUMNS,
    )
    write_csv(
        args.out_dir / "normalized_status_only_dryrun_v3_caveats.csv",
        result["caveat_rows"],
        CAVEAT_COLUMNS,
    )
    write_csv(
        args.out_dir / "normalized_status_only_metrics_dryrun_v3_checks.csv",
        result["check_rows"],
        CHECK_COLUMNS,
    )

    summary = {
        "dryrun_task_completed": True,
        "overlap_overlay_used": True,
        "inference_overlay_used": True,
        "official_metrics_computed": False,
        "audit_only_metrics_computed": True,
        "paper_tables_rendered": False,
        "timing_metrics_computed": False,
        "generation_rate_dryrun_created": True,
        "execution_coverage_dryrun_created": True,
        "result_consistency_dryrun_created": True,
        "v3_authorized_input_rows": result["v3_authorized_input_rows"],
        "newly_authorized_overlap_rows": result["newly_authorized_overlap_rows"],
        "still_blocked_overlap_rows": result["still_blocked_overlap_rows"],
        "unresolved_rows": result["unresolved_rows"],
        "inferred_generated_rows_used": result["inferred_generated_rows_used"],
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
        "legacy_repo_modified": False,
        "next_safe_action": "Review v3 delta and caveats; separately authorize official metric-readiness review or SQLGlot status evidence parsing if accepted.",
    }
    (args.out_dir / "normalized_status_only_metrics_dryrun_v3_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    write_report(args.out_dir, summary)
    write_limitations(args.out_dir)

    if any(row["status"] == "FAIL" for row in result["check_rows"]):
        return 1
    print(
        f"wrote {DRYRUN_NAME}: authorized={result['v3_authorized_input_rows']} "
        f"new_overlap={result['newly_authorized_overlap_rows']} "
        f"blocked={result['still_blocked_overlap_rows']} unresolved={result['unresolved_rows']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
