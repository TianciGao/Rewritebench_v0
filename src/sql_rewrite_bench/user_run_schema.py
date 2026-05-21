"""Schemas and status constants for local user-run outputs."""

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
    "candidate_preflight_status",
    "candidate_preflight_passed",
    "candidate_preflight_failure_class",
    "candidate_safety_status",
    "candidate_parse_status",
    "source_like_status",
    "diagnostic_mode",
    "source_reference_engine",
    "target_candidate_engine",
    "cross_dialect_status",
    "required_backend",
    "backend_status",
    "execution_status",
    "checker_status",
    "exact_status",
    "timed_status",
    "failure_bucket",
    "artifact_path",
    "notes",
    "execution_enabled",
    "checker_enabled",
    "source_execution_status",
    "candidate_execution_status",
    "source_result_path",
    "candidate_result_path",
    "checker_config_path",
    "normalization_config_path",
    "compare_config_path",
    "execution_failure_class",
    "checker_failure_class",
    "mismatch_artifact_path",
    "db_artifact_dir",
    "local_execution_only",
    "official_metric_input",
    "retained_evidence_input",
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
EXECUTION_STATUS_NOT_ENABLED = "execution_not_enabled"
EXECUTION_STATUS_SOURCE_SUCCESS = "source_execution_success"
EXECUTION_STATUS_CANDIDATE_SUCCESS = "candidate_execution_success"
EXECUTION_STATUS_SOURCE_FAILED = "source_execution_failed"
EXECUTION_STATUS_CANDIDATE_FAILED = "candidate_execution_failed"
EXECUTION_STATUS_SOURCE_BACKEND_MISSING = "source_backend_missing"
EXECUTION_STATUS_TIMEOUT = "execution_timeout"
EXECUTION_STATUS_UNSUPPORTED = "execution_unsupported"
EXECUTION_STATUS_INTERNAL_ERROR = "execution_internal_error"

CHECKER_STATUS_NON_DB = "not_run_non_db_mvp"
CHECKER_STATUS_NOT_ENABLED = "checker_not_enabled"
CHECKER_STATUS_SUCCESS = "checker_success"
CHECKER_STATUS_MISMATCH = "checker_mismatch"
CHECKER_STATUS_FAILED = "checker_failed"
CHECKER_STATUS_TIMEOUT = "checker_timeout"
CHECKER_STATUS_UNSUPPORTED = "checker_unsupported"
CHECKER_STATUS_CONFIG_MISSING = "checker_config_missing"
CHECKER_STATUS_NORMALIZATION_MISSING = "normalization_config_missing"
CHECKER_STATUS_INTERNAL_ERROR = "checker_internal_error"

EXACT_STATUS_NON_DB = "not_evaluated_non_db_mvp"
EXACT_STATUS_EXACT = "exact"
EXACT_STATUS_MISMATCH = "mismatch"
EXACT_STATUS_EXECUTION_FAILURE = "not_exact_due_to_execution_failure"
EXACT_STATUS_CHECKER_FAILURE = "not_exact_due_to_checker_failure"
EXACT_STATUS_TIMEOUT = "not_exact_due_to_timeout"
EXACT_STATUS_CHECKER_MISSING = "not_evaluated_checker_missing"

TIMED_STATUS_NON_DB = "not_timed_non_db_mvp"

CANDIDATE_PREFLIGHT_STATUS_NOT_RUN = "not_run"
CANDIDATE_PREFLIGHT_STATUS_PASSED = "passed"
CANDIDATE_PREFLIGHT_STATUS_FAILED = "failed"
CANDIDATE_PREFLIGHT_STATUS_SKIPPED = "skipped"

CANDIDATE_PREFLIGHT_FAILURE_NONE = "none"
CANDIDATE_PREFLIGHT_FAILURE_CANDIDATE_MISSING = "candidate_missing"
CANDIDATE_PREFLIGHT_FAILURE_EMPTY_CANDIDATE = "empty_candidate"
CANDIDATE_PREFLIGHT_FAILURE_UNSAFE_SQL = "unsafe_sql"
CANDIDATE_PREFLIGHT_FAILURE_MULTI_STATEMENT = "multi_statement"
CANDIDATE_PREFLIGHT_FAILURE_UNSUPPORTED_STATEMENT_TYPE = "unsupported_statement_type"
CANDIDATE_PREFLIGHT_FAILURE_PARSE_FAILED = "parse_failed"
CANDIDATE_PREFLIGHT_FAILURE_PREFLIGHT_ERROR = "preflight_error"

CANDIDATE_SAFETY_STATUS_NOT_CHECKED = "not_checked"
CANDIDATE_SAFETY_STATUS_SAFE = "safe"
CANDIDATE_SAFETY_STATUS_UNSAFE = "unsafe"

CANDIDATE_PARSE_STATUS_NOT_CHECKED = "not_checked"
CANDIDATE_PARSE_STATUS_PARSE_OK = "parse_ok"
CANDIDATE_PARSE_STATUS_PARSE_FAILED = "parse_failed"
CANDIDATE_PARSE_STATUS_PARSER_UNAVAILABLE = "parser_unavailable"

SOURCE_LIKE_STATUS_NOT_CHECKED = "not_checked"
SOURCE_LIKE_STATUS_SOURCE_LIKE = "source_like"
SOURCE_LIKE_STATUS_CHANGED = "changed"

DIAGNOSTIC_MODE_SAME_ENGINE = "same_engine"
DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE = "cross_dialect_reference"
DIAGNOSTIC_MODE_UNSUPPORTED = "unsupported"

CROSS_DIALECT_STATUS_NOT_APPLICABLE = "not_applicable"
CROSS_DIALECT_STATUS_BACKEND_MISSING = "backend_missing"
CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED = "source_reference_executed"
CROSS_DIALECT_STATUS_SOURCE_REFERENCE_FAILED = "source_reference_failed"

BACKEND_STATUS_NOT_REQUIRED = "not_required"
BACKEND_STATUS_NOT_IMPLEMENTED = "not_implemented"
BACKEND_STATUS_AVAILABLE = "available"
BACKEND_STATUS_CLIENT_MISSING = "client_missing"
BACKEND_STATUS_CONFIG_MISSING = "config_missing"
BACKEND_STATUS_SCHEMA_MISSING = "schema_missing"
BACKEND_STATUS_CONNECTION_FAILED = "connection_failed"

CANDIDATE_PREFLIGHT_STATUS_VALUES = {
    CANDIDATE_PREFLIGHT_STATUS_NOT_RUN,
    CANDIDATE_PREFLIGHT_STATUS_PASSED,
    CANDIDATE_PREFLIGHT_STATUS_FAILED,
    CANDIDATE_PREFLIGHT_STATUS_SKIPPED,
}

CANDIDATE_PREFLIGHT_FAILURE_CLASS_VALUES = {
    CANDIDATE_PREFLIGHT_FAILURE_NONE,
    CANDIDATE_PREFLIGHT_FAILURE_CANDIDATE_MISSING,
    CANDIDATE_PREFLIGHT_FAILURE_EMPTY_CANDIDATE,
    CANDIDATE_PREFLIGHT_FAILURE_UNSAFE_SQL,
    CANDIDATE_PREFLIGHT_FAILURE_MULTI_STATEMENT,
    CANDIDATE_PREFLIGHT_FAILURE_UNSUPPORTED_STATEMENT_TYPE,
    CANDIDATE_PREFLIGHT_FAILURE_PARSE_FAILED,
    CANDIDATE_PREFLIGHT_FAILURE_PREFLIGHT_ERROR,
}

CANDIDATE_SAFETY_STATUS_VALUES = {
    CANDIDATE_SAFETY_STATUS_NOT_CHECKED,
    CANDIDATE_SAFETY_STATUS_SAFE,
    CANDIDATE_SAFETY_STATUS_UNSAFE,
}

CANDIDATE_PARSE_STATUS_VALUES = {
    CANDIDATE_PARSE_STATUS_NOT_CHECKED,
    CANDIDATE_PARSE_STATUS_PARSE_OK,
    CANDIDATE_PARSE_STATUS_PARSE_FAILED,
    CANDIDATE_PARSE_STATUS_PARSER_UNAVAILABLE,
}

SOURCE_LIKE_STATUS_VALUES = {
    SOURCE_LIKE_STATUS_NOT_CHECKED,
    SOURCE_LIKE_STATUS_SOURCE_LIKE,
    SOURCE_LIKE_STATUS_CHANGED,
}

FAILURE_NONE = "none"
FAILURE_ADAPTER_FAILED = "adapter_failed"
FAILURE_NO_CANDIDATE_SQL = "no_candidate_sql"
FAILURE_ADAPTER_TIMEOUT = "adapter_timeout"
FAILURE_CANDIDATE_PREFLIGHT_FAILED = "candidate_preflight_failed"
FAILURE_SOURCE_EXECUTION_FAILED = "source_execution_failed"
FAILURE_CANDIDATE_EXECUTION_FAILED = "candidate_execution_failed"
FAILURE_CROSS_DIALECT_BACKEND_MISSING = "cross_dialect_backend_missing"
FAILURE_EXECUTION_TIMEOUT = "execution_timeout"
FAILURE_CHECKER_CONFIG_MISSING = "checker_config_missing"
FAILURE_CHECKER_FAILED = "checker_failed"
FAILURE_CHECKER_TIMEOUT = "checker_timeout"
FAILURE_MISMATCH = "mismatch"
FAILURE_UNSUPPORTED_ENGINE = "unsupported_engine"
FAILURE_INTERNAL_RUNNER_ERROR = "internal_runner_error"

EXECUTION_STATUS_VALUES = {
    EXECUTION_STATUS_NON_DB,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_SOURCE_FAILED,
    EXECUTION_STATUS_CANDIDATE_FAILED,
    EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    EXECUTION_STATUS_TIMEOUT,
    EXECUTION_STATUS_UNSUPPORTED,
    EXECUTION_STATUS_INTERNAL_ERROR,
}

CHECKER_STATUS_VALUES = {
    CHECKER_STATUS_NON_DB,
    CHECKER_STATUS_NOT_ENABLED,
    CHECKER_STATUS_SUCCESS,
    CHECKER_STATUS_MISMATCH,
    CHECKER_STATUS_FAILED,
    CHECKER_STATUS_TIMEOUT,
    CHECKER_STATUS_UNSUPPORTED,
    CHECKER_STATUS_CONFIG_MISSING,
    CHECKER_STATUS_NORMALIZATION_MISSING,
    CHECKER_STATUS_INTERNAL_ERROR,
}

EXACT_STATUS_VALUES = {
    EXACT_STATUS_NON_DB,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_MISMATCH,
    EXACT_STATUS_EXECUTION_FAILURE,
    EXACT_STATUS_CHECKER_FAILURE,
    EXACT_STATUS_TIMEOUT,
    EXACT_STATUS_CHECKER_MISSING,
}

FAILURE_BUCKET_VALUES = {
    FAILURE_NONE,
    FAILURE_ADAPTER_FAILED,
    FAILURE_NO_CANDIDATE_SQL,
    FAILURE_ADAPTER_TIMEOUT,
    FAILURE_CANDIDATE_PREFLIGHT_FAILED,
    FAILURE_SOURCE_EXECUTION_FAILED,
    FAILURE_CANDIDATE_EXECUTION_FAILED,
    FAILURE_CROSS_DIALECT_BACKEND_MISSING,
    FAILURE_EXECUTION_TIMEOUT,
    FAILURE_CHECKER_CONFIG_MISSING,
    FAILURE_CHECKER_FAILED,
    FAILURE_CHECKER_TIMEOUT,
    FAILURE_MISMATCH,
    FAILURE_UNSUPPORTED_ENGINE,
    FAILURE_INTERNAL_RUNNER_ERROR,
}
