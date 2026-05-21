"""Engine execution router for local user-entry diagnostics.

This module dispatches optional DB execution to engine-specific local
diagnostic executors. It does not run checkers, compute timing/speedup,
compute official metrics, update reports/results, or create leaderboard data.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .case_package_resolver import ResolvedCasePackage
from .case_selection import SelectedCaseEngineRow
from .postgres_execution import (
    PostgresExecutionResult,
    _csv_stdout_to_jsonl,
    _query_script,
    _quote_ident,
    _run_psql_file,
    _schema_name,
    _setup_script,
    execute_postgres_case,
    postgres_config_available,
    resolve_postgres_schema_assets,
)
from .user_run_schema import (
    BACKEND_STATUS_NOT_IMPLEMENTED,
    BACKEND_STATUS_AVAILABLE,
    CROSS_DIALECT_STATUS_BACKEND_MISSING,
    CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
    DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE,
    DIAGNOSTIC_MODE_UNSUPPORTED,
    EXECUTION_STATUS_CANDIDATE_FAILED,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_INTERNAL_ERROR,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    EXECUTION_STATUS_TIMEOUT,
    EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    EXECUTION_STATUS_UNSUPPORTED,
    FAILURE_CANDIDATE_EXECUTION_FAILED,
    FAILURE_CROSS_DIALECT_BACKEND_MISSING,
    FAILURE_EXECUTION_TIMEOUT,
    FAILURE_INTERNAL_RUNNER_ERROR,
    FAILURE_NONE,
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


def unsupported_local_diagnostic_role_result(
    *,
    row: SelectedCaseEngineRow,
    workspace_dir: Path,
    resolved_package: ResolvedCasePackage,
    execution_failure_class: str = "local_diagnostic_target_engine_unsupported",
) -> EngineExecutionResult:
    execution_dir = workspace_dir / "execution"
    execution_dir.mkdir(parents=True, exist_ok=True)
    notes = resolved_package.unsupported_reason or (
        "local diagnostic route is explicit but unsupported: "
        f"source_reference={resolved_package.source_reference_engine!r}, "
        f"target_candidate={resolved_package.target_candidate_engine!r}, "
        f"selected_engine={row.engine!r}"
    )
    required_backend = (
        f"{resolved_package.source_reference_engine}_to_{resolved_package.target_candidate_engine}"
        if resolved_package.source_reference_engine
        else row.engine
    )
    return EngineExecutionResult(
        source_execution_status=EXECUTION_STATUS_UNSUPPORTED,
        candidate_execution_status=EXECUTION_STATUS_UNSUPPORTED,
        source_result_path=None,
        candidate_result_path=None,
        db_artifact_dir=execution_dir,
        failure_bucket=FAILURE_UNSUPPORTED_ENGINE,
        execution_failure_class=execution_failure_class,
        notes=notes + "; no source, target, target_reference, or checker fallback was attempted",
        engine=row.engine,
        case_id=row.case_id,
        pool=row.pool,
        denominator_id=row.denominator_id,
        schema_setup_status="not_supported",
        db_execution_attempted=False,
        source_executable=False,
        candidate_executable=False,
        cross_dialect_status=CROSS_DIALECT_STATUS_BACKEND_MISSING,
        required_backend=required_backend,
        backend_status=BACKEND_STATUS_NOT_IMPLEMENTED,
    )


def _execute_postgres_target_candidate(
    *,
    repo_root: Path,
    run_id: str,
    row: SelectedCaseEngineRow,
    candidate_sql_path: Path,
    workspace_dir: Path,
    timeout_sec: int,
    schema_prefix: str,
    dsn_env: str,
    source_result: EngineExecutionResult,
) -> EngineExecutionResult:
    """Execute only the declared target candidate side for cross-dialect mode."""

    execution_root = workspace_dir / "execution"
    execution_dir = execution_root / "postgres_target"
    execution_dir.mkdir(parents=True, exist_ok=True)

    try:
        schema_assets = resolve_postgres_schema_assets(repo_root=repo_root, row=row)
    except ValueError as exc:
        return EngineExecutionResult(
            source_execution_status=source_result.source_execution_status,
            candidate_execution_status=EXECUTION_STATUS_CANDIDATE_FAILED,
            source_result_path=source_result.source_result_path,
            candidate_result_path=None,
            db_artifact_dir=execution_root,
            failure_bucket=FAILURE_CANDIDATE_EXECUTION_FAILED,
            execution_failure_class="target_schema_resolution_failed",
            notes=str(exc),
            engine=row.engine,
            case_id=row.case_id,
            pool=row.pool,
            denominator_id=row.denominator_id,
            schema_setup_status="target_schema_metadata_failed",
            source_error_path=source_result.source_error_path,
            db_execution_attempted=source_result.db_execution_attempted,
            source_executable=source_result.source_executable,
            candidate_executable=False,
            cross_dialect_status=CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
            required_backend=source_result.required_backend,
            backend_status=source_result.backend_status,
        )

    if not postgres_config_available(dsn_env=dsn_env):
        return EngineExecutionResult(
            source_execution_status=source_result.source_execution_status,
            candidate_execution_status=EXECUTION_STATUS_NOT_ENABLED,
            source_result_path=source_result.source_result_path,
            candidate_result_path=None,
            db_artifact_dir=execution_root,
            failure_bucket=FAILURE_INTERNAL_RUNNER_ERROR,
            execution_failure_class="postgres_config_missing",
            notes=(
                source_result.notes
                + "; target candidate execution skipped because PostgreSQL config is missing"
            ),
            engine=row.engine,
            case_id=row.case_id,
            pool=row.pool,
            denominator_id=row.denominator_id,
            schema_setup_status="target_schema_not_attempted_config_missing",
            source_error_path=source_result.source_error_path,
            db_execution_attempted=source_result.db_execution_attempted,
            source_executable=source_result.source_executable,
            candidate_executable=False,
            cross_dialect_status=CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
            required_backend=source_result.required_backend,
            backend_status=source_result.backend_status,
        )

    if not candidate_sql_path.exists():
        return EngineExecutionResult(
            source_execution_status=source_result.source_execution_status,
            candidate_execution_status=EXECUTION_STATUS_CANDIDATE_FAILED,
            source_result_path=source_result.source_result_path,
            candidate_result_path=None,
            db_artifact_dir=execution_root,
            failure_bucket=FAILURE_CANDIDATE_EXECUTION_FAILED,
            execution_failure_class="candidate_sql_missing",
            notes=f"candidate SQL file is missing: {candidate_sql_path}",
            engine=row.engine,
            case_id=row.case_id,
            pool=row.pool,
            denominator_id=row.denominator_id,
            schema_setup_status="target_schema_not_attempted_candidate_missing",
            source_error_path=source_result.source_error_path,
            db_execution_attempted=source_result.db_execution_attempted,
            source_executable=source_result.source_executable,
            candidate_executable=False,
            cross_dialect_status=CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
            required_backend=source_result.required_backend,
            backend_status=source_result.backend_status,
        )

    schema = _schema_name(schema_prefix, run_id, row.case_id, row.engine)
    setup_script_path = execution_dir / "setup.sql"
    candidate_script_path = execution_dir / "candidate_query.sql"
    candidate_result_path = execution_dir / "candidate_result.jsonl"
    candidate_error_path = execution_dir / "candidate_error.txt"
    cleanup_script_path = execution_dir / "cleanup.sql"
    cleanup_log = execution_dir / "cleanup_log.txt"

    try:
        setup_script_path.write_text(
            _setup_script(schema, schema_assets.ddl_path, schema_assets.load_path),
            encoding="utf-8",
        )
        setup = _run_psql_file(
            script_path=setup_script_path,
            timeout=timeout_sec,
            cwd=repo_root,
            dsn_env=dsn_env,
        )
        if setup.returncode != 0:
            candidate_error_path.write_text(
                setup.stderr or setup.stdout or "target schema setup failed",
                encoding="utf-8",
            )
            return EngineExecutionResult(
                source_execution_status=source_result.source_execution_status,
                candidate_execution_status=EXECUTION_STATUS_CANDIDATE_FAILED,
                source_result_path=source_result.source_result_path,
                candidate_result_path=None,
                db_artifact_dir=execution_root,
                failure_bucket=FAILURE_CANDIDATE_EXECUTION_FAILED,
                execution_failure_class="target_schema_setup_failed",
                notes=source_result.notes + "; target PostgreSQL schema setup failed",
                engine=row.engine,
                case_id=row.case_id,
                pool=row.pool,
                denominator_id=row.denominator_id,
                schema_setup_status="target_schema_setup_failed",
                source_error_path=source_result.source_error_path,
                candidate_error_path=candidate_error_path,
                db_execution_attempted=True,
                source_executable=source_result.source_executable,
                candidate_executable=False,
                cross_dialect_status=CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
                required_backend=source_result.required_backend,
                backend_status=source_result.backend_status,
            )

        candidate_script_path.write_text(
            _query_script(schema, candidate_sql_path),
            encoding="utf-8",
        )
        candidate = _run_psql_file(
            script_path=candidate_script_path,
            timeout=timeout_sec,
            cwd=repo_root,
            dsn_env=dsn_env,
        )
        if candidate.returncode != 0:
            candidate_error_path.write_text(
                candidate.stderr or candidate.stdout or "target candidate execution failed",
                encoding="utf-8",
            )
            return EngineExecutionResult(
                source_execution_status=source_result.source_execution_status,
                candidate_execution_status=EXECUTION_STATUS_CANDIDATE_FAILED,
                source_result_path=source_result.source_result_path,
                candidate_result_path=None,
                db_artifact_dir=execution_root,
                failure_bucket=FAILURE_CANDIDATE_EXECUTION_FAILED,
                execution_failure_class="target_candidate_execution_failed",
                notes=source_result.notes + "; target PostgreSQL candidate execution failed",
                engine=row.engine,
                case_id=row.case_id,
                pool=row.pool,
                denominator_id=row.denominator_id,
                schema_setup_status="target_schema_setup_success",
                source_error_path=source_result.source_error_path,
                candidate_error_path=candidate_error_path,
                db_execution_attempted=True,
                source_executable=source_result.source_executable,
                candidate_executable=False,
                cross_dialect_status=CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
                required_backend=source_result.required_backend,
                backend_status=source_result.backend_status,
            )
        _csv_stdout_to_jsonl(candidate.stdout, candidate_result_path)

        return EngineExecutionResult(
            source_execution_status=source_result.source_execution_status,
            candidate_execution_status=EXECUTION_STATUS_CANDIDATE_SUCCESS,
            source_result_path=source_result.source_result_path,
            candidate_result_path=candidate_result_path,
            db_artifact_dir=execution_root,
            failure_bucket=FAILURE_NONE,
            execution_failure_class="",
            notes=(
                source_result.notes
                + "; target candidate SQL executed locally through PostgreSQL; "
                "target_reference was not used as a checker oracle"
            ),
            engine=row.engine,
            case_id=row.case_id,
            pool=row.pool,
            denominator_id=row.denominator_id,
            schema_setup_status="target_schema_setup_success",
            source_error_path=source_result.source_error_path,
            db_execution_attempted=True,
            source_executable=source_result.source_executable,
            candidate_executable=True,
            cross_dialect_status=CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
            required_backend=source_result.required_backend,
            backend_status=BACKEND_STATUS_AVAILABLE,
        )
    except subprocess.TimeoutExpired as exc:
        candidate_error_path.write_text(str(exc), encoding="utf-8")
        return EngineExecutionResult(
            source_execution_status=source_result.source_execution_status,
            candidate_execution_status=EXECUTION_STATUS_TIMEOUT,
            source_result_path=source_result.source_result_path,
            candidate_result_path=None,
            db_artifact_dir=execution_root,
            failure_bucket=FAILURE_EXECUTION_TIMEOUT,
            execution_failure_class="target_candidate_execution_timeout",
            notes=f"target PostgreSQL candidate execution timed out after {timeout_sec} seconds",
            engine=row.engine,
            case_id=row.case_id,
            pool=row.pool,
            denominator_id=row.denominator_id,
            schema_setup_status="target_execution_timeout",
            source_error_path=source_result.source_error_path,
            candidate_error_path=candidate_error_path,
            db_execution_attempted=True,
            source_executable=source_result.source_executable,
            candidate_executable=False,
            cross_dialect_status=CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
            required_backend=source_result.required_backend,
            backend_status=source_result.backend_status,
        )
    except Exception as exc:
        candidate_error_path.write_text(str(exc), encoding="utf-8")
        return EngineExecutionResult(
            source_execution_status=source_result.source_execution_status,
            candidate_execution_status=EXECUTION_STATUS_INTERNAL_ERROR,
            source_result_path=source_result.source_result_path,
            candidate_result_path=None,
            db_artifact_dir=execution_root,
            failure_bucket=FAILURE_INTERNAL_RUNNER_ERROR,
            execution_failure_class="target_candidate_execution_internal_error",
            notes=f"target PostgreSQL candidate execution internal error: {exc}",
            engine=row.engine,
            case_id=row.case_id,
            pool=row.pool,
            denominator_id=row.denominator_id,
            schema_setup_status="target_execution_internal_error",
            source_error_path=source_result.source_error_path,
            candidate_error_path=candidate_error_path,
            db_execution_attempted=True,
            source_executable=source_result.source_executable,
            candidate_executable=False,
            cross_dialect_status=CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
            required_backend=source_result.required_backend,
            backend_status=source_result.backend_status,
        )
    finally:
        try:
            cleanup_script_path.write_text(
                f"DROP SCHEMA IF EXISTS {_quote_ident(schema)} CASCADE;\n",
                encoding="utf-8",
            )
            cleanup = _run_psql_file(
                script_path=cleanup_script_path,
                timeout=timeout_sec,
                cwd=repo_root,
                dsn_env=dsn_env,
            )
            cleanup_log.write_text(
                "cleanup_returncode="
                + str(cleanup.returncode)
                + "\n"
                + (cleanup.stderr or cleanup.stdout or ""),
                encoding="utf-8",
            )
        except Exception as exc:
            cleanup_log.write_text(f"cleanup_failed: {exc}\n", encoding="utf-8")


def _execute_cross_dialect_case(
    *,
    repo_root: Path,
    run_id: str,
    row: SelectedCaseEngineRow,
    candidate_sql_path: Path,
    workspace_dir: Path,
    timeout_sec: int,
    schema_prefix: str,
    postgres_dsn_env: str,
    resolved_package: ResolvedCasePackage,
) -> EngineExecutionResult:
    source_engine = resolved_package.source_reference_engine
    target_engine = resolved_package.target_candidate_engine
    if target_engine != row.engine:
        return unsupported_local_diagnostic_role_result(
            row=row,
            workspace_dir=workspace_dir,
            resolved_package=resolved_package,
            execution_failure_class="cross_dialect_target_engine_mismatch",
        )
    if source_engine != "mysql":
        return unsupported_local_diagnostic_role_result(
            row=row,
            workspace_dir=workspace_dir,
            resolved_package=resolved_package,
            execution_failure_class="cross_dialect_route_unsupported",
        )
    if row.engine != "postgres":
        return unsupported_engine_result(
            row=row,
            workspace_dir=workspace_dir,
            execution_failure_class="cross_dialect_target_backend_unsupported",
            notes=(
                "cross-dialect local diagnostic currently supports mysql "
                "source_reference to postgres target_candidate only; no fallback "
                "or target_reference substitution was attempted"
            ),
        )

    from .mysql_execution import execute_mysql_source_reference

    source_result = execute_mysql_source_reference(
        repo_root=repo_root,
        run_id=run_id,
        row=row,
        resolved_package=resolved_package,
        workspace_dir=workspace_dir,
        timeout_sec=timeout_sec,
        schema_prefix=schema_prefix,
    )
    if source_result.failure_bucket != FAILURE_NONE:
        return source_result
    if source_result.source_execution_status != EXECUTION_STATUS_SOURCE_SUCCESS:
        return source_result
    return _execute_postgres_target_candidate(
        repo_root=repo_root,
        run_id=run_id,
        row=row,
        candidate_sql_path=candidate_sql_path,
        workspace_dir=workspace_dir,
        timeout_sec=timeout_sec,
        schema_prefix=schema_prefix,
        dsn_env=postgres_dsn_env,
        source_result=source_result,
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

    PostgreSQL and same-engine MySQL delegate to engine-specific local
    diagnostic executors. Spark currently fails closed through an explicit
    stub; unsupported engines fail closed here.
    """

    if (
        resolved_package is not None
        and resolved_package.diagnostic_mode == DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE
    ):
        return _execute_cross_dialect_case(
            repo_root=repo_root,
            run_id=run_id,
            row=row,
            candidate_sql_path=candidate_sql_path,
            workspace_dir=workspace_dir,
            timeout_sec=timeout_sec,
            schema_prefix=schema_prefix,
            postgres_dsn_env=postgres_dsn_env,
            resolved_package=resolved_package,
        )
    if (
        resolved_package is not None
        and resolved_package.diagnostic_mode == DIAGNOSTIC_MODE_UNSUPPORTED
    ):
        return unsupported_local_diagnostic_role_result(
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
