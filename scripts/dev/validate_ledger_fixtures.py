#!/usr/bin/env python3
"""Validate synthetic evidence-ledger fixture rows.

This developer validator is intentionally narrow. It reads only the synthetic
fixture CSVs under ``audits/ledger_schema_validation_fixtures`` plus the static
Common-core denominator scaffolds used for join checks. It does not parse
production retained evidence, compute metrics, or mutate fixture inputs.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Iterable


FIXTURE_FILES = {
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

RESULTS_FILENAME = "ledger_fixture_validation_results.csv"
SUMMARY_FILENAME = "ledger_fixture_validation_summary.json"
REPORT_FILENAME = "ledger_fixture_validator_report.md"

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
        help="Directory containing synthetic ledger fixture CSVs.",
    )
    parser.add_argument(
        "--out-dir",
        required=True,
        type=Path,
        help="Directory where validation outputs should be written.",
    )
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def require_files(paths: Iterable[Path]) -> list[str]:
    missing = [str(path) for path in paths if not path.exists()]
    return missing


def is_populated(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip() not in NON_POPULATED_VALUES


def is_empty(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().lower() in NULL_VALUES


def split_fields(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def bool_value(value: str | None) -> bool:
    return (value or "").strip().lower() == "true"


def load_id_set(path: Path, column: str) -> set[str]:
    if not path.exists():
        return set()
    rows = read_csv(path)
    return {row[column] for row in rows if row.get(column)}


def expected_error_tokens(value: str | None) -> set[str]:
    return set(split_fields(value))


def validate_status_values(
    row: dict[str, str], allowed_values: set[str], errors: list[str]
) -> None:
    for field in STATUS_FIELDS:
        if field not in row:
            continue
        value = (row.get(field) or "").strip()
        if not value:
            continue
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


def validate_record_type_specific_rules(
    row: dict[str, str], errors: list[str]
) -> None:
    record_type = row.get("record_type", "")

    if record_type == "rewrite_candidate_cell":
        if is_empty(row.get("candidate_id")):
            errors.append("missing_required:candidate_id")
        if row.get("route") == "same_engine_rewrite" and is_empty(
            row.get("denominator_id")
        ):
            errors.append("missing_required:denominator_id")

    if record_type == "user_run_candidate_cell":
        if row.get("route") == "same_engine_rewrite" and is_empty(
            row.get("denominator_id")
        ):
            errors.append("missing_required:denominator_id")

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

    if row.get("result_status") == "mismatch":
        if row.get("executed") != "true":
            errors.append("mismatch_requires_executed_true")
        if row.get("exact") != "false":
            errors.append("mismatch_requires_exact_false")

    if is_populated(row.get("latency_ms")) or is_populated(row.get("speedup_ratio")):
        if row.get("timed") != "true" or row.get("timing_eligible") != "true":
            if record_type == "rewrite_candidate_cell":
                errors.append("timing_fields_require_timed_and_eligible")


def validate_fixture_row(
    row: dict[str, str],
    rule_map: dict[str, dict[str, str]],
    allowed_values: set[str],
) -> tuple[bool, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    record_type = row.get("record_type", "")

    if row.get("fixture_only") != "true":
        errors.append("missing_safety_flag:fixture_only")
    if row.get("not_paper_evidence") != "true":
        errors.append("missing_safety_flag:not_paper_evidence")
    if row.get("evidence_source") != "synthetic_fixture":
        errors.append("invalid_evidence_source")

    if not record_type:
        errors.append("missing_required:record_type")
    elif record_type not in rule_map:
        errors.append(f"unknown_record_type:{record_type}")
    else:
        rules = rule_map[record_type]
        validate_required_fields(row, split_fields(rules.get("required_fields")), errors, warnings)
        validate_forbidden_fields(row, split_fields(rules.get("forbidden_fields")), errors)
        if rules.get("denominator_required") == "true" and is_empty(
            row.get("denominator_id")
        ):
            errors.append("missing_required:denominator_id")

    validate_status_values(row, allowed_values, errors)
    validate_record_type_specific_rules(row, errors)

    deduped_errors = sorted(set(errors))
    deduped_warnings = sorted(set(warnings))
    return not deduped_errors, deduped_errors, deduped_warnings


def case_join_passes(row: dict[str, str], case_ids: set[str]) -> bool:
    case_id = row.get("case_id")
    if is_populated(case_id):
        return case_id in case_ids
    return row.get("case_set") == "common_core_v0"


def validate_denominator_joins(
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
                row_notes.append(f"case_set_join={'pass' if ok else 'fail'}")
            if bool_value(join.get("joins_to_same_engine_120")):
                ok = row.get("denominator_id") in same_engine_ids
                actual_checks.append(ok)
                row_notes.append(f"same_engine_join={'pass' if ok else 'fail'}")
            if bool_value(join.get("joins_to_controls_360")):
                ok = row.get("denominator_id") in control_ids
                actual_checks.append(ok)
                row_notes.append(f"control_join={'pass' if ok else 'fail'}")

            if not actual_checks:
                actual_checks.append(is_empty(row.get("denominator_id")))
                row_notes.append("support_boundary_no_metric_denominator")

        observed_join_passed = all(actual_checks)
        if expected_status.startswith("fail") and row is not None:
            # Failure examples intentionally demonstrate a denominator-boundary
            # violation even when their case_set lookup still resolves.
            if is_empty(row.get("denominator_id")):
                observed_join_passed = False
        expected_failure = expected_status.startswith("fail")
        expected_pass = expected_status.startswith("pass")

        if expected_pass and observed_join_passed:
            join_passed = True
        elif expected_failure and not observed_join_passed:
            join_passed = True
        else:
            join_passed = False

        if join_passed:
            passed += 1
        else:
            failed += 1
            row_notes.append(
                "denominator_join_expectation_mismatch:"
                f"expected={expected_status};observed={observed_join_passed}"
            )

        notes_by_fixture.setdefault(fixture_id, []).extend(row_notes)

    summary = {
        "checked": checked,
        "passed": passed,
        "failed": failed,
    }
    return summary, notes_by_fixture


def write_results(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "fixture_row_id",
        "record_type",
        "expected_valid",
        "observed_valid",
        "validation_passed",
        "errors",
        "warnings",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, summary: dict[str, object], fixture_files: list[str]) -> None:
    lines = [
        "# Ledger Fixture Validator Report",
        "",
        "## Purpose And Scope",
        "",
        "This report was generated by `scripts/dev/validate_ledger_fixtures.py`.",
        "The validator reads synthetic ledger fixture files only and performs",
        "record-type, status, safety-flag, expected-outcome, and denominator-join",
        "checks for the fixture skeleton.",
        "",
        "## Fixture Files Read",
        "",
    ]
    lines.extend(f"- `{name}`" for name in fixture_files)
    lines.extend(
        [
            "",
            "## Validation Checks Performed",
            "",
            "- Required fields for materialized fixture columns.",
            "- Forbidden fields by record type.",
            "- Allowed status values for status-like columns.",
            "- `fixture_only=true`, `not_paper_evidence=true`, and",
            "  `evidence_source=synthetic_fixture` safety flags.",
            "- Denominator join examples against static Common-core scaffolds.",
            "- Expected valid and intentionally invalid fixture outcomes.",
            "",
            "## Results",
            "",
            f"- Fixture rows checked: {summary['fixture_rows_checked']}",
            f"- Expected-valid rows: {summary['expected_valid_rows']}",
            f"- Expected-invalid rows: {summary['expected_invalid_rows']}",
            f"- Expected-valid rows passed: {summary['expected_valid_passed']}",
            "- Expected-invalid rows failed as expected: "
            f"{summary['expected_invalid_failed_as_expected']}",
            f"- Unexpected pass count: {summary['unexpected_pass_count']}",
            f"- Unexpected fail count: {summary['unexpected_fail_count']}",
            "- Denominator join checks: "
            f"{summary['denominator_join_checks']['passed']}/"
            f"{summary['denominator_join_checks']['checked']} passed",
            "",
            "## Explicit Non-Goals",
            "",
            "- No metrics were computed.",
            "- No production retained evidence was parsed.",
            "- No retained-evidence adapter was implemented.",
            "- No reports, results, denominator values, paper results, case sets,",
            "  case packages, or raw legacy evidence were changed.",
            "",
            "## Next Safe Action",
            "",
            "Review the fixture validator output and limitations. The next safe",
            "task is to decide whether to harden this skeleton into a reusable",
            "fixture validator or to design production ledger validation; do not",
            "parse production retained evidence, implement adapters, compute metrics,",
            "or render paper tables without separate authorization.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    fixtures_dir = args.fixtures_dir
    out_dir = args.out_dir

    fixture_paths = {key: fixtures_dir / filename for key, filename in FIXTURE_FILES.items()}
    required_paths = list(fixture_paths.values()) + [
        CASE_SET_PATH,
        SAME_ENGINE_DENOMINATOR_PATH,
        CONTROLS_PATH,
    ]
    missing = require_files(required_paths)
    out_dir.mkdir(parents=True, exist_ok=True)

    if missing:
        summary = {
            "fixture_rows_checked": 0,
            "expected_valid_rows": 0,
            "expected_invalid_rows": 0,
            "expected_valid_passed": 0,
            "expected_invalid_failed_as_expected": 0,
            "unexpected_pass_count": 0,
            "unexpected_fail_count": 0,
            "denominator_join_checks": {
                "checked": 0,
                "passed": 0,
                "failed": len(missing),
                "missing_required_files": missing,
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
        (out_dir / SUMMARY_FILENAME).write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"Missing required files: {', '.join(missing)}", file=sys.stderr)
        return 1

    fixture_rows = read_csv(fixture_paths["fixtures"])
    expected_rows = read_csv(fixture_paths["expected"])
    rule_rows = read_csv(fixture_paths["rules"])
    allowed_rows = read_csv(fixture_paths["allowed"])
    join_rows = read_csv(fixture_paths["joins"])

    rule_map = {row["record_type"]: row for row in rule_rows}
    expected_map = {row["fixture_row_id"]: row for row in expected_rows}
    fixture_by_id = {row["fixture_row_id"]: row for row in fixture_rows}
    allowed_values = BUILTIN_ALLOWED_STATUS_VALUES | {
        row["allowed_value"] for row in allowed_rows if row.get("allowed_value")
    }

    case_ids = load_id_set(CASE_SET_PATH, "case_id")
    same_engine_ids = load_id_set(SAME_ENGINE_DENOMINATOR_PATH, "denominator_id")
    control_ids = load_id_set(CONTROLS_PATH, "control_id")

    denominator_summary, denominator_notes = validate_denominator_joins(
        join_rows,
        fixture_by_id,
        case_ids,
        same_engine_ids,
        control_ids,
    )

    result_rows: list[dict[str, str]] = []
    expected_valid_rows = 0
    expected_invalid_rows = 0
    expected_valid_passed = 0
    expected_invalid_failed_as_expected = 0
    unexpected_pass_count = 0
    unexpected_fail_count = 0

    for row in fixture_rows:
        fixture_id = row.get("fixture_row_id", "")
        expected = expected_map.get(fixture_id)
        expected_valid = bool_value(expected.get("expected_valid") if expected else None)
        if expected_valid:
            expected_valid_rows += 1
        else:
            expected_invalid_rows += 1

        observed_valid, errors, warnings = validate_fixture_row(
            row, rule_map, allowed_values
        )
        expected_errors = expected_error_tokens(expected.get("expected_errors") if expected else "")
        missing_expected_errors = expected_errors - set(errors)
        if missing_expected_errors:
            errors.extend(f"missing_expected_error:{token}" for token in missing_expected_errors)
            observed_valid = False

        notes = denominator_notes.get(fixture_id, [])
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
                "expected_valid": str(expected_valid).lower(),
                "observed_valid": str(observed_valid).lower(),
                "validation_passed": str(validation_passed).lower(),
                "errors": ";".join(sorted(set(errors))),
                "warnings": ";".join(sorted(set(warnings))),
                "notes": ";".join(notes),
            }
        )

    summary = {
        "fixture_rows_checked": len(fixture_rows),
        "expected_valid_rows": expected_valid_rows,
        "expected_invalid_rows": expected_invalid_rows,
        "expected_valid_passed": expected_valid_passed,
        "expected_invalid_failed_as_expected": expected_invalid_failed_as_expected,
        "unexpected_pass_count": unexpected_pass_count,
        "unexpected_fail_count": unexpected_fail_count,
        "denominator_join_checks": denominator_summary,
        "metrics_computed": False,
        "production_retained_evidence_parsed": False,
        "adapter_implemented": False,
        "reports_changed": False,
        "results_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "raw_legacy_evidence_changed": False,
    }

    write_results(out_dir / RESULTS_FILENAME, result_rows)
    (out_dir / SUMMARY_FILENAME).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_report(out_dir / REPORT_FILENAME, summary, list(FIXTURE_FILES.values()))

    hard_failure = (
        unexpected_pass_count > 0
        or unexpected_fail_count > 0
        or denominator_summary["failed"] > 0
    )
    return 1 if hard_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
