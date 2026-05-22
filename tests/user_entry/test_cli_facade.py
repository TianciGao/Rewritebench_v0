import io
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
        self.assertIn("POCR remains deferred", text)

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
        self.assertIn("POCR=deferred", output)
        self.assertIn("official_metric_input=false", output)
        self.assertIn("paper_result_input=false", output)
        self.assertIn("retained_evidence_promoted=false", output)
        self.assertIn("leaderboard_input=false", output)

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

    def test_pyproject_exposes_sqlrb_console_script(self) -> None:
        pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(pyproject["project"]["scripts"]["sqlrb"], "cli.main:main")


if __name__ == "__main__":
    unittest.main()
