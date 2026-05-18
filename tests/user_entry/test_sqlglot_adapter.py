import csv
import importlib.util
import os
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


if __name__ == "__main__":
    unittest.main()
