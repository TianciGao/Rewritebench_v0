import csv
import json
import shutil
import sys
import tempfile
import unittest
import uuid
from argparse import Namespace
from pathlib import Path
from unittest import mock

from sql_rewrite_bench.case_selection import SelectedCaseEngineRow
from sql_rewrite_bench.engine_execution import EngineExecutionResult, execute_engine_case
from sql_rewrite_bench.postgres_execution import PostgresExecutionResult
from sql_rewrite_bench.spark_execution import (
    SparkEnvironmentStatus,
    execute_spark_case,
    inspect_spark_environment,
)
from sql_rewrite_bench.local_result_checker import run_local_checker
from sql_rewrite_bench.user_run import run_user_benchmark
from sql_rewrite_bench.user_run_schema import (
    BACKEND_STATUS_AVAILABLE,
    BACKEND_STATUS_CLIENT_MISSING,
    BACKEND_STATUS_CONFIG_MISSING,
    BACKEND_STATUS_SCHEMA_MISSING,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_CANDIDATE_FAILED,
    EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    EXECUTION_STATUS_SOURCE_FAILED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    EXECUTION_STATUS_UNSUPPORTED,
    FAILURE_CANDIDATE_EXECUTION_FAILED,
    FAILURE_NONE,
    FAILURE_SOURCE_EXECUTION_FAILED,
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


def _spark_available_status() -> SparkEnvironmentStatus:
    return SparkEnvironmentStatus(
        spark_local_ip_set=True,
        spark_home_set=False,
        pyspark_python_set=False,
        spark_sql_path="",
        pyspark_importable=True,
        environment_configured=True,
        client_available=True,
        backend_status=BACKEND_STATUS_AVAILABLE,
        failure_class="",
    )


class _FakeRow:
    def __init__(self, values: list[object]) -> None:
        self._values = values

    def __getitem__(self, index: int) -> object:
        return self._values[index]


class _FakeDataFrame:
    columns = ["answer", "amount"]

    def collect(self) -> list[_FakeRow]:
        return [_FakeRow([1, "1.00"])]


class _FakeSpark:
    def __init__(self, *, fail_on_source: bool = False, fail_on_candidate: bool = False) -> None:
        self.statements: list[str] = []
        self.query_count = 0
        self.fail_on_source = fail_on_source
        self.fail_on_candidate = fail_on_candidate
        self.stopped = False

    def sql(self, statement: str) -> _FakeDataFrame | None:
        self.statements.append(statement)
        if statement.strip().lower().startswith("select"):
            self.query_count += 1
            if self.fail_on_source and self.query_count == 1:
                raise RuntimeError("source failed")
            if self.fail_on_candidate and self.query_count == 2:
                raise RuntimeError("candidate failed")
            return _FakeDataFrame()
        return None

    def stop(self) -> None:
        self.stopped = True


def _write_minimal_spark_case(root: Path) -> tuple[SelectedCaseEngineRow, Path, Path]:
    case_dir = root / "cases" / "PERF" / "PERF_0006"
    schema_dir = root / "schemas" / "minimal_spark_v0" / "spark"
    checker_dir = case_dir / "checker"
    (case_dir / "sql").mkdir(parents=True)
    schema_dir.mkdir(parents=True)
    checker_dir.mkdir(parents=True)
    (case_dir / "manifest.yaml").write_text(
        "\n".join(
            [
                "case_id: PERF_0006",
                "pool: PERF",
                "schema:",
                "  external_profile: schemas/minimal_spark_v0/schema_profile.yaml",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / "schemas" / "minimal_spark_v0" / "schema_profile.yaml").write_text(
        "\n".join(
            [
                "schema_id: minimal_spark_v0",
                "engines:",
                "  spark:",
                "    ddl: schemas/minimal_spark_v0/spark/ddl.sql",
                "    load: schemas/minimal_spark_v0/spark/load.sql",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (schema_dir / "ddl.sql").write_text("CREATE TABLE numbers (answer INT, amount STRING);\n", encoding="utf-8")
    (schema_dir / "load.sql").write_text("INSERT INTO numbers VALUES (1, '1.00');\n", encoding="utf-8")
    (case_dir / "sql" / "source.sql").write_text("SELECT answer, amount FROM numbers;\n", encoding="utf-8")
    (checker_dir / "checker.yaml").write_text("case_id: PERF_0006\n", encoding="utf-8")
    (checker_dir / "normalization.yaml").write_text(
        "case_id: PERF_0006\nsort_rows: true\n", encoding="utf-8"
    )
    (checker_dir / "compare_config.yaml").write_text("case_id: PERF_0006\n", encoding="utf-8")
    row = SelectedCaseEngineRow(
        denominator_id="PERF_0006__spark",
        case_id="PERF_0006",
        pool="PERF",
        engine="spark",
        planned="true",
        case_path="cases/PERF/PERF_0006",
        source_sql_path="cases/PERF/PERF_0006/sql/source.sql",
    )
    workspace = root / "runs" / "user" / "spark" / "workspaces" / "PERF_0006" / "spark"
    candidate = workspace / "candidate.sql"
    candidate.parent.mkdir(parents=True)
    candidate.write_text("SELECT answer, amount FROM numbers;\n", encoding="utf-8")
    return row, workspace, candidate


class EngineExecutionRouterTests(unittest.TestCase):
    def test_spark_environment_detector_reports_missing_config(self) -> None:
        status = inspect_spark_environment(
            {},
            spark_sql_path="",
            pyspark_importable=False,
        )

        self.assertFalse(status.environment_configured)
        self.assertFalse(status.client_available)
        self.assertEqual(status.backend_status, BACKEND_STATUS_CONFIG_MISSING)
        self.assertEqual(status.failure_class, "spark_config_missing")
        self.assertEqual(status.implementation_status, "spark_live_backend_v0")

    def test_spark_environment_detector_reports_missing_client(self) -> None:
        status = inspect_spark_environment(
            {"SPARK_LOCAL_IP": "127.0.0.1"},
            spark_sql_path="",
            pyspark_importable=False,
        )

        self.assertTrue(status.environment_configured)
        self.assertFalse(status.client_available)
        self.assertEqual(status.backend_status, BACKEND_STATUS_CLIENT_MISSING)
        self.assertEqual(status.failure_class, "spark_pyspark_missing")

    def test_spark_environment_detector_reports_missing_pyspark_when_only_cli_visible(self) -> None:
        status = inspect_spark_environment(
            {"SPARK_LOCAL_IP": "127.0.0.1"},
            spark_sql_path="/usr/bin/spark-sql",
            pyspark_importable=False,
        )

        self.assertTrue(status.environment_configured)
        self.assertFalse(status.client_available)
        self.assertEqual(status.backend_status, BACKEND_STATUS_CLIENT_MISSING)
        self.assertEqual(status.failure_class, "spark_pyspark_missing")

    def test_spark_environment_detector_reports_available_when_pyspark_visible(self) -> None:
        status = inspect_spark_environment(
            {},
            spark_sql_path="",
            pyspark_importable=True,
        )

        self.assertTrue(status.environment_configured)
        self.assertTrue(status.client_available)
        self.assertEqual(status.backend_status, BACKEND_STATUS_AVAILABLE)
        self.assertEqual(status.failure_class, "")

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

    def test_router_dispatches_mysql_to_same_engine_executor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "runs" / "user" / "router" / "workspaces" / "PERF_0006" / "mysql"
            execution_dir = workspace / "execution" / "mysql_same_engine"
            candidate_sql = workspace / "candidate.sql"
            candidate_sql.parent.mkdir(parents=True)
            candidate_sql.write_text("select 1;\n", encoding="utf-8")
            mysql_result = EngineExecutionResult(
                source_execution_status=EXECUTION_STATUS_SOURCE_SUCCESS,
                candidate_execution_status=EXECUTION_STATUS_CANDIDATE_SUCCESS,
                source_result_path=execution_dir / "source_result.jsonl",
                candidate_result_path=execution_dir / "candidate_result.jsonl",
                db_artifact_dir=execution_dir,
                failure_bucket=FAILURE_NONE,
                execution_failure_class="",
                notes="mysql ok",
                engine="mysql",
                case_id="PERF_0006",
                pool="PERF",
                denominator_id="PERF_0006__mysql",
                schema_setup_status="schema_setup_success",
                db_execution_attempted=True,
                source_executable=True,
                candidate_executable=True,
                required_backend="mysql",
                backend_status="available",
            )
            with mock.patch("sql_rewrite_bench.engine_execution.execute_postgres_case") as postgres, mock.patch(
                "sql_rewrite_bench.mysql_execution.execute_mysql_case",
                return_value=mysql_result,
            ) as mysql_case:
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
        mysql_case.assert_called_once()
        self.assertEqual(result.engine, "mysql")
        self.assertEqual(result.source_execution_status, EXECUTION_STATUS_SOURCE_SUCCESS)
        self.assertEqual(result.candidate_execution_status, EXECUTION_STATUS_CANDIDATE_SUCCESS)
        self.assertEqual(result.failure_bucket, FAILURE_NONE)
        self.assertTrue(result.db_execution_attempted)

    def test_router_dispatches_spark_to_fail_closed_backend_when_pyspark_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "runs" / "user" / "router" / "workspaces" / "PERF_0006" / "spark"
            candidate_sql = workspace / "candidate.sql"
            candidate_sql.parent.mkdir(parents=True)
            candidate_sql.write_text("select 1;\n", encoding="utf-8")
            spark_status = SparkEnvironmentStatus(
                spark_local_ip_set=True,
                spark_home_set=False,
                pyspark_python_set=False,
                spark_sql_path="/usr/bin/spark-sql",
                pyspark_importable=False,
                environment_configured=True,
                client_available=False,
                backend_status=BACKEND_STATUS_CLIENT_MISSING,
                failure_class="spark_pyspark_missing",
            )
            with mock.patch(
                "sql_rewrite_bench.engine_execution.execute_postgres_case"
            ) as postgres, mock.patch(
                "sql_rewrite_bench.mysql_execution.execute_mysql_case"
            ) as mysql_case, mock.patch(
                "sql_rewrite_bench.spark_execution.inspect_spark_environment",
                return_value=spark_status,
            ):
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
            mysql_case.assert_not_called()
            self.assertEqual(result.engine, "spark")
            self.assertEqual(result.source_execution_status, EXECUTION_STATUS_UNSUPPORTED)
            self.assertEqual(result.candidate_execution_status, EXECUTION_STATUS_UNSUPPORTED)
            self.assertEqual(result.failure_bucket, FAILURE_UNSUPPORTED_ENGINE)
            self.assertEqual(result.execution_failure_class, "spark_pyspark_missing")
            self.assertEqual(result.required_backend, "spark")
            self.assertEqual(result.backend_status, BACKEND_STATUS_CLIENT_MISSING)
            self.assertIn("no PostgreSQL/MySQL fallback", result.notes)
            self.assertFalse(result.db_execution_attempted)
            self.assertIsNone(result.source_result_path)
            self.assertIsNone(result.candidate_result_path)
            self.assertFalse((result.db_artifact_dir / "source_result.jsonl").exists())
            self.assertFalse((result.db_artifact_dir / "candidate_result.jsonl").exists())
            metadata = result.db_artifact_dir / "spark_environment_status.json"
            self.assertTrue(metadata.exists())
            payload = json.loads(metadata.read_text(encoding="utf-8"))
            self.assertTrue(payload["spark_live_execution_implemented"])
            self.assertFalse(payload["spark_sql_executed"])

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

    def test_user_run_mysql_db_execution_uses_same_engine_result_without_checker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _unique_out("unittest_u7_mysql_same_engine")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            execution_dir = REPO_ROOT / out / "workspaces" / "PERF_0006" / "mysql" / "execution" / "mysql_same_engine"
            source_result = execution_dir / "source_result.jsonl"
            candidate_result = execution_dir / "candidate_result.jsonl"
            execution_dir.mkdir(parents=True, exist_ok=True)
            source_result.write_text('{"answer": "42"}\n', encoding="utf-8")
            candidate_result.write_text('{"answer": "42"}\n', encoding="utf-8")
            mysql_result = EngineExecutionResult(
                source_execution_status=EXECUTION_STATUS_SOURCE_SUCCESS,
                candidate_execution_status=EXECUTION_STATUS_CANDIDATE_SUCCESS,
                source_result_path=source_result,
                candidate_result_path=candidate_result,
                db_artifact_dir=execution_dir,
                failure_bucket=FAILURE_NONE,
                execution_failure_class="",
                notes="mysql ok",
                engine="mysql",
                case_id="PERF_0006",
                pool="PERF",
                denominator_id="PERF_0006__mysql",
                schema_setup_status="schema_setup_success",
                db_execution_attempted=True,
                source_executable=True,
                candidate_executable=True,
                required_backend="mysql",
                backend_status="available",
            )
            with mock.patch(
                "sql_rewrite_bench.user_run.execute_engine_case",
                return_value=mysql_result,
            ):
                summary = run_user_benchmark(_args(out, case_list, engine="mysql"), REPO_ROOT)

        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["source_execution_success_rows"], 1)
        self.assertEqual(summary["candidate_execution_success_rows"], 1)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["engine"], "mysql")
        self.assertEqual(rows[0]["source_reference_engine"], "mysql")
        self.assertEqual(rows[0]["target_candidate_engine"], "mysql")
        self.assertEqual(rows[0]["execution_status"], EXECUTION_STATUS_CANDIDATE_SUCCESS)
        self.assertEqual(rows[0]["failure_bucket"], FAILURE_NONE)
        self.assertEqual(rows[0]["backend_status"], "available")
        self.assertTrue((REPO_ROOT / out / "workspaces" / "PERF_0006" / "mysql" / "checker").exists())

    def test_user_run_spark_db_execution_fails_closed_without_result_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _unique_out("unittest_u8_spark_fail_closed")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            spark_status = SparkEnvironmentStatus(
                spark_local_ip_set=False,
                spark_home_set=False,
                pyspark_python_set=False,
                spark_sql_path="",
                pyspark_importable=False,
                environment_configured=False,
                client_available=False,
                backend_status=BACKEND_STATUS_CONFIG_MISSING,
                failure_class="spark_config_missing",
            )
            with mock.patch(
                "sql_rewrite_bench.spark_execution.inspect_spark_environment",
                return_value=spark_status,
            ):
                summary = run_user_benchmark(_args(out, case_list, engine="spark"), REPO_ROOT)

        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["candidate_generated_rows"], 1)
        self.assertEqual(summary["source_execution_success_rows"], 0)
        self.assertEqual(summary["candidate_execution_success_rows"], 0)
        out_dir = REPO_ROOT / out
        with (out_dir / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["engine"], "spark")
        self.assertEqual(rows[0]["failure_bucket"], FAILURE_UNSUPPORTED_ENGINE)
        self.assertEqual(rows[0]["execution_failure_class"], "spark_config_missing")
        self.assertEqual(rows[0]["backend_status"], BACKEND_STATUS_CONFIG_MISSING)
        self.assertEqual(rows[0]["required_backend"], "spark")
        self.assertEqual(rows[0]["checker_status"], "checker_not_enabled")
        self.assertEqual(rows[0]["exact_status"], "not_exact_due_to_execution_failure")
        execution_dir = out_dir / "workspaces" / "PERF_0006" / "spark" / "execution"
        self.assertTrue((execution_dir / "spark_environment_status.json").exists())
        self.assertFalse((execution_dir / "source_result.jsonl").exists())
        self.assertFalse((execution_dir / "candidate_result.jsonl").exists())
        self.assertFalse((out_dir / "workspaces" / "PERF_0006" / "spark" / "checker").exists())
        for name in ["quality_summary.json", "quality_report.md", "tag_slices.csv"]:
            self.assertTrue((out_dir / name).exists())

    def test_spark_backend_writes_artifacts_under_mocked_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row, workspace, candidate = _write_minimal_spark_case(root)
            fake_spark = _FakeSpark()
            with mock.patch(
                "sql_rewrite_bench.spark_execution.inspect_spark_environment",
                return_value=_spark_available_status(),
            ), mock.patch(
                "sql_rewrite_bench.spark_execution._create_spark_session",
                return_value=fake_spark,
            ):
                result = execute_spark_case(
                    repo_root=root,
                    run_id="spark_success",
                    row=row,
                    candidate_sql_path=candidate,
                    workspace_dir=workspace,
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                )

            self.assertEqual(result.source_execution_status, EXECUTION_STATUS_SOURCE_SUCCESS)
            self.assertEqual(result.candidate_execution_status, EXECUTION_STATUS_CANDIDATE_SUCCESS)
            self.assertEqual(result.failure_bucket, FAILURE_NONE)
            self.assertEqual(result.required_backend, "spark")
            self.assertEqual(result.backend_status, BACKEND_STATUS_AVAILABLE)
            self.assertTrue(result.source_result_path and result.source_result_path.exists())
            self.assertTrue(result.candidate_result_path and result.candidate_result_path.exists())
            payload = json.loads(result.source_result_path.read_text(encoding="utf-8").strip())
            self.assertEqual(payload, {"answer": 1, "amount": "1.00"})
            metadata = result.db_artifact_dir / "spark_execution_metadata.json"
            self.assertTrue(metadata.exists())
            self.assertIn("DROP DATABASE", fake_spark.statements[-1])

            checker = run_local_checker(
                case_dir=root / row.case_path,
                source_result_path=result.source_result_path,
                candidate_result_path=result.candidate_result_path,
                checker_dir=workspace / "checker",
            )
            self.assertEqual(checker.failure_bucket, FAILURE_NONE)

    def test_spark_backend_fails_closed_when_schema_assets_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row, workspace, candidate = _write_minimal_spark_case(root)
            (root / "schemas" / "minimal_spark_v0" / "schema_profile.yaml").write_text(
                "schema_id: minimal_spark_v0\nengines:\n  postgres: {}\n",
                encoding="utf-8",
            )
            with mock.patch(
                "sql_rewrite_bench.spark_execution.inspect_spark_environment",
                return_value=_spark_available_status(),
            ), mock.patch("sql_rewrite_bench.spark_execution._create_spark_session") as create:
                result = execute_spark_case(
                    repo_root=root,
                    run_id="spark_schema_missing",
                    row=row,
                    candidate_sql_path=candidate,
                    workspace_dir=workspace,
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                )

            create.assert_not_called()
            self.assertEqual(result.execution_failure_class, "spark_schema_missing")
            self.assertEqual(result.backend_status, BACKEND_STATUS_SCHEMA_MISSING)
            self.assertEqual(result.failure_bucket, FAILURE_SOURCE_EXECUTION_FAILED)
            self.assertEqual(result.source_execution_status, EXECUTION_STATUS_SOURCE_BACKEND_MISSING)
            self.assertIsNone(result.source_result_path)
            self.assertFalse((result.db_artifact_dir / "source_result.jsonl").exists())

    def test_spark_backend_separates_source_and_candidate_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row, workspace, candidate = _write_minimal_spark_case(root)
            with mock.patch(
                "sql_rewrite_bench.spark_execution.inspect_spark_environment",
                return_value=_spark_available_status(),
            ), mock.patch(
                "sql_rewrite_bench.spark_execution._create_spark_session",
                return_value=_FakeSpark(fail_on_source=True),
            ):
                source_failed = execute_spark_case(
                    repo_root=root,
                    run_id="spark_source_failure",
                    row=row,
                    candidate_sql_path=candidate,
                    workspace_dir=workspace,
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                )

            self.assertEqual(source_failed.execution_failure_class, "spark_source_execution_failed")
            self.assertEqual(source_failed.source_execution_status, EXECUTION_STATUS_SOURCE_FAILED)
            self.assertEqual(source_failed.failure_bucket, FAILURE_SOURCE_EXECUTION_FAILED)
            self.assertIsNone(source_failed.source_result_path)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row, workspace, candidate = _write_minimal_spark_case(root)
            with mock.patch(
                "sql_rewrite_bench.spark_execution.inspect_spark_environment",
                return_value=_spark_available_status(),
            ), mock.patch(
                "sql_rewrite_bench.spark_execution._create_spark_session",
                return_value=_FakeSpark(fail_on_candidate=True),
            ):
                candidate_failed = execute_spark_case(
                    repo_root=root,
                    run_id="spark_candidate_failure",
                    row=row,
                    candidate_sql_path=candidate,
                    workspace_dir=workspace,
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                )

            self.assertEqual(candidate_failed.execution_failure_class, "spark_candidate_execution_failed")
            self.assertEqual(candidate_failed.source_execution_status, EXECUTION_STATUS_SOURCE_SUCCESS)
            self.assertEqual(
                candidate_failed.candidate_execution_status,
                EXECUTION_STATUS_CANDIDATE_FAILED,
            )
            self.assertEqual(candidate_failed.failure_bucket, FAILURE_CANDIDATE_EXECUTION_FAILED)
            self.assertTrue(
                candidate_failed.source_result_path
                and candidate_failed.source_result_path.exists()
            )
            self.assertIsNone(candidate_failed.candidate_result_path)


if __name__ == "__main__":
    unittest.main()
