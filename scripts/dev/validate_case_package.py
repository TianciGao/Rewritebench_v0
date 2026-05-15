#!/usr/bin/env python3
"""Static validator for SQL-RewriteBench release case-package evidence pilots.

Version: v0.1
Initial mode: evidence-pilot

This validator is intentionally static. It does not read the legacy repository,
run database engines, execute validation scripts, regenerate evidence, or call
external services.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

VALIDATOR_VERSION = "v0.1"
SUPPORTED_MODES = {"evidence-pilot"}

SANITIZED_SCAN_PATTERNS = [
    "/home/tianci_gao",
    "file:/home",
    "file:/mnt",
    "file:/tmp",
    "C:\\",
    "localhost",
    "127.0.0.1",
    "WSL",
    "OPENAI_API_KEY",
    "api_key",
]

RESULT_CHECK_SCAN_PATTERNS = [
    "load_and_execute.log",
    "stderr.log",
    'stdout_log": "cases/',
    'stderr_log": "cases/',
]

REQUIRED_PILOT_PHRASES = [
    "evidence-mapping pilot only",
    "not a complete migrated case package",
    "No legacy evidence was modified",
    "denominator",
    "paper results",
    "Common-core membership",
]


@dataclass
class CheckResult:
    case_id: str
    case_path: str
    status: str = "pass"
    checks: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def fail(self, message: str) -> None:
        self.status = "fail"
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(f"PyYAML unavailable; cannot parse {path}: {exc}") from exc
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def scan_text(path: Path, patterns: list[str]) -> list[str]:
    text = read_text(path)
    return [pattern for pattern in patterns if pattern in text]


def boolish_ok(value: str | None, allowed: set[str]) -> bool:
    return (value or "").strip().lower() in allowed


def flatten_retention_entries(retention: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for key in (
        "retained_control_evidence",
        "retained_plan_evidence",
        "hard_negative_evidence",
        "sanitizable_public_evidence",
        "sanitized_public_copies",
        "private_or_original_archive",
    ):
        value = retention.get(key) or []
        if isinstance(value, list):
            entries.extend(item for item in value if isinstance(item, dict))
    return entries


def infer_case_id(case_path: Path) -> str:
    return case_path.name


def validate_migration_pilot(result: CheckResult, pilot_path: Path) -> None:
    if not pilot_path.exists():
        result.fail(f"missing {pilot_path}")
        result.checks["migration_pilot_md_exists"] = False
        return
    result.checks["migration_pilot_md_exists"] = True
    text = read_text(pilot_path)
    missing = [phrase for phrase in REQUIRED_PILOT_PHRASES if phrase not in text]
    result.checks["migration_pilot_required_phrases_ok"] = not missing
    if missing:
        result.fail(f"{pilot_path} missing required phrases: {missing}")


def validate_retention(
    result: CheckResult,
    retention_path: Path,
    case_id: str,
) -> dict[str, Any] | None:
    if not retention_path.exists():
        result.fail(f"missing {retention_path}")
        result.checks["runs_retention_yaml_exists"] = False
        return None

    result.checks["runs_retention_yaml_exists"] = True
    try:
        retention = load_yaml(retention_path)
        result.checks["yaml_parse_ok"] = True
    except Exception as exc:
        result.checks["yaml_parse_ok"] = False
        result.fail(str(exc))
        return None

    if not isinstance(retention, dict):
        result.fail(f"{retention_path} did not parse to a mapping")
        return None

    expected = {
        "case_id": case_id,
        "pool": "PORT",
        "policy_version": "runs_retention_policy_v1",
        "status": "formal_evidence_mapping_pilot",
        "physical_pilot_status": "evidence_mapping_only_not_full_case_migration",
    }
    for key, value in expected.items():
        ok = retention.get(key) == value
        result.checks[f"runs_retention_{key}_ok"] = ok
        if not ok:
            result.fail(f"{retention_path} expected {key}={value!r}, got {retention.get(key)!r}")

    notes = retention.get("public_release_notes") or {}
    required_false = {
        "full_case_package_migrated": notes.get("full_case_package_migrated") is False,
        "denominator_changed": notes.get("denominator_changed") is False,
        "paper_results_changed": notes.get("paper_results_changed") is False,
    }
    for key, ok in required_false.items():
        result.checks[f"{key}_false"] = ok
        if not ok:
            result.fail(f"{retention_path} public_release_notes.{key} must be false")

    human = retention.get("human_approval") or {}
    formal_approved = (
        human.get("formal_pilot") == "approved"
        or human.get("status") in {"approved_for_formal_pilot", "formal_pilot_approved"}
    )
    full_later = (
        human.get("full_case_migration") == "required_later"
        or retention.get("physical_pilot_status") == "evidence_mapping_only_not_full_case_migration"
    )
    result.checks["human_approval_formal_pilot_ok"] = formal_approved
    result.checks["full_case_migration_required_later_ok"] = full_later
    if not formal_approved:
        result.fail(f"{retention_path} does not record formal pilot approval")
    if not full_later:
        result.fail(f"{retention_path} does not record full case migration as required later")

    entries = flatten_retention_entries(retention)
    plan_originals = {
        f"cases/PORT/{case_id}/runs/spark/plans/rewrite_neg_01.txt",
        f"cases/PORT/{case_id}/runs/spark/plans/rewrite_pos_01.txt",
    }
    do_not_delete = {
        entry.get("original_legacy_path")
        for entry in entries
        if entry.get("do_not_delete_original") is True
    }
    public_safe = {
        entry.get("original_legacy_path")
        for entry in entries
        if entry.get("public_safe") is True
        and (entry.get("public_copy_path") or entry.get("proposed_public_path"))
    }
    do_not_ok = plan_originals.issubset(do_not_delete)
    public_safe_ok = plan_originals.issubset(public_safe)
    result.checks["spark_plan_do_not_delete_original_ok"] = do_not_ok
    result.checks["spark_plan_public_safe_copy_ok"] = public_safe_ok
    if not do_not_ok:
        result.fail(f"{retention_path} missing do_not_delete_original for all Spark plan originals")
    if not public_safe_ok:
        result.fail(f"{retention_path} missing public_safe sanitized copies for all Spark plan originals")

    return retention


def validate_sanitized_files(
    result: CheckResult,
    case_path: Path,
    case_id: str,
) -> None:
    files = [
        case_path / "evidence/retained_plans/rewrite_neg_01.sanitized.txt",
        case_path / "evidence/retained_plans/rewrite_pos_01.sanitized.txt",
    ]
    for path in files:
        exists_key = f"{path.name}_exists"
        result.checks[exists_key] = path.exists()
        if not path.exists():
            result.fail(f"missing {path}")
            continue
        hits = scan_text(path, SANITIZED_SCAN_PATTERNS)
        result.checks[f"{path.name}_scan_ok"] = not hits
        if hits:
            result.fail(f"{path} contains forbidden sanitized-scan patterns: {hits}")

    for path in [
        case_path / "MIGRATION_PILOT.md",
        case_path / "evidence/runs_retention.yaml",
    ]:
        if path.exists():
            hits = scan_text(path, SANITIZED_SCAN_PATTERNS)
            result.checks[f"{path.name}_scan_ok"] = not hits
            if hits:
                result.fail(f"{path} contains forbidden sanitized-scan patterns: {hits}")

    if case_id == "PORT_0024":
        path = case_path / "evidence/retained_controls/spark_result_check.sanitized_summary.json"
        result.checks["result_check_summary_required"] = True
        result.checks["result_check_summary_exists"] = path.exists()
        if not path.exists():
            result.fail(f"missing {path}")
            return
        try:
            parsed = json.loads(read_text(path))
            result.checks["result_check_summary_json_ok"] = True
        except Exception as exc:
            result.checks["result_check_summary_json_ok"] = False
            result.fail(f"{path} JSON parse failed: {exc}")
            return
        hits = scan_text(path, SANITIZED_SCAN_PATTERNS + RESULT_CHECK_SCAN_PATTERNS)
        has_placeholder = "<LOG_PATH_REDACTED>" in read_text(path)
        result.checks["result_check_summary_scan_ok"] = not hits and has_placeholder
        result.checks["result_check_summary_uses_log_placeholders"] = has_placeholder
        result.checks["result_check_summary_artifact_type"] = parsed.get("artifact_type")
        if hits:
            result.fail(f"{path} contains forbidden result-check patterns: {hits}")
        if not has_placeholder:
            result.fail(f"{path} does not contain <LOG_PATH_REDACTED> placeholders")
    else:
        result.checks["result_check_summary_required"] = False

    copied_logs = sorted(str(path) for path in case_path.rglob("*.log"))
    result.checks["raw_log_files_copied"] = copied_logs
    if copied_logs:
        result.fail(f"raw log files found in case package: {copied_logs}")


def validate_formal_csv(result: CheckResult, repo_root: Path, case_id: str) -> None:
    path = (
        repo_root
        / "audits/port_manual_review_resolution/formal_pilots"
        / f"{case_id}_formal_mapping_validation.csv"
    )
    result.checks["formal_validation_csv_exists"] = path.exists()
    if not path.exists():
        result.fail(f"missing {path}")
        return

    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result.checks["formal_validation_csv_row_count"] = len(rows)
    if not rows:
        result.fail(f"{path} has no rows")
        return

    failures: list[str] = []
    for index, row in enumerate(rows, start=1):
        if not boolish_ok(row.get("sha256_matches_trial"), {"yes", "n/a"}):
            failures.append(f"row {index}: sha256_matches_trial={row.get('sha256_matches_trial')!r}")
        if not boolish_ok(row.get("raw_local_path_remaining"), {"no", "false"}):
            failures.append(f"row {index}: raw_local_path_remaining={row.get('raw_local_path_remaining')!r}")
        if not boolish_ok(row.get("prompt_api_token_trace_remaining"), {"no", "false"}):
            failures.append(
                f"row {index}: prompt_api_token_trace_remaining={row.get('prompt_api_token_trace_remaining')!r}"
            )
        if not boolish_ok(row.get("public_safe"), {"yes", "true"}):
            failures.append(f"row {index}: public_safe={row.get('public_safe')!r}")
        if "raw_stdout_stderr_log_path_remaining" in row and not boolish_ok(
            row.get("raw_stdout_stderr_log_path_remaining"), {"no", "false"}
        ):
            failures.append(
                "row "
                f"{index}: raw_stdout_stderr_log_path_remaining="
                f"{row.get('raw_stdout_stderr_log_path_remaining')!r}"
            )
    result.checks["formal_validation_csv_flags_ok"] = not failures
    if failures:
        result.fail(f"{path} validation flags failed: {failures}")


def validate_case(repo_root: Path, case_arg: str) -> CheckResult:
    case_path = (repo_root / case_arg).resolve() if not Path(case_arg).is_absolute() else Path(case_arg)
    try:
        rel_path = case_path.relative_to(repo_root.resolve())
    except ValueError:
        case_id = infer_case_id(case_path)
        result = CheckResult(case_id=case_id, case_path=str(case_path), status="fail")
        result.fail("case path must be inside the release repository")
        return result

    case_id = infer_case_id(case_path)
    result = CheckResult(case_id=case_id, case_path=str(rel_path))
    if not case_path.exists():
        result.fail(f"case path does not exist: {case_path}")
        return result
    if rel_path.parts[:2] != ("cases", "PORT"):
        result.fail("evidence-pilot v0.1 currently supports cases/PORT/<CASE_ID> paths only")

    validate_migration_pilot(result, case_path / "MIGRATION_PILOT.md")
    validate_retention(result, case_path / "evidence/runs_retention.yaml", case_id)
    validate_sanitized_files(result, case_path, case_id)
    validate_formal_csv(result, repo_root.resolve(), case_id)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Static SQL-RewriteBench case-package validator."
    )
    parser.add_argument("--mode", required=True, choices=sorted(SUPPORTED_MODES))
    parser.add_argument(
        "--case",
        dest="cases",
        action="append",
        required=True,
        help="Case package path relative to repo root, e.g. cases/PORT/PORT_0008. May be repeated.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Release repository root. Defaults to current working directory.",
    )
    parser.add_argument(
        "--json-output",
        help="Optional path to write machine-readable validation results.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print failing details and final summary.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    results = [validate_case(repo_root, case_arg) for case_arg in args.cases]
    ok = all(result.status == "pass" for result in results)

    payload = {
        "validator": "validate_case_package.py",
        "version": VALIDATOR_VERSION,
        "mode": args.mode,
        "repo_root": ".",
        "status": "pass" if ok else "fail",
        "cases": [
            {
                "case_id": result.case_id,
                "case_path": result.case_path,
                "status": result.status,
                "checks": result.checks,
                "errors": result.errors,
                "warnings": result.warnings,
            }
            for result in results
        ],
    }

    if args.json_output:
        output_path = Path(args.json_output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not args.quiet:
        for result in results:
            print(f"{result.status.upper()} {result.case_id} {result.case_path}")
            for warning in result.warnings:
                print(f"  WARN {warning}")
            for error in result.errors:
                print(f"  ERROR {error}")

    print(
        f"validate_case_package {VALIDATOR_VERSION} {args.mode}: "
        f"{payload['status']} ({sum(r.status == 'pass' for r in results)}/{len(results)} passed)"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
