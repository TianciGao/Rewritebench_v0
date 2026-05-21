"""Fail-closed Spark SQL execution stub for local user-entry diagnostics."""

from __future__ import annotations

from pathlib import Path

from .case_selection import SelectedCaseEngineRow
from .engine_execution import EngineExecutionResult, unsupported_engine_result


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

    Arguments are accepted to match the future executor interface. They are not
    used to start Spark, execute SQL, compute metrics, or fall back to
    PostgreSQL.
    """

    _ = (repo_root, run_id, candidate_sql_path, timeout_sec, schema_prefix)
    return unsupported_engine_result(
        row=row,
        workspace_dir=workspace_dir,
        execution_failure_class="spark_execution_not_implemented",
        notes=(
            "spark execution is not implemented for user-entry local diagnostics; "
            "no SQL was executed and no PostgreSQL fallback was used"
        ),
    )
