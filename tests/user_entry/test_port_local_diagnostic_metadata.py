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

from sql_rewrite_bench.case_package_resolver import resolve_case_package
from sql_rewrite_bench.case_selection import (
    SelectedCaseEngineRow,
    resolve_common_core_selection,
)
from sql_rewrite_bench.engine_execution import execute_engine_case
from sql_rewrite_bench.user_run import run_user_benchmark
from sql_rewrite_bench.user_run_schema import (
    BACKEND_STATUS_CLIENT_MISSING,
    BACKEND_STATUS_CONFIG_MISSING,
    CHECKER_STATUS_NOT_ENABLED,
    CROSS_DIALECT_STATUS_BACKEND_MISSING,
    DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE,
    DIAGNOSTIC_MODE_SAME_ENGINE,
    EXACT_STATUS_EXECUTION_FAILURE,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_BACKEND_MISSING,
    FAILURE_CROSS_DIALECT_BACKEND_MISSING,
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


def _unique_out(name: str) -> Path:
    return Path("runs/user") / f"{name}_{uuid.uuid4().hex}"


def _args(out: Path, case_list: Path) -> Namespace:
    adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
    return Namespace(
        case_set="common_core_v0",
        pool="all",
        engine="postgres",
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


class PortLocalDiagnosticMetadataTests(unittest.TestCase):
    def test_resolver_exposes_port_diagnostic_modes(self) -> None:
        same_engine = resolve_case_package(repo_root=REPO_ROOT, row=_selected_row("PORT_0003"))
        cross_dialect = resolve_case_package(repo_root=REPO_ROOT, row=_selected_row("PORT_0004"))

        self.assertEqual(same_engine.diagnostic_mode, DIAGNOSTIC_MODE_SAME_ENGINE)
        self.assertEqual(same_engine.source_reference_engine, "postgres")
        self.assertEqual(cross_dialect.diagnostic_mode, DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE)
        self.assertEqual(cross_dialect.source_reference_engine, "mysql")
        self.assertEqual(cross_dialect.target_candidate_engine, "postgres")
        self.assertEqual(cross_dialect.source_reference_query_path.name, "source.sql")
        self.assertEqual(cross_dialect.target_reference_query_path.name, "pos_01.sql")
        self.assertEqual(cross_dialect.target_reference_role, "positive_reference")

    def test_resolver_defaults_non_port_cases_to_same_engine(self) -> None:
        for case_id in ("PERF_0006", "CONS_0005", "LONGTAIL_0011"):
            with self.subTest(case_id=case_id):
                resolved = resolve_case_package(
                    repo_root=REPO_ROOT,
                    row=_selected_row(case_id),
                )
                self.assertEqual(resolved.diagnostic_mode, DIAGNOSTIC_MODE_SAME_ENGINE)
                self.assertEqual(resolved.source_reference_engine, "postgres")
                self.assertEqual(resolved.target_candidate_engine, "postgres")

    def test_cross_dialect_router_fails_closed_without_postgres_source_execution(self) -> None:
        row = _selected_row("PORT_0004")
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir) / "workspace"
            candidate_sql = workspace / "candidate.sql"
            candidate_sql.parent.mkdir(parents=True)
            candidate_sql.write_text("select 1;\n", encoding="utf-8")
            with mock.patch(
                "sql_rewrite_bench.engine_execution.execute_postgres_case",
                side_effect=AssertionError("PostgreSQL source execution must not run"),
            ) as postgres:
                with mock.patch(
                    "sql_rewrite_bench.mysql_execution.mysql_client_available",
                    return_value=False,
                ):
                    result = execute_engine_case(
                        repo_root=REPO_ROOT,
                        run_id="port_router_test",
                        row=row,
                        candidate_sql_path=candidate_sql,
                        workspace_dir=workspace,
                        timeout_sec=30,
                        schema_prefix="sqlrb_user",
                        resolved_package=resolved,
                    )

        postgres.assert_not_called()
        self.assertEqual(result.failure_bucket, FAILURE_CROSS_DIALECT_BACKEND_MISSING)
        self.assertEqual(result.source_execution_status, EXECUTION_STATUS_SOURCE_BACKEND_MISSING)
        self.assertEqual(result.candidate_execution_status, EXECUTION_STATUS_NOT_ENABLED)
        self.assertEqual(result.required_backend, "mysql")
        self.assertEqual(result.backend_status, BACKEND_STATUS_CLIENT_MISSING)
        self.assertFalse(result.db_execution_attempted)
        self.assertIn("mysql CLI is not available", result.notes)

    def test_user_run_records_cross_dialect_backend_missing_and_skips_checker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PORT_0004")
            out = _unique_out("unittest_p3_port_cross_dialect")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            with mock.patch(
                "sql_rewrite_bench.mysql_execution.mysql_client_available",
                return_value=True,
            ), mock.patch(
                "sql_rewrite_bench.mysql_execution.mysql_config_available",
                return_value=False,
            ):
                summary = run_user_benchmark(_args(out, case_list), REPO_ROOT)

        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["candidate_generated_rows"], 1)
        self.assertEqual(summary["source_execution_success_rows"], 0)
        self.assertEqual(summary["candidate_execution_success_rows"], 0)

        run_root = REPO_ROOT / out
        with (run_root / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["diagnostic_mode"], DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE)
        self.assertEqual(row["source_reference_engine"], "mysql")
        self.assertEqual(row["target_candidate_engine"], "postgres")
        self.assertEqual(row["cross_dialect_status"], CROSS_DIALECT_STATUS_BACKEND_MISSING)
        self.assertEqual(row["required_backend"], "mysql")
        self.assertEqual(row["backend_status"], BACKEND_STATUS_CONFIG_MISSING)
        self.assertEqual(row["failure_bucket"], FAILURE_CROSS_DIALECT_BACKEND_MISSING)
        self.assertEqual(row["source_execution_status"], EXECUTION_STATUS_SOURCE_BACKEND_MISSING)
        self.assertEqual(row["execution_status"], EXECUTION_STATUS_NOT_ENABLED)
        self.assertEqual(row["checker_status"], CHECKER_STATUS_NOT_ENABLED)
        self.assertEqual(row["exact_status"], EXACT_STATUS_EXECUTION_FAILURE)
        self.assertNotIn("syntax error at or near", row["notes"])
        self.assertFalse((run_root / "workspaces" / "PORT_0004" / "postgres" / "checker").exists())

        quality = json.loads((run_root / "quality_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(
            quality["failure_bucket_counts"][FAILURE_CROSS_DIALECT_BACKEND_MISSING],
            1,
        )
        with (run_root / "tag_slices.csv").open(newline="", encoding="utf-8") as f:
            tag_rows = list(csv.DictReader(f))
        self.assertTrue(tag_rows)


if __name__ == "__main__":
    unittest.main()
