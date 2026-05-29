import csv
import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from cli.main import main


class OptionalPOCRUserRunIntegrationTests(unittest.TestCase):
    def test_default_off_does_not_call_pocr_facade(self) -> None:
        with patch("cli.pocr_diagnostic.run_pocr_diagnostic_user_facade") as facade_mock:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(["user", "pocr-diagnostic"])

        self.assertEqual(code, 0)
        facade_mock.assert_not_called()
        text = stdout.getvalue()
        self.assertIn("POCR diagnostic disabled", text)
        self.assertIn("official_pocr_computed=false", text)
        self.assertIn("route_level_pocr_aggregated=false", text)

    def test_annotation_jsonl_requires_enable_flag(self) -> None:
        with patch("cli.pocr_diagnostic.run_pocr_diagnostic_user_facade") as facade_mock:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["user", "pocr-diagnostic", "--annotation-jsonl", "annotations.jsonl"])

        self.assertEqual(code, 2)
        facade_mock.assert_not_called()
        self.assertIn("--annotation-jsonl is accepted only with --enable-pocr-diagnostic", stderr.getvalue())

    def test_enabled_missing_required_args_fails_before_facade(self) -> None:
        with patch("cli.pocr_diagnostic.run_pocr_diagnostic_user_facade") as facade_mock:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["user", "pocr-diagnostic", "--enable-pocr-diagnostic"])

        self.assertEqual(code, 2)
        facade_mock.assert_not_called()
        self.assertIn("--candidate-root", stderr.getvalue())

    def test_optional_pocr_writes_d035_outputs_under_temp_root_only(self, tmp_path: Path | None = None) -> None:
        # unittest does not inject pytest fixtures, so use a local temporary directory.
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            candidate_root = root / "candidate_sql"
            output_root = root / "output"
            case_list = root / "case_list.txt"
            candidate_root.mkdir()
            (candidate_root / "PERF_0006__postgres.sql").write_text("select 1;\n", encoding="utf-8")
            case_list.write_text("PERF_0006\n", encoding="utf-8")

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "user",
                        "pocr-diagnostic",
                        "--enable-pocr-diagnostic",
                        "--candidate-root",
                        candidate_root.as_posix(),
                        "--method-id",
                        "direct_llm_original",
                        "--route-id",
                        "direct_llm_original_pg40_pocr_diagnostic",
                        "--engine",
                        "postgres",
                        "--run-id",
                        "pocr_optional_cli_test",
                        "--output-root",
                        output_root.as_posix(),
                        "--case-list",
                        case_list.as_posix(),
                    ]
                )

            self.assertEqual(code, 0)
            rows_path = output_root / "results" / "pocr_optional_cli_test" / "pocr" / "diagnostic_rows.csv"
            summary_path = output_root / "results" / "pocr_optional_cli_test" / "pocr" / "diagnostic_summary_by_pool.csv"
            stage_b_path = (
                output_root
                / "results"
                / "pocr_optional_cli_test"
                / "pocr"
                / "stage_b"
                / "pocr_stage_b_row_metrics.csv"
            )
            log_path = output_root / "logs" / "pocr_optional_cli_test" / "pocr" / "pocr_diagnostic.log"
            report_path = output_root / "reports" / "pocr_optional_cli_test" / "pocr_diagnostic.md"
            for path in [rows_path, summary_path, stage_b_path, log_path, report_path]:
                self.assertTrue(path.is_file(), path)
                self.assertTrue(path.resolve().is_relative_to(output_root.resolve()))

            with rows_path.open(newline="", encoding="utf-8") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row["annotation_status"], "annotation_missing")
            self.assertEqual(row["diagnostic_only"], "true")
            self.assertEqual(row["official_pocr_computed"], "false")
            self.assertEqual(row["route_level_pocr_aggregated"], "false")
            self.assertEqual(row["paper_metric_promoted"], "false")
            self.assertGreater(int(row["semantic_guard_atoms_count"]), 0)

            with stage_b_path.open(newline="", encoding="utf-8") as handle:
                stage_b_row = next(csv.DictReader(handle))
            self.assertEqual(stage_b_row["annotation_status"], "annotation_missing")
            self.assertEqual(stage_b_row["diagnostic_only"], "true")
            self.assertEqual(stage_b_row["official_pocr_computed"], "false")
            self.assertEqual(stage_b_row["route_level_pocr_aggregated"], "false")
            self.assertEqual(stage_b_row["paper_metric_promoted"], "false")
            self.assertEqual(stage_b_row["pocr_curated_denominator_member"], "false")

            report = report_path.read_text(encoding="utf-8")
            self.assertIn("Positive Operation Coverage diagnostic support", report)
            self.assertIn("This is not official POCR.", report)
            self.assertIn("Stage A annotation alone is not counted.", report)
            self.assertIn("Stage B transformation-aware validation is diagnostic only.", report)
            self.assertIn("Semantic guard atoms are not part of operation coverage numerator.", report)
            self.assertIn("No route-level POCR score is emitted.", report)
            self.assertIn("No paper-facing metric is promoted.", report)
            self.assertIn("official_pocr_computed=false", stdout.getvalue())

    def test_enabled_annotation_jsonl_is_passed_to_facade(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            candidate_root = root / "candidate_sql"
            output_root = root / "output"
            annotation_path = root / "annotations.jsonl"
            candidate_root.mkdir()
            annotation_path.write_text("", encoding="utf-8")

            with patch("cli.pocr_diagnostic.run_pocr_diagnostic_user_facade") as facade_mock:
                fake_output_paths = type("FakePaths", (), {})()
                facade_mock.return_value = type("FakeResult", (), {"rows": (), "output_paths": fake_output_paths})()
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    code = main(
                        [
                            "user",
                            "pocr-diagnostic",
                            "--enable-pocr-diagnostic",
                            "--candidate-root",
                            candidate_root.as_posix(),
                            "--method-id",
                            "direct_llm_original",
                            "--route-id",
                            "direct_llm_original_pg40_pocr_diagnostic",
                            "--engine",
                            "postgres",
                            "--run-id",
                            "pocr_optional_cli_replay_test",
                            "--output-root",
                            output_root.as_posix(),
                            "--annotation-jsonl",
                            annotation_path.as_posix(),
                        ]
                    )

            self.assertEqual(code, 0)
            facade_mock.assert_called_once()
            self.assertEqual(facade_mock.call_args.kwargs["annotation_jsonl"], annotation_path)

    def test_top_level_reports_output_root_is_rejected(self) -> None:
        with patch("cli.pocr_diagnostic.run_pocr_diagnostic_user_facade") as facade_mock:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(
                    [
                        "user",
                        "pocr-diagnostic",
                        "--enable-pocr-diagnostic",
                        "--candidate-root",
                        "candidate_sql",
                        "--method-id",
                        "direct_llm_original",
                        "--route-id",
                        "direct_llm_original_pg40_pocr_diagnostic",
                        "--engine",
                        "postgres",
                        "--run-id",
                        "bad_output_root",
                        "--output-root",
                        "reports",
                    ]
                )

        self.assertEqual(code, 2)
        facade_mock.assert_not_called()
        self.assertIn("top-level reports", stderr.getvalue())
