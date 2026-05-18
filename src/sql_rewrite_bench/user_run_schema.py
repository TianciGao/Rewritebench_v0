"""Schemas and status constants for the non-DB user-run MVP."""

from __future__ import annotations

LEDGER_FIELDS = [
    "run_id",
    "case_id",
    "pool",
    "engine",
    "denominator_id",
    "planned",
    "selected",
    "adapter_invoked",
    "adapter_exit_code",
    "candidate_generated",
    "candidate_sql_path",
    "extraction_status",
    "execution_status",
    "checker_status",
    "exact_status",
    "timed_status",
    "failure_bucket",
    "artifact_path",
    "notes",
]

SELECTED_CASE_FIELDS = [
    "run_id",
    "case_id",
    "pool",
    "engine",
    "denominator_id",
    "planned",
    "case_path",
    "source_sql_path",
]

FAILURE_FIELDS = [
    "run_id",
    "case_id",
    "pool",
    "engine",
    "denominator_id",
    "failure_bucket",
    "artifact_path",
    "notes",
]

EXTRACTION_CAPTURED_FROM_CANDIDATE_FILE = "captured_from_candidate_file"
EXTRACTION_CAPTURED_FROM_STDOUT = "captured_from_stdout"
EXTRACTION_NO_CANDIDATE_SQL = "no_candidate_sql"
EXTRACTION_ADAPTER_FAILED = "adapter_failed"
EXTRACTION_SKIPPED = "skipped"
EXTRACTION_SKIPPED_DRY_RUN = "skipped_dry_run"

EXECUTION_STATUS_NON_DB = "not_run_non_db_mvp"
CHECKER_STATUS_NON_DB = "not_run_non_db_mvp"
EXACT_STATUS_NON_DB = "not_evaluated_non_db_mvp"
TIMED_STATUS_NON_DB = "not_timed_non_db_mvp"

FAILURE_NONE = "none"
FAILURE_ADAPTER_FAILED = "adapter_failed"
FAILURE_NO_CANDIDATE_SQL = "no_candidate_sql"
FAILURE_ADAPTER_TIMEOUT = "adapter_timeout"
FAILURE_INTERNAL_RUNNER_ERROR = "internal_runner_error"
