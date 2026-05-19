"""Local result checker for the bounded user-run DB/checker MVP.

This checker compares local JSONL execution artifacts. It is not an official
semantic-equivalence verifier and does not produce retained paper evidence.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .user_run_schema import (
    CHECKER_STATUS_CONFIG_MISSING,
    CHECKER_STATUS_FAILED,
    CHECKER_STATUS_MISMATCH,
    CHECKER_STATUS_NORMALIZATION_MISSING,
    CHECKER_STATUS_SUCCESS,
    EXACT_STATUS_CHECKER_FAILURE,
    EXACT_STATUS_CHECKER_MISSING,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_MISMATCH,
    FAILURE_CHECKER_CONFIG_MISSING,
    FAILURE_CHECKER_FAILED,
    FAILURE_MISMATCH,
    FAILURE_NONE,
)


@dataclass(frozen=True)
class CheckerResult:
    checker_status: str
    exact_status: str
    checker_failure_class: str
    mismatch_artifact_path: Path | None
    failure_bucket: str
    notes: str


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            if not isinstance(item, dict):
                raise ValueError(f"JSONL row is not an object: {path}")
            rows.append(item)
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def _simple_yaml_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip() or ":" not in line:
            continue
        key = line.split(":", 1)[0].strip()
        if key and not key.startswith("-"):
            keys.add(key)
    return keys


def _yaml_bool(path: Path, key: str, default: bool = False) -> bool:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line.startswith(f"{key}:"):
            continue
        value = line.split(":", 1)[1].strip().lower()
        if value in {"true", "yes", "1"}:
            return True
        if value in {"false", "no", "0"}:
            return False
    return default


def _normalize_value(value: object, *, trim: bool, normalize_numeric: bool) -> object:
    if not isinstance(value, str):
        return value
    normalized = value.strip() if trim else value
    if normalize_numeric:
        try:
            decimal = Decimal(normalized)
        except (InvalidOperation, ValueError):
            return normalized
        return format(decimal.normalize(), "f")
    return normalized


def _normalize_rows(rows: list[dict[str, object]], normalization_path: Path) -> list[dict[str, object]]:
    trim = _yaml_bool(normalization_path, "trim_whitespace", default=False)
    normalize_numeric = _yaml_bool(normalization_path, "normalize_numeric_format", default=False)
    sort_rows = _yaml_bool(normalization_path, "sort_rows", default=False)
    normalized = [
        {
            key: _normalize_value(value, trim=trim, normalize_numeric=normalize_numeric)
            for key, value in row.items()
        }
        for row in rows
    ]
    if sort_rows:
        normalized = sorted(normalized, key=lambda row: json.dumps(row, sort_keys=True))
    return normalized


def run_local_checker(
    *,
    case_dir: Path,
    source_result_path: Path,
    candidate_result_path: Path,
    checker_dir: Path,
) -> CheckerResult:
    """Compare local source and candidate JSONL results using case-local configs."""

    checker_dir.mkdir(parents=True, exist_ok=True)
    checker_config = case_dir / "checker" / "checker.yaml"
    normalization_config = case_dir / "checker" / "normalization.yaml"
    compare_config = case_dir / "checker" / "compare_config.yaml"
    checker_log = checker_dir / "checker_log.txt"
    checker_result_path = checker_dir / "checker_result.json"
    normalized_source_path = checker_dir / "normalized_source_result.jsonl"
    normalized_candidate_path = checker_dir / "normalized_candidate_result.jsonl"
    mismatch_path = checker_dir / "mismatch_summary.json"

    if not checker_config.exists() or not compare_config.exists():
        result = CheckerResult(
            checker_status=CHECKER_STATUS_CONFIG_MISSING,
            exact_status=EXACT_STATUS_CHECKER_MISSING,
            checker_failure_class="checker_config_missing",
            mismatch_artifact_path=None,
            failure_bucket=FAILURE_CHECKER_CONFIG_MISSING,
            notes="checker.yaml or compare_config.yaml is missing",
        )
        checker_result_path.write_text(json.dumps(result.__dict__, default=str, indent=2) + "\n")
        checker_log.write_text(result.notes + "\n", encoding="utf-8")
        return result

    if not normalization_config.exists():
        result = CheckerResult(
            checker_status=CHECKER_STATUS_NORMALIZATION_MISSING,
            exact_status=EXACT_STATUS_CHECKER_MISSING,
            checker_failure_class="normalization_config_missing",
            mismatch_artifact_path=None,
            failure_bucket=FAILURE_CHECKER_CONFIG_MISSING,
            notes="normalization.yaml is missing",
        )
        checker_result_path.write_text(json.dumps(result.__dict__, default=str, indent=2) + "\n")
        checker_log.write_text(result.notes + "\n", encoding="utf-8")
        return result

    try:
        source_rows = _read_jsonl(source_result_path)
        candidate_rows = _read_jsonl(candidate_result_path)
        normalized_source = _normalize_rows(source_rows, normalization_config)
        normalized_candidate = _normalize_rows(candidate_rows, normalization_config)
        _write_jsonl(normalized_source_path, normalized_source)
        _write_jsonl(normalized_candidate_path, normalized_candidate)

        known_keys = {
            "case_id",
            "normalization_version",
            "row_format",
            "sort_rows",
            "trim_whitespace",
            "normalize_numeric_format",
            "normalize_null",
            "numeric_tolerance",
            "mode",
            "migration_did_not_recompute_outputs",
            "claim_boundary",
            "derived_from_legacy_checker",
            "no_new_result_claim",
        }
        unknown_keys = sorted(_simple_yaml_keys(normalization_config) - known_keys)

        if normalized_source == normalized_candidate:
            result = CheckerResult(
                checker_status=CHECKER_STATUS_SUCCESS,
                exact_status=EXACT_STATUS_EXACT,
                checker_failure_class="",
                mismatch_artifact_path=None,
                failure_bucket=FAILURE_NONE,
                notes="local checker exact match"
                + (f"; unknown normalization keys recorded: {unknown_keys}" if unknown_keys else ""),
            )
        else:
            mismatch_payload = {
                "source_row_count": len(normalized_source),
                "candidate_row_count": len(normalized_candidate),
                "source_preview": normalized_source[:5],
                "candidate_preview": normalized_candidate[:5],
                "notes": "local checker mismatch; no official metric computed",
            }
            mismatch_path.write_text(json.dumps(mismatch_payload, indent=2, sort_keys=True) + "\n")
            result = CheckerResult(
                checker_status=CHECKER_STATUS_MISMATCH,
                exact_status=EXACT_STATUS_MISMATCH,
                checker_failure_class="mismatch",
                mismatch_artifact_path=mismatch_path,
                failure_bucket=FAILURE_MISMATCH,
                notes="local checker mismatch"
                + (f"; unknown normalization keys recorded: {unknown_keys}" if unknown_keys else ""),
            )

        checker_result_path.write_text(json.dumps(result.__dict__, default=str, indent=2) + "\n")
        checker_log.write_text(result.notes + "\n", encoding="utf-8")
        return result
    except Exception as exc:
        result = CheckerResult(
            checker_status=CHECKER_STATUS_FAILED,
            exact_status=EXACT_STATUS_CHECKER_FAILURE,
            checker_failure_class="checker_failed",
            mismatch_artifact_path=None,
            failure_bucket=FAILURE_CHECKER_FAILED,
            notes=f"local checker failed: {exc}",
        )
        checker_result_path.write_text(json.dumps(result.__dict__, default=str, indent=2) + "\n")
        checker_log.write_text(result.notes + "\n", encoding="utf-8")
        return result
