"""Ledger row construction and CSV writing for local user-entry runs."""

from __future__ import annotations

import csv
from pathlib import Path

from .adapter_runner import AdapterInvocationResult, relative_to_repo
from .candidate_preflight import CandidatePreflightResult
from .case_selection import SelectedCaseEngineRow
from .user_run_schema import (
    CANDIDATE_PARSE_STATUS_NOT_CHECKED,
    CANDIDATE_PREFLIGHT_FAILURE_CANDIDATE_MISSING,
    CANDIDATE_PREFLIGHT_FAILURE_NONE,
    CANDIDATE_PREFLIGHT_STATUS_FAILED,
    CANDIDATE_PREFLIGHT_STATUS_NOT_RUN,
    CANDIDATE_PREFLIGHT_STATUS_SKIPPED,
    CANDIDATE_SAFETY_STATUS_NOT_CHECKED,
    BACKEND_STATUS_NOT_REQUIRED,
    CHECKER_STATUS_NON_DB,
    CROSS_DIALECT_STATUS_NOT_APPLICABLE,
    DIAGNOSTIC_MODE_SAME_ENGINE,
    EXECUTION_STATUS_NON_DB,
    EXACT_STATUS_NON_DB,
    EXTRACTION_NO_CANDIDATE_SQL,
    EXTRACTION_SKIPPED_DRY_RUN,
    FAILURE_CANDIDATE_PREFLIGHT_FAILED,
    FAILURE_FIELDS,
    FAILURE_NO_CANDIDATE_SQL,
    FAILURE_NONE,
    LEDGER_FIELDS,
    SOURCE_LIKE_STATUS_NOT_CHECKED,
    TIMED_STATUS_NON_DB,
)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ledger_base(run_id: str, row: SelectedCaseEngineRow, artifact_path: str) -> dict[str, object]:
    return {
        "run_id": run_id,
        "case_id": row.case_id,
        "pool": row.pool,
        "engine": row.engine,
        "denominator_id": row.denominator_id,
        "planned": "true",
        "selected": "true",
        "adapter_invoked": "true",
        "adapter_exit_code": "",
        "candidate_generated": "false",
        "candidate_sql_path": "",
        "extraction_status": EXTRACTION_NO_CANDIDATE_SQL,
        "candidate_preflight_status": CANDIDATE_PREFLIGHT_STATUS_NOT_RUN,
        "candidate_preflight_passed": "",
        "candidate_preflight_failure_class": CANDIDATE_PREFLIGHT_FAILURE_NONE,
        "candidate_safety_status": CANDIDATE_SAFETY_STATUS_NOT_CHECKED,
        "candidate_parse_status": CANDIDATE_PARSE_STATUS_NOT_CHECKED,
        "source_like_status": SOURCE_LIKE_STATUS_NOT_CHECKED,
        "diagnostic_mode": DIAGNOSTIC_MODE_SAME_ENGINE,
        "source_reference_engine": row.engine,
        "target_candidate_engine": row.engine,
        "cross_dialect_status": CROSS_DIALECT_STATUS_NOT_APPLICABLE,
        "required_backend": "",
        "backend_status": BACKEND_STATUS_NOT_REQUIRED,
        "execution_status": EXECUTION_STATUS_NON_DB,
        "checker_status": CHECKER_STATUS_NON_DB,
        "exact_status": EXACT_STATUS_NON_DB,
        "timed_status": TIMED_STATUS_NON_DB,
        "failure_bucket": FAILURE_NO_CANDIDATE_SQL,
        "artifact_path": artifact_path,
        "notes": "non_db_mvp_adapter_capture_only",
        "execution_enabled": "false",
        "checker_enabled": "false",
        "source_execution_status": EXECUTION_STATUS_NON_DB,
        "candidate_execution_status": EXECUTION_STATUS_NON_DB,
        "source_result_path": "",
        "candidate_result_path": "",
        "checker_config_path": "",
        "normalization_config_path": "",
        "compare_config_path": "",
        "execution_failure_class": "",
        "checker_failure_class": "",
        "mismatch_artifact_path": "",
        "db_artifact_dir": "",
        "local_execution_only": "true",
        "official_metric_input": "false",
        "retained_evidence_input": "false",
    }


def dry_run_ledger_for_row(
    *, run_id: str, row: SelectedCaseEngineRow, repo_root: Path, out_dir: Path
) -> dict[str, object]:
    workspace_dir = out_dir / "workspaces" / row.case_id / row.engine
    workspace_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = relative_to_repo(workspace_dir, repo_root)
    ledger = ledger_base(run_id, row, artifact_path)
    ledger.update(
        {
            "adapter_invoked": "false",
            "adapter_exit_code": "",
            "candidate_generated": "false",
            "candidate_sql_path": "",
            "extraction_status": EXTRACTION_SKIPPED_DRY_RUN,
            "failure_bucket": FAILURE_NONE,
            "notes": "dry_run_selection_only_no_adapter_invoked",
        }
    )
    return ledger


def ledger_from_adapter_result(
    *,
    run_id: str,
    row: SelectedCaseEngineRow,
    adapter_result: AdapterInvocationResult,
    repo_root: Path,
) -> dict[str, object]:
    ledger = ledger_base(run_id, row, adapter_result.artifact_path)
    ledger.update(
        {
            "adapter_invoked": "true" if adapter_result.adapter_invoked else "false",
            "adapter_exit_code": ""
            if adapter_result.adapter_exit_code is None
            else str(adapter_result.adapter_exit_code),
            "candidate_generated": "true" if adapter_result.candidate_generated else "false",
            "candidate_sql_path": relative_to_repo(adapter_result.candidate_sql_path, repo_root)
            if adapter_result.candidate_sql_path
            else "",
            "extraction_status": adapter_result.extraction_status,
            "failure_bucket": adapter_result.failure_bucket_hint,
            "notes": adapter_result.notes,
        }
    )
    return ledger


def apply_candidate_preflight_result(
    ledger: dict[str, object], result: CandidatePreflightResult
) -> dict[str, object]:
    ledger.update(
        {
            "candidate_preflight_status": result.candidate_preflight_status,
            "candidate_preflight_passed": result.candidate_preflight_passed,
            "candidate_preflight_failure_class": result.candidate_preflight_failure_class,
            "candidate_safety_status": result.candidate_safety_status,
            "candidate_parse_status": result.candidate_parse_status,
            "source_like_status": result.source_like_status,
            "notes": str(ledger.get("notes", "")) + "; " + result.notes,
        }
    )
    if result.candidate_preflight_status == CANDIDATE_PREFLIGHT_STATUS_FAILED:
        ledger["failure_bucket"] = FAILURE_CANDIDATE_PREFLIGHT_FAILED
    return ledger


def mark_candidate_preflight_skipped(
    ledger: dict[str, object],
    *,
    failure_class: str = CANDIDATE_PREFLIGHT_FAILURE_CANDIDATE_MISSING,
    notes: str = "candidate preflight skipped because no candidate SQL was generated",
) -> dict[str, object]:
    ledger.update(
        {
            "candidate_preflight_status": CANDIDATE_PREFLIGHT_STATUS_SKIPPED,
            "candidate_preflight_passed": "",
            "candidate_preflight_failure_class": failure_class,
            "candidate_safety_status": CANDIDATE_SAFETY_STATUS_NOT_CHECKED,
            "candidate_parse_status": CANDIDATE_PARSE_STATUS_NOT_CHECKED,
            "source_like_status": SOURCE_LIKE_STATUS_NOT_CHECKED,
            "notes": str(ledger.get("notes", "")) + "; " + notes,
        }
    )
    return ledger


def failure_rows_from_ledger(ledger_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "run_id": row["run_id"],
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "denominator_id": row["denominator_id"],
            "failure_bucket": row["failure_bucket"],
            "artifact_path": row["artifact_path"],
            "notes": row["notes"],
        }
        for row in ledger_rows
        if row["failure_bucket"] != FAILURE_NONE
    ]


def write_ledger(path: Path, ledger_rows: list[dict[str, object]]) -> None:
    write_csv(path, ledger_rows, LEDGER_FIELDS)


def write_failures(path: Path, failure_rows: list[dict[str, object]]) -> None:
    write_csv(path, failure_rows, FAILURE_FIELDS)
