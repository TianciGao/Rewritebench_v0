"""Postgres-only local execution helpers for user-run DB/checker MVP.

This module uses the `psql` CLI and writes only local user-run artifacts. It
does not compute official metrics or update retained evidence.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .case_selection import SelectedCaseEngineRow
from .user_run_schema import (
    EXECUTION_STATUS_CANDIDATE_FAILED,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_INTERNAL_ERROR,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_FAILED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    EXECUTION_STATUS_TIMEOUT,
    FAILURE_CANDIDATE_EXECUTION_FAILED,
    FAILURE_EXECUTION_TIMEOUT,
    FAILURE_INTERNAL_RUNNER_ERROR,
    FAILURE_NONE,
    FAILURE_SOURCE_EXECUTION_FAILED,
    FAILURE_UNSUPPORTED_ENGINE,
)


@dataclass(frozen=True)
class PostgresExecutionResult:
    source_execution_status: str
    candidate_execution_status: str
    source_result_path: Path | None
    candidate_result_path: Path | None
    db_artifact_dir: Path
    failure_bucket: str
    execution_failure_class: str
    notes: str


def postgres_config_available(*, dsn_env: str = "SQLRB_POSTGRES_DSN") -> bool:
    """Return whether an allowed Postgres connection source is present."""

    if os.environ.get(dsn_env):
        return True
    required_libpq = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER"]
    return all(os.environ.get(name) for name in required_libpq)


def redacted_postgres_config_source(*, dsn_env: str = "SQLRB_POSTGRES_DSN") -> str:
    """Return a non-secret connection-source description."""

    if os.environ.get(dsn_env):
        return f"{dsn_env}=<set>"
    present = [name for name in ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"] if os.environ.get(name)]
    if present:
        return "libpq_env:" + ",".join(f"{name}=<set>" for name in present)
    return "none"


def _psql_base_command(*, dsn_env: str) -> list[str]:
    if not shutil.which("psql"):
        raise FileNotFoundError("psql CLI is not available")
    command = ["psql"]
    dsn = os.environ.get(dsn_env)
    if dsn:
        command.append(dsn)
    command.extend(["-X", "-v", "ON_ERROR_STOP=1", "-q"])
    return command


def _quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _schema_name(prefix: str, run_id: str, case_id: str, engine: str) -> str:
    raw = f"{prefix}_{run_id}_{case_id}_{engine}".lower()
    safe = re.sub(r"[^a-z0-9_]+", "_", raw).strip("_")
    if not safe or not re.match(r"[a-z_]", safe):
        safe = "sqlrb_" + safe
    if len(safe) <= 63:
        return safe
    digest = hashlib.sha1(safe.encode("utf-8")).hexdigest()[:10]
    return f"{safe[:52]}_{digest}"


def _ensure_under(child: Path, parent: Path) -> None:
    child_resolved = child.resolve()
    parent_resolved = parent.resolve()
    if child_resolved != parent_resolved and parent_resolved not in child_resolved.parents:
        raise ValueError(f"output path escapes allowed directory: {child}")


def _run_psql_file(
    *,
    script_path: Path,
    timeout: int,
    cwd: Path,
    dsn_env: str,
) -> subprocess.CompletedProcess[str]:
    command = _psql_base_command(dsn_env=dsn_env)
    command.extend(["-f", str(script_path)])
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def _csv_stdout_to_jsonl(stdout: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = stdout.strip()
    if not text:
        output_path.write_text("", encoding="utf-8")
        return
    reader = csv.DictReader(io.StringIO(text))
    with output_path.open("w", encoding="utf-8") as f:
        for row in reader:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def _query_script(schema: str, sql_path: Path) -> str:
    sql = sql_path.read_text(encoding="utf-8")
    return "\n".join(
        [
            f"SET search_path TO {_quote_ident(schema)}, public;",
            "\\pset format csv",
            sql,
            "",
        ]
    )


def _setup_script(schema: str, ddl_path: Path, load_path: Path) -> str:
    return "\n".join(
        [
            f"DROP SCHEMA IF EXISTS {_quote_ident(schema)} CASCADE;",
            f"CREATE SCHEMA {_quote_ident(schema)};",
            f"SET search_path TO {_quote_ident(schema)}, public;",
            ddl_path.read_text(encoding="utf-8"),
            load_path.read_text(encoding="utf-8"),
            "",
        ]
    )


def execute_postgres_case(
    *,
    repo_root: Path,
    run_id: str,
    row: SelectedCaseEngineRow,
    candidate_sql_path: Path,
    workspace_dir: Path,
    timeout_sec: int,
    schema_prefix: str,
    dsn_env: str = "SQLRB_POSTGRES_DSN",
) -> PostgresExecutionResult:
    """Execute source and candidate SQL for one postgres case-engine row."""

    execution_dir = workspace_dir / "execution"
    execution_dir.mkdir(parents=True, exist_ok=True)
    _ensure_under(execution_dir, workspace_dir)

    if row.engine != "postgres":
        return PostgresExecutionResult(
            source_execution_status=EXECUTION_STATUS_NOT_ENABLED,
            candidate_execution_status=EXECUTION_STATUS_NOT_ENABLED,
            source_result_path=None,
            candidate_result_path=None,
            db_artifact_dir=execution_dir,
            failure_bucket=FAILURE_UNSUPPORTED_ENGINE,
            execution_failure_class="unsupported_engine",
            notes="postgres execution MVP only supports engine=postgres",
        )

    if not postgres_config_available(dsn_env=dsn_env):
        return PostgresExecutionResult(
            source_execution_status=EXECUTION_STATUS_NOT_ENABLED,
            candidate_execution_status=EXECUTION_STATUS_NOT_ENABLED,
            source_result_path=None,
            candidate_result_path=None,
            db_artifact_dir=execution_dir,
            failure_bucket=FAILURE_INTERNAL_RUNNER_ERROR,
            execution_failure_class="postgres_config_missing",
            notes="allowed Postgres connection configuration is not available",
        )

    case_dir = repo_root / row.case_path
    source_sql_path = repo_root / row.source_sql_path
    ddl_path = case_dir / "schema" / "postgres" / "ddl.sql"
    load_path = case_dir / "schema" / "postgres" / "load.sql"
    for required in [source_sql_path, candidate_sql_path, ddl_path, load_path]:
        if not required.exists():
            return PostgresExecutionResult(
                source_execution_status=EXECUTION_STATUS_SOURCE_FAILED,
                candidate_execution_status=EXECUTION_STATUS_NOT_ENABLED,
                source_result_path=None,
                candidate_result_path=None,
                db_artifact_dir=execution_dir,
                failure_bucket=FAILURE_SOURCE_EXECUTION_FAILED,
                execution_failure_class="required_sql_asset_missing",
                notes=f"missing required SQL asset: {required}",
            )

    schema = _schema_name(schema_prefix, run_id, row.case_id, row.engine)
    source_result = execution_dir / "source_result.jsonl"
    candidate_result = execution_dir / "candidate_result.jsonl"
    cleanup_log = execution_dir / "cleanup_log.txt"
    setup_script_path = execution_dir / "setup.sql"
    source_script_path = execution_dir / "source_query.sql"
    candidate_script_path = execution_dir / "candidate_query.sql"
    cleanup_script_path = execution_dir / "cleanup.sql"

    try:
        setup_script_path.write_text(_setup_script(schema, ddl_path, load_path), encoding="utf-8")
        setup = _run_psql_file(
            script_path=setup_script_path,
            timeout=timeout_sec,
            cwd=repo_root,
            dsn_env=dsn_env,
        )
        if setup.returncode != 0:
            (execution_dir / "source_error.txt").write_text(
                setup.stderr or setup.stdout or "schema setup failed", encoding="utf-8"
            )
            return PostgresExecutionResult(
                source_execution_status=EXECUTION_STATUS_SOURCE_FAILED,
                candidate_execution_status=EXECUTION_STATUS_NOT_ENABLED,
                source_result_path=None,
                candidate_result_path=None,
                db_artifact_dir=execution_dir,
                failure_bucket=FAILURE_SOURCE_EXECUTION_FAILED,
                execution_failure_class="schema_setup_failed",
                notes="postgres schema setup failed before source execution",
            )

        source_script_path.write_text(_query_script(schema, source_sql_path), encoding="utf-8")
        source = _run_psql_file(
            script_path=source_script_path,
            timeout=timeout_sec,
            cwd=repo_root,
            dsn_env=dsn_env,
        )
        if source.returncode != 0:
            (execution_dir / "source_error.txt").write_text(
                source.stderr or source.stdout or "source execution failed", encoding="utf-8"
            )
            return PostgresExecutionResult(
                source_execution_status=EXECUTION_STATUS_SOURCE_FAILED,
                candidate_execution_status=EXECUTION_STATUS_NOT_ENABLED,
                source_result_path=None,
                candidate_result_path=None,
                db_artifact_dir=execution_dir,
                failure_bucket=FAILURE_SOURCE_EXECUTION_FAILED,
                execution_failure_class="source_execution_failed",
                notes="source SQL execution failed",
            )
        _csv_stdout_to_jsonl(source.stdout, source_result)

        candidate_script_path.write_text(
            _query_script(schema, candidate_sql_path), encoding="utf-8"
        )
        candidate = _run_psql_file(
            script_path=candidate_script_path,
            timeout=timeout_sec,
            cwd=repo_root,
            dsn_env=dsn_env,
        )
        if candidate.returncode != 0:
            (execution_dir / "candidate_error.txt").write_text(
                candidate.stderr or candidate.stdout or "candidate execution failed",
                encoding="utf-8",
            )
            return PostgresExecutionResult(
                source_execution_status=EXECUTION_STATUS_SOURCE_SUCCESS,
                candidate_execution_status=EXECUTION_STATUS_CANDIDATE_FAILED,
                source_result_path=source_result,
                candidate_result_path=None,
                db_artifact_dir=execution_dir,
                failure_bucket=FAILURE_CANDIDATE_EXECUTION_FAILED,
                execution_failure_class="candidate_execution_failed",
                notes="candidate SQL execution failed",
            )
        _csv_stdout_to_jsonl(candidate.stdout, candidate_result)

        return PostgresExecutionResult(
            source_execution_status=EXECUTION_STATUS_SOURCE_SUCCESS,
            candidate_execution_status=EXECUTION_STATUS_CANDIDATE_SUCCESS,
            source_result_path=source_result,
            candidate_result_path=candidate_result,
            db_artifact_dir=execution_dir,
            failure_bucket=FAILURE_NONE,
            execution_failure_class="",
            notes="source and candidate SQL executed locally through psql",
        )
    except subprocess.TimeoutExpired as exc:
        error_target = execution_dir / "source_error.txt"
        error_target.write_text(str(exc), encoding="utf-8")
        return PostgresExecutionResult(
            source_execution_status=EXECUTION_STATUS_TIMEOUT,
            candidate_execution_status=EXECUTION_STATUS_TIMEOUT,
            source_result_path=None,
            candidate_result_path=None,
            db_artifact_dir=execution_dir,
            failure_bucket=FAILURE_EXECUTION_TIMEOUT,
            execution_failure_class="execution_timeout",
            notes=f"postgres execution timed out after {timeout_sec} seconds",
        )
    except Exception as exc:
        (execution_dir / "source_error.txt").write_text(str(exc), encoding="utf-8")
        return PostgresExecutionResult(
            source_execution_status=EXECUTION_STATUS_INTERNAL_ERROR,
            candidate_execution_status=EXECUTION_STATUS_INTERNAL_ERROR,
            source_result_path=None,
            candidate_result_path=None,
            db_artifact_dir=execution_dir,
            failure_bucket=FAILURE_INTERNAL_RUNNER_ERROR,
            execution_failure_class="execution_internal_error",
            notes=f"postgres execution internal error: {exc}",
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
