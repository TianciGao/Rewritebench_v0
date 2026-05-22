import json
import shutil
import sys
import tempfile
import unittest
import uuid
from argparse import Namespace
from pathlib import Path

from sql_rewrite_bench.user_run import run_user_benchmark


REPO_ROOT = Path(__file__).resolve().parents[2]


def _case_list(tmp_path: Path, *case_ids: str) -> Path:
    path = tmp_path / "case_ids.txt"
    path.write_text("\n".join(case_ids) + "\n", encoding="utf-8")
    return path


def _unique_out(name: str) -> Path:
    return Path("runs/user") / f"{name}_{uuid.uuid4().hex}"


def _args(
    out: Path,
    case_list: Path,
    adapter: Path,
    *,
    dry_run: bool = False,
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
        adapter_timeout=30,
        dry_run=dry_run,
        enable_db_execution=False,
        enable_checker=False,
        postgres_dsn_env="SQLRB_POSTGRES_DSN",
        execution_timeout_sec=30,
        db_schema_prefix="sqlrb_user",
    )


class UserQualityReportTests(unittest.TestCase):
    def test_quality_summary_is_written_for_dry_run_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "IGNORED_FOR_SMOKE")
            out = _unique_out("unittest_u4_quality_dry_run")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
            summary = run_user_benchmark(
                _args(out, case_list, adapter, dry_run=True, smoke=True),
                REPO_ROOT,
            )

        out_dir = REPO_ROOT / out
        payload = json.loads((out_dir / "quality_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["selected_rows"], 2)
        self.assertTrue((out_dir / "quality_report.md").exists())
        self.assertEqual(payload["schema_version"], "local_quality_report_v0")
        self.assertEqual(payload["funnel_counts"]["selected_rows"], 2)
        self.assertEqual(payload["funnel_counts"]["candidate_generated_rows"], 0)
        self.assertEqual(payload["funnel_counts"]["candidate_preflight_passed_rows"], 0)
        self.assertIs(payload["scope"]["official_metrics"], False)
        self.assertIs(payload["scope"]["leaderboard_created"], False)
        self.assertIs(payload["interpretation_boundary"]["tag_slices_included"], True)
        self.assertTrue((out_dir / "tag_slices.csv").exists())

    def test_quality_outputs_are_written_for_adapter_capture_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "IGNORED_FOR_SMOKE")
            out = _unique_out("unittest_u4_quality_adapter_capture")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
            summary = run_user_benchmark(_args(out, case_list, adapter, smoke=True), REPO_ROOT)

        out_dir = REPO_ROOT / out
        payload = json.loads((out_dir / "quality_summary.json").read_text(encoding="utf-8"))
        report = (out_dir / "quality_report.md").read_text(encoding="utf-8")
        self.assertEqual(summary["selected_rows"], 2)
        self.assertEqual(summary["candidate_generated_rows"], 2)
        self.assertEqual(payload["funnel_counts"]["selected_rows"], 2)
        self.assertEqual(payload["funnel_counts"]["candidate_generated_rows"], 2)
        self.assertEqual(payload["funnel_counts"]["candidate_preflight_passed_rows"], 2)
        self.assertEqual(payload["funnel_counts"]["source_like_rows"], 2)
        self.assertIn("none", payload["failure_bucket_counts"])
        self.assertEqual(payload["failure_bucket_counts"]["none"], 2)
        self.assertEqual(payload["diagnostic_counts"]["label_only_mismatch_rows"], 0)
        self.assertIs(payload["scope"]["official_metrics"], False)
        self.assertIs(payload["scope"]["paper_results_updated"], False)
        self.assertIs(payload["scope"]["retained_evidence_input"], False)
        self.assertIs(payload["scope"]["leaderboard_created"], False)
        self.assertIn("# Local Quality Report", report)
        self.assertIn("not official metrics", report)
        self.assertIn("not a paper table", report)
        self.assertIn("not retained evidence", report)
        self.assertIs(payload["interpretation_boundary"]["tag_slices_included"], True)
        self.assertIn("Tag-aware slices are available as local diagnostics", report)
        self.assertIn("Timing and speedup are not included", report)
        self.assertTrue((out_dir / "tag_slices.csv").exists())

    def test_quality_summary_counts_label_only_mismatch_notes(self) -> None:
        from sql_rewrite_bench.user_quality_report import build_quality_summary

        payload = build_quality_summary(
            [
                {
                    "selected": "true",
                    "adapter_invoked": "true",
                    "candidate_generated": "true",
                    "candidate_preflight_status": "passed",
                    "candidate_preflight_passed": "true",
                    "execution_status": "candidate_execution_success",
                    "source_execution_status": "source_execution_success",
                    "candidate_execution_status": "candidate_execution_success",
                    "checker_status": "checker_mismatch",
                    "exact_status": "mismatch",
                    "failure_bucket": "mismatch",
                    "source_like_status": "changed",
                    "timed_status": "not_timed_non_db_mvp",
                    "notes": "local checker mismatch; label_only_mismatch=true",
                },
                {
                    "selected": "true",
                    "adapter_invoked": "true",
                    "candidate_generated": "true",
                    "candidate_preflight_status": "passed",
                    "candidate_preflight_passed": "true",
                    "execution_status": "candidate_execution_success",
                    "source_execution_status": "source_execution_success",
                    "candidate_execution_status": "candidate_execution_success",
                    "checker_status": "checker_mismatch",
                    "exact_status": "mismatch",
                    "failure_bucket": "mismatch",
                    "source_like_status": "changed",
                    "timed_status": "not_timed_non_db_mvp",
                    "notes": "local checker mismatch; value mismatch",
                },
            ]
        )

        self.assertEqual(payload["diagnostic_counts"]["label_only_mismatch_rows"], 1)

    def test_quality_summary_has_no_timing_or_speedup_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "IGNORED_FOR_SMOKE")
            out = _unique_out("unittest_u4_quality_no_timing")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
            run_user_benchmark(_args(out, case_list, adapter, smoke=True), REPO_ROOT)

        payload = json.loads(
            (REPO_ROOT / out / "quality_summary.json").read_text(encoding="utf-8")
        )
        self.assertEqual(payload["funnel_counts"]["timed_rows"], 0)
        serialized = json.dumps(payload, sort_keys=True)
        self.assertNotIn("speedup", serialized.lower())
        self.assertNotIn("generation rate", serialized.lower())
        self.assertNotIn("execution coverage rate", serialized.lower())
        self.assertNotIn("result consistency rate", serialized.lower())


if __name__ == "__main__":
    unittest.main()
