import csv
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from sql_rewrite_bench.user_run import run_user_benchmark, validate_output_root


REPO_ROOT = Path(__file__).resolve().parents[2]


def _case_list(tmp_path: Path, *case_ids: str) -> Path:
    path = tmp_path / "case_ids.txt"
    path.write_text("\n".join(case_ids) + "\n", encoding="utf-8")
    return path


def _args(out: Path, case_list: Path, adapter: Path) -> Namespace:
    return Namespace(
        case_set="common_core_v0",
        pool="PERF",
        engine="postgres",
        case_list=case_list,
        adapter_command=f"{sys.executable} {adapter}",
        out=out,
        run_id=None,
        adapter_timeout=30,
    )


class UserRunOutputTests(unittest.TestCase):
    def test_output_root_guard_accepts_only_runs_user(self) -> None:
        resolved = validate_output_root(Path("runs/user/demo"), REPO_ROOT)
        self.assertEqual(resolved, (REPO_ROOT / "runs" / "user" / "demo").resolve())
        for invalid in [
            Path("cases/PERF/PERF_0006/runs/demo"),
            Path("results/retained/demo"),
            Path("reports/evaluation/demo"),
            Path("/tmp/demo"),
            Path("../somewhere"),
            Path("runs/user"),
        ]:
            with self.assertRaises(ValueError):
                validate_output_root(invalid, REPO_ROOT)

    def test_user_run_writes_required_outputs_under_runs_user(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006", "PERF_0007")
            run_name = "unittest_user_entry_success"
            out = Path("runs/user") / run_name
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
        self.assertEqual({row["execution_status"] for row in rows}, {"not_run_non_db_mvp"})
        self.assertTrue(all(row["candidate_sql_path"].startswith("runs/user/") for row in rows))
        with (out_dir / "failures.csv").open(newline="", encoding="utf-8") as f:
            self.assertEqual(list(csv.DictReader(f)), [])

        payload = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertIs(payload["official_metrics_computed"], False)
        self.assertIs(payload["paper_tables_rendered"], False)
        self.assertIs(payload["case_sets_changed"], False)
        self.assertIs(payload["no_global_leaderboard"], True)

        report = (out_dir / "report.md").read_text(encoding="utf-8")
        self.assertIn("local user-run output, not retained paper evidence", report)
        self.assertIn("No global leaderboard is created", report)
        self.assertIn("Official metrics are not computed", report)

    def test_empty_adapter_records_no_candidate_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = Path("runs/user/unittest_user_entry_empty")
            adapter = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "empty_adapter.py"
            summary = run_user_benchmark(_args(out, case_list, adapter), REPO_ROOT)
        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["candidate_generated_rows"], 0)
        self.assertEqual(summary["no_candidate_sql_rows"], 1)
        with (REPO_ROOT / out / "failures.csv").open(newline="", encoding="utf-8") as f:
            failures = list(csv.DictReader(f))
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]["failure_bucket"], "no_candidate_sql")


if __name__ == "__main__":
    unittest.main()
