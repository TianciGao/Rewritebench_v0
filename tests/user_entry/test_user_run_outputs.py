import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
import uuid
from argparse import Namespace
from pathlib import Path

from sql_rewrite_bench.user_run import parse_args, run_user_benchmark, validate_output_root


REPO_ROOT = Path(__file__).resolve().parents[2]


def _case_list(tmp_path: Path, *case_ids: str) -> Path:
    path = tmp_path / "case_ids.txt"
    path.write_text("\n".join(case_ids) + "\n", encoding="utf-8")
    return path


def _args(
    out: Path,
    case_list: Path,
    adapter: Path,
    *,
    dry_run: bool = False,
    adapter_timeout: int = 30,
    smoke: bool = False,
) -> Namespace:
    return Namespace(
        case_set="common_core_v0",
        pool="all" if smoke else "PERF",
        engine="postgres",
        case_list=None if smoke else case_list,
        smoke=smoke,
        adapter_command=f"{sys.executable} {adapter}",
        out=out,
        run_id=None,
        adapter_timeout=adapter_timeout,
        dry_run=dry_run,
    )


def _unique_out(name: str) -> Path:
    return Path("runs/user") / f"{name}_{uuid.uuid4().hex}"


def _pythonpath_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    return env


class UserRunOutputTests(unittest.TestCase):
    def test_module_and_wrapper_help_work(self) -> None:
        commands = [
            [sys.executable, "-m", "sql_rewrite_bench.user_run", "--help"],
            [sys.executable, "scripts/user/run_user_benchmark.py", "--help"],
        ]
        for command in commands:
            completed = subprocess.run(
                command,
                cwd=REPO_ROOT,
                env=_pythonpath_env(),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("--case-set", completed.stdout)
            self.assertIn("--adapter-command", completed.stdout)
            self.assertIn("--dry-run", completed.stdout)

    def test_documented_examples_match_current_cli_options(self) -> None:
        guide = (REPO_ROOT / "docs" / "USER_BENCHMARK_GUIDE.md").read_text(
            encoding="utf-8"
        )
        for option in [
            "--case-set",
            "--pool",
            "--engines",
            "--case-list",
            "--adapter-command",
            "--output-root",
            "--run-id",
            "--dry-run",
        ]:
            self.assertIn(option, guide)
        self.assertIn("python -m cli.main user evaluate", guide)
        self.assertIn("sqlrb user evaluate", guide)
        self.assertIn("output/results/<run_id>/", guide)
        self.assertIn("runs/user/<run_id>/", guide)

        parsed = parse_args(
            [
                "--case-set",
                "common_core_v0",
                "--pool",
                "PERF",
                "--engine",
                "postgres",
                "--case-list",
                "path/to/case_ids.txt",
                "--adapter-command",
                "python my_rewriter.py",
                "--out",
                "runs/user/demo_dry_run",
                "--dry-run",
            ]
        )
        self.assertEqual(parsed.case_set, "common_core_v0")
        self.assertEqual(parsed.pool, "PERF")
        self.assertEqual(parsed.engine, "postgres")
        self.assertTrue(parsed.dry_run)

        smoke_parsed = parse_args(
            [
                "--case-set",
                "common_core_v0",
                "--engine",
                "postgres",
                "--smoke",
                "--adapter-command",
                "python examples/user/noop_adapter.py",
                "--out",
                "runs/user/smoke_dry_run",
                "--dry-run",
            ]
        )
        self.assertTrue(smoke_parsed.smoke)

    def test_output_root_guard_accepts_only_runs_user(self) -> None:
        resolved = validate_output_root(Path("runs/user/demo"), REPO_ROOT)
        self.assertEqual(resolved, (REPO_ROOT / "runs" / "user" / "demo").resolve())
        for invalid in [
            Path("cases/PERF/PERF_0006/runs/demo"),
            Path("results/retained/demo"),
            Path("reports/evaluation/demo"),
            Path("/tmp/demo"),
            Path("../demo"),
            Path("../somewhere"),
            Path("runs/user"),
        ]:
            with self.assertRaisesRegex(ValueError, "runs/user"):
                validate_output_root(invalid, REPO_ROOT)

    def test_user_run_writes_required_outputs_under_runs_user(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006", "PERF_0007")
            out = _unique_out("unittest_user_entry_success")
            adapter = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "dummy_adapter.py"
            summary = run_user_benchmark(_args(out, case_list, adapter), REPO_ROOT)
        out_dir = REPO_ROOT / out

        self.assertEqual(summary["selected_rows"], 2)
        self.assertEqual(summary["candidate_generated_rows"], 2)
        for name in [
            "config.yaml",
            "selected_cases.csv",
            "ledger.csv",
            "summary.json",
            "failures.csv",
            "report.md",
        ]:
            self.assertTrue((out_dir / name).exists())

        with (out_dir / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 2)
        self.assertEqual({row["candidate_generated"] for row in rows}, {"true"})
        self.assertEqual({row["extraction_status"] for row in rows}, {"captured_from_candidate_file"})
        self.assertEqual({row["execution_status"] for row in rows}, {"not_run_non_db_mvp"})
        self.assertTrue(all(row["candidate_sql_path"].startswith("runs/user/") for row in rows))
        with (out_dir / "failures.csv").open(newline="", encoding="utf-8") as f:
            self.assertEqual(list(csv.DictReader(f)), [])

        payload = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertIs(payload["official_metrics_computed"], False)
        self.assertIs(payload["paper_tables_rendered"], False)
        self.assertIs(payload["case_sets_changed"], False)
        self.assertIs(payload["no_global_leaderboard"], True)
        self.assertIs(payload["dry_run"], False)

        report = (out_dir / "report.md").read_text(encoding="utf-8")
        self.assertIn("local user-run output only", report)
        self.assertIn("not retained paper evidence", report)
        self.assertIn("No global leaderboard is created", report)
        self.assertIn("Official metrics are not computed", report)
        self.assertIn("Dry-run mode", report)

    def test_dry_run_writes_outputs_without_invoking_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _unique_out("unittest_user_entry_dry_run")
            adapter = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "dummy_adapter.py"
            summary = run_user_benchmark(
                _args(out, case_list, adapter, dry_run=True),
                REPO_ROOT,
            )
        out_dir = REPO_ROOT / out
        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["adapter_invoked_rows"], 0)
        self.assertEqual(summary["candidate_generated_rows"], 0)
        self.assertIs(summary["dry_run"], True)
        with (out_dir / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["adapter_invoked"], "false")
        self.assertEqual(rows[0]["candidate_generated"], "false")
        self.assertEqual(rows[0]["extraction_status"], "skipped_dry_run")
        self.assertEqual(rows[0]["failure_bucket"], "none")
        with (out_dir / "failures.csv").open(newline="", encoding="utf-8") as f:
            self.assertEqual(list(csv.DictReader(f)), [])
        report = (out_dir / "report.md").read_text(encoding="utf-8")
        self.assertIn("Dry-run mode: `True`", report)

    def test_public_smoke_noop_adapter_writes_only_runs_user(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "IGNORED_FOR_SMOKE")
            out = _unique_out("unittest_public_smoke")
            adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
            summary = run_user_benchmark(_args(out, case_list, adapter, smoke=True), REPO_ROOT)
        self.assertEqual(summary["selected_rows"], 2)
        self.assertEqual(summary["candidate_generated_rows"], 2)
        out_dir = REPO_ROOT / out
        with (out_dir / "selected_cases.csv").open(newline="", encoding="utf-8") as f:
            selected = list(csv.DictReader(f))
        self.assertEqual([row["case_id"] for row in selected], ["PERF_0006", "CONS_0005"])
        with (out_dir / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertTrue(all(row["candidate_sql_path"].startswith("runs/user/") for row in rows))
        self.assertEqual({row["extraction_status"] for row in rows}, {"captured_from_candidate_file"})

    def test_stdout_adapter_records_stdout_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _unique_out("unittest_user_entry_stdout")
            adapter = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "stdout_adapter.py"
            summary = run_user_benchmark(_args(out, case_list, adapter), REPO_ROOT)
        self.assertEqual(summary["candidate_generated_rows"], 1)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["candidate_generated"], "true")
        self.assertEqual(rows[0]["extraction_status"], "captured_from_stdout")
        self.assertEqual(rows[0]["failure_bucket"], "none")
        self.assertTrue((REPO_ROOT / rows[0]["candidate_sql_path"]).exists())

    def test_failing_adapter_records_adapter_failed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _unique_out("unittest_user_entry_failed")
            adapter = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "failing_adapter.py"
            summary = run_user_benchmark(_args(out, case_list, adapter), REPO_ROOT)
        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["candidate_generated_rows"], 0)
        self.assertEqual(summary["adapter_failed_rows"], 1)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["adapter_invoked"], "true")
        self.assertEqual(rows[0]["adapter_exit_code"], "7")
        self.assertEqual(rows[0]["candidate_generated"], "false")
        self.assertEqual(rows[0]["extraction_status"], "adapter_failed")
        self.assertEqual(rows[0]["failure_bucket"], "adapter_failed")

    def test_empty_adapter_records_no_candidate_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _unique_out("unittest_user_entry_empty")
            adapter = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "empty_adapter.py"
            summary = run_user_benchmark(_args(out, case_list, adapter), REPO_ROOT)
        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["candidate_generated_rows"], 0)
        self.assertEqual(summary["no_candidate_sql_rows"], 1)
        with (REPO_ROOT / out / "failures.csv").open(newline="", encoding="utf-8") as f:
            failures = list(csv.DictReader(f))
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]["failure_bucket"], "no_candidate_sql")

    def test_slow_adapter_records_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _unique_out("unittest_user_entry_timeout")
            adapter = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "slow_adapter.py"
            summary = run_user_benchmark(
                _args(out, case_list, adapter, adapter_timeout=1),
                REPO_ROOT,
            )
        self.assertEqual(summary["candidate_generated_rows"], 0)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["adapter_invoked"], "true")
        self.assertEqual(rows[0]["candidate_generated"], "false")
        self.assertEqual(rows[0]["extraction_status"], "adapter_failed")
        self.assertEqual(rows[0]["failure_bucket"], "adapter_timeout")


if __name__ == "__main__":
    unittest.main()
