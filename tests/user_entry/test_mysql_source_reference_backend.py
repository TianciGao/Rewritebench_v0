import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from sql_rewrite_bench.case_package_resolver import resolve_case_package
from sql_rewrite_bench.case_selection import (
    SelectedCaseEngineRow,
    resolve_common_core_selection,
)
from sql_rewrite_bench.engine_execution import EngineExecutionResult, execute_engine_case
from sql_rewrite_bench.mysql_execution import (
    execute_mysql_source_reference,
    resolve_mysql_schema_assets,
)
from sql_rewrite_bench.user_run_schema import (
    BACKEND_STATUS_AVAILABLE,
    BACKEND_STATUS_CLIENT_MISSING,
    BACKEND_STATUS_CONFIG_MISSING,
    BACKEND_STATUS_SCHEMA_MISSING,
    CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    FAILURE_CROSS_DIALECT_BACKEND_MISSING,
    FAILURE_NONE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _case_list(tmp_path: Path, *case_ids: str) -> Path:
    path = tmp_path / "case_ids.txt"
    path.write_text("\n".join(case_ids) + "\n", encoding="utf-8")
    return path


def _selected_row(case_id: str, *, engine: str = "postgres") -> SelectedCaseEngineRow:
    with tempfile.TemporaryDirectory() as temp_dir:
        rows = resolve_common_core_selection(
            repo_root=REPO_ROOT,
            case_set="common_core_v0",
            engine=engine,
            case_list=_case_list(Path(temp_dir), case_id),
        )
    if len(rows) != 1:
        raise AssertionError(f"expected one selected row for {case_id}, got {len(rows)}")
    return rows[0]


class MySQLSourceReferenceBackendTests(unittest.TestCase):
    def test_mysql_backend_fails_closed_when_client_missing(self) -> None:
        row = _selected_row("PORT_0004")
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch(
                "sql_rewrite_bench.mysql_execution.mysql_client_available",
                return_value=False,
            ):
                result = execute_mysql_source_reference(
                    repo_root=REPO_ROOT,
                    run_id="mysql_client_missing",
                    row=row,
                    resolved_package=resolved,
                    workspace_dir=Path(temp_dir),
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                )

        self.assertEqual(result.failure_bucket, FAILURE_CROSS_DIALECT_BACKEND_MISSING)
        self.assertEqual(result.execution_failure_class, "mysql_client_missing")
        self.assertEqual(result.source_execution_status, EXECUTION_STATUS_SOURCE_BACKEND_MISSING)
        self.assertEqual(result.candidate_execution_status, EXECUTION_STATUS_NOT_ENABLED)
        self.assertEqual(result.backend_status, BACKEND_STATUS_CLIENT_MISSING)

    def test_mysql_backend_fails_closed_when_config_missing(self) -> None:
        row = _selected_row("PORT_0004")
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch(
                "sql_rewrite_bench.mysql_execution.mysql_client_available",
                return_value=True,
            ), mock.patch(
                "sql_rewrite_bench.mysql_execution.mysql_config_available",
                return_value=False,
            ):
                result = execute_mysql_source_reference(
                    repo_root=REPO_ROOT,
                    run_id="mysql_config_missing",
                    row=row,
                    resolved_package=resolved,
                    workspace_dir=Path(temp_dir),
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                )

        self.assertEqual(result.failure_bucket, FAILURE_CROSS_DIALECT_BACKEND_MISSING)
        self.assertEqual(result.execution_failure_class, "mysql_config_missing")
        self.assertEqual(result.backend_status, BACKEND_STATUS_CONFIG_MISSING)
        self.assertFalse(result.db_execution_attempted)

    def test_mysql_schema_assets_resolve_only_explicit_mysql_paths(self) -> None:
        row = _selected_row("PORT_0004")
        assets = resolve_mysql_schema_assets(repo_root=REPO_ROOT, row=row)

        self.assertIn("/mysql/", assets.ddl_path.as_posix())
        self.assertIn("/mysql/", assets.load_path.as_posix())
        self.assertNotIn("/postgres/", assets.ddl_path.as_posix())
        self.assertNotIn("/postgres/", assets.load_path.as_posix())

    def test_mysql_schema_assets_missing_mysql_entry_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "cases" / "PORT" / "PORT_X"
            profile = root / "schemas" / "profile.yaml"
            (case_dir / "sql").mkdir(parents=True)
            profile.parent.mkdir(parents=True)
            (case_dir / "manifest.yaml").write_text(
                "\n".join(
                    [
                        "case_id: PORT_X",
                        "pool: PORT",
                        "schema:",
                        "  external_profile: schemas/profile.yaml",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            profile.write_text(
                "\n".join(
                    [
                        "engines:",
                        "  postgres:",
                        "    ddl: schemas/postgres/ddl.sql",
                        "    load: schemas/postgres/load.sql",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            row = SelectedCaseEngineRow(
                denominator_id="PORT_X__postgres",
                case_id="PORT_X",
                pool="PORT",
                engine="postgres",
                planned="true",
                case_path="cases/PORT/PORT_X",
                source_sql_path="cases/PORT/PORT_X/sql/source.sql",
            )

            with self.assertRaisesRegex(ValueError, "no mysql engine entry"):
                resolve_mysql_schema_assets(repo_root=root, row=row)

    def test_mysql_backend_writes_source_reference_artifacts_with_mocked_execution(self) -> None:
        row = _selected_row("PORT_0004")
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        completed = [
            subprocess.CompletedProcess(["mysql"], 0, stdout="", stderr=""),
            subprocess.CompletedProcess(["mysql"], 0, stdout="answer\n42\n", stderr=""),
            subprocess.CompletedProcess(["mysql"], 0, stdout="", stderr=""),
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            with mock.patch(
                "sql_rewrite_bench.mysql_execution.mysql_client_available",
                return_value=True,
            ), mock.patch(
                "sql_rewrite_bench.mysql_execution.mysql_config_available",
                return_value=True,
            ), mock.patch(
                "sql_rewrite_bench.mysql_execution._run_mysql_file",
                side_effect=completed,
            ):
                result = execute_mysql_source_reference(
                    repo_root=REPO_ROOT,
                    run_id="mysql_artifact_test",
                    row=row,
                    resolved_package=resolved,
                    workspace_dir=workspace,
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                )

            self.assertEqual(result.failure_bucket, FAILURE_NONE)
            self.assertEqual(result.source_execution_status, EXECUTION_STATUS_SOURCE_SUCCESS)
            self.assertEqual(result.backend_status, BACKEND_STATUS_AVAILABLE)
            self.assertTrue((result.db_artifact_dir / "setup.sql").exists())
            self.assertTrue((result.db_artifact_dir / "source_query.sql").exists())
            self.assertTrue((result.db_artifact_dir / "command_metadata.json").exists())
            self.assertIsNotNone(result.source_result_path)
            rows = [
                json.loads(line)
                for line in result.source_result_path.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(rows, [{"answer": "42"}])

    def test_cross_dialect_router_uses_mysql_source_then_postgres_target_candidate(self) -> None:
        row = _selected_row("PORT_0004")
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir) / "workspace"
            candidate_sql = workspace / "candidate.sql"
            source_result = workspace / "execution" / "mysql_source" / "source_result.jsonl"
            candidate_result = workspace / "execution" / "postgres_target" / "candidate_result.jsonl"
            candidate_sql.parent.mkdir(parents=True)
            source_result.parent.mkdir(parents=True)
            candidate_result.parent.mkdir(parents=True)
            candidate_sql.write_text("select 1;\n", encoding="utf-8")
            mysql_result = EngineExecutionResult(
                source_execution_status=EXECUTION_STATUS_SOURCE_SUCCESS,
                candidate_execution_status=EXECUTION_STATUS_NOT_ENABLED,
                source_result_path=source_result,
                candidate_result_path=None,
                db_artifact_dir=source_result.parent,
                failure_bucket=FAILURE_NONE,
                execution_failure_class="",
                notes="mysql source ok",
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
            target_result = EngineExecutionResult(
                source_execution_status=EXECUTION_STATUS_SOURCE_SUCCESS,
                candidate_execution_status=EXECUTION_STATUS_CANDIDATE_SUCCESS,
                source_result_path=source_result,
                candidate_result_path=candidate_result,
                db_artifact_dir=workspace / "execution",
                failure_bucket=FAILURE_NONE,
                execution_failure_class="",
                notes="target candidate ok; target_reference was not used as a checker oracle",
                engine=row.engine,
                case_id=row.case_id,
                pool=row.pool,
                denominator_id=row.denominator_id,
                schema_setup_status="target_schema_setup_success",
                db_execution_attempted=True,
                source_executable=True,
                candidate_executable=True,
                cross_dialect_status=CROSS_DIALECT_STATUS_SOURCE_REFERENCE_EXECUTED,
                required_backend="mysql",
                backend_status=BACKEND_STATUS_AVAILABLE,
            )
            with mock.patch(
                "sql_rewrite_bench.engine_execution.execute_postgres_case",
                side_effect=AssertionError("PostgreSQL source execution must not run"),
            ) as postgres, mock.patch(
                "sql_rewrite_bench.mysql_execution.execute_mysql_source_reference",
                return_value=mysql_result,
            ) as mysql_source, mock.patch(
                "sql_rewrite_bench.engine_execution._execute_postgres_target_candidate",
                return_value=target_result,
            ) as target_candidate:
                result = execute_engine_case(
                    repo_root=REPO_ROOT,
                    run_id="cross_dialect_success",
                    row=row,
                    candidate_sql_path=candidate_sql,
                    workspace_dir=workspace,
                    timeout_sec=30,
                    schema_prefix="sqlrb_user",
                    resolved_package=resolved,
                )

        postgres.assert_not_called()
        mysql_source.assert_called_once()
        target_candidate.assert_called_once()
        self.assertEqual(result.failure_bucket, FAILURE_NONE)
        self.assertEqual(result.candidate_execution_status, EXECUTION_STATUS_CANDIDATE_SUCCESS)


if __name__ == "__main__":
    unittest.main()
