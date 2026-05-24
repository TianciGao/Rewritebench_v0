import csv
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from argparse import Namespace
from pathlib import Path

from sql_rewrite_bench.user_run import run_user_benchmark


REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTER = REPO_ROOT / "baselines" / "sqlglot" / "sqlglot_user_adapter.py"
SQLGLOT_AVAILABLE = importlib.util.find_spec("sqlglot") is not None


def _load_adapter_module():
    spec = importlib.util.spec_from_file_location("sqlglot_user_adapter", ADAPTER)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load SQLGlot adapter module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pythonpath_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    return env


def _case_list(tmp_path: Path, *case_ids: str) -> Path:
    path = tmp_path / "case_ids.txt"
    path.write_text("\n".join(case_ids) + "\n", encoding="utf-8")
    return path


def _out(name: str) -> Path:
    return Path("runs/user") / f"{name}_{uuid.uuid4().hex}"


def _user_args(out: Path, case_list: Path, route: str, *, dry_run: bool = False) -> Namespace:
    return Namespace(
        case_set="common_core_v0",
        pool="PERF",
        engine="postgres",
        case_list=case_list,
        adapter_command=f"{sys.executable} {ADAPTER} --route {route}",
        out=out,
        run_id=None,
        adapter_timeout=30,
        dry_run=dry_run,
    )


def _adapter_env(temp_dir: Path) -> dict[str, str]:
    source_path = temp_dir / "source.sql"
    source_path.write_text("select 1 as value\n", encoding="utf-8")
    workspace = temp_dir / "workspace"
    return {
        **_pythonpath_env(),
        "SQLRB_RUN_ID": "test_run",
        "SQLRB_CASE_ID": "PERF_TEST",
        "SQLRB_POOL": "PERF",
        "SQLRB_ENGINE": "postgres",
        "SQLRB_SOURCE_SQL_PATH": str(source_path),
        "SQLRB_CASE_DIR": str(temp_dir),
        "SQLRB_WORKSPACE_DIR": str(workspace),
        "SQLRB_CANDIDATE_SQL_PATH": str(workspace / "candidate.sql"),
    }


class SqlglotAdapterTests(unittest.TestCase):
    def test_adapter_help_works(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ADAPTER), "--help"],
            cwd=REPO_ROOT,
            env=_pythonpath_env(),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--route", completed.stdout)
        self.assertIn("noop", completed.stdout)
        self.assertIn("optimize", completed.stdout)
        self.assertIn("optimize_schema_aware", completed.stdout)

    def test_adapter_refuses_missing_environment_variables(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ADAPTER), "--route", "noop"],
            cwd=REPO_ROOT,
            env={"PYTHONPATH": str(REPO_ROOT / "src")},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("missing required environment variables", completed.stderr)

    def test_adapter_route_validation_works(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ADAPTER), "--route", "invalid"],
            cwd=REPO_ROOT,
            env=_pythonpath_env(),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("invalid choice", completed.stderr)

    def test_schema_aware_route_is_separately_named(self) -> None:
        module = _load_adapter_module()

        self.assertEqual(module.ROUTE_IDS["optimize"], "sqlglot_optimize")
        self.assertEqual(
            module.ROUTE_IDS["optimize_schema_aware"],
            "sqlglot_optimize_schema_aware",
        )
        self.assertEqual(module.parse_args(["--route", "optimize"]).route, "optimize")
        self.assertEqual(
            module.parse_args(["--route", "optimize_schema_aware"]).route,
            "optimize_schema_aware",
        )

    def test_mysql_array_any_detection_is_mysql_schema_aware_scoped(self) -> None:
        module = _load_adapter_module()
        candidate = "SELECT * FROM t WHERE ARRAY_ANY(x, `_x` -> y = `_x`);\n"

        self.assertEqual(
            module.unsupported_mysql_schema_aware_output_bucket(
                route="optimize_schema_aware",
                dialect="mysql",
                candidate_sql=candidate,
            ),
            "mysql_unsupported_array_any",
        )
        self.assertIsNone(
            module.unsupported_mysql_schema_aware_output_bucket(
                route="optimize_schema_aware",
                dialect="postgres",
                candidate_sql=candidate,
            )
        )
        self.assertIsNone(
            module.unsupported_mysql_schema_aware_output_bucket(
                route="optimize_schema_aware",
                dialect="spark",
                candidate_sql=candidate,
            )
        )
        self.assertIsNone(
            module.unsupported_mysql_schema_aware_output_bucket(
                route="optimize",
                dialect="mysql",
                candidate_sql=candidate,
            )
        )

    def test_mysql_lambda_detection_without_array_any_has_explicit_bucket(self) -> None:
        module = _load_adapter_module()

        self.assertEqual(
            module.unsupported_mysql_schema_aware_output_bucket(
                route="optimize_schema_aware",
                dialect="mysql",
                candidate_sql="SELECT FILTER(xs, `_x` -> `_x` > 0) FROM t;\n",
            ),
            "sqlglot_unsupported_mysql_lambda",
        )

    def test_schema_context_parses_simple_engine_ddl(self) -> None:
        module = _load_adapter_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            ddl_path = Path(temp_dir) / "ddl.sql"
            ddl_path.write_text(
                "CREATE TABLE table1 (i INTEGER, j INTEGER);\n"
                "CREATE TABLE table2 (i INT, j INT);\n",
                encoding="utf-8",
            )
            schema = module.schema_context_from_ddl(ddl_path)

        self.assertEqual(schema["table1"], {"i": "INTEGER", "j": "INTEGER"})
        self.assertEqual(schema["table2"], {"i": "INT", "j": "INT"})

    def test_schema_aware_route_fails_closed_without_schema_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            completed = subprocess.run(
                [sys.executable, str(ADAPTER), "--route", "optimize_schema_aware"],
                cwd=REPO_ROOT,
                env=_adapter_env(Path(temp_dir)),
                text=True,
                capture_output=True,
                check=False,
            )
            status_path = Path(temp_dir) / "workspace" / "sqlglot_status.json"
            payload = json.loads(status_path.read_text(encoding="utf-8"))

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("schema_context_unavailable", completed.stderr)
        self.assertEqual(payload["route_id"], "sqlglot_optimize_schema_aware")
        self.assertFalse(payload["candidate_generated"])
        self.assertEqual(payload["failure_bucket"], "schema_context_unavailable")

    def test_missing_sqlglot_dependency_guard_when_unavailable(self) -> None:
        if SQLGLOT_AVAILABLE:
            self.skipTest("SQLGlot is installed in this environment")
        with tempfile.TemporaryDirectory() as temp_dir:
            completed = subprocess.run(
                [sys.executable, str(ADAPTER), "--route", "noop"],
                cwd=REPO_ROOT,
                env=_adapter_env(Path(temp_dir)),
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("SQLGlot is not installed", completed.stderr)

    def test_user_run_dry_run_with_sqlglot_command_does_not_invoke_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _out("unittest_sqlglot_dry_run")
            summary = run_user_benchmark(
                _user_args(out, case_list, "noop", dry_run=True),
                REPO_ROOT,
            )
        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["adapter_invoked_rows"], 0)
        self.assertEqual(summary["candidate_generated_rows"], 0)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["extraction_status"], "skipped_dry_run")
        self.assertEqual(rows[0]["failure_bucket"], "none")

    @unittest.skipUnless(SQLGLOT_AVAILABLE, "SQLGlot is not installed")
    def test_user_run_sqlglot_noop_smoke_when_available(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _out("unittest_sqlglot_noop")
            summary = run_user_benchmark(_user_args(out, case_list, "noop"), REPO_ROOT)
        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["candidate_generated_rows"], 1)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["candidate_generated"], "true")
        self.assertEqual(rows[0]["extraction_status"], "captured_from_candidate_file")
        self.assertTrue((REPO_ROOT / rows[0]["candidate_sql_path"]).exists())

    @unittest.skipUnless(SQLGLOT_AVAILABLE, "SQLGlot is not installed")
    def test_user_run_sqlglot_optimize_smoke_when_available(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _out("unittest_sqlglot_optimize")
            summary = run_user_benchmark(_user_args(out, case_list, "optimize"), REPO_ROOT)
        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["candidate_generated_rows"], 1)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["candidate_generated"], "true")
        self.assertEqual(rows[0]["extraction_status"], "captured_from_candidate_file")
        self.assertTrue((REPO_ROOT / rows[0]["candidate_sql_path"]).exists())

    @unittest.skipUnless(SQLGLOT_AVAILABLE, "SQLGlot is not installed")
    def test_schema_aware_optimize_avoids_cons0005_invalid_qualification(self) -> None:
        module = _load_adapter_module()
        source_sql = (REPO_ROOT / "cases" / "CONS" / "CONS_0005" / "sql" / "source.sql").read_text(
            encoding="utf-8"
        )
        schema_context = {
            "table1": {"i": "INT", "j": "INT"},
            "table2": {"i": "INT", "j": "INT"},
        }

        for dialect in ["postgres", "mysql", "spark"]:
            candidate = module.generate_candidate(
                source_sql,
                route="optimize_schema_aware",
                dialect=dialect,
                schema_context=schema_context,
            )
            self.assertNotIn('"table1"."table2"."i"', candidate)
            self.assertNotIn("`table1`.`table2`.`i`", candidate)

    @unittest.skipUnless(SQLGLOT_AVAILABLE, "SQLGlot is not installed")
    def test_mysql_array_any_schema_aware_route_fails_closed_without_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source_path = temp_path / "source.sql"
            source_path.write_text(
                (
                    REPO_ROOT / "cases" / "CONS" / "CONS_0005" / "sql" / "source.sql"
                ).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            schema_dir = temp_path / "schema"
            schema_dir.mkdir()
            (schema_dir / "ddl_mysql.sql").write_text(
                "CREATE TABLE table1 (i INT, j INT);\n"
                "CREATE TABLE table2 (i INT, j INT);\n",
                encoding="utf-8",
            )
            workspace = temp_path / "workspace"
            env = {
                **_pythonpath_env(),
                "SQLRB_RUN_ID": "test_run",
                "SQLRB_CASE_ID": "CONS_0005",
                "SQLRB_POOL": "CONS",
                "SQLRB_ENGINE": "mysql",
                "SQLRB_SOURCE_SQL_PATH": str(source_path),
                "SQLRB_CASE_DIR": str(temp_path),
                "SQLRB_WORKSPACE_DIR": str(workspace),
                "SQLRB_CANDIDATE_SQL_PATH": str(workspace / "candidate.sql"),
            }
            completed = subprocess.run(
                [sys.executable, str(ADAPTER), "--route", "optimize_schema_aware"],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            status = json.loads((workspace / "sqlglot_status.json").read_text(encoding="utf-8"))

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("ARRAY_ANY", completed.stderr)
            self.assertFalse((workspace / "candidate.sql").exists())
            self.assertEqual(status["route_id"], "sqlglot_optimize_schema_aware")
            self.assertFalse(status["candidate_generated"])
            self.assertEqual(status["failure_bucket"], "mysql_unsupported_array_any")
            self.assertEqual(status["preflight_status"], "mysql_unsupported_array_any")
            unsupported_candidate = Path(status["unsupported_candidate_sql_path"])
            self.assertTrue(unsupported_candidate.exists())
            self.assertIn("ARRAY_ANY", unsupported_candidate.read_text(encoding="utf-8"))

    @unittest.skipUnless(SQLGLOT_AVAILABLE, "SQLGlot is not installed")
    def test_user_run_sqlglot_schema_aware_smoke_when_available(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _out("unittest_sqlglot_schema_aware")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            summary = run_user_benchmark(
                _user_args(out, case_list, "optimize_schema_aware"),
                REPO_ROOT,
            )
        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["candidate_generated_rows"], 1)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["candidate_generated"], "true")
        self.assertEqual(rows[0]["extraction_status"], "captured_from_candidate_file")
        self.assertTrue((REPO_ROOT / rows[0]["candidate_sql_path"]).exists())


if __name__ == "__main__":
    unittest.main()
