import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _pythonpath_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    return env


def _run_user_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sql_rewrite_bench.user_run", *args],
        cwd=REPO_ROOT,
        env=_pythonpath_env(),
        text=True,
        capture_output=True,
        check=False,
    )


def _run_dirs() -> set[Path]:
    root = REPO_ROOT / "runs" / "user"
    if not root.exists():
        return set()
    return {path for path in root.iterdir() if path.is_dir()}


class ReadabilityCommandTests(unittest.TestCase):
    def test_list_cases_prints_common_core_cases_without_outputs(self) -> None:
        before = _run_dirs()
        completed = _run_user_command("--case-set", "common_core_v0", "--list-cases")
        after = _run_dirs()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("case_id", completed.stdout)
        self.assertIn("PERF_0006", completed.stdout)
        self.assertIn("CONS_0005", completed.stdout)
        self.assertIn("common_core_v0_member", completed.stdout)
        self.assertEqual(before, after)

    def test_list_cases_pool_filter_prints_perf_only(self) -> None:
        completed = _run_user_command(
            "--case-set",
            "common_core_v0",
            "--pool",
            "PERF",
            "--list-cases",
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("PERF_0006", completed.stdout)
        self.assertNotIn("CONS_0005", completed.stdout)
        data_lines = [
            line for line in completed.stdout.splitlines()[2:] if line.strip()
        ]
        self.assertTrue(all(" PERF " in f" {line} " for line in data_lines))

    def test_explain_selection_smoke_reports_counts_without_outputs(self) -> None:
        before = _run_dirs()
        completed = _run_user_command(
            "--case-set",
            "common_core_v0",
            "--engine",
            "postgres",
            "--smoke",
            "--explain-selection",
        )
        after = _run_dirs()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("selected_rows: 2", completed.stdout)
        self.assertIn("selected_unique_cases: 2", completed.stdout)
        self.assertIn("smoke_subset_applied: true", completed.stdout)
        self.assertIn("- postgres: 2", completed.stdout)
        self.assertIn("adapter_invoked: false", completed.stdout)
        self.assertEqual(before, after)

    def test_explain_selection_pool_distribution(self) -> None:
        completed = _run_user_command(
            "--case-set",
            "common_core_v0",
            "--pool",
            "CONS",
            "--engine",
            "postgres",
            "--explain-selection",
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("selected_rows: 9", completed.stdout)
        self.assertIn("selected_unique_cases: 9", completed.stdout)
        self.assertIn("- CONS: 9", completed.stdout)
        self.assertIn("- postgres: 9", completed.stdout)

    def test_explain_selection_reports_case_list_misses(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = Path(temp_dir) / "cases.txt"
            case_list.write_text("PERF_0006\nNOT_A_CASE\n", encoding="utf-8")
            completed = _run_user_command(
                "--case-set",
                "common_core_v0",
                "--engine",
                "postgres",
                "--case-list",
                str(case_list),
                "--explain-selection",
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("selected_rows: 1", completed.stdout)
        self.assertIn("case_list_filter_applied: true", completed.stdout)
        self.assertIn("requested_case_ids_outside_case_set: NOT_A_CASE", completed.stdout)

    def test_show_output_schema_prints_local_only_schema_without_outputs(self) -> None:
        before = _run_dirs()
        completed = _run_user_command("--show-output-schema")
        after = _run_dirs()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        for name in [
            "ledger.csv",
            "failures.csv",
            "summary.json",
            "quality_summary.json",
            "quality_report.md",
            "tag_slices.csv",
        ]:
            self.assertIn(name, completed.stdout)
        self.assertIn("No official metrics", completed.stdout)
        self.assertIn("No paper table rendering", completed.stdout)
        self.assertIn("No leaderboard input", completed.stdout)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
