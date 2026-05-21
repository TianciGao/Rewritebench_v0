"""MySQL local diagnostic execution helpers for user-entry source references.

This module implements a bounded MySQL source-reference backend for declared
PORT cross-dialect diagnostics. It writes local artifacts only, does not fall
back to PostgreSQL, and does not compute timing, official metrics, reports, or
leaderboard data.
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
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from .case_package_resolver import ResolvedCasePackage
from .case_selection import SelectedCaseEngineRow
from .engine_execution import EngineExecutionResult, unsupported_engine_result
from .user_run_schema import (
    BACKEND_STATUS_AVAILABLE,
    BACKEND_STATUS_CLIENT_MISSING,
    BACKEND_STATUS_CONFIG_MISSING,
    BACKEND_STATUS_CONNECTION_FAILED,
    BACKEND_STATUS_NOT_IMPLEMENTED,
    BACKEND_STATUS_SCHEMA_MISSING,
    CROSS_DIALECT_STATUS_BACKEND_MISSING,
    CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
    CROSS_DIALECT_STATUS_SOURCE_REFERENCE_FAILED,
    EXECUTION_STATUS_INTERNAL_ERROR,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    EXECUTION_STATUS_SOURCE_FAILED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    EXECUTION_STATUS_TIMEOUT,
    EXECUTION_STATUS_UNSUPPORTED,
    FAILURE_CROSS_DIALECT_BACKEND_MISSING,
    FAILURE_EXECUTION_TIMEOUT,
    FAILURE_INTERNAL_RUNNER_ERROR,
    FAILURE_NONE,
    FAILURE_SOURCE_EXECUTION_FAILED,
    FAILURE_UNSUPPORTED_ENGINE,
)

MYSQL_HOST_ENV = "SQLRB_MYSQL_HOST"
MYSQL_PORT_ENV = "SQLRB_MYSQL_PORT"
MYSQL_USER_ENV = "SQLRB_MYSQL_USER"
MYSQL_PASSWORD_ENV = "SQLRB_MYSQL_PASSWORD"
MYSQL_REQUIRED_ENV = (MYSQL_HOST_ENV, MYSQL_PORT_ENV, MYSQL_USER_ENV)


@dataclass(frozen=True)
class MySQLSchemaAssets:
    """MySQL DDL/load paths resolved from explicit external schema metadata."""

    external_profile_path: Path
    ddl_path: Path
    load_path: Path


def _simple_yaml_mapping(path: Path) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line_without_comment = raw_line.split("#", 1)[0].rstrip()
        if not line_without_comment.strip():
            continue
        stripped = line_without_comment.strip()
        if stripped.startswith("-") or ":" not in stripped:
            continue
        indent = len(line_without_comment) - len(line_without_comment.lstrip(" "))
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
            continue
        parent[key] = value.strip("'\"")
    return root


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception:
        return _simple_yaml_mapping(path)

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def _resolve_repo_relative(repo_root: Path, raw: object, *, field: str) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError(f"{field} is required")
    path = Path(raw.strip())
    if path.is_absolute():
        raise ValueError(f"{field} must be repository-relative: {raw}")
    if ".." in path.parts:
        raise ValueError(f"{field} must not contain '..': {raw}")
    resolved = (repo_root / path).resolve()
    repo_resolved = repo_root.resolve()
    if resolved != repo_resolved and repo_resolved not in resolved.parents:
        raise ValueError(f"{field} escapes repository root: {raw}")
    return resolved


def _ensure_under(child: Path, parent: Path) -> None:
    child_resolved = child.resolve()
    parent_resolved = parent.resolve()
    if child_resolved != parent_resolved and parent_resolved not in child_resolved.parents:
        raise ValueError(f"output path escapes allowed directory: {child}")


def resolve_mysql_schema_assets(*, repo_root: Path, row: SelectedCaseEngineRow) -> MySQLSchemaAssets:
    """Resolve MySQL DDL/load paths from manifest schema.external_profile."""

    case_dir = repo_root / row.case_path
    manifest_path = case_dir / "manifest.yaml"
    if not manifest_path.exists():
        raise ValueError(f"manifest is required for external schema resolution: {manifest_path}")

    manifest = _load_yaml_mapping(manifest_path)
    schema = manifest.get("schema")
    if not isinstance(schema, dict):
        raise ValueError(f"manifest schema section must be a mapping: {manifest_path}")
    external_profile = _resolve_repo_relative(
        repo_root,
        schema.get("external_profile"),
        field="schema.external_profile",
    )
    if not external_profile.exists():
        raise ValueError(f"schema.external_profile does not exist: {external_profile}")

    profile = _load_yaml_mapping(external_profile)
    engines = profile.get("engines")
    if not isinstance(engines, dict):
        raise ValueError(f"external schema profile engines section must be a mapping: {external_profile}")
    mysql = engines.get("mysql")
    if not isinstance(mysql, dict):
        raise ValueError(f"external schema profile has no mysql engine entry: {external_profile}")

    ddl_path = _resolve_repo_relative(repo_root, mysql.get("ddl"), field="engines.mysql.ddl")
    load_path = _resolve_repo_relative(repo_root, mysql.get("load"), field="engines.mysql.load")
    missing = [path for path in (ddl_path, load_path) if not path.exists()]
    if missing:
        raise ValueError(
            "external mysql schema asset missing: "
            + ", ".join(str(path) for path in missing)
        )
    return MySQLSchemaAssets(
        external_profile_path=external_profile,
        ddl_path=ddl_path,
        load_path=load_path,
    )


def mysql_client_available() -> bool:
    return shutil.which("mysql") is not None


def mysql_config_available() -> bool:
    return all(os.environ.get(name) for name in MYSQL_REQUIRED_ENV)


def redacted_mysql_config_source() -> str:
    present = [
        name
        for name in [*MYSQL_REQUIRED_ENV, MYSQL_PASSWORD_ENV, "MYSQL_PWD"]
        if os.environ.get(name)
    ]
    if not present:
        return "none"
    return ",".join(f"{name}=<set>" for name in present)


def _mysql_base_command() -> list[str]:
    if not mysql_client_available():
        raise FileNotFoundError("mysql CLI is not available")
    return [
        "mysql",
        "--batch",
        "--raw",
        "--quick",
        "--column-names",
        "--default-character-set=utf8mb4",
        "--protocol=TCP",
        "--host",
        os.environ[MYSQL_HOST_ENV],
        "--port",
        os.environ[MYSQL_PORT_ENV],
        "--user",
        os.environ[MYSQL_USER_ENV],
    ]


def _mysql_subprocess_env() -> dict[str, str]:
    env = os.environ.copy()
    if MYSQL_PASSWORD_ENV in env:
        env["MYSQL_PWD"] = env[MYSQL_PASSWORD_ENV]
    return env


def _quote_ident(identifier: str) -> str:
    return "`" + identifier.replace("`", "``") + "`"


def _database_name(prefix: str, run_id: str, case_id: str) -> str:
    raw = f"{prefix}_{run_id}_{case_id}_mysql_src".lower()
    safe = re.sub(r"[^a-z0-9_]+", "_", raw).strip("_")
    if not safe or not re.match(r"[a-z_]", safe):
        safe = "sqlrb_" + safe
    if len(safe) <= 64:
        return safe
    digest = hashlib.sha1(safe.encode("utf-8")).hexdigest()[:10]
    return f"{safe[:53]}_{digest}"


def _setup_script(database: str, ddl_path: Path, load_path: Path) -> str:
    return "\n".join(
        [
            f"DROP DATABASE IF EXISTS {_quote_ident(database)};",
            (
                f"CREATE DATABASE {_quote_ident(database)} "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            ),
            f"USE {_quote_ident(database)};",
            ddl_path.read_text(encoding="utf-8"),
            load_path.read_text(encoding="utf-8"),
            "",
        ]
    )


def _query_script(database: str, sql_path: Path) -> str:
    return "\n".join(
        [
            f"USE {_quote_ident(database)};",
            sql_path.read_text(encoding="utf-8"),
            "",
        ]
    )


def _run_mysql_file(
    *,
    script_path: Path,
    timeout: int,
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        _mysql_base_command(),
        input=script_path.read_text(encoding="utf-8"),
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
        env=_mysql_subprocess_env(),
    )


def _tsv_stdout_to_jsonl(stdout: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = stdout.rstrip("\n")
    if not text:
        output_path.write_text("", encoding="utf-8")
        return
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    with output_path.open("w", encoding="utf-8") as f:
        for row in reader:
            normalized = {
                key: (None if value == "\\N" else value)
                for key, value in row.items()
            }
            f.write(json.dumps(normalized, sort_keys=True) + "\n")


def _write_command_metadata(path: Path) -> None:
    payload = {
        "client": "mysql",
        "config_source": redacted_mysql_config_source(),
        "local_diagnostic_only": True,
        "official_metrics": False,
        "timing": False,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _setup_failure_class(stderr: str, stdout: str) -> tuple[str, str, str, str]:
    text = f"{stderr}\n{stdout}".lower()
    connection_markers = [
        "access denied",
        "can't connect",
        "cannot connect",
        "unknown mysql server host",
        "lost connection",
        "error 2002",
        "error 2003",
        "error 1045",
    ]
    if any(marker in text for marker in connection_markers):
        return (
            FAILURE_CROSS_DIALECT_BACKEND_MISSING,
            "mysql_connection_failed",
            BACKEND_STATUS_CONNECTION_FAILED,
            EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
        )
    return (
        FAILURE_SOURCE_EXECUTION_FAILED,
        "mysql_schema_setup_failed",
        BACKEND_STATUS_AVAILABLE,
        EXECUTION_STATUS_SOURCE_FAILED,
    )


def _fail_closed_result(
    *,
    row: SelectedCaseEngineRow,
    execution_dir: Path,
    failure_bucket: str,
    execution_failure_class: str,
    notes: str,
    source_status: str = EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    backend_status: str,
    db_execution_attempted: bool = False,
    schema_setup_status: str = "not_attempted_backend_missing",
    error_path: Path | None = None,
) -> EngineExecutionResult:
    return EngineExecutionResult(
        source_execution_status=source_status,
        candidate_execution_status=EXECUTION_STATUS_NOT_ENABLED,
        source_result_path=None,
        candidate_result_path=None,
        db_artifact_dir=execution_dir,
        failure_bucket=failure_bucket,
        execution_failure_class=execution_failure_class,
        notes=notes,
        engine=row.engine,
        case_id=row.case_id,
        pool=row.pool,
        denominator_id=row.denominator_id,
        schema_setup_status=schema_setup_status,
        source_error_path=error_path,
        candidate_error_path=None,
        db_execution_attempted=db_execution_attempted,
        source_executable=False,
        candidate_executable=False,
        cross_dialect_status=CROSS_DIALECT_STATUS_BACKEND_MISSING
        if failure_bucket == FAILURE_CROSS_DIALECT_BACKEND_MISSING
        else CROSS_DIALECT_STATUS_SOURCE_REFERENCE_FAILED,
        required_backend="mysql",
        backend_status=backend_status,
    )


def execute_mysql_source_reference(
    *,
    repo_root: Path,
    run_id: str,
    row: SelectedCaseEngineRow,
    resolved_package: ResolvedCasePackage,
    workspace_dir: Path,
    timeout_sec: int,
    schema_prefix: str,
) -> EngineExecutionResult:
    """Execute a manifest-declared MySQL source-reference query locally."""

    execution_dir = workspace_dir / "execution" / "mysql_source"
    execution_dir.mkdir(parents=True, exist_ok=True)
    _ensure_under(execution_dir, workspace_dir)
    _write_command_metadata(execution_dir / "command_metadata.json")

    if not mysql_client_available():
        return _fail_closed_result(
            row=row,
            execution_dir=execution_dir,
            failure_bucket=FAILURE_CROSS_DIALECT_BACKEND_MISSING,
            execution_failure_class="mysql_client_missing",
            notes=(
                "mysql CLI is not available; source reference was not executed, "
                "target execution and checker were skipped"
            ),
            backend_status=BACKEND_STATUS_CLIENT_MISSING,
        )

    if not mysql_config_available():
        return _fail_closed_result(
            row=row,
            execution_dir=execution_dir,
            failure_bucket=FAILURE_CROSS_DIALECT_BACKEND_MISSING,
            execution_failure_class="mysql_config_missing",
            notes=(
                "required MySQL local diagnostic environment is missing "
                f"({', '.join(MYSQL_REQUIRED_ENV)}); no SQL was executed"
            ),
            backend_status=BACKEND_STATUS_CONFIG_MISSING,
        )

    try:
        schema_assets = resolve_mysql_schema_assets(repo_root=repo_root, row=row)
    except ValueError as exc:
        return _fail_closed_result(
            row=row,
            execution_dir=execution_dir,
            failure_bucket=FAILURE_CROSS_DIALECT_BACKEND_MISSING,
            execution_failure_class="mysql_schema_missing",
            notes=str(exc),
            backend_status=BACKEND_STATUS_SCHEMA_MISSING,
        )

    source_sql_path = resolved_package.source_reference_query_path
    for required in [source_sql_path, schema_assets.ddl_path, schema_assets.load_path]:
        if not required.exists():
            return _fail_closed_result(
                row=row,
                execution_dir=execution_dir,
                failure_bucket=FAILURE_CROSS_DIALECT_BACKEND_MISSING,
                execution_failure_class="mysql_schema_missing",
                notes=f"missing required MySQL source-reference asset: {required}",
                backend_status=BACKEND_STATUS_SCHEMA_MISSING,
            )

    database = _database_name(schema_prefix, run_id, row.case_id)
    source_result = execution_dir / "source_result.jsonl"
    setup_script_path = execution_dir / "setup.sql"
    source_script_path = execution_dir / "source_query.sql"
    cleanup_script_path = execution_dir / "cleanup.sql"
    cleanup_log = execution_dir / "cleanup_log.txt"
    source_error_path = execution_dir / "source_error.txt"

    try:
        setup_script_path.write_text(
            _setup_script(database, schema_assets.ddl_path, schema_assets.load_path),
            encoding="utf-8",
        )
        setup = _run_mysql_file(
            script_path=setup_script_path,
            timeout=timeout_sec,
            cwd=repo_root,
        )
        if setup.returncode != 0:
            source_error_path.write_text(
                setup.stderr or setup.stdout or "mysql schema setup failed",
                encoding="utf-8",
            )
            failure_bucket, failure_class, backend_status, source_status = _setup_failure_class(
                setup.stderr,
                setup.stdout,
            )
            return _fail_closed_result(
                row=row,
                execution_dir=execution_dir,
                failure_bucket=failure_bucket,
                execution_failure_class=failure_class,
                notes="mysql source-reference setup failed",
                source_status=source_status,
                backend_status=backend_status,
                db_execution_attempted=True,
                schema_setup_status="connection_failed"
                if failure_class == "mysql_connection_failed"
                else "schema_setup_failed",
                error_path=source_error_path,
            )

        source_script_path.write_text(_query_script(database, source_sql_path), encoding="utf-8")
        source = _run_mysql_file(
            script_path=source_script_path,
            timeout=timeout_sec,
            cwd=repo_root,
        )
        if source.returncode != 0:
            source_error_path.write_text(
                source.stderr or source.stdout or "mysql source execution failed",
                encoding="utf-8",
            )
            return _fail_closed_result(
                row=row,
                execution_dir=execution_dir,
                failure_bucket=FAILURE_SOURCE_EXECUTION_FAILED,
                execution_failure_class="mysql_source_execution_failed",
                notes="mysql source-reference SQL execution failed",
                source_status=EXECUTION_STATUS_SOURCE_FAILED,
                backend_status=BACKEND_STATUS_AVAILABLE,
                db_execution_attempted=True,
                schema_setup_status="schema_setup_success",
                error_path=source_error_path,
            )
        _tsv_stdout_to_jsonl(source.stdout, source_result)

        return EngineExecutionResult(
            source_execution_status=EXECUTION_STATUS_SOURCE_SUCCESS,
            candidate_execution_status=EXECUTION_STATUS_NOT_ENABLED,
            source_result_path=source_result,
            candidate_result_path=None,
            db_artifact_dir=execution_dir,
            failure_bucket=FAILURE_NONE,
            execution_failure_class="",
            notes=(
                "source reference SQL executed locally through mysql using explicit "
                f"external schema profile {schema_assets.external_profile_path}"
            ),
            engine=row.engine,
            case_id=row.case_id,
            pool=row.pool,
            denominator_id=row.denominator_id,
            schema_setup_status="schema_setup_success",
            db_execution_attempted=True,
            source_executable=True,
            candidate_executable=False,
            cross_dialect_status=CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
            required_backend="mysql",
            backend_status=BACKEND_STATUS_AVAILABLE,
        )
    except subprocess.TimeoutExpired as exc:
        source_error_path.write_text(str(exc), encoding="utf-8")
        return _fail_closed_result(
            row=row,
            execution_dir=execution_dir,
            failure_bucket=FAILURE_EXECUTION_TIMEOUT,
            execution_failure_class="mysql_execution_timeout",
            notes=f"mysql source-reference execution timed out after {timeout_sec} seconds",
            source_status=EXECUTION_STATUS_TIMEOUT,
            backend_status=BACKEND_STATUS_AVAILABLE,
            db_execution_attempted=True,
            schema_setup_status="timeout",
            error_path=source_error_path,
        )
    except Exception as exc:
        source_error_path.write_text(str(exc), encoding="utf-8")
        return _fail_closed_result(
            row=row,
            execution_dir=execution_dir,
            failure_bucket=FAILURE_INTERNAL_RUNNER_ERROR,
            execution_failure_class="mysql_execution_internal_error",
            notes=f"mysql source-reference execution internal error: {exc}",
            source_status=EXECUTION_STATUS_INTERNAL_ERROR,
            backend_status=BACKEND_STATUS_AVAILABLE,
            db_execution_attempted=True,
            schema_setup_status="internal_error",
            error_path=source_error_path,
        )
    finally:
        try:
            cleanup_script_path.write_text(
                f"DROP DATABASE IF EXISTS {_quote_ident(database)};\n",
                encoding="utf-8",
            )
            cleanup = _run_mysql_file(
                script_path=cleanup_script_path,
                timeout=timeout_sec,
                cwd=repo_root,
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


def execute_mysql_case(
    *,
    repo_root: Path,
    run_id: str,
    row: SelectedCaseEngineRow,
    candidate_sql_path: Path,
    workspace_dir: Path,
    timeout_sec: int,
    schema_prefix: str,
) -> EngineExecutionResult:
    """Fail closed for same-engine MySQL execution, which remains deferred."""

    _ = (repo_root, run_id, candidate_sql_path, timeout_sec, schema_prefix)
    result = unsupported_engine_result(
        row=row,
        workspace_dir=workspace_dir,
        execution_failure_class="mysql_same_engine_execution_not_implemented",
        notes=(
            "same-engine mysql execution remains deferred for user-entry local "
            "diagnostics; source-reference execution is available only through "
            "explicit cross-dialect metadata and no PostgreSQL fallback was used"
        ),
    )
    return replace(
        result,
        backend_status=BACKEND_STATUS_NOT_IMPLEMENTED,
        required_backend="mysql",
    )
