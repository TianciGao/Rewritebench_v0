#!/usr/bin/env python3
"""Static non-destructive validator for case package v2 references."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from sql_rewrite_bench.case_package_v2_resolver import (
    DirectoryClassification,
    FormatFinding,
    InternalFormatCheck,
    ResolvedReference,
    resolve_case_package_v2,
)


REFERENCE_FIELDS = [
    "case_id",
    "reference_group",
    "field",
    "observed_value",
    "resolved_path",
    "path_base",
    "required",
    "exists",
    "safety_status",
    "status",
    "notes",
]

INTERNAL_CHECK_FIELDS = [
    "field_group",
    "field",
    "observed_value",
    "expected_shape",
    "status",
    "notes",
]

FINDING_FIELDS = [
    "case_id",
    "file_path",
    "finding_type",
    "severity",
    "current_value",
    "recommended_v2_value",
    "fix_now",
    "notes",
]

DIRECTORY_FIELDS = [
    "directory",
    "current_role",
    "v2_role",
    "keep_now",
    "delete_later_condition",
    "notes",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _rel(path: str, repo_root: Path) -> str:
    try:
        return str(Path(path).resolve().relative_to(repo_root.resolve()))
    except Exception:
        return path


def reference_rows(case_id: str, refs: list[ResolvedReference], repo_root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for ref in refs:
        rows.append(
            {
                "case_id": case_id,
                "reference_group": ref.field_group,
                "field": ref.field,
                "observed_value": ref.observed_value,
                "resolved_path": _rel(ref.resolved_path, repo_root) if ref.resolved_path else "",
                "path_base": ref.path_base,
                "required": str(ref.required).lower(),
                "exists": str(ref.exists).lower(),
                "safety_status": ref.safety_status,
                "status": ref.status,
                "notes": ref.notes,
            }
        )
    return rows


def internal_check_rows(checks: list[InternalFormatCheck]) -> list[dict[str, str]]:
    return [
        {
            "field_group": check.field_group,
            "field": check.field,
            "observed_value": check.observed_value,
            "expected_shape": check.expected_shape,
            "status": check.status,
            "notes": check.notes,
        }
        for check in checks
    ]


def finding_rows(findings: list[FormatFinding], repo_root: Path) -> list[dict[str, str]]:
    return [
        {
            "case_id": finding.case_id,
            "file_path": _rel(finding.file_path, repo_root),
            "finding_type": finding.finding_type,
            "severity": finding.severity,
            "current_value": finding.current_value,
            "recommended_v2_value": finding.recommended_v2_value,
            "fix_now": str(finding.fix_now).lower(),
            "notes": finding.notes,
        }
        for finding in findings
    ]


def directory_rows(rows: list[DirectoryClassification]) -> list[dict[str, str]]:
    return [
        {
            "directory": row.directory,
            "current_role": row.current_role,
            "v2_role": row.v2_role,
            "keep_now": str(row.keep_now).lower(),
            "delete_later_condition": row.delete_later_condition,
            "notes": row.notes,
        }
        for row in rows
    ]


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, help="Case directory, for example cases/PERF/PERF_0006")
    parser.add_argument(
        "--output-dir",
        help="Optional directory for CSV outputs. The validator never writes inside the case package.",
    )
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    result = resolve_case_package_v2(repo_root=repo_root, case_path=Path(args.case))

    print(f"case_id={result.case_id}")
    print(f"overall_status={result.overall_status}")
    print(f"reference_rows={len(result.references)}")
    print(f"internal_checks={len(result.internal_checks)}")
    print(f"format_findings={len(result.findings)}")
    print("profile_first_schema_ref_supported=true")
    print("db_execution_run=false")
    print("checker_execution_run=false")
    print("official_metrics_computed=false")

    if args.output_dir:
        out_dir = Path(args.output_dir)
        refs = reference_rows(result.case_id, result.references, repo_root)
        checks = internal_check_rows(result.internal_checks)
        findings = finding_rows(result.findings, repo_root)
        dirs = directory_rows(result.directory_classification)
        _write_csv(out_dir / "v2_ref_validation_results.csv", REFERENCE_FIELDS, refs)
        _write_csv(out_dir / "perf0006_v2_ref_check.csv", REFERENCE_FIELDS, refs)
        _write_csv(out_dir / "perf0006_internal_format_check.csv", INTERNAL_CHECK_FIELDS, checks)
        _write_csv(out_dir / "v2_format_inconsistency_findings.csv", FINDING_FIELDS, findings)
        _write_csv(out_dir / "perf0006_directory_classification.csv", DIRECTORY_FIELDS, dirs)

    return 0 if result.overall_status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
