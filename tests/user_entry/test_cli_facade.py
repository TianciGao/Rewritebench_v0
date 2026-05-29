import io
import csv
import json
import tempfile
import tomllib
import unittest
from argparse import Namespace
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from cli.main import build_parser, main
from sql_rewrite_bench.pocr.stage_b_row_metrics import stage_b_row_metric_fields


REPO_ROOT = Path(__file__).resolve().parents[2]


class CliFacadeTests(unittest.TestCase):
    def test_parser_accepts_user_evaluate(self) -> None:
        parser = build_parser()
        args = parser.parse_args(
            [
                "user",
                "evaluate",
                "--case-set",
                "common_core_v0",
                "--engines",
                "postgres",
                "--adapter-command",
                "python adapter.py",
                "--output-root",
                "output",
                "--run-id",
                "demo",
                "--smoke",
            ]
        )
        self.assertEqual(args.command_group, "user")
        self.assertEqual(args.user_command, "evaluate")
        self.assertEqual(args.engines, "postgres")
        self.assertTrue(args.smoke)

    def test_parser_accepts_required_convenience_commands(self) -> None:
        parser = build_parser()
        for argv in [
            ["user", "list-cases", "--case-set", "common_core_v0"],
            ["user", "explain-selection", "--case-set", "common_core_v0"],
            ["user", "show-output-schema"],
            ["user", "show-boundary"],
        ]:
            args = parser.parse_args(argv)
            self.assertEqual(args.command_group, "user")

    def test_help_warns_local_diagnostic_only(self) -> None:
        parser = build_parser()
        help_text = parser.format_help()
        self.assertIn("local diagnostic", help_text)
        self.assertIn("outputs only", help_text)
        self.assertIn("leaderboard", help_text)

    def test_user_command_help_carries_local_only_boundary(self) -> None:
        for command in [
            "evaluate",
            "list-cases",
            "explain-selection",
            "show-output-schema",
            "show-boundary",
            "compute-local-metrics",
            "summarize",
            "verify",
            "pocr-diagnostic",
            "pocr-aggregate",
        ]:
            stdout = io.StringIO()
            with self.assertRaises(SystemExit):
                with redirect_stdout(stdout):
                    main(["user", command, "--help"])
            help_text = stdout.getvalue().lower()
            self.assertIn("local diagnostic", help_text)
            self.assertIn("official metrics", help_text)
            self.assertIn("paper results", help_text)
            self.assertIn("retained", help_text)
            self.assertIn("leaderboard", help_text)

    def test_no_leaderboard_or_ranking_command_exists(self) -> None:
        parser = build_parser()
        help_text = parser.format_help()
        self.assertNotIn(" winner", help_text)
        self.assertNotIn(" rank", help_text)
        user_action = next(
            action for action in parser._subparsers._actions if getattr(action, "dest", "") == "command_group"
        )
        user_parser = user_action.choices["user"]
        user_subparser_action = next(
            action for action in user_parser._subparsers._actions if getattr(action, "dest", "") == "user_command"
        )
        self.assertNotIn("leaderboard", user_subparser_action.choices)
        self.assertNotIn("rank", user_subparser_action.choices)
        self.assertNotIn("winner", user_subparser_action.choices)

    def test_evaluate_delegates_to_user_run_and_output_exporter(self) -> None:
        fake_summary = {"selected_rows": 2, "candidate_generated_rows": 2}
        fake_paths = SimpleNamespace(
            result_root=REPO_ROOT / "output" / "results" / "demo",
            report_root=REPO_ROOT / "output" / "reports" / "demo",
        )
        fake_exported = SimpleNamespace(run_id="demo", paths=fake_paths)
        with patch("cli.main.user_run.run_user_benchmark", return_value=fake_summary) as run_mock, patch(
            "cli.main.export_run_to_output", return_value=fake_exported
        ) as export_mock:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "user",
                        "evaluate",
                        "--case-set",
                        "common_core_v0",
                        "--engines",
                        "postgres",
                        "--adapter-command",
                        "python adapter.py",
                        "--output-root",
                        "output",
                        "--run-id",
                        "demo",
                        "--smoke",
                    ]
                )

        self.assertEqual(code, 0)
        run_mock.assert_called_once()
        export_mock.assert_called_once()
        run_args = run_mock.call_args.args[0]
        self.assertIsInstance(run_args, Namespace)
        self.assertEqual(run_args.engine, "postgres")
        self.assertEqual(run_args.out, Path("runs/user/demo"))
        self.assertEqual(run_args.run_id, "demo")
        self.assertTrue(run_args.smoke)
        export_args = export_mock.call_args.args
        self.assertEqual(export_args[0], REPO_ROOT / "runs" / "user" / "demo")
        self.assertEqual(export_args[1], REPO_ROOT / "output")
        self.assertEqual(export_mock.call_args.kwargs["run_id"], "demo")
        output = stdout.getvalue()
        self.assertIn("official_metric_input=false", output)
        self.assertIn("leaderboard_input=false", output)

    def test_output_schema_and_boundary_commands_are_local_only(self) -> None:
        for argv in [["user", "show-output-schema"], ["user", "show-boundary"]]:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(argv)
            self.assertEqual(code, 0)
            text = stdout.getvalue()
            self.assertIn("local", text.lower())
            self.assertIn("official", text.lower())
            self.assertIn("leaderboard", text.lower())

    def test_show_boundary_includes_na_and_deferred_metrics(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = main(["user", "show-boundary"])
        self.assertEqual(code, 0)
        text = stdout.getvalue()
        self.assertIn("Not official metrics", text)
        self.assertIn("Not paper results", text)
        self.assertIn("Not retained evidence", text)
        self.assertIn("Not leaderboard input", text)
        self.assertIn("Semantic Equivalence Rate is N.A.", text)
        self.assertIn("POCR is available as optional diagnostic support", text)
        self.assertIn("not an official paper metric unless separately promoted", text.replace("\n", " "))

    def test_evaluate_rejects_unimplemented_verifier_flags(self) -> None:
        with patch("cli.main.user_run.run_user_benchmark") as run_mock:
            for verifier in ["verieql", "sqlsolver"]:
                stderr = io.StringIO()
                with redirect_stderr(stderr):
                    code = main(
                        [
                            "user",
                            "evaluate",
                            "--case-set",
                            "common_core_v0",
                            "--engines",
                            "postgres",
                            "--adapter-command",
                            "python adapter.py",
                            "--output-root",
                            "output",
                            "--run-id",
                            "demo",
                            "--verifier",
                            verifier,
                        ]
                    )
                self.assertEqual(code, 2)
                self.assertIn("not implemented", stderr.getvalue())
                self.assertIn("Semantic Equivalence Rate remains N.A.", stderr.getvalue())
        self.assertEqual(code, 2)
        run_mock.assert_not_called()

    def test_evaluate_rejects_top_level_reports_output_before_running(self) -> None:
        with patch("cli.main.user_run.run_user_benchmark") as run_mock:
            code = main(
                [
                    "user",
                    "evaluate",
                    "--case-set",
                    "common_core_v0",
                    "--engines",
                    "postgres",
                    "--adapter-command",
                    "python adapter.py",
                    "--output-root",
                    "reports",
                    "--run-id",
                    "demo",
                ]
            )
        self.assertEqual(code, 2)
        run_mock.assert_not_called()

    def test_compute_local_metrics_delegates_and_exports_local_only(self) -> None:
        fake_outputs = SimpleNamespace(metrics_dir=REPO_ROOT / "runs" / "user" / "demo" / "metrics")
        fake_paths = SimpleNamespace(
            result_root=REPO_ROOT / "output" / "results" / "demo",
            report_root=REPO_ROOT / "output" / "reports" / "demo",
        )
        fake_exported = SimpleNamespace(paths=fake_paths)
        with patch("cli.main.compute_and_write_local_metrics", return_value=fake_outputs) as metrics_mock, patch(
            "cli.main.export_run_to_output", return_value=fake_exported
        ) as export_mock:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(["user", "compute-local-metrics", "--run-id", "demo", "--output-root", "output"])
        self.assertEqual(code, 0)
        metrics_mock.assert_called_once_with(REPO_ROOT / "runs" / "user" / "demo")
        export_mock.assert_called_once()
        output = stdout.getvalue()
        self.assertIn("local diagnostic metrics only", output)
        self.assertIn("user-facing metrics output", output)
        self.assertIn("metrics_summary.md", output)
        self.assertIn("Semantic Equivalence Rate=N.A.", output)
        self.assertIn("POCR available via pocr-diagnostic and pocr-aggregate", output)
        self.assertIn("not an official paper metric unless separately promoted", output)
        self.assertIn("official_metric_input=false", output)
        self.assertIn("paper_result_input=false", output)
        self.assertIn("retained_evidence_promoted=false", output)
        self.assertIn("leaderboard_input=false", output)

    def test_compute_local_metrics_aggregates_per_engine_runs(self) -> None:
        fake_outputs = SimpleNamespace(metrics_dir=REPO_ROOT / "runs" / "user" / "track_a" / "metrics")
        fake_paths = SimpleNamespace(
            result_root=REPO_ROOT / "output" / "results" / "track_a",
            report_root=REPO_ROOT / "output" / "reports" / "track_a",
        )
        fake_exported = SimpleNamespace(paths=fake_paths)
        with patch("cli.main.compute_and_write_aggregate_local_metrics", return_value=fake_outputs) as metrics_mock, patch(
            "cli.main.export_run_to_output", return_value=fake_exported
        ) as export_mock:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "user",
                        "compute-local-metrics",
                        "--run-id-prefix",
                        "track_a",
                        "--engines",
                        "postgres,mysql,spark",
                        "--aggregate-run-id",
                        "track_a",
                        "--output-root",
                        "output",
                    ]
                )
        self.assertEqual(code, 0)
        metrics_mock.assert_called_once_with(
            [
                REPO_ROOT / "runs" / "user" / "track_a__postgres",
                REPO_ROOT / "runs" / "user" / "track_a__mysql",
                REPO_ROOT / "runs" / "user" / "track_a__spark",
            ],
            REPO_ROOT / "runs" / "user" / "track_a",
            aggregate_run_id="track_a",
        )
        export_mock.assert_called_once()
        self.assertEqual(export_mock.call_args.args[0], REPO_ROOT / "runs" / "user" / "track_a")
        self.assertEqual(export_mock.call_args.kwargs["run_id"], "track_a")
        output = stdout.getvalue()
        self.assertIn("local aggregate metrics written", output)
        self.assertIn("source runs aggregated: track_a__postgres, track_a__mysql, track_a__spark", output)
        self.assertIn("user-facing metrics output", output)

    def test_compute_local_metrics_requires_complete_aggregate_options(self) -> None:
        with patch("cli.main.compute_and_write_aggregate_local_metrics") as metrics_mock:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["user", "compute-local-metrics", "--run-id-prefix", "track_a"])
        self.assertEqual(code, 2)
        self.assertIn("--run-id-prefix, --engines, and --aggregate-run-id", stderr.getvalue())
        metrics_mock.assert_not_called()

    def test_compute_local_metrics_rejects_top_level_results_output_before_computing(self) -> None:
        with patch("cli.main.compute_and_write_local_metrics") as metrics_mock:
            code = main(["user", "compute-local-metrics", "--run-id", "demo", "--output-root", "results"])
        self.assertEqual(code, 2)
        metrics_mock.assert_not_called()

    def test_summarize_reads_local_output_summary_and_related_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "output"
            summary = output_root / "reports" / "demo" / "summary.md"
            summary.parent.mkdir(parents=True)
            summary.write_text(
                "# Summary\n\nThis is local diagnostic output only.\n\nOfficial metrics computed: `false`\n",
                encoding="utf-8",
            )
            (summary.parent / "failure_buckets.md").write_text(
                "# Failure Buckets\n\n| failure_bucket | count |\n| --- | ---: |\n| mismatch | 1 |\n",
                encoding="utf-8",
            )
            (summary.parent / "tag_slices.md").write_text(
                "# Tag Slices\n\nRows available: `2`.\n",
                encoding="utf-8",
            )
            (summary.parent / "metrics_summary.md").write_text(
                "# Local Metrics Summary\n\n- Semantic Equivalence Rate: `N.A.` without verifier evidence\n- POCR: deferred\n",
                encoding="utf-8",
            )
            (summary.parent / "verifier_summary.md").write_text(
                "# Verifier Summary\n\n- Semantic Equivalence Rate: `N.A.`\n- VeriEQL: not run\n- SQLSolver: not run\n",
                encoding="utf-8",
            )
            (summary.parent / "boundary.md").write_text(
                "# Boundary\n\nThis is local diagnostic output only.\n\n- Leaderboard input: `false`\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(["user", "summarize", "--output-root", output_root.as_posix(), "--run-id", "demo"])
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn("SQL-RewriteBench Local Output Summary", output)
        self.assertIn("local diagnostic output only", output)
        self.assertIn("Official metrics computed", output)
        self.assertIn("Failure Buckets", output)
        self.assertIn("mismatch", output)
        self.assertIn("Tag Slices", output)
        self.assertIn("Rows available", output)
        self.assertIn("Local Metrics", output)
        self.assertIn("Semantic Equivalence Rate", output)
        self.assertIn("POCR", output)
        self.assertIn("Verifier", output)
        self.assertIn("SQLSolver", output)
        self.assertIn("Boundary", output)

    def test_summarize_reports_na_when_optional_reports_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "output"
            manifest = output_root / "results" / "demo" / "run_manifest.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(
                json.dumps(
                    {
                        "run_id": "demo",
                        "case_set": "common_core_v0",
                        "selected_case_count": 2,
                        "selected_engines": ["postgres"],
                        "route_id": "sqlglot_noop",
                        "method_id": "sqlglot",
                        "local_diagnostic_only": True,
                        "official_metric_input": False,
                        "paper_result_input": False,
                        "retained_evidence_promoted": False,
                        "leaderboard_input": False,
                    }
                ),
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(["user", "summarize", "--output-root", output_root.as_posix(), "--run-id", "demo"])
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn("Run Manifest", output)
        self.assertIn("Failure buckets: N.A.", output)
        self.assertIn("Tag slices: N.A.", output)
        self.assertIn("Local metrics: N.A.", output)
        self.assertIn("Verifier: N.A.", output)
        self.assertIn("Semantic Equivalence Rate", output)
        self.assertIn("POCR", output)

    def test_show_boundary_reads_exported_boundary_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "output"
            boundary = output_root / "reports" / "demo" / "boundary.md"
            boundary.parent.mkdir(parents=True)
            boundary.write_text("# Boundary\n\ncustom local boundary\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "user",
                        "show-boundary",
                        "--output-root",
                        output_root.as_posix(),
                        "--run-id",
                        "demo",
                    ]
                )
        self.assertEqual(code, 0)
        self.assertIn("custom local boundary", stdout.getvalue())

    def test_verify_verieql_unavailable_writes_fail_closed_local_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "output"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "user",
                        "verify",
                        "--run-id",
                        "verify_verieql",
                        "--tool",
                        "verieql",
                        "--tool-cmd",
                        "/definitely/missing/verieql",
                        "--output-root",
                        output_root.as_posix(),
                    ]
                )

            self.assertEqual(code, 0)
            self.assertIn("tool_available=false", stdout.getvalue())
            verifier_root = output_root / "results" / "verify_verieql" / "verifier"
            summary = json.loads((verifier_root / "semantic_equivalence_summary.json").read_text(encoding="utf-8"))
            verdicts = _read_jsonl(verifier_root / "verifier_verdicts.jsonl")
            self.assertEqual(summary["semantic_equivalence_rate"], None)
            self.assertEqual(summary["semantic_equivalence_rate_status"], "not_applicable")
            self.assertEqual(summary["na_reason"], "verieql_unavailable")
            self.assertFalse(summary["result_checker_exactness_used"])
            self.assertTrue(summary["local_diagnostic_only"])
            self.assertFalse(summary["official_metric_input"])
            self.assertFalse(summary["paper_result_input"])
            self.assertFalse(summary["retained_evidence_promoted"])
            self.assertFalse(summary["leaderboard_input"])
            self.assertEqual(len(verdicts), 1)
            self.assertEqual(verdicts[0]["normalized_verdict"], "not_attempted")
            self.assertTrue((output_root / "logs" / "verify_verieql" / "verifier.log").exists())
            self.assertTrue((output_root / "reports" / "verify_verieql" / "verifier_summary.md").exists())
            self.assertFalse((Path(tmp) / "reports").exists())
            self.assertFalse((Path(tmp) / "results").exists())
            payload = json.dumps(summary) + "\n".join(json.dumps(row) for row in verdicts)
            for token in ["winner", "best_method", "rank"]:
                self.assertNotIn(token, payload)

    def test_verify_sqlsolver_unavailable_writes_fail_closed_local_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "output"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "user",
                        "verify",
                        "--run-id",
                        "verify_sqlsolver",
                        "--tool",
                        "sqlsolver",
                        "--tool-cmd",
                        "/definitely/missing/sqlsolver",
                        "--output-root",
                        output_root.as_posix(),
                    ]
                )

            self.assertEqual(code, 0)
            self.assertIn("tool_available=false", stdout.getvalue())
            verifier_root = output_root / "results" / "verify_sqlsolver" / "verifier"
            summary = json.loads((verifier_root / "semantic_equivalence_summary.json").read_text(encoding="utf-8"))
            verdicts = _read_jsonl(verifier_root / "verifier_verdicts.jsonl")
            self.assertEqual(summary["semantic_equivalence_rate"], None)
            self.assertEqual(summary["semantic_equivalence_rate_status"], "not_applicable")
            self.assertEqual(summary["na_reason"], "sqlsolver_unavailable")
            self.assertFalse(summary["result_checker_exactness_used"])
            self.assertEqual(len(verdicts), 2)
            self.assertTrue(all(row["normalized_verdict"] == "not_attempted" for row in verdicts))
            self.assertTrue((output_root / "logs" / "verify_sqlsolver" / "verifier.log").exists())
            self.assertTrue((output_root / "reports" / "verify_sqlsolver" / "verifier_summary.md").exists())
            self.assertFalse((Path(tmp) / "reports").exists())
            self.assertFalse((Path(tmp) / "results").exists())
            payload = json.dumps(summary) + "\n".join(json.dumps(row) for row in verdicts)
            for token in ["winner", "best_method", "rank"]:
                self.assertNotIn(token, payload)

    def test_verify_invalid_tool_fails_with_clear_argparse_error(self) -> None:
        stderr = io.StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stderr(stderr):
                main(["user", "verify", "--run-id", "demo", "--tool", "bogus"])
        self.assertIn("invalid choice", stderr.getvalue())

    def test_verify_rejects_top_level_results_output_before_writing(self) -> None:
        code = main(
            [
                "user",
                "verify",
                "--run-id",
                "demo",
                "--tool",
                "verieql",
                "--output-root",
                "results",
                "--tool-cmd",
                "/definitely/missing/verieql",
            ]
        )
        self.assertEqual(code, 2)

    def test_pocr_aggregate_requires_enable_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            row_metrics = _write_pocr_row_metrics(Path(tmp) / "pocr_stage_b_row_metrics.csv")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(
                    [
                        "user",
                        "pocr-aggregate",
                        "--row-metrics",
                        row_metrics.as_posix(),
                        "--run-id",
                        "pocr_aggregate_demo",
                        "--output-root",
                        (Path(tmp) / "output").as_posix(),
                    ]
                )
        self.assertEqual(code, 2)
        self.assertIn("--enable-pocr-diagnostic", stderr.getvalue())

    def test_pocr_aggregate_writes_route_summary_under_output_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            row_metrics = _write_pocr_row_metrics(root / "pocr_stage_b_row_metrics.csv")
            output_root = root / "output"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(
                    [
                        "user",
                        "pocr-aggregate",
                        "--enable-pocr-diagnostic",
                        "--row-metrics",
                        row_metrics.as_posix(),
                        "--run-id",
                        "pocr_aggregate_demo",
                        "--output-root",
                        output_root.as_posix(),
                    ]
                )

            self.assertEqual(code, 0)
            summary_path = output_root / "results" / "pocr_aggregate_demo" / "pocr" / "aggregates" / "pocr_route_summary.csv"
            report_path = output_root / "reports" / "pocr_aggregate_demo" / "pocr_route_summary.md"
            self.assertTrue(summary_path.exists())
            self.assertTrue(report_path.exists())
            with summary_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["pocr_planned_macro"], "0.500000000000")
            self.assertEqual(rows[0]["pocr_candidate_macro"], "0.500000000000")
            self.assertEqual(rows[0]["pocr_curated"], "NA")
            self.assertEqual(rows[0]["pocr_curated_status"], "curated_manifest_missing")
            self.assertEqual(rows[0]["official_pocr_computed"], "false")
            self.assertEqual(rows[0]["route_level_official_pocr_score_emitted"], "false")
            self.assertEqual(rows[0]["paper_metric_promoted"], "false")
            self.assertEqual(rows[0]["leaderboard_output"], "false")
            output = stdout.getvalue()
            self.assertIn("pocr-aggregate complete", output)
            self.assertIn("official_pocr_computed=false", output)
            self.assertFalse((root / "reports").exists())
            self.assertFalse((root / "results").exists())

    def test_pocr_aggregate_help_does_not_imply_official_promotion(self) -> None:
        stdout = io.StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stdout(stdout):
                main(["user", "pocr-aggregate", "--help"])
        help_text = stdout.getvalue().replace("-\n", "-").replace("\n", " ")
        self.assertIn("promotion-diagnostic", help_text)
        self.assertIn("does not call APIs", help_text)
        self.assertIn("compute official POCR", help_text)
        self.assertNotIn("paper-facing metric is promoted", help_text.lower())

    def test_pyproject_exposes_sqlrb_console_script(self) -> None:
        pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(pyproject["project"]["scripts"]["sqlrb"], "cli.main:main")


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_pocr_row_metrics(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "run_id": "pocr_row_fixture",
        "case_set_id": "common_core_v0",
        "denominator_scope": "pg40_postgres_only",
        "case_id": "PERF_0006",
        "pool": "PERF",
        "engine": "postgres",
        "method_id": "fixture_method",
        "route_id": "fixture_route",
        "candidate_sha256": "a" * 64,
        "planned_pocr_eligible": "true",
        "candidate_bound": "true",
        "annotation_status": "schema_valid",
        "replay_row_present": "true",
        "route_mismatch": "false",
        "candidate_mismatch": "false",
        "expected_operation_atoms": "2",
        "stage_b_supported_operation_atoms": "1",
        "presence_only_operation_atoms": "0",
        "insufficient_transformation_evidence_atoms": "1",
        "rejected_noop_equivalent_atoms": "0",
        "semantic_guard_atoms": "1",
        "oc_i": "0.500000000000",
        "oc_i_fail_closed": "0.500000000000",
        "pocr_planned_denominator_member": "true",
        "pocr_candidate_denominator_member": "true",
        "pocr_curated_denominator_member": "false",
        "fail_closed_status": "none",
        "not_applicable_reason": "none",
        "diagnostic_only": "true",
        "official_pocr_computed": "false",
        "route_level_pocr_aggregated": "false",
        "paper_metric_promoted": "false",
        "notes": "fixture diagnostic row",
    }
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=stage_b_row_metric_fields(), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    return path


if __name__ == "__main__":
    unittest.main()
