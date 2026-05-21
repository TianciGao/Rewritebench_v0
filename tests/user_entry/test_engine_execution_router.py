import csv
import shutil
import sys
import tempfile
import unittest
import uuid
from argparse import Namespace
from pathlib import Path
from unittest import mock

from sql_rewrite_bench.case_selection import SelectedCaseEngineRow
from sql_rewrite_bench.engine_execution import execute_engine_case
from sql_rewrite_bench.postgres_execution import PostgresExecutionResult
from sql_rewrite_bench.user_run import run_user_benchmark
from sql_rewrite_bench.user_run_schema import (
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    EXECUTION_STATUS_UNSUPPORTED,
    FAILURE_NONE,
    FAILURE_UNSUPPORTED_ENGINE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _row(engine: str) -> SelectedCaseEngineRow:
    return SelectedCaseEngineRow(
        denominator_id=f"PERF_0006__{engine}",
        case_id="PERF_0006",
        pool="PERF",
        engine=engine,
        planned="true",
        case_path="cases/PERF/PERF_0006",
        source_sql_path="cases/PERF/PERF_0006/sql/source.sql",
    )


def _case_list(tmp_path: Path, *case_ids: str) -> Path:
    path = tmp_path / "case_ids.txt"
    path.write_text("\n".join(case_ids) + "\n", encoding="utf-8")
    return path


def _unique_out(name: str) -> Path:
    return Path("runs/user") / f"{name}_{uuid.uuid4().hex}"


def _args(out: Path, case_list: Path, *, engine: str) -> Namespace:
    adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
    return Namespace(
        case_set="common_core_v0",
        pool="PERF",
        engine=engine,
        case_list=case_list,
        smoke=False,
        adapter_command=f"{sys.executable} {adapter}",
        out=out,
        run_id=None,
        adapter_timeout=30,
        dry_run=False,
        enable_db_execution=True,
        enable_checker=True,
        postgres_dsn_env="SQLRB_POSTGRES_DSN",
        execution_timeout_sec=30,
        db_schema_prefix="sqlrb_user",
    )


class EngineExecutionRouterTests(unittest.TestCase):
    def test_router_dispatches_postgres_to_existing_executor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "runs" / "user" / "router" / "workspaces" / "PERF_0006" / "postgres"
            execution_dir = workspace / "execution"
            source_result = execution_dir / "source_result.jsonl"
            candidate_result = execution_dir / "candidate_result.jsonl"
            candidate_sql = workspace / "candidate.sql"
            candidate_sql.parent.mkdir(parents=True)
            candidate_sql.write_text("select 1;\n", encoding="utf-8")
            pg_result = PostgresExecutionResult(
                source_execution_status=EXECUTION_STATUS_SOURCE_SUCCESS,
                candidate_execution_status=EXECUTION_STATUS_CANDIDATE_SUCCESS,
                source_result_path=source_result,
                candidate_result_path=candidate_result,
                db_artifact_dir=execution_dir,
                failure_bucket=FAILURE_NONE,
                execution_failure_class="",
                notes="postgres ok",
            )
            with mock.patch(
                "sql_rewrite_bench.engine_execution.execute_postgres_case",
                return_value=pg_result,
            ) as execute:
                result = execute_engine_case(
                    repo_root=root,
                    run_id="router",
                    row=_row("postgres"),
                    candidate_sql_path=candidate_sql,
                    workspace_dir=workspace,
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                    postgres_dsn_env="SQLRB_POSTGRES_DSN",
                )

        execute.assert_called_once()
        self.assertEqual(result.engine, "postgres")
        self.assertEqual(result.source_execution_status, EXECUTION_STATUS_SOURCE_SUCCESS)
        self.assertEqual(result.candidate_execution_status, EXECUTION_STATUS_CANDIDATE_SUCCESS)
        self.assertEqual(result.failure_bucket, FAILURE_NONE)
        self.assertTrue(result.db_execution_attempted)

    def test_router_dispatches_mysql_to_fail_closed_stub(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "runs" / "user" / "router" / "workspaces" / "PERF_0006" / "mysql"
            candidate_sql = workspace / "candidate.sql"
            candidate_sql.parent.mkdir(parents=True)
            candidate_sql.write_text("select 1;\n", encoding="utf-8")
            with mock.patch("sql_rewrite_bench.engine_execution.execute_postgres_case") as postgres:
                result = execute_engine_case(
                    repo_root=root,
                    run_id="router",
                    row=_row("mysql"),
                    candidate_sql_path=candidate_sql,
                    workspace_dir=workspace,
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                )

        postgres.assert_not_called()
        self.assertEqual(result.engine, "mysql")
        self.assertEqual(result.source_execution_status, EXECUTION_STATUS_UNSUPPORTED)
        self.assertEqual(result.candidate_execution_status, EXECUTION_STATUS_UNSUPPORTED)
        self.assertEqual(result.failure_bucket, FAILURE_UNSUPPORTED_ENGINE)
        self.assertEqual(
            result.execution_failure_class,
            "mysql_same_engine_execution_not_implemented",
        )
        self.assertIn("no PostgreSQL fallback", result.notes)
        self.assertFalse(result.db_execution_attempted)

    def test_router_dispatches_spark_to_fail_closed_stub(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "runs" / "user" / "router" / "workspaces" / "PERF_0006" / "spark"
            candidate_sql = workspace / "candidate.sql"
            candidate_sql.parent.mkdir(parents=True)
            candidate_sql.write_text("select 1;\n", encoding="utf-8")
            with mock.patch("sql_rewrite_bench.engine_execution.execute_postgres_case") as postgres:
                result = execute_engine_case(
                    repo_root=root,
                    run_id="router",
                    row=_row("spark"),
                    candidate_sql_path=candidate_sql,
                    workspace_dir=workspace,
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                )

        postgres.assert_not_called()
        self.assertEqual(result.engine, "spark")
        self.assertEqual(result.source_execution_status, EXECUTION_STATUS_UNSUPPORTED)
        self.assertEqual(result.candidate_execution_status, EXECUTION_STATUS_UNSUPPORTED)
        self.assertEqual(result.failure_bucket, FAILURE_UNSUPPORTED_ENGINE)
        self.assertEqual(result.execution_failure_class, "spark_execution_not_implemented")
        self.assertIn("no PostgreSQL fallback", result.notes)
        self.assertFalse(result.db_execution_attempted)

    def test_router_fails_closed_for_unknown_engine(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "runs" / "user" / "router" / "workspaces" / "PERF_0006" / "duckdb"
            candidate_sql = workspace / "candidate.sql"
            candidate_sql.parent.mkdir(parents=True)
            candidate_sql.write_text("select 1;\n", encoding="utf-8")
            with mock.patch("sql_rewrite_bench.engine_execution.execute_postgres_case") as postgres:
                result = execute_engine_case(
                    repo_root=root,
                    run_id="router",
                    row=_row("duckdb"),
                    candidate_sql_path=candidate_sql,
                    workspace_dir=workspace,
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                )

        postgres.assert_not_called()
        self.assertEqual(result.engine, "duckdb")
        self.assertEqual(result.failure_bucket, FAILURE_UNSUPPORTED_ENGINE)
        self.assertEqual(result.execution_failure_class, "unsupported_engine")
        self.assertEqual(result.source_execution_status, EXECUTION_STATUS_UNSUPPORTED)

    def test_user_run_mysql_db_execution_fails_closed_without_checker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _unique_out("unittest_u7_mysql_fail_closed")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            summary = run_user_benchmark(_args(out, case_list, engine="mysql"), REPO_ROOT)

        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["source_execution_success_rows"], 0)
        self.assertEqual(summary["candidate_execution_success_rows"], 0)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["engine"], "mysql")
        self.assertEqual(rows[0]["execution_status"], EXECUTION_STATUS_UNSUPPORTED)
        self.assertEqual(rows[0]["failure_bucket"], FAILURE_UNSUPPORTED_ENGINE)
        self.assertEqual(
            rows[0]["execution_failure_class"],
            "mysql_same_engine_execution_not_implemented",
        )
        self.assertFalse((REPO_ROOT / out / "workspaces" / "PERF_0006" / "mysql" / "checker").exists())


if __name__ == "__main__":
    unittest.main()
