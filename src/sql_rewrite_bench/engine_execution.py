"""Engine execution router for local user-entry diagnostics.

This module dispatches optional DB execution to engine-specific local
diagnostic executors. It does not run checkers, compute timing/speedup,
compute official metrics, update reports/results, or create leaderboard data.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .case_package_resolver import ResolvedCasePackage
from .case_selection import SelectedCaseEngineRow
from .postgres_execution import PostgresExecutionResult, execute_postgres_case
from .user_run_schema import (
    BACKEND_STATUS_NOT_IMPLEMENTED,
    CROSS_DIALECT_STATUS_BACKEND_MISSING,
    DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    EXECUTION_STATUS_UNSUPPORTED,
    FAILURE_CROSS_DIALECT_BACKEND_MISSING,
    FAILURE_UNSUPPORTED_ENGINE,
)


@dataclass(frozen=True)
class EngineExecutionResult:
    """Common local diagnostic execution result returned by the engine router."""

    source_execution_status: str
    candidate_execution_status: str
    source_result_path: Path | None
    candidate_result_path: Path | None
    db_artifact_dir: Path
    failure_bucket: str
    execution_failure_class: str
    notes: str
    engine: str
    case_id: str
    pool: str
    denominator_id: str
    schema_setup_status: str
    source_error_path: Path | None = None
    candidate_error_path: Path | None = None
    engine_version: str = ""
    db_execution_attempted: bool = False
    source_executable: bool = False
    candidate_executable: bool = False
    local_diagnostic_only: bool = True
    cross_dialect_status: str = ""
    required_backend: str = ""
    backend_status: str = ""


def _schema_setup_status(result: PostgresExecutionResult) -> str:
    if result.execution_failure_class in {
        "external_schema_resolution_failed",
        "required_sql_asset_missing",
    }:
        return "schema_metadata_failed"
    if result.execution_failure_class == "schema_setup_failed":
        return "schema_setup_failed"
    if result.failure_bucket == FAILURE_UNSUPPORTED_ENGINE:
        return "not_supported"
    return "schema_setup_attempted"


def _from_postgres_result(
    result: PostgresExecutionResult, row: SelectedCaseEngineRow
) -> EngineExecutionResult:
    return EngineExecutionResult(
        source_execution_status=result.source_execution_status,
        candidate_execution_status=result.candidate_execution_status,
        source_result_path=result.source_result_path,
        candidate_result_path=result.candidate_result_path,
        db_artifact_dir=result.db_artifact_dir,
        failure_bucket=result.failure_bucket,
        execution_failure_class=result.execution_failure_class,
        notes=result.notes,
        engine=row.engine,
        case_id=row.case_id,
        pool=row.pool,
        denominator_id=row.denominator_id,
        schema_setup_status=_schema_setup_status(result),
        db_execution_attempted=True,
        source_executable=result.source_result_path is not None,
        candidate_executable=result.candidate_result_path is not None,
    )


def unsupported_engine_result(
    *,
    row: SelectedCaseEngineRow,
    workspace_dir: Path,
    execution_failure_class: str = "unsupported_engine",
    notes: str | None = None,
) -> EngineExecutionResult:
    execution_dir = workspace_dir / "execution"
    execution_dir.mkdir(parents=True, exist_ok=True)
    return EngineExecutionResult(
        source_execution_status=EXECUTION_STATUS_UNSUPPORTED,
        candidate_execution_status=EXECUTION_STATUS_UNSUPPORTED,
        source_result_path=None,
        candidate_result_path=None,
        db_artifact_dir=execution_dir,
        failure_bucket=FAILURE_UNSUPPORTED_ENGINE,
        execution_failure_class=execution_failure_class,
        notes=notes
        or f"{row.engine} execution is unsupported; no SQL was executed",
        engine=row.engine,
        case_id=row.case_id,
        pool=row.pool,
        denominator_id=row.denominator_id,
        schema_setup_status="not_supported",
        db_execution_attempted=False,
        source_executable=False,
        candidate_executable=False,
    )


def cross_dialect_backend_missing_result(
    *,
    row: SelectedCaseEngineRow,
    workspace_dir: Path,
    resolved_package: ResolvedCasePackage,
) -> EngineExecutionResult:
    """Fail closed for declared cross-dialect diagnostics without source backend."""

    execution_dir = workspace_dir / "execution"
    execution_dir.mkdir(parents=True, exist_ok=True)
    required_backend = resolved_package.source_reference_engine
    return EngineExecutionResult(
        source_execution_status=EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
        candidate_execution_status=EXECUTION_STATUS_NOT_ENABLED,
        source_result_path=None,
        candidate_result_path=None,
        db_artifact_dir=execution_dir,
        failure_bucket=FAILURE_CROSS_DIALECT_BACKEND_MISSING,
        execution_failure_class="cross_dialect_source_backend_missing",
        notes=(
            "cross-dialect local diagnostic requires source reference backend "
            f"{required_backend!r}; backend is not implemented/configured, "
            "so no PostgreSQL source execution, target_reference substitution, "
            "or checker fallback was attempted"
        ),
        engine=row.engine,
        case_id=row.case_id,
        pool=row.pool,
        denominator_id=row.denominator_id,
        schema_setup_status="not_attempted_backend_missing",
        db_execution_attempted=False,
        source_executable=False,
        candidate_executable=False,
        cross_dialect_status=CROSS_DIALECT_STATUS_BACKEND_MISSING,
        required_backend=required_backend,
        backend_status=BACKEND_STATUS_NOT_IMPLEMENTED,
    )


def execute_engine_case(
    *,
    repo_root: Path,
    run_id: str,
    row: SelectedCaseEngineRow,
    candidate_sql_path: Path,
    workspace_dir: Path,
    timeout_sec: int,
    schema_prefix: str,
    postgres_dsn_env: str = "SQLRB_POSTGRES_DSN",
    resolved_package: ResolvedCasePackage | None = None,
) -> EngineExecutionResult:
    """Dispatch optional local DB execution by engine.

    PostgreSQL delegates to the existing executor. MySQL and Spark currently
    fail closed through explicit stubs; unsupported engines fail closed here.
    """

    if (
        resolved_package is not None
        and resolved_package.diagnostic_mode == DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE
    ):
        return cross_dialect_backend_missing_result(
            row=row,
            workspace_dir=workspace_dir,
            resolved_package=resolved_package,
        )

    if row.engine == "postgres":
        return _from_postgres_result(
            execute_postgres_case(
                repo_root=repo_root,
                run_id=run_id,
                row=row,
                candidate_sql_path=candidate_sql_path,
                workspace_dir=workspace_dir,
                timeout_sec=timeout_sec,
                schema_prefix=schema_prefix,
                dsn_env=postgres_dsn_env,
            ),
            row,
        )
    if row.engine == "mysql":
        from .mysql_execution import execute_mysql_case

        return execute_mysql_case(
            repo_root=repo_root,
            run_id=run_id,
            row=row,
            candidate_sql_path=candidate_sql_path,
            workspace_dir=workspace_dir,
            timeout_sec=timeout_sec,
            schema_prefix=schema_prefix,
        )
    if row.engine == "spark":
        from .spark_execution import execute_spark_case

        return execute_spark_case(
            repo_root=repo_root,
            run_id=run_id,
            row=row,
            candidate_sql_path=candidate_sql_path,
            workspace_dir=workspace_dir,
            timeout_sec=timeout_sec,
            schema_prefix=schema_prefix,
        )
    return unsupported_engine_result(
        row=row,
        workspace_dir=workspace_dir,
        execution_failure_class="unsupported_engine",
        notes=f"unsupported engine {row.engine!r}; no SQL was executed",
    )
