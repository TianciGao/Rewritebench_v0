"""Fail-closed Spark SQL execution skeleton for local user-entry diagnostics.

This module intentionally does not start Spark, load schemas, execute SQL, or
export result rows. It only detects local Spark-environment signals and returns
structured local diagnostic statuses so Spark rows fail closed explicitly.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path

from .case_selection import SelectedCaseEngineRow
from .engine_execution import EngineExecutionResult
from .user_run_schema import (
    BACKEND_STATUS_CLIENT_MISSING,
    BACKEND_STATUS_CONFIG_MISSING,
    BACKEND_STATUS_NOT_IMPLEMENTED,
    EXECUTION_STATUS_UNSUPPORTED,
    FAILURE_UNSUPPORTED_ENGINE,
)


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
    implementation_status: str = "spark_execution_not_implemented"

    @property
    def summary(self) -> str:
        client_parts = []
        if self.spark_sql_path:
            client_parts.append("spark-sql")
        if self.pyspark_importable:
            client_parts.append("pyspark")
        clients = "+".join(client_parts) if client_parts else "no_client"
        configured = "configured" if self.environment_configured else "not_configured"
        return f"{configured}; {clients}; {self.implementation_status}"


def inspect_spark_environment(
    env: Mapping[str, str] | None = None,
    *,
    spark_sql_path: str | None = None,
    pyspark_importable: bool | None = None,
) -> SparkEnvironmentStatus:
    """Inspect lightweight Spark environment signals without importing Spark.

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

    environment_configured = any(
        (spark_local_ip_set, spark_home_set, pyspark_python_set)
    )
    client_available = bool(resolved_spark_sql) or bool(resolved_pyspark)
    if not environment_configured and not client_available:
        backend_status = BACKEND_STATUS_CONFIG_MISSING
        failure_class = "spark_not_configured"
    elif not client_available:
        backend_status = BACKEND_STATUS_CLIENT_MISSING
        failure_class = "spark_client_missing"
    else:
        backend_status = BACKEND_STATUS_NOT_IMPLEMENTED
        failure_class = "spark_execution_not_implemented"

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


def _write_environment_metadata(
    execution_dir: Path,
    *,
    row: SelectedCaseEngineRow,
    run_id: str,
    status: SparkEnvironmentStatus,
) -> Path:
    execution_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = execution_dir / "spark_environment_status.json"
    payload = {
        "run_id": run_id,
        "case_id": row.case_id,
        "engine": row.engine,
        "local_diagnostic_only": True,
        "spark_live_execution_implemented": False,
        "spark_sql_executed": False,
        "source_result_artifact_created": False,
        "candidate_result_artifact_created": False,
        "environment": asdict(status),
    }
    metadata_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata_path


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
    """Return an explicit fail-closed result without running Spark SQL.

    Arguments are accepted to match the future executor interface. They are
    not used to start Spark, execute SQL, compute metrics, or fall back to
    PostgreSQL/MySQL.
    """

    _ = (repo_root, candidate_sql_path, timeout_sec, schema_prefix)
    execution_dir = workspace_dir / "execution"
    status = inspect_spark_environment()
    metadata_path = _write_environment_metadata(
        execution_dir,
        row=row,
        run_id=run_id,
        status=status,
    )
    return EngineExecutionResult(
        source_execution_status=EXECUTION_STATUS_UNSUPPORTED,
        candidate_execution_status=EXECUTION_STATUS_UNSUPPORTED,
        source_result_path=None,
        candidate_result_path=None,
        db_artifact_dir=execution_dir,
        failure_bucket=FAILURE_UNSUPPORTED_ENGINE,
        execution_failure_class=status.failure_class,
        notes=(
            "spark execution backend is fail-closed and live Spark SQL execution "
            "is not implemented; no Spark session was started, no SQL was "
            "executed, and no PostgreSQL/MySQL fallback was used; "
            f"environment_status={status.summary}; metadata={metadata_path.name}"
        ),
        engine=row.engine,
        case_id=row.case_id,
        pool=row.pool,
        denominator_id=row.denominator_id,
        schema_setup_status="not_attempted_spark_execution_not_implemented",
        db_execution_attempted=False,
        source_executable=False,
        candidate_executable=False,
        local_diagnostic_only=True,
        required_backend="spark",
        backend_status=status.backend_status,
    )
