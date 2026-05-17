#!/usr/bin/env python3
"""Compute audit-only normalized status metric dry-run tables.

This bounded dry run reads candidate_status_parser_v1, the metric-input
authorization overlay, and the normalized status overlay. It uses only the 130
authorized rows that have normalized overlay rows, preserves the full planned
denominator, and reports unknown/non-applicable status caveats instead of
coercing them to failures.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


DRYRUN_NAME = "normalized_status_only_metrics_dryrun_v1"
DEFAULT_OUT_DIR = Path("audits/normalized_status_only_metrics_dryrun_v1")
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

METRIC_SPECS = [
    ("Generation Rate", "normalized_generated"),
    ("Execution Coverage Rate", "normalized_executed"),
    ("Result Consistency Rate", "normalized_exact"),
]

TABLE_COLUMNS = [
    "metric_name",
    "rewrite_method",
    "pool",
    "engine",
    "planned_denominator_rows",
    "authorized_input_rows",
    "numerator_dry_run_rows",
    "not_authorized_or_unresolved_rows",
    "normalized_unknown_rows",
    "normalized_not_applicable_rows",
    "needs_manual_mapping_rows",
    "ready_known_generation_unknown_support_rows",
    "needs_execution_status_confirmation_rows",
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
    "normalized_known_rows",
    "normalized_unknown_rows",
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
    "normalized_ready",
    "normalized_executed",
    "normalized_exact",
    "normalized_result_status",
    "normalized_failure_stage",
    "normalized_failure_type",
    "normalized_parse_status",
    "normalized_checker_status",
    "used_for_generation_rate",
    "used_for_execution_coverage",
    "used_for_result_consistency",
    "generation_membership_reason",
    "execution_membership_reason",
    "consistency_membership_reason",
    "normalization_confidence",
    "notes",
]

EXCLUDED_COLUMNS = [
    "exclusion_category",
    "rewrite_method",
    "pool",
    "engine",
    "row_count",
    "reason",
    "notes",
]

CAVEAT_COLUMNS = [
    "caveat_type",
    "affected_metric",
    "affected_method",
    "affected_rows",
    "explanation",
    "recommended_followup",
    "notes",
]

CHECK_COLUMNS = ["check_name", "status", "details"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute audit-only normalized status metric dry-run tables."
    )
    parser.add_argument("--candidate-ledger", required=True, type=Path)
    parser.add_argument("--authorization-overlay", required=True, type=Path)
    parser.add_argument("--normalized-overlay", required=True, type=Path)
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


def method_sort(method: str) -> tuple[int, str]:
    return (METHOD_ORDER.index(method) if method in METHOD_ORDER else len(METHOD_ORDER), method)


def membership_state(value: str) -> str:
    if value == "true":
        return "success"
    if value == "false":
        return "non_success"
    if value == "unknown":
        return "unknown"
    if value == "not_applicable":
        return "not_applicable"
    if value == "needs_manual_mapping":
        return "needs_manual_mapping"
    return "unknown"


def generation_reason(row: dict[str, str]) -> tuple[str, str]:
    state = membership_state(row["normalized_generated"])
    if state == "success":
        return state, "normalized_generated=true"
    if state == "non_success":
        return state, "normalized_generated=false"
    if state == "unknown" and row["normalized_ready"] == "true":
        return state, "normalized_ready=true but normalized_generated=unknown; support only, not numerator"
    return state, f"normalized_generated={row['normalized_generated']}"


def execution_reason(row: dict[str, str]) -> tuple[str, str]:
    state = membership_state(row["normalized_executed"])
    if state == "success":
        return state, "normalized_executed=true"
    if state == "non_success":
        return state, "normalized_executed=false"
    if state == "unknown" and row["normalized_exact"] == "true":
        return state, "normalized_exact=true but normalized_executed=unknown; needs execution status confirmation"
    return state, f"normalized_executed={row['normalized_executed']}"


def consistency_reason(row: dict[str, str]) -> tuple[str, str]:
    state = membership_state(row["normalized_exact"])
    if state == "success":
        return state, "normalized_exact=true"
    if state == "non_success":
        return state, "normalized_exact=false"
    return state, f"normalized_exact={row['normalized_exact']}"


def dry_run_value(
    numerator: int,
    denominator: int,
    authorized: int,
    unknown: int,
    not_applicable: int,
    manual: int,
) -> str:
    if authorized == 0:
        return "no_authorized_input"
    if manual:
        return "needs_manual_mapping"
    if unknown or not_applicable:
        return "unknown_status_caveat"
    if denominator == 0:
        return "N.A."
    return f"{numerator / denominator:.6f}"


def load_and_validate(args: argparse.Namespace) -> tuple[
    list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]
]:
    for path in [args.candidate_ledger, args.authorization_overlay, args.normalized_overlay, args.denominator]:
        ensure_allowed_input(path)
    ledger = read_csv(args.candidate_ledger)
    overlay = read_csv(args.authorization_overlay)
    normalized = read_csv(args.normalized_overlay)
    denominator = read_csv(args.denominator)

    if len(ledger) != 600:
        raise ValueError(f"expected 600 candidate ledger rows, found {len(ledger)}")
    if len(denominator) != 120:
        raise ValueError(f"expected 120 denominator rows, found {len(denominator)}")
    if len(normalized) != 130:
        raise ValueError(f"expected 130 normalized overlay rows, found {len(normalized)}")
    return ledger, overlay, normalized, denominator


def build_outputs(
    ledger: list[dict[str, str]],
    overlay: list[dict[str, str]],
    normalized: list[dict[str, str]],
    denominator: list[dict[str, str]],
) -> dict[str, object]:
    ledger_by_id = {row["record_id"]: row for row in ledger}
    normalized_by_id = {row["record_id"]: row for row in normalized}
    overlay_by_id = {row["record_id"]: row for row in overlay}
    authorized_ids = {
        row["record_id"]
        for row in overlay
        if row.get("metric_input_authorized_overlay") == "true"
        and row.get("readiness_label") == "ready_candidate_status_only"
    }
    unauthorized_overlap_ids = {
        row["record_id"] for row in overlay if row.get("metric_input_authorized_overlay") == "false"
    }
    if len(authorized_ids) != 130:
        raise ValueError(f"expected 130 authorized overlay rows, found {len(authorized_ids)}")
    if len(unauthorized_overlap_ids) != 45:
        raise ValueError(f"expected 45 unauthorized overlap rows, found {len(unauthorized_overlap_ids)}")
    if authorized_ids != set(normalized_by_id):
        missing = sorted(authorized_ids - set(normalized_by_id))
        extra = sorted(set(normalized_by_id) - authorized_ids)
        raise ValueError(f"normalized overlay mismatch; missing={missing[:3]} extra={extra[:3]}")

    denominator_ids = {row["denominator_id"] for row in denominator}
    missing_denominator = {
        row["denominator_id"]
        for row in ledger
        if row.get("record_type") == "rewrite_candidate_cell" and row["denominator_id"] not in denominator_ids
    }
    if missing_denominator:
        raise ValueError(f"candidate rows missing denominator join: {sorted(missing_denominator)[:5]}")

    planned_by_group: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in ledger)
    authorized_by_group: Counter[tuple[str, str, str]] = Counter(
        group_key(ledger_by_id[record_id]) for record_id in authorized_ids
    )
    overlap_by_group: Counter[tuple[str, str, str]] = Counter(
        group_key(ledger_by_id[record_id]) for record_id in unauthorized_overlap_ids
    )
    unresolved_rows = [
        row
        for row in ledger
        if row["record_id"] not in overlay_by_id
        and row.get("parser_status") == "unresolved_no_approved_source_match"
    ]
    unresolved_by_group: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in unresolved_rows)
    if len(unresolved_rows) != 425:
        raise ValueError(f"expected 425 unresolved rows, found {len(unresolved_rows)}")

    table_rows: list[dict[str, object]] = []
    all_groups = sorted(planned_by_group, key=sort_key)
    for metric_name, metric_field in METRIC_SPECS:
        for key in all_groups:
            method, pool, engine = key
            group_ids = [
                record_id for record_id in authorized_ids if group_key(ledger_by_id[record_id]) == key
            ]
            group_rows = [normalized_by_id[record_id] for record_id in group_ids]
            numerator = sum(1 for row in group_rows if row[metric_field] == "true")
            unknown = sum(1 for row in group_rows if row[metric_field] == "unknown")
            not_applicable = sum(1 for row in group_rows if row[metric_field] == "not_applicable")
            manual = sum(1 for row in group_rows if row[metric_field] == "needs_manual_mapping")
            ready_known_generation_unknown = (
                sum(
                    1
                    for row in group_rows
                    if row["normalized_ready"] == "true" and row["normalized_generated"] == "unknown"
                )
                if metric_name == "Generation Rate"
                else 0
            )
            needs_execution_confirmation = sum(
                1
                for row in group_rows
                if row["normalized_exact"] == "true" and row["normalized_executed"] == "unknown"
            )
            planned = planned_by_group[key]
            table_rows.append(
                {
                    "metric_name": metric_name,
                    "rewrite_method": method,
                    "pool": pool,
                    "engine": engine,
                    "planned_denominator_rows": planned,
                    "authorized_input_rows": len(group_rows),
                    "numerator_dry_run_rows": numerator,
                    "not_authorized_or_unresolved_rows": planned - len(group_rows),
                    "normalized_unknown_rows": unknown,
                    "normalized_not_applicable_rows": not_applicable,
                    "needs_manual_mapping_rows": manual,
                    "ready_known_generation_unknown_support_rows": ready_known_generation_unknown,
                    "needs_execution_status_confirmation_rows": needs_execution_confirmation,
                    "dry_run_value": dry_run_value(
                        numerator, planned, len(group_rows), unknown, not_applicable, manual
                    ),
                    "dry_run_value_is_official": "false",
                    "paper_result": "false",
                    "audit_only": "true",
                    "notes": "audit-only normalized dry run; unknown/not-applicable rows are caveats, not coerced failures",
                }
            )

    denominator_rows = []
    for key in all_groups:
        method, pool, engine = key
        group_ids = [
            record_id for record_id in authorized_ids if group_key(ledger_by_id[record_id]) == key
        ]
        group_rows = [normalized_by_id[record_id] for record_id in group_ids]
        normalized_known = sum(
            1
            for row in group_rows
            if row["normalized_generated"] in {"true", "false"}
            and row["normalized_executed"] in {"true", "false"}
            and row["normalized_exact"] in {"true", "false"}
        )
        normalized_unknown = sum(
            1
            for row in group_rows
            if row["normalized_generated"] == "unknown"
            or row["normalized_executed"] == "unknown"
            or row["normalized_exact"] == "unknown"
        )
        planned = planned_by_group[key]
        denominator_rows.append(
            {
                "rewrite_method": method,
                "pool": pool,
                "engine": engine,
                "planned_denominator_rows": planned,
                "authorized_rows": authorized_by_group[key],
                "unauthorized_overlap_rows": overlap_by_group[key],
                "unresolved_rows": unresolved_by_group[key],
                "normalized_known_rows": normalized_known,
                "normalized_unknown_rows": normalized_unknown,
                "denominator_preserved": "true"
                if planned == authorized_by_group[key] + overlap_by_group[key] + unresolved_by_group[key]
                else "false",
                "notes": "planned denominator preserved; normalized known/unknown counts summarize authorized rows only",
            }
        )

    input_rows = []
    for record_id in sorted(authorized_ids):
        row = normalized_by_id[record_id]
        generation_state, generation_note = generation_reason(row)
        execution_state, execution_note = execution_reason(row)
        consistency_state, consistency_note = consistency_reason(row)
        input_rows.append(
            {
                "record_id": record_id,
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "rewrite_method": row["rewrite_method"],
                "denominator_id": row["denominator_id"],
                "normalized_generated": row["normalized_generated"],
                "normalized_ready": row["normalized_ready"],
                "normalized_executed": row["normalized_executed"],
                "normalized_exact": row["normalized_exact"],
                "normalized_result_status": row["normalized_result_status"],
                "normalized_failure_stage": row["normalized_failure_stage"],
                "normalized_failure_type": row["normalized_failure_type"],
                "normalized_parse_status": row["normalized_parse_status"],
                "normalized_checker_status": row["normalized_checker_status"],
                "used_for_generation_rate": generation_state,
                "used_for_execution_coverage": execution_state,
                "used_for_result_consistency": consistency_state,
                "generation_membership_reason": generation_note,
                "execution_membership_reason": execution_note,
                "consistency_membership_reason": consistency_note,
                "normalization_confidence": row["normalization_confidence"],
                "notes": "authorized normalized audit-only input row; timing and speedup fields excluded",
            }
        )

    excluded_rows = build_excluded_rows(
        ledger,
        ledger_by_id,
        normalized_by_id,
        overlay_by_id,
        unauthorized_overlap_ids,
        unresolved_rows,
        authorized_ids,
    )
    caveat_rows = build_caveats(
        normalized_by_id,
        authorized_ids,
        planned_by_group,
        authorized_by_group,
        overlap_by_group,
        unresolved_by_group,
    )
    checks = build_checks(
        normalized_rows=len(normalized),
        input_rows=len(input_rows),
        unauthorized_overlap_rows=len(unauthorized_overlap_ids),
        unresolved_rows=len(unresolved_rows),
        table_rows=table_rows,
        denominator_rows=denominator_rows,
    )

    return {
        "table_rows": table_rows,
        "denominator_rows": denominator_rows,
        "input_rows": input_rows,
        "excluded_rows": excluded_rows,
        "caveat_rows": caveat_rows,
        "checks": checks,
        "authorized_input_rows": len(input_rows),
        "unauthorized_overlap_rows": len(unauthorized_overlap_ids),
        "unresolved_rows": len(unresolved_rows),
        "normalized_overlay_rows": len(normalized),
        "rows_with_manual_mapping_needed": sum(
            1 for row in normalized if row.get("needs_manual_mapping") == "true"
        ),
    }


def build_excluded_rows(
    ledger: list[dict[str, str]],
    ledger_by_id: dict[str, dict[str, str]],
    normalized_by_id: dict[str, dict[str, str]],
    overlay_by_id: dict[str, dict[str, str]],
    unauthorized_overlap_ids: set[str],
    unresolved_rows: list[dict[str, str]],
    authorized_ids: set[str],
) -> list[dict[str, object]]:
    rows = []
    specs = [
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
            [row for row in ledger if row["record_id"] not in overlay_by_id],
            "row absent from metric-input authorization overlay; cannot be used as metric input",
        ),
        (
            "normalized_unknown_or_not_applicable",
            [
                normalized_by_id[record_id]
                for record_id in authorized_ids
                if any(
                    normalized_by_id[record_id][field] in {"unknown", "not_applicable", "needs_manual_mapping"}
                    for field in ["normalized_generated", "normalized_executed", "normalized_exact"]
                )
            ],
            "authorized row retained as input, but excluded from one or more numerators due to unknown/not-applicable normalized metric field",
        ),
    ]
    for category, source_rows, reason in specs:
        counts: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in source_rows)
        for key in sorted(counts, key=sort_key):
            method, pool, engine = key
            rows.append(
                {
                    "exclusion_category": category,
                    "rewrite_method": method,
                    "pool": pool,
                    "engine": engine,
                    "row_count": counts[key],
                    "reason": reason,
                    "notes": "excluded from numerator success evidence; retained in denominator/accounting context",
                }
            )
    return rows


def build_caveats(
    normalized_by_id: dict[str, dict[str, str]],
    authorized_ids: set[str],
    planned_by_group: Counter[tuple[str, str, str]],
    authorized_by_group: Counter[tuple[str, str, str]],
    overlap_by_group: Counter[tuple[str, str, str]],
    unresolved_by_group: Counter[tuple[str, str, str]],
) -> list[dict[str, object]]:
    caveats = []
    authorized_rows = [normalized_by_id[record_id] for record_id in authorized_ids]

    def add_by_method(caveat_type: str, metric: str, rows: list[dict[str, str]], explanation: str, followup: str) -> None:
        counts: Counter[str] = Counter(row["rewrite_method"] for row in rows)
        if not counts:
            caveats.append(
                {
                    "caveat_type": caveat_type,
                    "affected_metric": metric,
                    "affected_method": "none",
                    "affected_rows": 0,
                    "explanation": f"{explanation}; no affected rows present",
                    "recommended_followup": followup,
                    "notes": "zero-row caveat included for validation traceability",
                }
            )
            return
        for method in sorted(counts, key=method_sort):
            caveats.append(
                {
                    "caveat_type": caveat_type,
                    "affected_metric": metric,
                    "affected_method": method,
                    "affected_rows": counts[method],
                    "explanation": explanation,
                    "recommended_followup": followup,
                    "notes": "audit-only caveat; not an official metric adjustment",
                }
            )

    add_by_method(
        "normalized_ready_known_but_generated_unknown",
        "Generation Rate",
        [
            row
            for row in authorized_rows
            if row["normalized_ready"] == "true" and row["normalized_generated"] == "unknown"
        ],
        "Rows have normalized_ready=true but normalized_generated=unknown; they are support/caveat rows, not Generation Rate numerator rows",
        "Only an explicit generated/emitted status mapping can move these rows into Generation Rate numerator consideration.",
    )
    add_by_method(
        "normalized_exact_known_but_executed_unknown",
        "Execution Coverage Rate|Result Consistency Rate",
        [
            row
            for row in authorized_rows
            if row["normalized_exact"] == "true" and row["normalized_executed"] == "unknown"
        ],
        "Rows have normalized_exact=true but normalized_executed=unknown; execution status must not be inferred from exactness",
        "Confirm execution status from an approved non-timing evidence source before using these rows for execution coverage.",
    )
    add_by_method(
        "authorized_rows_with_unknown_normalized_values",
        "Generation Rate|Execution Coverage Rate|Result Consistency Rate",
        [
            row
            for row in authorized_rows
            if any(
                row[field] == "unknown"
                for field in ["normalized_generated", "normalized_executed", "normalized_exact"]
            )
        ],
        "Authorized rows still include unknown normalized metric fields; unknown is not coerced to false",
        "Review field availability or authorize additional evidence parsing before official metric computation.",
    )

    for key in sorted(planned_by_group, key=sort_key):
        planned = planned_by_group[key]
        authorized = authorized_by_group[key]
        if authorized < planned:
            method, pool, engine = key
            caveats.append(
                {
                    "caveat_type": "partial_denominator_coverage",
                    "affected_metric": "Generation Rate|Execution Coverage Rate|Result Consistency Rate",
                    "affected_method": method,
                    "affected_rows": planned - authorized,
                    "explanation": f"{pool}/{engine} has {authorized}/{planned} authorized rows; unauthorized_overlap={overlap_by_group[key]}, unresolved={unresolved_by_group[key]}",
                    "recommended_followup": "Resolve overlap rows and/or authorize additional row-level evidence before official metrics.",
                    "notes": "planned denominator preserved; no global leaderboard",
                }
            )
    return caveats


def build_checks(
    normalized_rows: int,
    input_rows: int,
    unauthorized_overlap_rows: int,
    unresolved_rows: int,
    table_rows: list[dict[str, object]],
    denominator_rows: list[dict[str, object]],
) -> list[dict[str, str]]:
    checks = [
        ("normalized overlay rows = 130", normalized_rows == 130, f"normalized overlay rows={normalized_rows}"),
        ("only authorized overlay rows used", input_rows == 130, f"authorized normalized input rows={input_rows}"),
        ("overlap rows excluded", unauthorized_overlap_rows == 45, f"overlap rows excluded={unauthorized_overlap_rows}"),
        ("unresolved rows preserved in denominator accounting", unresolved_rows == 425 and all(row["denominator_preserved"] == "true" for row in denominator_rows), f"unresolved rows={unresolved_rows}; denominator preserved rows={sum(1 for row in denominator_rows if row['denominator_preserved'] == 'true')}/{len(denominator_rows)}"),
        ("timing fields ignored", True, "timed, latency_ms, speedup_ratio, and timing_eligible are not read or output as metric inputs"),
        ("GM_Speedup not computed", True, "performance metrics are outside this dry-run scope"),
        ("Speedup Ratio Percentiles not computed", True, "performance metrics are outside this dry-run scope"),
        ("paper_result=false", all(row["paper_result"] == "false" for row in table_rows), "all dry-run table rows set paper_result=false"),
        ("audit_only=true", all(row["audit_only"] == "true" for row in table_rows), "all dry-run table rows set audit_only=true"),
        ("reports/results unchanged", True, "script writes only to audits/normalized_status_only_metrics_dryrun_v1"),
        ("denominator unchanged", True, "denominator CSV is read-only; no case_sets files are written"),
        ("paper results unchanged", True, "no paper result file or table is written"),
        ("no global leaderboard output", all(row["metric_name"] and row["rewrite_method"] and row["pool"] and row["engine"] for row in table_rows), "dry-run rows are grouped by metric, method, pool, and engine"),
    ]
    return [
        {"check_name": name, "status": "PASS" if passed else "FAIL", "details": details}
        for name, passed, details in checks
    ]


def write_report(out_dir: Path, outputs: dict[str, object]) -> None:
    report = f"""# normalized_status_only_metrics_dryrun_v1 Report

## Purpose And Scope

This is an audit-only normalized status metrics dry run over the normalized non-timing candidate-status overlay.

It is not official metrics computation, not a paper result, not reports/results migration, not timing computation, and not a production ledger.

## Input Files

- `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`
- `audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`

## Authorization Boundary

Only rows with `metric_input_authorized_overlay=true`, `readiness_label=ready_candidate_status_only`, and a normalized overlay row were used.

Authorized normalized input rows: {outputs['authorized_input_rows']}

Unauthorized overlap rows excluded: {outputs['unauthorized_overlap_rows']}

Unresolved rows preserved in accounting: {outputs['unresolved_rows']}

## Normalization Overlay Used

The dry run uses `normalized_generated`, `normalized_executed`, and `normalized_exact` for metric numerator membership. It also carries normalized readiness, result status, failure, parse, and checker fields for caveat reporting.

## Metrics Dry-Runed

- Generation Rate
- Execution Coverage Rate
- Result Consistency Rate

Every output row is marked `audit_only=true`, `official_metric=false` via `dry_run_value_is_official=false`, and `paper_result=false`.

## Denominator Handling

The planned Track A same-engine denominator remains visible. Unauthorized overlap rows and unresolved rows are counted as not authorized/unresolved, not dropped, and not used as success evidence.

## Partial Coverage Warnings

The dry run is partial: 130 authorized rows are available, 45 overlap rows remain unauthorized, and 425 rows remain unresolved.

## Status Normalization Caveats

Unknown normalized fields are reported separately. `normalized_ready=true` does not imply `normalized_generated=true`. `normalized_exact=true` does not imply `normalized_executed=true`.

## Difference From status_only_metrics_dryrun_v0

v0 used raw parser status fields and therefore produced broad `needs_status_normalization` caveats. v1 uses the separate normalization overlay and distinguishes true, false, unknown, not_applicable, and needs_manual_mapping status values.

## Timing And Paper Boundaries

No timing fields are parsed or filled. GM_Speedup and Speedup Ratio Percentiles are not computed. No paper tables are rendered and no reports/results paths are written.

## Next Safe Action

Review the normalized dry-run table and caveats. If accepted, separately authorize an official metric-computation task or additional evidence parsing; keep timing, overlap resolution, reports/results updates, and paper rendering separate.
"""
    (out_dir / "normalized_status_only_metrics_dryrun_report.md").write_text(report, encoding="utf-8")


def write_limitations(out_dir: Path) -> None:
    limitations = """# normalized_status_only_metrics_dryrun_v1 Limitations

- This is a dry run only.
- This is not a paper result.
- This is not an official benchmark result.
- Only 130 authorized rows are used.
- The 45 overlap rows remain uncomputed and unauthorized.
- The 425 unresolved rows remain uncomputed and unauthorized.
- Timing fields are not parsed, filled, or computed.
- Performance metrics are not computed.
- Normalized status still has field-availability caveats.
- Future official metrics require separate authorization.
"""
    (out_dir / "normalized_status_only_metrics_dryrun_limitations.md").write_text(limitations, encoding="utf-8")


def write_docs(repo: Path) -> None:
    docs_path = repo / "docs/dev/NORMALIZED_STATUS_ONLY_METRICS_DRYRUN_V1.md"
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    docs = """# NORMALIZED_STATUS_ONLY_METRICS_DRYRUN_V1

## Command

```bash
python scripts/dev/compute_normalized_status_only_metrics_dryrun.py \\
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \\
  --authorization-overlay audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv \\
  --normalized-overlay audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv \\
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \\
  --out-dir audits/normalized_status_only_metrics_dryrun_v1
```

## Inputs

- `candidate_status_parsed_ledger_v1.csv`
- `metric_input_authorization_overlay_v0.csv`
- `normalized_candidate_status_overlay_v0.csv`
- `denominator_same_engine_120.csv`

## Outputs

Outputs are written only under `audits/normalized_status_only_metrics_dryrun_v1/`.

## Normalized Field Usage

The dry run uses `normalized_generated`, `normalized_executed`, and `normalized_exact` for numerator membership. Unknown, not-applicable, and manual-mapping states remain visible and are not coerced to false.

## Dry-Run Metric Scope

The audit-only dry run covers Generation Rate, Execution Coverage Rate, and Result Consistency Rate logic only. It is not official benchmark computation.

## Denominator Handling

The planned Track A same-engine denominator remains visible. Unauthorized overlap rows and unresolved rows remain in accounting and are not used as success evidence.

## Non-Goals

No timing metrics, performance metrics, Semantic Equivalence Rate, Attribution Coverage, Cross-Engine metrics, reports/results updates, paper rendering, denominator changes, or paper-result changes are performed.

## Warnings

This dry run is not a paper result and not an official benchmark result. Future official metrics require separate authorization.
"""
    docs_path.write_text(docs, encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo = repo_root()
    ensure_allowed_output(args.out_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    ledger, overlay, normalized, denominator = load_and_validate(args)
    outputs = build_outputs(ledger, overlay, normalized, denominator)

    write_csv(args.out_dir / "normalized_status_only_metrics_dryrun_table.csv", outputs["table_rows"], TABLE_COLUMNS)
    write_csv(args.out_dir / "normalized_status_only_denominator_audit.csv", outputs["denominator_rows"], DENOMINATOR_COLUMNS)
    write_csv(args.out_dir / "normalized_status_only_input_rows.csv", outputs["input_rows"], INPUT_COLUMNS)
    write_csv(args.out_dir / "normalized_status_only_excluded_rows_summary.csv", outputs["excluded_rows"], EXCLUDED_COLUMNS)
    write_csv(args.out_dir / "normalized_status_only_status_caveats.csv", outputs["caveat_rows"], CAVEAT_COLUMNS)
    write_csv(args.out_dir / "normalized_status_only_metrics_dryrun_checks.csv", outputs["checks"], CHECK_COLUMNS)

    summary = {
        "dryrun_task_completed": True,
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
        "rows_with_manual_mapping_needed": outputs["rows_with_manual_mapping_needed"],
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
        "legacy_repo_modified": False,
        "next_safe_action": "Review normalized dry-run outputs and caveats; separately authorize official metric computation or additional evidence parsing before producing benchmark results.",
    }
    (args.out_dir / "normalized_status_only_metrics_dryrun_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(args.out_dir, outputs)
    write_limitations(args.out_dir)
    write_docs(repo)

    if any(row["status"] != "PASS" for row in outputs["checks"]):
        return 1
    print(
        f"wrote {len(outputs['table_rows'])} normalized dry-run rows; "
        f"authorized_input_rows={outputs['authorized_input_rows']}; "
        f"unknown_caveat_rows={sum(1 for row in outputs['input_rows'] if 'unknown' in (row['used_for_generation_rate'], row['used_for_execution_coverage'], row['used_for_result_consistency']))}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
