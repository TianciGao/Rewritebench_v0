#!/usr/bin/env python3
"""Validate synthetic evidence-ledger fixture rows.

This developer validator is deliberately fixture-only. It reads the synthetic
fixture tables under ``audits/ledger_schema_validation_fixtures`` plus optional
synthetic hardening fixture tables. It may also read static Common-core
case-set denominator scaffolds for join checks. It does not parse production
retained evidence, read legacy reports/results/runs, compute metrics, or mutate
case packages.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable


BASE_FIXTURE_FILES = {
    "fixtures": "fixture_all_record_types.csv",
    "expected": "fixture_expected_validation_results.csv",
    "rules": "record_type_required_fields_matrix.csv",
    "allowed": "allowed_status_values.csv",
    "joins": "fixture_denominator_join_examples.csv",
}

CASE_SET_PATH = Path("case_sets/common_core_v0/cases.csv")
SAME_ENGINE_DENOMINATOR_PATH = Path(
    "case_sets/common_core_v0/denominator_same_engine_120.csv"
)
CONTROLS_PATH = Path("case_sets/common_core_v0/controls_360.csv")

RESULTS_FILENAME = "ledger_fixture_hardening_validation_results.csv"
SUMMARY_FILENAME = "ledger_fixture_hardening_summary.json"
REPORT_FILENAME = "ledger_fixture_validator_hardening_report.md"

LEGACY_REPO_ROOT = Path("/home/tianci_gao/code/sql-rewrite-bench-artifact-clean")
DISALLOWED_READ_PARTS = {
    "reports",
    "results",
    "runs",
}

NULL_VALUES = {"", "null", "none", "n/a"}
NON_POPULATED_VALUES = NULL_VALUES | {"not_applicable", "unknown", "N.A."}

STATUS_FIELDS = {
    "status",
    "result_status",
    "parse_status",
    "checker_status",
    "generated",
    "ready",
    "executed",
    "exact",
    "timed",
    "plan_available",
    "timing_eligible",
    "metric_eligible",
    "support_only",
    "fixture_only",
    "not_paper_evidence",
}

BOOLEAN_FIELDS = {
    "fixture_only",
    "not_paper_evidence",
    "generated",
    "ready",
    "executed",
    "exact",
    "timed",
    "plan_available",
    "timing_eligible",
    "metric_eligible",
    "support_only",
}

BOOLEAN_OR_NA_VALUES = {"true", "false", "null", "not_applicable", "unknown"}

BUILTIN_ALLOWED_STATUS_VALUES = {
    "true",
    "false",
    "null",
    "not_applicable",
    "unknown",
    "unsupported",
    "verifier_unknown",
    "timing_missing",
    "target_timing_missing",
    "evidence_not_retained",
    "manual_review_required",
    "blocked",
    "generated",
    "ready",
    "executed",
    "exact",
    "mismatch",
    "failed",
    "N.A.",
    "pass",
    "fail",
    "reject_expected",
    "reject_unexpected",
    "parsed",
    "not_parsed",
    "not_run",
    "checker_rejected",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate synthetic ledger fixture rows only."
    )
    parser.add_argument(
        "--fixtures-dir",
        required=True,
        type=Path,
        help="Directory containing base synthetic ledger fixture CSVs.",
    )
    parser.add_argument(
        "--out-dir",
        required=True,
        type=Path,
        help="Directory where validation outputs should be written.",
    )
    parser.add_argument(
        "--extra-fixtures",
        type=Path,
        default=None,
        help="Optional CSV of additional synthetic hardening fixture rows.",
    )
    parser.add_argument(
        "--extra-expected",
        type=Path,
        default=None,
        help="Optional CSV of expected outcomes for extra hardening rows.",
    )
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require_files(paths: Iterable[Path]) -> list[str]:
    return [str(path) for path in paths if not path.exists()]


def split_fields(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def is_empty(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().lower() in NULL_VALUES


def is_populated(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip() not in NON_POPULATED_VALUES


def bool_value(value: str | None) -> bool:
    return (value or "").strip().lower() == "true"


def expected_error_tokens(value: str | None) -> set[str]:
    return set(split_fields(value))


def load_id_set(path: Path, column: str) -> set[str]:
    rows = read_csv(path)
    return {row[column] for row in rows if row.get(column)}


def path_is_safe_input(path: Path, *, allow_case_sets: bool = False) -> bool:
    resolved = path.resolve()
    if resolved == LEGACY_REPO_ROOT or LEGACY_REPO_ROOT in resolved.parents:
        return False
    parts = set(path.parts)
    if allow_case_sets and "case_sets" in parts:
        return True
    return not bool(parts & DISALLOWED_READ_PARTS)


def safe_read_paths(paths: Iterable[Path]) -> tuple[bool, list[str]]:
    violations: list[str] = []
    for path in paths:
        allow_case_sets = path in {
            CASE_SET_PATH,
            SAME_ENGINE_DENOMINATOR_PATH,
            CONTROLS_PATH,
        }
        if not path_is_safe_input(path, allow_case_sets=allow_case_sets):
            violations.append(str(path))
    return not violations, violations


def add_source_file(rows: list[dict[str, str]], source_file: str) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for row in rows:
        copied = dict(row)
        copied["_source_file"] = source_file
        result.append(copied)
    return result


def combine_expected_rows(
    base_expected: list[dict[str, str]], extra_expected: list[dict[str, str]]
) -> dict[str, dict[str, str]]:
    expected_map: dict[str, dict[str, str]] = {}
    for row in base_expected + extra_expected:
        expected_map[row["fixture_row_id"]] = row
    return expected_map


def duplicate_positions(rows: list[dict[str, str]], field: str) -> set[int]:
    seen: set[str] = set()
    duplicate_indexes: set[int] = set()
    for index, row in enumerate(rows):
        value = row.get(field, "")
        if is_empty(value):
            continue
        if value in seen:
            duplicate_indexes.add(index)
        seen.add(value)
    return duplicate_indexes


def validate_status_values(
    row: dict[str, str], allowed_values: set[str], errors: list[str]
) -> None:
    for field in STATUS_FIELDS:
        if field not in row:
            continue
        value = (row.get(field) or "").strip()
        if not value:
            continue
        if field in BOOLEAN_FIELDS and value not in BOOLEAN_OR_NA_VALUES:
            errors.append(f"invalid_boolean_value:{field}={value}")
        if value not in allowed_values:
            errors.append(f"invalid_status_value:{field}={value}")


def validate_required_fields(
    row: dict[str, str],
    required_fields: list[str],
    errors: list[str],
    warnings: list[str],
) -> None:
    for field in required_fields:
        if field not in row:
            warnings.append(f"required_field_not_materialized_in_fixture:{field}")
            continue
        if is_empty(row.get(field)):
            errors.append(f"missing_required:{field}")


def validate_forbidden_fields(
    row: dict[str, str], forbidden_fields: list[str], errors: list[str]
) -> None:
    for field in forbidden_fields:
        if field in row and is_populated(row.get(field)):
            errors.append(f"forbidden_field:{field}")


def validate_identity_fields(row: dict[str, str], errors: list[str]) -> None:
    if is_empty(row.get("fixture_row_id")):
        errors.append("missing_required:fixture_row_id")
    if is_empty(row.get("record_id")):
        errors.append("missing_required:record_id")


def validate_safety_flags(row: dict[str, str], errors: list[str]) -> int:
    failed = 0
    if row.get("fixture_only") != "true":
        errors.append("missing_safety_flag:fixture_only")
        failed += 1
    if row.get("not_paper_evidence") != "true":
        errors.append("missing_safety_flag:not_paper_evidence")
        failed += 1
    if row.get("evidence_source") != "synthetic_fixture":
        errors.append("invalid_evidence_source")
        failed += 1
    return failed


def validate_record_type_specific_rules(
    row: dict[str, str], errors: list[str]
) -> None:
    record_type = row.get("record_type", "")

    if record_type in {"rewrite_candidate_cell", "user_run_candidate_cell"}:
        if is_empty(row.get("candidate_id")):
            errors.append("missing_required:candidate_id")

    if record_type == "rewrite_candidate_cell":
        if row.get("route") == "same_engine_rewrite" and is_empty(
            row.get("denominator_id")
        ):
            errors.append("missing_required:denominator_id")

    if record_type == "user_run_candidate_cell":
        if row.get("route") == "same_engine_rewrite" and is_empty(
            row.get("denominator_id")
        ):
            errors.append("missing_required:denominator_id")

    if record_type in {"plan_observability_artifact", "retained_summary_artifact"}:
        if is_empty(row.get("artifact_id")):
            errors.append("missing_required:artifact_id")

    if record_type == "verifier_support_pair":
        if is_empty(row.get("support_pair_id")):
            errors.append("missing_required:support_pair_id")

    if record_type == "portability_candidate_cell":
        if is_empty(row.get("target_engine")):
            errors.append("missing_required:target_engine")
        if is_populated(row.get("denominator_id")):
            errors.append("forbidden_field:denominator_id")

    if record_type == "retained_summary_artifact":
        if bool_value(row.get("metric_eligible")):
            errors.append("forbidden_value:metric_eligible_true")

    if row.get("status") == "N.A." and is_empty(row.get("na_reason")):
        errors.append("missing_required:na_reason")

    if row.get("na_reason") == "target_timing_missing" and record_type != (
        "portability_candidate_cell"
    ):
        errors.append("target_timing_missing_requires_portability_record")

    if row.get("failure_type") == "verifier_unknown" and record_type != (
        "verifier_support_pair"
    ):
        errors.append("verifier_unknown_requires_verifier_support_pair")

    if any(
        row.get(field) == "timing_missing"
        for field in ("status", "result_status", "failure_type", "na_reason")
    ):
        if row.get("timed") == "true" and row.get("timing_eligible") == "true":
            errors.append("timing_missing_requires_not_timed_or_ineligible")

    if any(
        row.get(field) == "target_timing_missing"
        for field in ("status", "result_status", "failure_type", "na_reason")
    ):
        if record_type != "portability_candidate_cell":
            errors.append("target_timing_missing_requires_portability_record")
        if row.get("timed") == "true" and row.get("timing_eligible") == "true":
            errors.append("target_timing_missing_requires_not_timed_or_ineligible")

    if row.get("exact") == "true" and row.get("executed") == "false":
        errors.append("exact_true_requires_executed_true")

    if row.get("result_status") == "mismatch":
        if row.get("executed") != "true":
            errors.append("mismatch_requires_executed_true")
        if row.get("exact") != "false":
            errors.append("mismatch_requires_exact_false")

    if is_populated(row.get("latency_ms")) or is_populated(row.get("speedup_ratio")):
        if row.get("timed") != "true" or row.get("timing_eligible") != "true":
            if record_type == "rewrite_candidate_cell":
                errors.append("timing_fields_require_timed_and_eligible")


def case_join_passes(row: dict[str, str], case_ids: set[str]) -> bool:
    case_id = row.get("case_id")
    if is_populated(case_id):
        return case_id in case_ids
    return row.get("case_set") == "common_core_v0"


def validate_record_denominator_policy(
    row: dict[str, str],
    case_ids: set[str],
    same_engine_ids: set[str],
    control_ids: set[str],
    errors: list[str],
    notes: list[str],
) -> None:
    record_type = row.get("record_type", "")
    case_id = row.get("case_id")

    if is_populated(case_id):
        if case_id in case_ids:
            notes.append("case_set_join=pass")
        else:
            errors.append("case_join_failed:common_core_v0")
            notes.append("case_set_join=fail")
    elif row.get("case_set") == "common_core_v0":
        notes.append("case_set_join=pass_support_scope")

    denominator_id = row.get("denominator_id", "")
    if record_type == "control_cell":
        if is_empty(denominator_id):
            errors.append("missing_required:denominator_id")
            return
        if denominator_id not in control_ids:
            errors.append("denominator_join_failed:controls_360")
            notes.append("control_join=fail")
        else:
            notes.append("control_join=pass")
    elif record_type in {"rewrite_candidate_cell", "user_run_candidate_cell"}:
        if row.get("route") == "same_engine_rewrite":
            if is_empty(denominator_id):
                errors.append("missing_required:denominator_id")
                return
            if denominator_id not in same_engine_ids:
                errors.append("denominator_join_failed:same_engine_120")
                notes.append("same_engine_join=fail")
            else:
                notes.append("same_engine_join=pass")
    elif record_type in {
        "plan_observability_artifact",
        "verifier_support_pair",
        "retained_summary_artifact",
        "portability_candidate_cell",
    }:
        if is_empty(denominator_id):
            notes.append("support_or_portability_boundary_no_track_a_join")


def validate_fixture_row(
    row: dict[str, str],
    row_index: int,
    duplicate_fixture_indexes: set[int],
    duplicate_record_indexes: set[int],
    rule_map: dict[str, dict[str, str]],
    allowed_values: set[str],
    case_ids: set[str],
    same_engine_ids: set[str],
    control_ids: set[str],
) -> tuple[bool, list[str], list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []
    record_type = row.get("record_type", "")

    safety_failures = validate_safety_flags(row, errors)
    validate_identity_fields(row, errors)

    if row_index in duplicate_fixture_indexes:
        errors.append("duplicate_fixture_row_id")
    if row_index in duplicate_record_indexes:
        errors.append("duplicate_record_id")

    if not record_type:
        errors.append("missing_required:record_type")
    elif record_type not in rule_map:
        errors.append(f"unknown_record_type:{record_type}")
    else:
        rules = rule_map[record_type]
        validate_required_fields(
            row,
            split_fields(rules.get("required_fields")),
            errors,
            warnings,
        )
        validate_forbidden_fields(row, split_fields(rules.get("forbidden_fields")), errors)
        if rules.get("denominator_required") == "true" and is_empty(
            row.get("denominator_id")
        ):
            errors.append("missing_required:denominator_id")

    validate_status_values(row, allowed_values, errors)
    validate_record_type_specific_rules(row, errors)
    validate_record_denominator_policy(
        row,
        case_ids,
        same_engine_ids,
        control_ids,
        errors,
        notes,
    )

    return (
        not errors,
        sorted(set(errors)),
        sorted(set(warnings)),
        sorted(set(notes)),
        safety_failures,
    )


def validate_join_examples(
    join_rows: list[dict[str, str]],
    fixture_by_id: dict[str, dict[str, str]],
    case_ids: set[str],
    same_engine_ids: set[str],
    control_ids: set[str],
) -> tuple[dict[str, object], dict[str, list[str]]]:
    notes_by_fixture: dict[str, list[str]] = {}
    checked = 0
    passed = 0
    failed = 0

    for join in join_rows:
        checked += 1
        fixture_id = join.get("fixture_row_id", "")
        row = fixture_by_id.get(fixture_id)
        expected_status = join.get("expected_join_status", "")
        row_notes: list[str] = []
        actual_checks: list[bool] = []

        if row is None:
            actual_checks.append(False)
            row_notes.append("denominator_join_fixture_missing")
        else:
            if bool_value(join.get("joins_to_case_sets")):
                ok = case_join_passes(row, case_ids)
                actual_checks.append(ok)
                row_notes.append(f"example_case_set_join={'pass' if ok else 'fail'}")
            if bool_value(join.get("joins_to_same_engine_120")):
                ok = row.get("denominator_id") in same_engine_ids
                actual_checks.append(ok)
                row_notes.append(f"example_same_engine_join={'pass' if ok else 'fail'}")
            if bool_value(join.get("joins_to_controls_360")):
                ok = row.get("denominator_id") in control_ids
                actual_checks.append(ok)
                row_notes.append(f"example_control_join={'pass' if ok else 'fail'}")
            if not actual_checks:
                actual_checks.append(is_empty(row.get("denominator_id")))
                row_notes.append("example_support_boundary_no_metric_denominator")

        observed_join_passed = all(actual_checks)
        if expected_status.startswith("fail") and row is not None:
            if is_empty(row.get("denominator_id")):
                observed_join_passed = False

        expected_failure = expected_status.startswith("fail")
        expected_pass = expected_status.startswith("pass")
        join_passed = (
            (expected_pass and observed_join_passed)
            or (expected_failure and not observed_join_passed)
        )

        if join_passed:
            passed += 1
        else:
            failed += 1
            row_notes.append(
                "denominator_join_expectation_mismatch:"
                f"expected={expected_status};observed={observed_join_passed}"
            )

        notes_by_fixture.setdefault(fixture_id, []).extend(row_notes)

    return {"checked": checked, "passed": passed, "failed": failed}, notes_by_fixture


def make_failure_summary(missing: list[str], path_violations: list[str]) -> dict[str, object]:
    failed_count = len(missing) + len(path_violations)
    return {
        "base_fixture_rows_checked": 0,
        "extra_fixture_rows_checked": 0,
        "total_fixture_rows_checked": 0,
        "expected_valid_rows": 0,
        "expected_invalid_rows": 0,
        "expected_valid_passed": 0,
        "expected_invalid_failed_as_expected": 0,
        "unexpected_pass_count": 0,
        "unexpected_fail_count": 0,
        "duplicate_id_checks": {
            "duplicate_fixture_row_ids": 0,
            "duplicate_record_ids": 0,
        },
        "denominator_join_checks": {
            "checked": 0,
            "passed": 0,
            "failed": failed_count,
            "missing_required_files": missing,
            "disallowed_read_paths": path_violations,
        },
        "safety_flag_checks": {
            "checked": 0,
            "failed": 0,
        },
        "metrics_computed": False,
        "production_retained_evidence_parsed": False,
        "adapter_implemented": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }


def write_summary(path: Path, summary: dict[str, object]) -> None:
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(
    path: Path,
    summary: dict[str, object],
    fixture_files: list[str],
    extra_files: list[str],
) -> None:
    extra_count = summary["extra_fixture_rows_checked"]
    lines = [
        "# Ledger Fixture Validator Hardening Report",
        "",
        "## Purpose And Scope",
        "",
        "This report was generated by `scripts/dev/validate_ledger_fixtures.py`.",
        "The validator remains fixture-only: it reads synthetic fixture CSVs and",
        "static Common-core denominator scaffolds for join checks.",
        "",
        "## What Was Hardened",
        "",
        "- Optional extra synthetic fixture and expected-result inputs.",
        "- Duplicate `fixture_row_id` and `record_id` detection.",
        "- Stronger ID, safety-flag, status, denominator, and consistency checks.",
        "- Record-type-specific identity checks for candidates, artifacts, and support pairs.",
        "- Hardening-specific machine-readable outputs.",
        "",
        "## Fixture Files Read",
        "",
    ]
    lines.extend(f"- `{name}`" for name in fixture_files)
    if extra_files:
        lines.append("")
        lines.append("Extra synthetic hardening files:")
        lines.extend(f"- `{name}`" for name in extra_files)
    lines.extend(
        [
            "",
            "## Additional Cases Added",
            "",
            f"- Extra fixture rows checked: {extra_count}",
            "- Invalid hardening examples cover unknown record types, duplicate",
            "  record IDs, safety-flag failures, invalid evidence source, paper",
            "  evidence flag failures, missing candidate/target IDs, forbidden",
            "  timing fields, retained summary metric eligibility, invalid status",
            "  values, denominator mismatches, and inconsistent timing/exact states.",
            "- Valid hardening examples cover timing-missing rewrite rows,",
            "  target-timing-missing portability rows, and retained-summary support rows.",
            "",
            "## Results",
            "",
            f"- Base fixture rows checked: {summary['base_fixture_rows_checked']}",
            f"- Extra fixture rows checked: {summary['extra_fixture_rows_checked']}",
            f"- Total fixture rows checked: {summary['total_fixture_rows_checked']}",
            f"- Expected-valid rows: {summary['expected_valid_rows']}",
            f"- Expected-invalid rows: {summary['expected_invalid_rows']}",
            f"- Expected-valid rows passed: {summary['expected_valid_passed']}",
            "- Expected-invalid rows failed as expected: "
            f"{summary['expected_invalid_failed_as_expected']}",
            f"- Unexpected pass count: {summary['unexpected_pass_count']}",
            f"- Unexpected fail count: {summary['unexpected_fail_count']}",
            "- Denominator join examples: "
            f"{summary['denominator_join_checks']['passed']}/"
            f"{summary['denominator_join_checks']['checked']} passed",
            "- Safety flag failures observed as expected where fixtures are invalid: "
            f"{summary['safety_flag_checks']['failed']}",
            "",
            "## Limitations",
            "",
            "This validator does not validate production retained evidence. Some",
            "future production ledger columns named by policy are not materialized",
            "in the synthetic fixture table and remain warnings rather than hard",
            "failures for otherwise valid synthetic rows.",
            "",
            "## Explicit Non-Goals",
            "",
            "- No metrics were computed.",
            "- No production retained evidence was parsed.",
            "- No retained-evidence adapter was implemented.",
            "- No reports/results were read or written.",
            "- No denominator values, paper results, case membership, case packages,",
            "  or raw legacy evidence were changed.",
            "",
            "## Next Safe Action",
            "",
            "Review this hardened fixture-only validator and decide whether to add",
            "CI/dev-smoke wiring or plan a separately authorized production ledger",
            "validator. Do not parse production retained evidence, implement adapters,",
            "compute metrics, or render paper tables without explicit authorization.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    fixtures_dir = args.fixtures_dir
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    base_paths = {key: fixtures_dir / filename for key, filename in BASE_FIXTURE_FILES.items()}
    required_paths = list(base_paths.values()) + [
        CASE_SET_PATH,
        SAME_ENGINE_DENOMINATOR_PATH,
        CONTROLS_PATH,
    ]

    input_paths = list(required_paths)
    extra_fixture_rows: list[dict[str, str]] = []
    extra_expected_rows: list[dict[str, str]] = []
    extra_files_read: list[str] = []

    if args.extra_fixtures and args.extra_expected:
        if args.extra_fixtures.exists() and args.extra_expected.exists():
            input_paths.extend([args.extra_fixtures, args.extra_expected])
            extra_fixture_rows = add_source_file(
                read_csv(args.extra_fixtures), str(args.extra_fixtures)
            )
            extra_expected_rows = read_csv(args.extra_expected)
            extra_files_read = [str(args.extra_fixtures), str(args.extra_expected)]
        elif args.extra_fixtures.exists() or args.extra_expected.exists():
            missing_extra = [
                str(path)
                for path in (args.extra_fixtures, args.extra_expected)
                if not path.exists()
            ]
            missing = require_files(required_paths) + missing_extra
            safe, path_violations = safe_read_paths(input_paths)
            summary = make_failure_summary(missing, [] if safe else path_violations)
            write_summary(out_dir / SUMMARY_FILENAME, summary)
            print(f"Missing required files: {', '.join(missing)}", file=sys.stderr)
            return 1
    elif args.extra_fixtures or args.extra_expected:
        existing = [path for path in (args.extra_fixtures, args.extra_expected) if path]
        input_paths.extend(existing)

    missing = require_files(required_paths)
    safe, path_violations = safe_read_paths(input_paths)
    if missing or path_violations:
        summary = make_failure_summary(missing, path_violations)
        write_summary(out_dir / SUMMARY_FILENAME, summary)
        if missing:
            print(f"Missing required files: {', '.join(missing)}", file=sys.stderr)
        if path_violations:
            print(
                f"Disallowed read paths: {', '.join(path_violations)}",
                file=sys.stderr,
            )
        return 1

    base_fixture_rows = add_source_file(read_csv(base_paths["fixtures"]), str(base_paths["fixtures"]))
    base_expected_rows = read_csv(base_paths["expected"])
    rule_rows = read_csv(base_paths["rules"])
    allowed_rows = read_csv(base_paths["allowed"])
    join_rows = read_csv(base_paths["joins"])

    all_fixture_rows = base_fixture_rows + extra_fixture_rows
    expected_map = combine_expected_rows(base_expected_rows, extra_expected_rows)
    rule_map = {row["record_type"]: row for row in rule_rows}
    allowed_values = BUILTIN_ALLOWED_STATUS_VALUES | {
        row["allowed_value"] for row in allowed_rows if row.get("allowed_value")
    }

    case_ids = load_id_set(CASE_SET_PATH, "case_id")
    same_engine_ids = load_id_set(SAME_ENGINE_DENOMINATOR_PATH, "denominator_id")
    control_ids = load_id_set(CONTROLS_PATH, "control_id")

    fixture_by_id = {row["fixture_row_id"]: row for row in all_fixture_rows}
    join_summary, join_notes = validate_join_examples(
        join_rows,
        fixture_by_id,
        case_ids,
        same_engine_ids,
        control_ids,
    )

    duplicate_fixture_indexes = duplicate_positions(all_fixture_rows, "fixture_row_id")
    duplicate_record_indexes = duplicate_positions(all_fixture_rows, "record_id")
    record_id_counts = Counter(
        row.get("record_id") for row in all_fixture_rows if is_populated(row.get("record_id"))
    )
    fixture_id_counts = Counter(
        row.get("fixture_row_id")
        for row in all_fixture_rows
        if is_populated(row.get("fixture_row_id"))
    )

    result_rows: list[dict[str, str]] = []
    expected_valid_rows = 0
    expected_invalid_rows = 0
    expected_valid_passed = 0
    expected_invalid_failed_as_expected = 0
    unexpected_pass_count = 0
    unexpected_fail_count = 0
    safety_checked = 0
    safety_failed = 0

    for index, row in enumerate(all_fixture_rows):
        fixture_id = row.get("fixture_row_id", "")
        expected = expected_map.get(fixture_id)
        expected_valid = bool_value(expected.get("expected_valid") if expected else None)
        if expected_valid:
            expected_valid_rows += 1
        else:
            expected_invalid_rows += 1

        observed_valid, errors, warnings, notes, safety_failures = validate_fixture_row(
            row,
            index,
            duplicate_fixture_indexes,
            duplicate_record_indexes,
            rule_map,
            allowed_values,
            case_ids,
            same_engine_ids,
            control_ids,
        )
        safety_checked += 3
        safety_failed += safety_failures

        expected_errors = expected_error_tokens(
            expected.get("expected_errors") if expected else "missing_expected_result"
        )
        if expected is None:
            errors.append("missing_expected_result")
            observed_valid = False

        missing_expected_errors = expected_errors - set(errors)
        if missing_expected_errors:
            errors.extend(
                f"missing_expected_error:{token}"
                for token in sorted(missing_expected_errors)
            )
            observed_valid = False

        notes.extend(join_notes.get(fixture_id, []))
        denominator_mismatch = any(
            note.startswith("denominator_join_expectation_mismatch") for note in notes
        )

        if expected_valid:
            validation_passed = observed_valid and not denominator_mismatch
            if validation_passed:
                expected_valid_passed += 1
            else:
                unexpected_fail_count += 1
        else:
            validation_passed = (not observed_valid) and not missing_expected_errors
            if validation_passed:
                expected_invalid_failed_as_expected += 1
            else:
                unexpected_pass_count += 1

        result_rows.append(
            {
                "fixture_row_id": fixture_id,
                "record_type": row.get("record_type", ""),
                "source_file": row.get("_source_file", ""),
                "expected_valid": str(expected_valid).lower(),
                "observed_valid": str(observed_valid).lower(),
                "validation_passed": str(validation_passed).lower(),
                "errors": ";".join(sorted(set(errors))),
                "warnings": ";".join(sorted(set(warnings))),
                "notes": ";".join(sorted(set(notes))),
            }
        )

    duplicate_fixture_values = [
        value for value, count in fixture_id_counts.items() if count > 1
    ]
    duplicate_record_values = [
        value for value, count in record_id_counts.items() if count > 1
    ]

    summary = {
        "base_fixture_rows_checked": len(base_fixture_rows),
        "extra_fixture_rows_checked": len(extra_fixture_rows),
        "total_fixture_rows_checked": len(all_fixture_rows),
        "expected_valid_rows": expected_valid_rows,
        "expected_invalid_rows": expected_invalid_rows,
        "expected_valid_passed": expected_valid_passed,
        "expected_invalid_failed_as_expected": expected_invalid_failed_as_expected,
        "unexpected_pass_count": unexpected_pass_count,
        "unexpected_fail_count": unexpected_fail_count,
        "duplicate_id_checks": {
            "checked": len(all_fixture_rows),
            "duplicate_fixture_row_ids": len(duplicate_fixture_values),
            "duplicate_record_ids": len(duplicate_record_values),
            "duplicate_fixture_row_id_values": duplicate_fixture_values,
            "duplicate_record_id_values": duplicate_record_values,
        },
        "denominator_join_checks": join_summary,
        "safety_flag_checks": {
            "checked": safety_checked,
            "failed": safety_failed,
        },
        "metrics_computed": False,
        "production_retained_evidence_parsed": False,
        "adapter_implemented": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }

    write_csv(
        out_dir / RESULTS_FILENAME,
        result_rows,
        [
            "fixture_row_id",
            "record_type",
            "source_file",
            "expected_valid",
            "observed_valid",
            "validation_passed",
            "errors",
            "warnings",
            "notes",
        ],
    )
    write_summary(out_dir / SUMMARY_FILENAME, summary)
    write_report(
        out_dir / REPORT_FILENAME,
        summary,
        list(BASE_FIXTURE_FILES.values()),
        extra_files_read,
    )

    hard_failure = (
        unexpected_pass_count > 0
        or unexpected_fail_count > 0
        or join_summary["failed"] > 0
    )
    return 1 if hard_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
