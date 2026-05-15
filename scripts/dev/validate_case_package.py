#!/usr/bin/env python3
"""Static validator for SQL-RewriteBench release case packages.

Version: v0.2

Supported modes:
- evidence-pilot: validates completed sanitized evidence-mapping pilot slices.
- full-case: validates the structure and claim boundaries expected from future
  copy-first full case migration pilots.

This validator is intentionally static. It does not read the legacy repository,
run database engines, execute validation scripts, regenerate evidence, or call
external services.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

VALIDATOR_VERSION = "v0.2"
SUPPORTED_MODES = {"evidence-pilot", "full-case"}

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

CSV_COLUMNS = [
    "case_id",
    "case_path",
    "mode",
    "manifest_exists",
    "source_sql_exists",
    "positive_rewrite_exists",
    "hard_negative_status",
    "schema_context_exists",
    "checker_exists",
    "validation_path_exists",
    "provenance_exists",
    "taxonomy_exists",
    "evidence_runs_retention_exists",
    "runs_retention_parse_ok",
    "sanitized_evidence_scan_ok",
    "no_raw_local_path_ok",
    "no_denominator_change_claim_ok",
    "no_paper_result_change_claim_ok",
    "no_global_leaderboard_claim_ok",
    "full_case_structure_ok",
    "evidence_mapping_ok",
    "overall_status",
    "failure_reasons",
    "warnings",
]


@dataclass
class YamlLoad:
    data: Any | None
    parse_ok: bool
    parser: str
    error: str | None
    text: str


@dataclass
class CheckResult:
    case_id: str
    case_path: str
    mode: str
    status: str = "pass"
    checks: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def fail(self, message: str) -> None:
        self.status = "fail"
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def scan_text(path: Path, patterns: list[str]) -> list[str]:
    text = read_text(path)
    return [pattern for pattern in patterns if pattern in text]


def boolish_ok(value: str | None, allowed: set[str]) -> bool:
    return (value or "").strip().lower() in allowed


def yes_no(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    if value is None:
        return ""
    return str(value)


def load_yaml_best_effort(path: Path) -> YamlLoad:
    text = read_text(path)
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        return YamlLoad(
            data=None,
            parse_ok=False,
            parser="text-fallback",
            error=f"PyYAML unavailable: {exc}",
            text=text,
        )
    try:
        with path.open("r", encoding="utf-8") as handle:
            return YamlLoad(
                data=yaml.safe_load(handle),
                parse_ok=True,
                parser="pyyaml",
                error=None,
                text=text,
            )
    except Exception as exc:
        return YamlLoad(
            data=None,
            parse_ok=False,
            parser="pyyaml",
            error=str(exc),
            text=text,
        )


def flatten_values(value: Any) -> list[Any]:
    if isinstance(value, dict):
        values: list[Any] = []
        for key, item in value.items():
            values.append(key)
            values.extend(flatten_values(item))
        return values
    if isinstance(value, list):
        values = []
        for item in value:
            values.extend(flatten_values(item))
        return values
    return [value]


def flatten_retention_entries(retention: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for key in (
        "retained_control_evidence",
        "retained_plan_evidence",
        "hard_negative_evidence",
        "sanitizable_public_evidence",
        "sanitized_public_copies",
        "private_or_original_archive",
        "external_archive_references",
        "do_not_delete",
    ):
        value = retention.get(key) or []
        if isinstance(value, list):
            entries.extend(item for item in value if isinstance(item, dict))
    return entries


def infer_case_id(case_path: Path) -> str:
    return case_path.name


def field_text_has(text: str, key: str, expected: str) -> bool:
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*:\s*['\"]?{re.escape(expected)}['\"]?\s*$", re.MULTILINE)
    return bool(pattern.search(text))


def text_has_key(text: str, key: str) -> bool:
    return bool(re.search(rf"^\s*{re.escape(key)}\s*:", text, re.MULTILINE))


def text_has_false(text: str, key: str) -> bool:
    return bool(re.search(rf"^\s*{re.escape(key)}\s*:\s*false\s*$", text, re.IGNORECASE | re.MULTILINE))


def nested_get(mapping: dict[str, Any], key: str) -> Any:
    for part in key.split("."):
        if not isinstance(mapping, dict):
            return None
        mapping = mapping.get(part)
    return mapping


def has_files(path: Path) -> bool:
    return path.exists() and any(child.is_file() for child in path.rglob("*"))


def manifest_values_contain(manifest: dict[str, Any] | None, tokens: list[str]) -> bool:
    if not manifest:
        return False
    lowered = [str(value).lower() for value in flatten_values(manifest)]
    return any(all(token in value for token in tokens) for value in lowered)


def manifest_declares_sql(manifest: dict[str, Any] | None, tokens: list[str]) -> bool:
    if not manifest:
        return False
    lowered = [str(value).lower() for value in flatten_values(manifest)]
    return any(".sql" in value and all(token in value for token in tokens) for value in lowered)


def manifest_has_block_or_path(manifest: dict[str, Any] | None, token: str) -> bool:
    if not manifest:
        return False
    lowered = [str(value).lower() for value in flatten_values(manifest)]
    return any(token in value for value in lowered)


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


def validate_evidence_pilot_retention(
    result: CheckResult,
    retention_path: Path,
    case_id: str,
) -> dict[str, Any] | None:
    if not retention_path.exists():
        result.fail(f"missing {retention_path}")
        result.checks["runs_retention_yaml_exists"] = False
        return None

    result.checks["runs_retention_yaml_exists"] = True
    loaded = load_yaml_best_effort(retention_path)
    result.checks["yaml_parse_ok"] = loaded.parse_ok if loaded.parser == "pyyaml" else "skipped"
    if loaded.error and loaded.parser == "text-fallback":
        result.warn(f"{loaded.error}; using text-level runs_retention checks")
    if loaded.error and loaded.parser == "pyyaml":
        result.fail(f"{retention_path} YAML parse failed: {loaded.error}")
        return None

    retention = loaded.data if isinstance(loaded.data, dict) else None
    expected = {
        "case_id": case_id,
        "pool": "PORT",
        "policy_version": "runs_retention_policy_v1",
        "status": "formal_evidence_mapping_pilot",
        "physical_pilot_status": "evidence_mapping_only_not_full_case_migration",
    }
    for key, value in expected.items():
        ok = retention.get(key) == value if retention else field_text_has(loaded.text, key, value)
        result.checks[f"runs_retention_{key}_ok"] = ok
        if not ok:
            result.fail(f"{retention_path} expected {key}={value!r}")

    if retention:
        notes = retention.get("public_release_notes") or {}
        required_false = {
            "full_case_package_migrated": notes.get("full_case_package_migrated") is False,
            "denominator_changed": notes.get("denominator_changed") is False,
            "paper_results_changed": notes.get("paper_results_changed") is False,
        }
    else:
        required_false = {
            "full_case_package_migrated": text_has_false(loaded.text, "full_case_package_migrated"),
            "denominator_changed": text_has_false(loaded.text, "denominator_changed"),
            "paper_results_changed": text_has_false(loaded.text, "paper_results_changed"),
        }
    for key, ok in required_false.items():
        result.checks[f"{key}_false"] = ok
        if not ok:
            result.fail(f"{retention_path} must record {key}: false")

    if retention:
        human = retention.get("human_approval") or {}
        formal_approved = (
            human.get("formal_pilot") == "approved"
            or human.get("status") in {"approved_for_formal_pilot", "formal_pilot_approved"}
        )
        full_later = (
            human.get("full_case_migration") == "required_later"
            or retention.get("physical_pilot_status") == "evidence_mapping_only_not_full_case_migration"
        )
    else:
        formal_approved = "approved" in loaded.text or "approved_for_formal_pilot" in loaded.text
        full_later = "required_later" in loaded.text or "evidence_mapping_only_not_full_case_migration" in loaded.text

    result.checks["human_approval_formal_pilot_ok"] = formal_approved
    result.checks["full_case_migration_required_later_ok"] = full_later
    if not formal_approved:
        result.fail(f"{retention_path} does not record formal pilot approval")
    if not full_later:
        result.fail(f"{retention_path} does not record full case migration as required later")

    if retention:
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
    else:
        do_not_ok = "do_not_delete_original: true" in loaded.text
        public_safe_ok = "public_safe: true" in loaded.text
    result.checks["spark_plan_do_not_delete_original_ok"] = do_not_ok
    result.checks["spark_plan_public_safe_copy_ok"] = public_safe_ok
    if not do_not_ok:
        result.fail(f"{retention_path} missing do_not_delete_original for Spark plan originals")
    if not public_safe_ok:
        result.fail(f"{retention_path} missing public_safe sanitized copies for Spark plan originals")

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


def validate_formal_csv(result: CheckResult, repo_root: Path, case_id: str, required: bool = True) -> None:
    path = (
        repo_root
        / "audits/port_manual_review_resolution/formal_pilots"
        / f"{case_id}_formal_mapping_validation.csv"
    )
    exists = path.exists()
    result.checks["formal_validation_csv_exists"] = exists
    if not exists:
        if required:
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


def case_public_files(case_path: Path) -> list[Path]:
    return sorted(path for path in case_path.rglob("*") if path.is_file())


def scan_public_hygiene(result: CheckResult, case_path: Path) -> None:
    hits: list[str] = []
    raw_log_hits: list[str] = []
    unreadable: list[str] = []
    for path in case_public_files(case_path):
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            unreadable.append(str(path.relative_to(case_path)))
            continue
        for pattern in SANITIZED_SCAN_PATTERNS:
            if pattern in text:
                hits.append(f"{path.relative_to(case_path)}:{pattern}")
        for pattern in RESULT_CHECK_SCAN_PATTERNS:
            if pattern in text:
                raw_log_hits.append(f"{path.relative_to(case_path)}:{pattern}")
    result.checks["public_hygiene_unreadable_files"] = unreadable
    result.checks["public_hygiene_hits"] = hits
    result.checks["result_check_raw_log_path_hits"] = raw_log_hits
    result.checks["no_raw_local_path_ok"] = not hits
    result.checks["sanitized_evidence_scan_ok"] = not hits and not raw_log_hits
    if hits:
        result.fail(f"public hygiene scan found forbidden patterns: {hits}")
    if raw_log_hits:
        result.fail(f"public hygiene scan found raw stdout/stderr log patterns: {raw_log_hits}")

    copied_logs = sorted(str(path.relative_to(case_path)) for path in case_path.rglob("*.log"))
    result.checks["raw_log_files_copied"] = copied_logs
    if copied_logs:
        result.fail(f"raw .log files found under release case slice: {copied_logs}")


def line_claims_global_leaderboard(line: str) -> bool:
    lowered = line.lower()
    if "global leaderboard" not in lowered:
        return False
    allowed = [
        "no global leaderboard",
        "not establish global leaderboard",
        "does not establish global leaderboard",
        "must not establish global leaderboard",
        "not a global leaderboard",
    ]
    return not any(phrase in lowered for phrase in allowed)


def scan_claim_boundaries(result: CheckResult, case_path: Path, full_structure_ok: bool) -> None:
    denominator_hits: list[str] = []
    paper_hits: list[str] = []
    membership_hits: list[str] = []
    leaderboard_hits: list[str] = []
    full_migration_hits: list[str] = []
    raw_evidence_hits: list[str] = []

    patterns = {
        "denominator": re.compile(r"denominator(?:_changed| changed)?\s*[:=]\s*(true|yes)", re.IGNORECASE),
        "paper": re.compile(r"paper(?:_results)?(?:_changed| results changed)?\s*[:=]\s*(true|yes)", re.IGNORECASE),
        "membership": re.compile(
            r"(case_membership_changed|Common-core membership changed)\s*[:=]\s*(true|yes)",
            re.IGNORECASE,
        ),
        "full_migration": re.compile(
            r"(full_case_package_migrated|full case migration|full case package migrated)\s*[:=]\s*(true|yes)",
            re.IGNORECASE,
        ),
        "raw_evidence": re.compile(
            r"(raw legacy evidence changed|raw legacy evidence was altered|raw runs/(?: was)? (?:cleaned|deleted)|runs/ (?:cleaned|deleted))\s*[:=]?\s*(true|yes)?",
            re.IGNORECASE,
        ),
    }

    for path in case_public_files(case_path):
        try:
            lines = read_text(path).splitlines()
        except UnicodeDecodeError:
            continue
        rel = str(path.relative_to(case_path))
        for line_no, line in enumerate(lines, start=1):
            if patterns["denominator"].search(line):
                denominator_hits.append(f"{rel}:{line_no}")
            if patterns["paper"].search(line):
                paper_hits.append(f"{rel}:{line_no}")
            if patterns["membership"].search(line):
                membership_hits.append(f"{rel}:{line_no}")
            if line_claims_global_leaderboard(line):
                leaderboard_hits.append(f"{rel}:{line_no}")
            if patterns["full_migration"].search(line):
                full_migration_hits.append(f"{rel}:{line_no}")
            if patterns["raw_evidence"].search(line):
                raw_evidence_hits.append(f"{rel}:{line_no}")

    result.checks["no_denominator_change_claim_ok"] = not denominator_hits
    result.checks["no_paper_result_change_claim_ok"] = not paper_hits
    result.checks["no_case_membership_change_claim_ok"] = not membership_hits
    result.checks["no_global_leaderboard_claim_ok"] = not leaderboard_hits
    result.checks["no_raw_legacy_evidence_change_claim_ok"] = not raw_evidence_hits
    result.checks["full_case_migration_claim_ok"] = full_structure_ok or not full_migration_hits

    if denominator_hits:
        result.fail(f"denominator-change claim found: {denominator_hits}")
    if paper_hits:
        result.fail(f"paper-result-change claim found: {paper_hits}")
    if membership_hits:
        result.fail(f"case-membership-change claim found: {membership_hits}")
    if leaderboard_hits:
        result.fail(f"global leaderboard claim found: {leaderboard_hits}")
    if raw_evidence_hits:
        result.fail(f"raw legacy evidence alteration/cleanup claim found: {raw_evidence_hits}")
    if full_migration_hits and not full_structure_ok:
        result.fail(
            "full case migration completion claim found while required full-case "
            f"components are missing: {full_migration_hits}"
        )


def validate_full_case_structure(
    result: CheckResult,
    case_path: Path,
    rel_path: Path,
    manifest: dict[str, Any] | None,
) -> bool:
    case_id = case_path.name
    pool = rel_path.parts[1] if len(rel_path.parts) > 1 else ""

    manifest_path = case_path / "manifest.yaml"
    manifest_exists = manifest_path.exists()
    result.checks["manifest_exists"] = manifest_exists
    if not manifest_exists:
        result.fail("missing manifest.yaml")

    if manifest_exists and manifest:
        manifest_case_id = manifest.get("case_id") or nested_get(manifest, "metadata.case_id")
        manifest_pool = manifest.get("pool") or nested_get(manifest, "metadata.pool")
        if manifest_case_id is not None and manifest_case_id != case_id:
            result.fail(f"manifest case_id {manifest_case_id!r} does not match directory {case_id!r}")
        if manifest_pool is not None and manifest_pool != pool:
            result.fail(f"manifest pool {manifest_pool!r} does not match parent directory {pool!r}")

    source_sql = (
        (case_path / "source.sql").exists()
        or (case_path / "sql/source.sql").exists()
        or manifest_declares_sql(manifest, ["source"])
    )
    positive_rewrite = (
        bool(list(case_path.glob("rewrite_pos_*.sql")))
        or bool(list((case_path / "sql/positives").glob("*.sql")))
        or manifest_declares_sql(manifest, ["positive"])
        or manifest_declares_sql(manifest, ["rewrite_pos"])
    )
    hard_negative_present = (
        bool(list(case_path.glob("rewrite_neg_*.sql")))
        or bool(list((case_path / "sql/negatives").glob("*.sql")))
        or manifest_declares_sql(manifest, ["negative"])
        or manifest_declares_sql(manifest, ["rewrite_neg"])
    )
    hard_negative_not_applicable = manifest_values_contain(manifest, ["hard", "negative", "not"])
    hard_negative_status = "present" if hard_negative_present else "not_applicable" if hard_negative_not_applicable else "missing"
    schema_context = has_files(case_path / "schema") or manifest_has_block_or_path(manifest, "schema")
    checker = (
        has_files(case_path / "checker")
        or (case_path / "validation/checker.yaml").exists()
        or manifest_has_block_or_path(manifest, "checker")
    )
    validation = has_files(case_path / "validation") or manifest_has_block_or_path(manifest, "validation")
    provenance = (
        has_files(case_path / "provenance")
        or (case_path / "metadata/provenance.yaml").exists()
        or manifest_has_block_or_path(manifest, "provenance")
    )
    taxonomy = (
        bool(list(case_path.glob("taxonomy*.yaml")))
        or (case_path / "metadata/taxonomy.yaml").exists()
        or manifest_has_block_or_path(manifest, "taxonomy")
    )
    notes = (
        (case_path / "README.md").exists()
        or (case_path / "MIGRATION_PILOT.md").exists()
        or has_files(case_path / "notes")
    )

    checks = {
        "source_sql_exists": source_sql,
        "positive_rewrite_exists": positive_rewrite,
        "schema_context_exists": schema_context,
        "checker_exists": checker,
        "validation_path_exists": validation,
        "provenance_exists": provenance,
        "taxonomy_exists": taxonomy,
        "readme_or_notes_exists": notes,
    }
    result.checks.update(checks)
    result.checks["hard_negative_status"] = hard_negative_status

    missing_messages = {
        "source_sql_exists": "missing source SQL: expected source.sql, sql/source.sql, or manifest-declared source path",
        "positive_rewrite_exists": "missing positive rewrite: expected rewrite_pos_*.sql, sql/positives/*.sql, or manifest-declared positive path",
        "schema_context_exists": "missing schema/data context: expected schema/ or manifest-declared schema paths",
        "checker_exists": "missing checker/normalization: expected checker/, validation/checker.yaml, or manifest-declared checker path",
        "validation_path_exists": "missing validation path: expected validation/ or manifest-declared validation scripts",
        "provenance_exists": "missing provenance: expected provenance/, metadata/provenance.yaml, or manifest-declared provenance",
        "taxonomy_exists": "missing taxonomy: expected taxonomy*.yaml, metadata/taxonomy.yaml, or manifest-declared 4+1 taxonomy",
        "readme_or_notes_exists": "missing README or notes: expected README.md, MIGRATION_PILOT.md, or notes/",
    }
    for key, ok in checks.items():
        if not ok:
            result.fail(missing_messages[key])
    if hard_negative_status == "missing":
        result.fail("missing hard negative or manifest-declared hard-negative not-applicable reason")

    full_structure_ok = (
        manifest_exists
        and source_sql
        and positive_rewrite
        and hard_negative_status in {"present", "not_applicable"}
        and schema_context
        and checker
        and validation
        and provenance
        and taxonomy
        and notes
    )
    result.checks["full_case_structure_ok"] = full_structure_ok
    return full_structure_ok


def validate_full_case_retention(
    result: CheckResult,
    retention_path: Path,
    case_id: str,
    pool: str,
    full_structure_ok: bool,
) -> dict[str, Any] | None:
    result.checks["evidence_runs_retention_exists"] = retention_path.exists()
    if not retention_path.exists():
        result.fail("missing evidence/runs_retention.yaml")
        result.checks["runs_retention_parse_ok"] = False
        return None

    loaded = load_yaml_best_effort(retention_path)
    result.checks["runs_retention_parse_ok"] = loaded.parse_ok if loaded.parser == "pyyaml" else "skipped"
    if loaded.error and loaded.parser == "text-fallback":
        result.warn(f"{loaded.error}; using text-level runs_retention checks")
    if loaded.error and loaded.parser == "pyyaml":
        result.fail(f"{retention_path} YAML parse failed: {loaded.error}")

    retention = loaded.data if isinstance(loaded.data, dict) else None
    required_fields = {
        "case_id": case_id,
        "pool": pool,
        "policy_version": "runs_retention_policy_v1",
    }
    for key, expected in required_fields.items():
        ok = retention.get(key) == expected if retention else field_text_has(loaded.text, key, expected)
        result.checks[f"runs_retention_{key}_ok"] = ok
        if not ok:
            result.fail(f"runs_retention missing or mismatched {key}: expected {expected!r}")

    status_ok = bool(retention.get("status")) if retention else text_has_key(loaded.text, "status")
    legacy_root_ok = bool(retention.get("legacy_runs_root")) if retention else text_has_key(loaded.text, "legacy_runs_root")
    result.checks["runs_retention_status_present"] = status_ok
    result.checks["runs_retention_legacy_runs_root_present"] = legacy_root_ok
    if not status_ok:
        result.fail("runs_retention missing status")
    if not legacy_root_ok:
        result.fail("runs_retention missing legacy_runs_root")

    if retention:
        notes = retention.get("public_release_notes") or {}
        full_case_migrated = notes.get("full_case_package_migrated")
        denominator_false = notes.get("denominator_changed") is False
        paper_false = notes.get("paper_results_changed") is False
    else:
        full_case_migrated = True if re.search(r"full_case_package_migrated\s*:\s*true", loaded.text) else False
        denominator_false = text_has_false(loaded.text, "denominator_changed")
        paper_false = text_has_false(loaded.text, "paper_results_changed")

    result.checks["full_case_package_migrated_value"] = full_case_migrated
    result.checks["full_case_package_migrated_claim_ok"] = full_structure_ok or full_case_migrated is not True
    result.checks["denominator_changed_false"] = denominator_false
    result.checks["paper_results_changed_false"] = paper_false
    if full_case_migrated is True and not full_structure_ok:
        result.fail("runs_retention claims full_case_package_migrated: true while required structure is missing")
    if not denominator_false:
        result.fail("runs_retention must record denominator_changed: false")
    if not paper_false:
        result.fail("runs_retention must record paper_results_changed: false")

    if retention:
        entries = flatten_retention_entries(retention)
        original_paths = [entry for entry in entries if entry.get("original_legacy_path")]
        do_not_ok = any(entry.get("do_not_delete_original") is True for entry in original_paths)
        sanitized_entries = [
            entry
            for entry in (retention.get("sanitized_public_copies") or [])
            if isinstance(entry, dict)
        ]
        if not sanitized_entries:
            sanitized_entries = [
                entry
                for entry in entries
                if ".sanitized" in str(entry.get("public_copy_path") or entry.get("proposed_public_path") or "")
            ]
        public_safe_ok = all(entry.get("public_safe") is True for entry in sanitized_entries) if sanitized_entries else True
        human = retention.get("human_approval") or {}
        approval_ok = bool(human.get("full_case_migration") or human.get("formal_pilot") or human.get("status"))
    else:
        original_paths = ["text"] if "original_legacy_path:" in loaded.text else []
        do_not_ok = "do_not_delete_original: true" in loaded.text
        public_safe_ok = "public_safe: false" not in loaded.text
        approval_ok = "human_approval:" in loaded.text and (
            "full_case_migration:" in loaded.text or "formal_pilot:" in loaded.text or "status:" in loaded.text
        )

    result.checks["retention_original_artifacts_mapped_ok"] = bool(original_paths)
    result.checks["retention_do_not_delete_original_ok"] = do_not_ok
    result.checks["retention_public_safe_copies_ok"] = public_safe_ok
    result.checks["retention_full_case_approval_status_ok"] = approval_ok
    if not original_paths:
        result.fail("runs_retention does not map original legacy artifacts")
    if not do_not_ok:
        result.fail("runs_retention does not record do_not_delete_original: true for retained evidence")
    if not public_safe_ok:
        result.fail("runs_retention has sanitized public copies not marked public_safe: true")
    if not approval_ok:
        result.fail("runs_retention does not record full-case or formal-pilot approval status")

    return retention


def validate_full_case_evidence_mapping(result: CheckResult, repo_root: Path, case_path: Path, case_id: str) -> None:
    sanitized_plan_files = sorted((case_path / "evidence/retained_plans").glob("*.sanitized.txt"))
    result.checks["sanitized_plan_file_count"] = len(sanitized_plan_files)
    sanitized_ok = True
    for path in sanitized_plan_files:
        hits = scan_text(path, SANITIZED_SCAN_PATTERNS)
        if hits:
            sanitized_ok = False
            result.fail(f"{path} contains forbidden sanitized evidence patterns: {hits}")
    result.checks["sanitized_plan_files_scan_ok"] = sanitized_ok

    if sanitized_plan_files:
        validate_formal_csv(result, repo_root, case_id, required=True)
    else:
        validate_formal_csv(result, repo_root, case_id, required=False)

    formal_ok = result.checks.get("formal_validation_csv_exists") is not False or not sanitized_plan_files
    if sanitized_plan_files and result.checks.get("formal_validation_csv_flags_ok") is not True:
        formal_ok = False
    mapping_ok = (
        result.checks.get("retention_original_artifacts_mapped_ok") is True
        and result.checks.get("retention_do_not_delete_original_ok") is True
        and result.checks.get("retention_public_safe_copies_ok") is True
        and sanitized_ok
        and formal_ok
    )
    result.checks["evidence_mapping_ok"] = mapping_ok


def validate_evidence_pilot_case(repo_root: Path, case_arg: str) -> CheckResult:
    case_path, rel_path, result = resolve_case(repo_root, case_arg, "evidence-pilot")
    if result.status == "fail":
        return result
    if rel_path.parts[:2] != ("cases", "PORT"):
        result.fail("evidence-pilot mode currently supports cases/PORT/<CASE_ID> paths only")

    case_id = result.case_id
    validate_migration_pilot(result, case_path / "MIGRATION_PILOT.md")
    validate_evidence_pilot_retention(result, case_path / "evidence/runs_retention.yaml", case_id)
    validate_sanitized_files(result, case_path, case_id)
    validate_formal_csv(result, repo_root.resolve(), case_id)
    populate_common_csv_checks(result)
    return result


def validate_full_case(repo_root: Path, case_arg: str) -> CheckResult:
    case_path, rel_path, result = resolve_case(repo_root, case_arg, "full-case")
    if result.status == "fail":
        populate_common_csv_checks(result)
        return result
    if len(rel_path.parts) < 3 or rel_path.parts[0] != "cases":
        result.fail("full-case mode expects cases/<POOL>/<CASE_ID> paths")

    case_id = result.case_id
    pool = rel_path.parts[1] if len(rel_path.parts) > 1 else ""
    manifest_path = case_path / "manifest.yaml"
    manifest_load = load_yaml_best_effort(manifest_path) if manifest_path.exists() else None
    manifest = manifest_load.data if manifest_load and isinstance(manifest_load.data, dict) else None
    if manifest_load and manifest_load.error and manifest_load.parser == "text-fallback":
        result.warn(f"{manifest_load.error}; using text-level manifest checks")
    if manifest_load and manifest_load.error and manifest_load.parser == "pyyaml":
        result.fail(f"{manifest_path} YAML parse failed: {manifest_load.error}")

    full_structure_ok = validate_full_case_structure(result, case_path, rel_path, manifest)
    validate_full_case_retention(result, case_path / "evidence/runs_retention.yaml", case_id, pool, full_structure_ok)
    scan_public_hygiene(result, case_path)
    scan_claim_boundaries(result, case_path, full_structure_ok)
    validate_full_case_evidence_mapping(result, repo_root.resolve(), case_path, case_id)
    populate_common_csv_checks(result)
    return result


def resolve_case(repo_root: Path, case_arg: str, mode: str) -> tuple[Path, Path, CheckResult]:
    case_path = (repo_root / case_arg).resolve() if not Path(case_arg).is_absolute() else Path(case_arg)
    try:
        rel_path = case_path.relative_to(repo_root.resolve())
    except ValueError:
        case_id = infer_case_id(case_path)
        result = CheckResult(case_id=case_id, case_path=str(case_path), mode=mode, status="fail")
        result.fail("case path must be inside the release repository")
        return case_path, Path(case_path.name), result

    case_id = infer_case_id(case_path)
    result = CheckResult(case_id=case_id, case_path=str(rel_path), mode=mode)
    if not case_path.exists():
        result.fail(f"case path does not exist: {case_path}")
    return case_path, rel_path, result


def populate_common_csv_checks(result: CheckResult) -> None:
    result.checks.setdefault("manifest_exists", False)
    result.checks.setdefault("source_sql_exists", False)
    result.checks.setdefault("positive_rewrite_exists", False)
    result.checks.setdefault("hard_negative_status", "")
    result.checks.setdefault("schema_context_exists", False)
    result.checks.setdefault("checker_exists", False)
    result.checks.setdefault("validation_path_exists", False)
    result.checks.setdefault("provenance_exists", False)
    result.checks.setdefault("taxonomy_exists", False)
    result.checks.setdefault(
        "evidence_runs_retention_exists",
        result.checks.get("runs_retention_yaml_exists", False),
    )
    result.checks.setdefault("runs_retention_parse_ok", result.checks.get("yaml_parse_ok", False))
    scan_keys = [
        key
        for key in result.checks
        if key.endswith("_scan_ok") or key in {"sanitized_evidence_scan_ok", "no_raw_local_path_ok"}
    ]
    if scan_keys:
        result.checks.setdefault("sanitized_evidence_scan_ok", all(result.checks[key] is True for key in scan_keys))
    else:
        result.checks.setdefault("sanitized_evidence_scan_ok", False)
    result.checks.setdefault("no_raw_local_path_ok", result.checks.get("sanitized_evidence_scan_ok", False))
    result.checks.setdefault("no_denominator_change_claim_ok", result.checks.get("denominator_changed_false", False))
    result.checks.setdefault("no_paper_result_change_claim_ok", result.checks.get("paper_results_changed_false", False))
    result.checks.setdefault("no_global_leaderboard_claim_ok", True)
    result.checks.setdefault("full_case_structure_ok", False)
    result.checks.setdefault(
        "evidence_mapping_ok",
        result.checks.get("spark_plan_do_not_delete_original_ok") is True
        and result.checks.get("spark_plan_public_safe_copy_ok") is True
        and result.checks.get("formal_validation_csv_flags_ok") is True,
    )


def result_to_csv_row(result: CheckResult) -> dict[str, str]:
    row = {
        "case_id": result.case_id,
        "case_path": result.case_path,
        "mode": result.mode,
        "overall_status": result.status,
        "failure_reasons": " | ".join(result.errors),
        "warnings": " | ".join(result.warnings),
    }
    for column in CSV_COLUMNS:
        if column in row:
            continue
        row[column] = yes_no(result.checks.get(column))
    return row


def write_csv(path: Path, results: list[CheckResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for result in results:
            writer.writerow(result_to_csv_row(result))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_payload(mode: str, results: list[CheckResult], ok: bool, advisory: bool) -> dict[str, Any]:
    return {
        "validator": "validate_case_package.py",
        "version": VALIDATOR_VERSION,
        "mode": mode,
        "repo_root": ".",
        "status": "pass" if ok else "fail",
        "advisory": advisory,
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
    parser.add_argument("--out", help="Optional CSV output path with one row per case.")
    parser.add_argument("--json-out", help="Optional JSON output path.")
    parser.add_argument(
        "--json-output",
        dest="json_output",
        help="Backward-compatible alias for --json-out.",
    )
    parser.add_argument(
        "--allow-failures",
        action="store_true",
        help="Advisory mode: report failures but exit 0.",
    )
    parser.add_argument(
        "--advisory",
        action="store_true",
        help="Alias for --allow-failures.",
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
    validator = validate_evidence_pilot_case if args.mode == "evidence-pilot" else validate_full_case
    results = [validator(repo_root, case_arg) for case_arg in args.cases]
    ok = all(result.status == "pass" for result in results)
    advisory = args.allow_failures or args.advisory

    payload = build_payload(args.mode, results, ok, advisory)

    if args.out:
        write_csv(Path(args.out), results)
    json_path = args.json_out or args.json_output
    if json_path:
        write_json(Path(json_path), payload)

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
        + (" [advisory exit allowed]" if advisory and not ok else "")
    )
    return 0 if ok or advisory else 1


if __name__ == "__main__":
    raise SystemExit(main())
