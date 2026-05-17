#!/usr/bin/env python3
"""Validate ledger-style CSV files without computing metrics.

This validator skeleton is intentionally non-mutating. It reads one supplied
ledger CSV plus static Common-core scaffolds, validates record identity,
record-type boundaries, denominator joins, and safety flags, then writes audit
outputs. It does not parse legacy retained evidence or compute metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable


LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")
DEFAULT_OUT_DIR = Path("audits/production_ledger_validator_skeleton")

RESULTS_FILENAME = "ledger_validation_results.csv"
SUMMARY_FILENAME = "ledger_validation_summary.json"
REPORT_FILENAME = "ledger_validation_report.md"

KNOWN_RECORD_TYPES = {
    "control_cell",
    "rewrite_candidate_cell",
    "plan_observability_artifact",
    "portability_candidate_cell",
    "verifier_support_pair",
    "retained_summary_artifact",
    "user_run_candidate_cell",
}

SUPPORTED_RECORD_TYPES = {
    "control_cell",
    "retained_summary_artifact",
    "rewrite_candidate_cell",
}

COMMON_REQUIRED_COLUMNS = {
    "record_id",
    "record_type",
    "case_set",
    "evidence_source",
    "status",
    "notes",
}

CONTROL_REQUIRED_COLUMNS = {
    "record_id",
    "record_type",
    "case_id",
    "pool",
    "case_set",
    "denominator_id",
    "engine",
    "control_route",
    "planned",
    "generated",
    "ready",
    "executed",
    "exact",
    "timed",
    "metrics_computed",
    "metric_input_authorized",
    "production_retained_evidence_parsed",
    "legacy_repo_read",
    "reports_changed",
    "results_changed",
    "denominator_changed",
    "paper_results_changed",
}

CONTROL_REQUIRED_COLUMNS_ALLOW_EMPTY_WITH_STATUS = {
    "retained_artifact_path",
}

REWRITE_CANDIDATE_REQUIRED_COLUMNS = {
    "record_id",
    "record_type",
    "adapter_name",
    "adapter_scope",
    "case_id",
    "pool",
    "case_set",
    "denominator_id",
    "engine",
    "rewrite_method",
    "route",
    "method_role",
    "candidate_id",
    "planned",
    "generated",
    "ready",
    "executed",
    "exact",
    "timed",
    "result_status",
    "metric_input_authorized",
    "metrics_computed",
    "production_retained_evidence_parsed",
    "legacy_repo_read",
    "reports_changed",
    "results_changed",
    "denominator_changed",
    "paper_results_changed",
}

REWRITE_CANDIDATE_NA_FIELDS = {
    "generated",
    "ready",
    "executed",
    "exact",
    "timed",
}

REWRITE_CANDIDATE_ALLOWED_NA_VALUES = {"N.A.", "evidence_not_adapted_yet"}

SAFETY_FALSE_FIELDS = {
    "metric_input_authorized",
    "metrics_computed",
    "reports_changed",
    "results_changed",
    "denominator_changed",
    "paper_results_changed",
}

SOURCE_READ_FLAGS = {
    "production_retained_evidence_parsed",
    "legacy_repo_read",
}

PARSED_CANDIDATE_OUTCOME_VALUES = {
    "N.A.",
    "evidence_not_adapted_yet",
    "requires_production_retained_evidence",
    "true",
    "false",
    "unknown",
    "not_applicable",
}

PARSED_CANDIDATE_RESULT_STATUS_VALUES = {
    "evidence_not_adapted_yet",
    "ready",
    "generated",
    "exact",
    "mismatch",
    "failed",
    "blocked",
    "manual_review_required",
    "unknown",
    "not_run",
}

RETAINED_SUMMARY_REQUIRED_ANY = [
    ("artifact", {"artifact_id", "source_artifact_path", "retained_artifact_path"}),
    ("role", {"evidence_role", "method_role"}),
]

METRIC_AGGREGATE_COLUMNS = {
    "generation_rate",
    "execution_coverage_rate",
    "result_consistency_rate",
    "semantic_equivalence_rate",
    "gm_speedup",
    "speedup_ratio_percentiles",
    "attribution_coverage",
    "cross_engine_execution",
    "cross_engine_consistency",
    "speedup_retention",
    "regression_at_20",
    "regression@20",
}

FORBIDDEN_LEADERBOARD_COLUMNS = {
    "global_leaderboard",
    "leaderboard_rank",
    "leaderboard_score",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a ledger-style CSV file.")
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--case-set", required=True, type=Path)
    parser.add_argument("--same-engine-denominator", required=True, type=Path)
    parser.add_argument("--controls", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_safe_path(path: Path) -> None:
    resolved = path.resolve()
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        raise ValueError(f"legacy repo path is not allowed: {path}")
    if "reports" in path.parts or "results" in path.parts:
        raise ValueError(f"reports/results paths are not valid validator inputs: {path}")


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows, list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def is_blank(value: str | None) -> bool:
    return value is None or value.strip() == ""


def value_is_true(value: str | None) -> bool:
    return (value or "").strip().lower() == "true"


def case_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["case_id"]: row for row in rows if row.get("case_id")}


def controls_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["control_id"]: row for row in rows if row.get("control_id")}


def same_engine_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["denominator_id"]: row for row in rows if row.get("denominator_id")}


def value_is_false(value: str | None) -> bool:
    return (value or "").strip().lower() == "false"


def is_approved_candidate_status_parser_row(row: dict[str, str]) -> bool:
    return (
        row.get("parser_name") == "candidate_status_parser_v1"
        and row.get("parser_scope") == "approved_non_timing_whitelist_only"
    )


def validate_common(
    row: dict[str, str], fieldnames: list[str], row_number: int
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    missing_common = sorted(column for column in COMMON_REQUIRED_COLUMNS if column not in fieldnames)
    if missing_common:
        errors.append("missing_common_columns:" + ";".join(missing_common))
    for column in COMMON_REQUIRED_COLUMNS & set(fieldnames):
        if is_blank(row.get(column)):
            errors.append(f"empty_required_common_field:{column}")

    record_type = row.get("record_type", "")
    if record_type not in KNOWN_RECORD_TYPES:
        errors.append(f"unknown_record_type:{record_type or '<blank>'}")
    elif record_type not in SUPPORTED_RECORD_TYPES:
        warnings.append(f"record_type_common_validation_only:{record_type}")

    if value_is_true(row.get("metrics_computed")):
        errors.append("metrics_computed_true")
    approved_parser_row = is_approved_candidate_status_parser_row(row)
    if value_is_true(row.get("production_retained_evidence_parsed")) and not approved_parser_row:
        errors.append("production_retained_evidence_parsed_true")
    if value_is_true(row.get("legacy_repo_read")) and not approved_parser_row:
        errors.append("legacy_repo_read_true")

    row_id = row.get("record_id", "")
    if not row_id:
        errors.append(f"missing_record_id_at_row:{row_number}")
    return errors, warnings


def validate_forbidden_columns(fieldnames: list[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    lower_fieldnames = {field.lower() for field in fieldnames}
    metric_columns = sorted(lower_fieldnames & METRIC_AGGREGATE_COLUMNS)
    if metric_columns:
        errors.append("metric_aggregate_columns_present:" + ";".join(metric_columns))
    leaderboard_columns = sorted(lower_fieldnames & FORBIDDEN_LEADERBOARD_COLUMNS)
    if leaderboard_columns:
        errors.append("global_leaderboard_columns_present:" + ";".join(leaderboard_columns))
    return errors, warnings


def validate_control_cell(
    row: dict[str, str],
    fieldnames: list[str],
    cases: dict[str, dict[str, str]],
    controls: dict[str, dict[str, str]],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required_control_columns = CONTROL_REQUIRED_COLUMNS | CONTROL_REQUIRED_COLUMNS_ALLOW_EMPTY_WITH_STATUS
    missing_columns = sorted(column for column in required_control_columns if column not in fieldnames)
    if missing_columns:
        errors.append("missing_control_columns:" + ";".join(missing_columns))
    for column in CONTROL_REQUIRED_COLUMNS & set(fieldnames):
        if is_blank(row.get(column)):
            errors.append(f"empty_control_field:{column}")

    case_id = row.get("case_id", "")
    if case_id and case_id not in cases:
        errors.append(f"case_id_not_in_case_set:{case_id}")
    elif case_id:
        expected_pool = cases[case_id].get("pool")
        if row.get("pool") and expected_pool and row.get("pool") != expected_pool:
            errors.append(f"pool_mismatch:{case_id}:{row.get('pool')}!={expected_pool}")

    denominator_id = row.get("denominator_id", "")
    control = controls.get(denominator_id)
    if not denominator_id:
        errors.append("missing_denominator_id")
    elif control is None:
        errors.append(f"control_denominator_join_missing:{denominator_id}")
    else:
        for column in ("case_id", "pool", "engine", "control_route"):
            if row.get(column) and control.get(column) and row.get(column) != control.get(column):
                errors.append(
                    f"control_join_{column}_mismatch:{row.get(column)}!={control.get(column)}"
                )

    if row.get("record_type") == "control_cell" and row.get("metric_input_authorized") == "true":
        errors.append("control_cell_metric_input_authorized_true")
    if "retained_artifact_path" in fieldnames and is_blank(row.get("retained_artifact_path")):
        if row.get("evidence_index_status") not in {"evidence_not_retained", "manual_review_required"}:
            errors.append("empty_retained_artifact_path_without_missingness_status")
    return errors, warnings


def validate_retained_summary_artifact(
    row: dict[str, str], fieldnames: list[str]
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for group_name, candidates in RETAINED_SUMMARY_REQUIRED_ANY:
        present = [column for column in candidates if column in fieldnames and not is_blank(row.get(column))]
        if not present:
            errors.append(f"missing_retained_summary_{group_name}_identifier")
    if "metric_input_authorized" in fieldnames and row.get("metric_input_authorized") == "true":
        errors.append("retained_summary_metric_input_authorized_true")
    if "denominator_id" in fieldnames and not is_blank(row.get("denominator_id")):
        warnings.append("retained_summary_denominator_id_present_reference_only")
    return errors, warnings


def validate_rewrite_candidate_cell(
    row: dict[str, str],
    fieldnames: list[str],
    cases: dict[str, dict[str, str]],
    same_engine_denominator: dict[str, dict[str, str]],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    missing_columns = sorted(
        column for column in REWRITE_CANDIDATE_REQUIRED_COLUMNS if column not in fieldnames
    )
    if missing_columns:
        errors.append("missing_rewrite_candidate_columns:" + ";".join(missing_columns))
    for column in REWRITE_CANDIDATE_REQUIRED_COLUMNS & set(fieldnames):
        if is_blank(row.get(column)):
            errors.append(f"empty_rewrite_candidate_field:{column}")

    case_id = row.get("case_id", "")
    if case_id and case_id not in cases:
        errors.append(f"case_id_not_in_case_set:{case_id}")
    elif case_id:
        expected_pool = cases[case_id].get("pool")
        if row.get("pool") and expected_pool and row.get("pool") != expected_pool:
            errors.append(f"pool_mismatch:{case_id}:{row.get('pool')}!={expected_pool}")

    denominator_id = row.get("denominator_id", "")
    denominator_row = same_engine_denominator.get(denominator_id)
    if not denominator_id:
        errors.append("missing_denominator_id")
    elif denominator_row is None:
        errors.append(f"same_engine_denominator_join_missing:{denominator_id}")
    else:
        for column in ("case_id", "pool", "engine"):
            if row.get(column) and denominator_row.get(column) and row.get(column) != denominator_row.get(column):
                errors.append(
                    f"same_engine_join_{column}_mismatch:{row.get(column)}!={denominator_row.get(column)}"
                )

    expected_denominator_id = None
    if case_id and row.get("engine"):
        expected_denominator_id = f"track_a_same_engine:{case_id}:{row.get('engine')}"
    if expected_denominator_id and denominator_id and denominator_id != expected_denominator_id:
        errors.append(
            f"same_engine_denominator_id_unexpected:{denominator_id}!={expected_denominator_id}"
        )

    if row.get("record_type") != "rewrite_candidate_cell":
        errors.append("rewrite_candidate_record_type_mismatch")
    if row.get("route") != "same_engine_rewrite":
        errors.append(f"rewrite_candidate_route_unexpected:{row.get('route')}")
    for column in ("rewrite_method", "route", "method_role", "candidate_id"):
        if column in fieldnames and is_blank(row.get(column)):
            errors.append(f"empty_rewrite_candidate_identity_field:{column}")

    for column in SAFETY_FALSE_FIELDS & set(fieldnames):
        if not value_is_false(row.get(column)):
            errors.append(f"safety_flag_not_false:{column}={row.get(column)}")
    for column in SOURCE_READ_FLAGS & set(fieldnames):
        if not is_approved_candidate_status_parser_row(row) and not value_is_false(row.get(column)):
            errors.append(f"safety_flag_not_false:{column}={row.get(column)}")

    if "planned" in fieldnames and (row.get("planned") or "").strip().lower() != "true":
        errors.append(f"planned_not_true:{row.get('planned')}")

    parsed_candidate_row = is_approved_candidate_status_parser_row(row)
    for column in REWRITE_CANDIDATE_NA_FIELDS & set(fieldnames):
        allowed_values = REWRITE_CANDIDATE_ALLOWED_NA_VALUES
        if parsed_candidate_row and column != "timed":
            allowed_values = PARSED_CANDIDATE_OUTCOME_VALUES
        if row.get(column) not in allowed_values:
            errors.append(f"rewrite_candidate_outcome_inferred:{column}={row.get(column)}")
    if "result_status" in fieldnames:
        if parsed_candidate_row:
            if row.get("result_status") not in PARSED_CANDIDATE_RESULT_STATUS_VALUES:
                errors.append(f"rewrite_candidate_result_status_unexpected:{row.get('result_status')}")
        elif row.get("result_status") != "evidence_not_adapted_yet":
            errors.append(f"rewrite_candidate_result_status_unexpected:{row.get('result_status')}")

    for column in ("latency_ms", "speedup_ratio"):
        if column in fieldnames and row.get(column) not in {"", "N.A."}:
            errors.append(f"rewrite_candidate_timing_value_populated:{column}")
    return errors, warnings


def validate_rows(
    rows: list[dict[str, str]],
    fieldnames: list[str],
    cases: dict[str, dict[str, str]],
    controls: dict[str, dict[str, str]],
    same_engine_denominator: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    global_errors, global_warnings = validate_forbidden_columns(fieldnames)
    seen_ids = Counter(row.get("record_id", "") for row in rows if row.get("record_id"))
    results: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        errors = list(global_errors)
        warnings = list(global_warnings)
        common_errors, common_warnings = validate_common(row, fieldnames, index)
        errors.extend(common_errors)
        warnings.extend(common_warnings)
        record_id = row.get("record_id", "")
        if record_id and seen_ids[record_id] > 1:
            errors.append(f"duplicate_record_id:{record_id}")

        record_type = row.get("record_type", "")
        if record_type == "control_cell":
            type_errors, type_warnings = validate_control_cell(row, fieldnames, cases, controls)
            errors.extend(type_errors)
            warnings.extend(type_warnings)
        elif record_type == "retained_summary_artifact":
            type_errors, type_warnings = validate_retained_summary_artifact(row, fieldnames)
            errors.extend(type_errors)
            warnings.extend(type_warnings)
        elif record_type == "rewrite_candidate_cell":
            type_errors, type_warnings = validate_rewrite_candidate_cell(
                row,
                fieldnames,
                cases,
                same_engine_denominator,
            )
            errors.extend(type_errors)
            warnings.extend(type_warnings)

        results.append(
            {
                "row_number": str(index),
                "record_id": record_id,
                "record_type": record_type,
                "validation_status": "FAIL" if errors else "PASS",
                "errors": ";".join(errors),
                "warnings": ";".join(warnings),
                "notes": "non-mutating ledger CSV validation; no metrics computed",
            }
        )
    return results


def write_report(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, object],
    record_type_counts: Counter[str],
) -> None:
    lines = [
        "# Ledger CSV Validation Report",
        "",
        "## Purpose And Scope",
        "",
        "This report records non-mutating validation of a ledger-style CSV file.",
        "The validator reads only the supplied ledger CSV and static Common-core scaffolds.",
        "",
        "## Inputs Read",
        "",
        f"- Ledger: `{args.ledger}`",
        f"- Case set: `{args.case_set}`",
        f"- Same-engine denominator: `{args.same_engine_denominator}`",
        f"- Controls: `{args.controls}`",
        "",
        "## Record Types Seen",
        "",
    ]
    lines.extend(f"- `{record_type}`: {count}" for record_type, count in sorted(record_type_counts.items()))
    lines.extend(
        [
            "",
            "## Validation Summary",
            "",
            f"- Rows checked: {summary['ledger_rows_checked']}",
            f"- Errors: {summary['errors_count']}",
            f"- Warnings: {summary['warnings_count']}",
            f"- Validation passed: {str(summary['validation_passed']).lower()}",
            "- Metrics computed: false",
            "- Production retained evidence parsed: false",
            "- Reports/results changed: false",
            "",
            "## Non-goals",
            "",
            "- No metrics were computed.",
            "- No legacy reports/results/runs were parsed.",
            "- No input files were mutated.",
            "- No reports/results or case-local runs outputs were written.",
            "",
            "## Next Safe Action",
            "",
            "Use this skeleton only as a validation gate for bounded adapter outputs. Full production validation, metrics computation, and paper rendering require separate authorization.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    root = repo_root()
    paths = [args.ledger, args.case_set, args.same_engine_denominator, args.controls]
    for path in paths:
        candidate = path if path.is_absolute() else root / path
        ensure_safe_path(candidate)
        if not candidate.exists():
            raise FileNotFoundError(candidate)

    ledger_path = args.ledger if args.ledger.is_absolute() else root / args.ledger
    case_set_path = args.case_set if args.case_set.is_absolute() else root / args.case_set
    same_engine_path = (
        args.same_engine_denominator
        if args.same_engine_denominator.is_absolute()
        else root / args.same_engine_denominator
    )
    controls_path = args.controls if args.controls.is_absolute() else root / args.controls
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    ensure_safe_path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ledger_rows, ledger_fields = read_csv(ledger_path)
    case_rows, _ = read_csv(case_set_path)
    same_engine_rows, _ = read_csv(same_engine_path)
    control_rows, _ = read_csv(controls_path)

    cases = case_lookup(case_rows)
    controls = controls_lookup(control_rows)
    same_engine_denominator = same_engine_lookup(same_engine_rows)
    record_type_counts = Counter(row.get("record_type", "") for row in ledger_rows)
    results = validate_rows(ledger_rows, ledger_fields, cases, controls, same_engine_denominator)
    errors_count = sum(1 for row in results if row["errors"])
    warnings_count = sum(1 for row in results if row["warnings"])
    adapter_output_validated = any(row.get("adapter_name") for row in ledger_rows)
    summary: dict[str, object] = {
        "ledger_rows_checked": len(ledger_rows),
        "record_types_seen": sorted(record_type_counts),
        "errors_count": errors_count,
        "warnings_count": warnings_count,
        "validation_passed": errors_count == 0,
        "metrics_computed": False,
        "production_retained_evidence_parsed": False,
        "adapter_implemented": False,
        "adapter_output_validated": adapter_output_validated,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }

    write_csv(
        out_dir / RESULTS_FILENAME,
        results,
        ["row_number", "record_id", "record_type", "validation_status", "errors", "warnings", "notes"],
    )
    (out_dir / SUMMARY_FILENAME).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(out_dir / REPORT_FILENAME, args, summary, record_type_counts)
    print(f"ledger_rows_checked: {len(ledger_rows)}")
    print(f"errors_count: {errors_count}")
    print(f"warnings_count: {warnings_count}")
    print(f"validation_passed: {summary['validation_passed']}")
    return 0 if errors_count == 0 else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
