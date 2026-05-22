"""Spark SQL local diagnostic execution helpers for user-entry diagnostics.

This module implements bounded same-engine Spark local diagnostics through
PySpark when a local PySpark client is available. It writes local artifacts
only, does not fall back to PostgreSQL/MySQL, and does not compute timing,
official metrics, reports, or leaderboard data.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from .case_selection import SelectedCaseEngineRow
from .engine_execution import EngineExecutionResult
from .user_run_schema import (
    BACKEND_STATUS_AVAILABLE,
    BACKEND_STATUS_CLIENT_MISSING,
    BACKEND_STATUS_CONFIG_MISSING,
    BACKEND_STATUS_SCHEMA_MISSING,
    CROSS_DIALECT_STATUS_NOT_APPLICABLE,
    EXECUTION_STATUS_CANDIDATE_FAILED,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_INTERNAL_ERROR,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    EXECUTION_STATUS_SOURCE_FAILED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    EXECUTION_STATUS_TIMEOUT,
    EXECUTION_STATUS_UNSUPPORTED,
    FAILURE_CANDIDATE_EXECUTION_FAILED,
    FAILURE_EXECUTION_TIMEOUT,
    FAILURE_INTERNAL_RUNNER_ERROR,
    FAILURE_NONE,
    FAILURE_SOURCE_EXECUTION_FAILED,
    FAILURE_UNSUPPORTED_ENGINE,
)

SPARK_MASTER_ENV = "SQLRB_SPARK_MASTER"
SPARK_APP_NAME_ENV = "SQLRB_SPARK_APP_NAME"


@dataclass(frozen=True)
class SparkEnvironmentStatus:
    """Conservative Spark local-environment detector result."""

    spark_local_ip_set: bool
    spark_home_set: bool
    pyspark_python_set: bool
    spark_sql_path: str
    pyspark_importable: bool
    environment_configured: bool
    client_available: bool
    backend_status: str
    failure_class: str
    implementation_status: str = "spark_live_backend_v0"

    @property
    def summary(self) -> str:
        client_parts = []
        if self.spark_sql_path:
            client_parts.append("spark-sql")
        if self.pyspark_importable:
            client_parts.append("pyspark")
        clients = "+".join(client_parts) if client_parts else "no_client"
        configured = "configured" if self.environment_configured else "not_configured"
        return f"{configured}; {clients}; {self.implementation_status}; {self.failure_class}"


@dataclass(frozen=True)
class SparkSchemaAssets:
    """Spark DDL/load paths resolved from explicit external schema metadata."""

    external_profile_path: Path
    ddl_path: Path
    load_path: Path


def inspect_spark_environment(
    env: Mapping[str, str] | None = None,
    *,
    spark_sql_path: str | None = None,
    pyspark_importable: bool | None = None,
) -> SparkEnvironmentStatus:
    """Inspect lightweight Spark environment signals without starting Spark.

    `spark_sql_path` and `pyspark_importable` are injectable for deterministic
    tests. The default path uses `shutil.which` and `importlib.util.find_spec`,
    which do not start Spark.
    """

    effective_env = env if env is not None else os.environ
    spark_local_ip_set = bool(effective_env.get("SPARK_LOCAL_IP"))
    spark_home_set = bool(effective_env.get("SPARK_HOME"))
    pyspark_python_set = bool(effective_env.get("PYSPARK_PYTHON"))
    resolved_spark_sql = spark_sql_path
    if resolved_spark_sql is None:
        resolved_spark_sql = shutil.which("spark-sql") or ""
    resolved_pyspark = pyspark_importable
    if resolved_pyspark is None:
        resolved_pyspark = importlib.util.find_spec("pyspark") is not None

    # PySpark importability is enough for local-mode execution. The env flags
    # remain useful diagnostics but are not mandatory when PySpark is present.
    environment_configured = bool(
        resolved_pyspark
        or resolved_spark_sql
        or spark_local_ip_set
        or spark_home_set
        or pyspark_python_set
        or effective_env.get(SPARK_MASTER_ENV)
    )
    client_available = bool(resolved_pyspark)
    if bool(resolved_pyspark):
        backend_status = BACKEND_STATUS_AVAILABLE
        failure_class = ""
    elif not environment_configured:
        backend_status = BACKEND_STATUS_CONFIG_MISSING
        failure_class = "spark_config_missing"
    else:
        backend_status = BACKEND_STATUS_CLIENT_MISSING
        failure_class = "spark_pyspark_missing"

    return SparkEnvironmentStatus(
        spark_local_ip_set=spark_local_ip_set,
        spark_home_set=spark_home_set,
        pyspark_python_set=pyspark_python_set,
        spark_sql_path=resolved_spark_sql,
        pyspark_importable=bool(resolved_pyspark),
        environment_configured=environment_configured,
        client_available=client_available,
        backend_status=backend_status,
        failure_class=failure_class,
    )


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


def resolve_spark_schema_assets(*, repo_root: Path, row: SelectedCaseEngineRow) -> SparkSchemaAssets:
    """Resolve Spark DDL/load paths from manifest schema.external_profile."""

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
    spark = engines.get("spark")
    if not isinstance(spark, dict):
        raise ValueError(f"external schema profile has no spark engine entry: {external_profile}")

    ddl_path = _resolve_repo_relative(repo_root, spark.get("ddl"), field="engines.spark.ddl")
    load_path = _resolve_repo_relative(repo_root, spark.get("load"), field="engines.spark.load")
    missing = [path for path in (ddl_path, load_path) if not path.exists()]
    if missing:
        raise ValueError(
            "external spark schema asset missing: "
            + ", ".join(str(path) for path in missing)
        )
    return SparkSchemaAssets(
        external_profile_path=external_profile,
        ddl_path=ddl_path,
        load_path=load_path,
    )


def _database_name(prefix: str, run_id: str, case_id: str) -> str:
    raw = f"{prefix}_{run_id}_{case_id}_spark".lower()
    safe = re.sub(r"[^a-z0-9_]+", "_", raw).strip("_")
    if not safe or not re.match(r"[a-z_]", safe):
        safe = "sqlrb_" + safe
    if len(safe) <= 128:
        return safe
    digest = hashlib.sha1(safe.encode("utf-8")).hexdigest()[:10]
    return f"{safe[:117]}_{digest}"


def _strip_sql_comments(sql: str) -> str:
    lines: list[str] = []
    for line in sql.splitlines():
        # The case-package schema scripts use line comments. Avoid handling
        # every SQL dialect comment form here; preserve literals below.
        if line.lstrip().startswith("--"):
            continue
        lines.append(line)
    return "\n".join(lines)


def _split_sql_statements(sql: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    in_single = False
    in_double = False
    i = 0
    text = _strip_sql_comments(sql)
    while i < len(text):
        char = text[i]
        if char == "'" and not in_double:
            current.append(char)
            if i + 1 < len(text) and text[i + 1] == "'":
                current.append(text[i + 1])
                i += 2
                continue
            in_single = not in_single
            i += 1
            continue
        if char == '"' and not in_single:
            in_double = not in_double
            current.append(char)
            i += 1
            continue
        if char == ";" and not in_single and not in_double:
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
            i += 1
            continue
        current.append(char)
        i += 1
    statement = "".join(current).strip()
    if statement:
        statements.append(statement)
    return statements


def _serialize_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, (bytes, bytearray)):
        return value.hex()
    if isinstance(value, (list, tuple)):
        return [_serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _serialize_value(item) for key, item in value.items()}
    if hasattr(value, "asDict"):
        return {str(key): _serialize_value(item) for key, item in value.asDict(recursive=True).items()}
    return str(value)


def _write_result_jsonl(dataframe: Any, output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    columns = list(getattr(dataframe, "columns", []))
    rows = dataframe.collect()
    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            payload = {
                column: _serialize_value(row[index])
                for index, column in enumerate(columns)
            }
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return len(rows)


def _create_spark_session(*, app_name: str, warehouse_dir: Path, env: Mapping[str, str] | None = None) -> Any:
    effective_env = env if env is not None else os.environ
    from pyspark.sql import SparkSession  # type: ignore

    builder = (
        SparkSession.builder.appName(app_name)
        .master(effective_env.get(SPARK_MASTER_ENV, "local[1]"))
        .config("spark.sql.warehouse.dir", str(warehouse_dir))
        .config("spark.ui.enabled", "false")
    )
    local_ip = effective_env.get("SPARK_LOCAL_IP")
    if local_ip:
        builder = builder.config("spark.driver.bindAddress", local_ip)
    return builder.getOrCreate()


def _write_environment_metadata(
    execution_dir: Path,
    *,
    row: SelectedCaseEngineRow,
    run_id: str,
    status: SparkEnvironmentStatus,
    spark_sql_executed: bool,
    source_result_artifact_created: bool,
    candidate_result_artifact_created: bool,
    schema_assets: SparkSchemaAssets | None = None,
    row_counts: Mapping[str, int] | None = None,
    cleanup_note: str = "",
) -> Path:
    execution_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = execution_dir / "spark_execution_metadata.json"
    payload: dict[str, Any] = {
        "run_id": run_id,
        "case_id": row.case_id,
        "engine": row.engine,
        "local_diagnostic_only": True,
        "spark_live_execution_implemented": True,
        "spark_sql_executed": spark_sql_executed,
        "source_result_artifact_created": source_result_artifact_created,
        "candidate_result_artifact_created": candidate_result_artifact_created,
        "environment": asdict(status),
        "official_metrics": False,
        "timing": False,
        "cleanup_note": cleanup_note,
    }
    if schema_assets is not None:
        payload["schema_assets"] = {
            "external_profile_path": str(schema_assets.external_profile_path),
            "ddl_path": str(schema_assets.ddl_path),
            "load_path": str(schema_assets.load_path),
        }
    if row_counts:
        payload["row_counts"] = dict(row_counts)
    metadata_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    # Keep the skeleton-era filename as a small compatibility breadcrumb.
    environment_path = execution_dir / "spark_environment_status.json"
    environment_path.write_text(
        json.dumps(
            {
                "run_id": run_id,
                "case_id": row.case_id,
                "engine": row.engine,
                "local_diagnostic_only": True,
                "spark_live_execution_implemented": True,
                "spark_sql_executed": spark_sql_executed,
                "environment": asdict(status),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return metadata_path


def _write_error(path: Path, message: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(message, encoding="utf-8")
    return path


def _fail_closed_result(
    *,
    row: SelectedCaseEngineRow,
    execution_dir: Path,
    failure_bucket: str,
    execution_failure_class: str,
    notes: str,
    backend_status: str,
    source_status: str = EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    candidate_status: str = EXECUTION_STATUS_NOT_ENABLED,
    db_execution_attempted: bool = False,
    schema_setup_status: str = "not_attempted_backend_missing",
    source_result_path: Path | None = None,
    source_error_path: Path | None = None,
    candidate_error_path: Path | None = None,
) -> EngineExecutionResult:
    return EngineExecutionResult(
        source_execution_status=source_status,
        candidate_execution_status=candidate_status,
        source_result_path=source_result_path,
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
        source_error_path=source_error_path,
        candidate_error_path=candidate_error_path,
        db_execution_attempted=db_execution_attempted,
        source_executable=source_result_path is not None
        and source_status == EXECUTION_STATUS_SOURCE_SUCCESS,
        candidate_executable=False,
        local_diagnostic_only=True,
        cross_dialect_status=CROSS_DIALECT_STATUS_NOT_APPLICABLE,
        required_backend="spark",
        backend_status=backend_status,
    )


def _execute_statement_batch(spark: Any, statements: list[str]) -> None:
    for statement in statements:
        spark.sql(statement)


def _run_query_to_jsonl(
    *,
    spark: Any,
    sql_path: Path,
    result_path: Path,
    error_path: Path,
) -> int:
    try:
        statements = _split_sql_statements(sql_path.read_text(encoding="utf-8"))
        if len(statements) != 1:
            raise ValueError(
                f"Spark diagnostic query must contain exactly one statement: {sql_path}"
            )
        dataframe = spark.sql(statements[0])
        return _write_result_jsonl(dataframe, result_path)
    except Exception as exc:
        _write_error(error_path, str(exc))
        raise


def execute_spark_case(
    *,
    repo_root: Path,
    run_id: str,
    row: SelectedCaseEngineRow,
    candidate_sql_path: Path,
    workspace_dir: Path,
    timeout_sec: int,
    schema_prefix: str,
) -> EngineExecutionResult:
    """Execute a same-engine Spark source/candidate local diagnostic row."""

    _ = timeout_sec
    execution_dir = workspace_dir / "execution"
    execution_dir.mkdir(parents=True, exist_ok=True)
    _ensure_under(execution_dir, workspace_dir)

    status = inspect_spark_environment()
    if status.backend_status == BACKEND_STATUS_CONFIG_MISSING:
        metadata_path = _write_environment_metadata(
            execution_dir,
            row=row,
            run_id=run_id,
            status=status,
            spark_sql_executed=False,
            source_result_artifact_created=False,
            candidate_result_artifact_created=False,
        )
        return _fail_closed_result(
            row=row,
            execution_dir=execution_dir,
            failure_bucket=FAILURE_UNSUPPORTED_ENGINE,
            execution_failure_class=status.failure_class,
            notes=(
                "Spark local diagnostic environment is not configured; no Spark "
                "session was started, no SQL was executed, and no PostgreSQL/MySQL "
                f"fallback was used; metadata={metadata_path.name}"
            ),
            backend_status=status.backend_status,
            source_status=EXECUTION_STATUS_UNSUPPORTED,
            candidate_status=EXECUTION_STATUS_UNSUPPORTED,
        )

    if status.backend_status == BACKEND_STATUS_CLIENT_MISSING:
        metadata_path = _write_environment_metadata(
            execution_dir,
            row=row,
            run_id=run_id,
            status=status,
            spark_sql_executed=False,
            source_result_artifact_created=False,
            candidate_result_artifact_created=False,
        )
        return _fail_closed_result(
            row=row,
            execution_dir=execution_dir,
            failure_bucket=FAILURE_UNSUPPORTED_ENGINE,
            execution_failure_class=status.failure_class,
            notes=(
                "PySpark is required for Spark local diagnostic execution; "
                "spark-sql CLI execution is not implemented, no SQL was executed, "
                f"and no PostgreSQL/MySQL fallback was used; metadata={metadata_path.name}"
            ),
            backend_status=status.backend_status,
            source_status=EXECUTION_STATUS_UNSUPPORTED,
            candidate_status=EXECUTION_STATUS_UNSUPPORTED,
        )

    try:
        schema_assets = resolve_spark_schema_assets(repo_root=repo_root, row=row)
    except ValueError as exc:
        error_path = _write_error(execution_dir / "source_error.txt", str(exc))
        _write_environment_metadata(
            execution_dir,
            row=row,
            run_id=run_id,
            status=status,
            spark_sql_executed=False,
            source_result_artifact_created=False,
            candidate_result_artifact_created=False,
        )
        return _fail_closed_result(
            row=row,
            execution_dir=execution_dir,
            failure_bucket=FAILURE_SOURCE_EXECUTION_FAILED,
            execution_failure_class="spark_schema_missing",
            notes=str(exc),
            backend_status=BACKEND_STATUS_SCHEMA_MISSING,
            source_status=EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
            db_execution_attempted=True,
            schema_setup_status="schema_missing",
            source_error_path=error_path,
        )

    source_sql_path = repo_root / row.source_sql_path
    required_paths = [source_sql_path, candidate_sql_path, schema_assets.ddl_path, schema_assets.load_path]
    missing_paths = [path for path in required_paths if not path.exists()]
    if missing_paths:
        message = "missing required Spark diagnostic asset: " + ", ".join(
            str(path) for path in missing_paths
        )
        error_path = _write_error(execution_dir / "source_error.txt", message)
        _write_environment_metadata(
            execution_dir,
            row=row,
            run_id=run_id,
            status=status,
            spark_sql_executed=False,
            source_result_artifact_created=False,
            candidate_result_artifact_created=False,
            schema_assets=schema_assets,
        )
        return _fail_closed_result(
            row=row,
            execution_dir=execution_dir,
            failure_bucket=FAILURE_SOURCE_EXECUTION_FAILED,
            execution_failure_class="spark_schema_missing",
            notes=message,
            backend_status=BACKEND_STATUS_SCHEMA_MISSING,
            source_status=EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
            db_execution_attempted=True,
            schema_setup_status="schema_missing",
            source_error_path=error_path,
        )

    database = _database_name(schema_prefix, run_id, row.case_id)
    setup_script_path = execution_dir / "setup.sql"
    source_query_path = execution_dir / "source_query.sql"
    candidate_query_path = execution_dir / "candidate_query.sql"
    source_result = execution_dir / "source_result.jsonl"
    candidate_result = execution_dir / "candidate_result.jsonl"
    source_error_path = execution_dir / "source_error.txt"
    candidate_error_path = execution_dir / "candidate_error.txt"

    setup_script_path.write_text(
        "\n".join(
            [
                f"DROP DATABASE IF EXISTS {database} CASCADE;",
                f"CREATE DATABASE IF NOT EXISTS {database};",
                f"USE {database};",
                schema_assets.ddl_path.read_text(encoding="utf-8"),
                schema_assets.load_path.read_text(encoding="utf-8"),
                "",
            ]
        ),
        encoding="utf-8",
    )
    source_query_path.write_text(source_sql_path.read_text(encoding="utf-8"), encoding="utf-8")
    candidate_query_path.write_text(candidate_sql_path.read_text(encoding="utf-8"), encoding="utf-8")

    spark = None
    cleanup_note = ""
    source_rows = 0
    candidate_rows = 0
    try:
        try:
            spark = _create_spark_session(
                app_name=os.environ.get(SPARK_APP_NAME_ENV, f"SQLRB {run_id} {row.case_id}"),
                warehouse_dir=execution_dir / "spark_warehouse",
            )
        except Exception as exc:
            error_path = _write_error(source_error_path, str(exc))
            _write_environment_metadata(
                execution_dir,
                row=row,
                run_id=run_id,
                status=status,
                spark_sql_executed=False,
                source_result_artifact_created=False,
                candidate_result_artifact_created=False,
                schema_assets=schema_assets,
            )
            return _fail_closed_result(
                row=row,
                execution_dir=execution_dir,
                failure_bucket=FAILURE_SOURCE_EXECUTION_FAILED,
                execution_failure_class="spark_session_failed",
                notes="Spark session startup failed; no PostgreSQL/MySQL fallback was used",
                backend_status=BACKEND_STATUS_AVAILABLE,
                source_status=EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
                db_execution_attempted=True,
                schema_setup_status="spark_session_failed",
                source_error_path=error_path,
            )

        try:
            _execute_statement_batch(
                spark,
                _split_sql_statements(setup_script_path.read_text(encoding="utf-8")),
            )
        except Exception as exc:
            error_path = _write_error(source_error_path, str(exc))
            _write_environment_metadata(
                execution_dir,
                row=row,
                run_id=run_id,
                status=status,
                spark_sql_executed=True,
                source_result_artifact_created=False,
                candidate_result_artifact_created=False,
                schema_assets=schema_assets,
            )
            return _fail_closed_result(
                row=row,
                execution_dir=execution_dir,
                failure_bucket=FAILURE_SOURCE_EXECUTION_FAILED,
                execution_failure_class="spark_schema_setup_failed",
                notes="Spark schema/load setup failed; no PostgreSQL/MySQL fallback was used",
                backend_status=BACKEND_STATUS_AVAILABLE,
                source_status=EXECUTION_STATUS_SOURCE_FAILED,
                db_execution_attempted=True,
                schema_setup_status="schema_setup_failed",
                source_error_path=error_path,
            )

        try:
            source_rows = _run_query_to_jsonl(
                spark=spark,
                sql_path=source_query_path,
                result_path=source_result,
                error_path=source_error_path,
            )
        except TimeoutError as exc:
            error_path = _write_error(source_error_path, str(exc))
            _write_environment_metadata(
                execution_dir,
                row=row,
                run_id=run_id,
                status=status,
                spark_sql_executed=True,
                source_result_artifact_created=False,
                candidate_result_artifact_created=False,
                schema_assets=schema_assets,
            )
            return _fail_closed_result(
                row=row,
                execution_dir=execution_dir,
                failure_bucket=FAILURE_EXECUTION_TIMEOUT,
                execution_failure_class="spark_timeout",
                notes="Spark source execution timed out",
                backend_status=BACKEND_STATUS_AVAILABLE,
                source_status=EXECUTION_STATUS_TIMEOUT,
                db_execution_attempted=True,
                schema_setup_status="schema_setup_success",
                source_error_path=error_path,
            )
        except Exception:
            return _fail_closed_result(
                row=row,
                execution_dir=execution_dir,
                failure_bucket=FAILURE_SOURCE_EXECUTION_FAILED,
                execution_failure_class="spark_source_execution_failed",
                notes="Spark source SQL execution failed; no PostgreSQL/MySQL fallback was used",
                backend_status=BACKEND_STATUS_AVAILABLE,
                source_status=EXECUTION_STATUS_SOURCE_FAILED,
                db_execution_attempted=True,
                schema_setup_status="schema_setup_success",
                source_error_path=source_error_path,
            )

        try:
            candidate_rows = _run_query_to_jsonl(
                spark=spark,
                sql_path=candidate_query_path,
                result_path=candidate_result,
                error_path=candidate_error_path,
            )
        except TimeoutError as exc:
            error_path = _write_error(candidate_error_path, str(exc))
            _write_environment_metadata(
                execution_dir,
                row=row,
                run_id=run_id,
                status=status,
                spark_sql_executed=True,
                source_result_artifact_created=source_result.exists(),
                candidate_result_artifact_created=False,
                schema_assets=schema_assets,
                row_counts={"source": source_rows},
            )
            return _fail_closed_result(
                row=row,
                execution_dir=execution_dir,
                failure_bucket=FAILURE_EXECUTION_TIMEOUT,
                execution_failure_class="spark_timeout",
                notes="Spark candidate execution timed out",
                backend_status=BACKEND_STATUS_AVAILABLE,
                source_status=EXECUTION_STATUS_SOURCE_SUCCESS,
                candidate_status=EXECUTION_STATUS_TIMEOUT,
                db_execution_attempted=True,
                schema_setup_status="schema_setup_success",
                source_result_path=source_result,
                candidate_error_path=error_path,
            )
        except Exception:
            _write_environment_metadata(
                execution_dir,
                row=row,
                run_id=run_id,
                status=status,
                spark_sql_executed=True,
                source_result_artifact_created=source_result.exists(),
                candidate_result_artifact_created=False,
                schema_assets=schema_assets,
                row_counts={"source": source_rows},
            )
            return _fail_closed_result(
                row=row,
                execution_dir=execution_dir,
                failure_bucket=FAILURE_CANDIDATE_EXECUTION_FAILED,
                execution_failure_class="spark_candidate_execution_failed",
                notes="Spark candidate SQL execution failed; no PostgreSQL/MySQL fallback was used",
                backend_status=BACKEND_STATUS_AVAILABLE,
                source_status=EXECUTION_STATUS_SOURCE_SUCCESS,
                candidate_status=EXECUTION_STATUS_CANDIDATE_FAILED,
                db_execution_attempted=True,
                schema_setup_status="schema_setup_success",
                source_result_path=source_result,
                candidate_error_path=candidate_error_path,
            )

        metadata_path = _write_environment_metadata(
            execution_dir,
            row=row,
            run_id=run_id,
            status=status,
            spark_sql_executed=True,
            source_result_artifact_created=True,
            candidate_result_artifact_created=True,
            schema_assets=schema_assets,
            row_counts={"source": source_rows, "candidate": candidate_rows},
            cleanup_note=cleanup_note,
        )
        return EngineExecutionResult(
            source_execution_status=EXECUTION_STATUS_SOURCE_SUCCESS,
            candidate_execution_status=EXECUTION_STATUS_CANDIDATE_SUCCESS,
            source_result_path=source_result,
            candidate_result_path=candidate_result,
            db_artifact_dir=execution_dir,
            failure_bucket=FAILURE_NONE,
            execution_failure_class="",
            notes=(
                "Spark source and candidate SQL executed locally through PySpark "
                f"using explicit external schema profile {schema_assets.external_profile_path}; "
                f"metadata={metadata_path.name}; no official metrics computed"
            ),
            engine=row.engine,
            case_id=row.case_id,
            pool=row.pool,
            denominator_id=row.denominator_id,
            schema_setup_status="schema_setup_success",
            db_execution_attempted=True,
            source_executable=True,
            candidate_executable=True,
            local_diagnostic_only=True,
            cross_dialect_status=CROSS_DIALECT_STATUS_NOT_APPLICABLE,
            required_backend="spark",
            backend_status=BACKEND_STATUS_AVAILABLE,
        )
    except Exception as exc:
        error_path = _write_error(source_error_path, str(exc))
        _write_environment_metadata(
            execution_dir,
            row=row,
            run_id=run_id,
            status=status,
            spark_sql_executed=spark is not None,
            source_result_artifact_created=source_result.exists(),
            candidate_result_artifact_created=candidate_result.exists(),
            schema_assets=schema_assets,
            row_counts={"source": source_rows, "candidate": candidate_rows},
        )
        return _fail_closed_result(
            row=row,
            execution_dir=execution_dir,
            failure_bucket=FAILURE_INTERNAL_RUNNER_ERROR,
            execution_failure_class="spark_internal_error",
            notes="Spark local diagnostic backend hit an internal error",
            backend_status=BACKEND_STATUS_AVAILABLE,
            source_status=EXECUTION_STATUS_INTERNAL_ERROR,
            candidate_status=EXECUTION_STATUS_NOT_ENABLED,
            db_execution_attempted=True,
            schema_setup_status="internal_error",
            source_error_path=error_path,
        )
    finally:
        if spark is not None:
            try:
                spark.sql(f"DROP DATABASE IF EXISTS {database} CASCADE")
            except Exception as exc:  # pragma: no cover - cleanup note only
                cleanup_note = f"cleanup_failed: {exc}"
            try:
                spark.stop()
            except Exception as exc:  # pragma: no cover - cleanup note only
                cleanup_note = (cleanup_note + "; " if cleanup_note else "") + f"stop_failed: {exc}"
