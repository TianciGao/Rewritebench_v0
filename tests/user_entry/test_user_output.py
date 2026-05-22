import csv
import json
import tempfile
import unittest
from pathlib import Path

from sql_rewrite_bench.user_output import build_output_paths, export_run_to_output
from sql_rewrite_bench.user_run_schema import LEDGER_FIELDS


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _base_ledger_row(case_id: str, *, failure_bucket: str = "none") -> dict[str, str]:
    row = {field: "" for field in LEDGER_FIELDS}
    row.update(
        {
            "run_id": "fixture_run",
            "case_id": case_id,
            "pool": "PERF",
            "engine": "postgres",
            "denominator_id": f"track_a_same_engine:{case_id}:postgres",
            "planned": "true",
            "selected": "true",
            "adapter_invoked": "true",
            "candidate_generated": "true",
            "candidate_sql_path": f"runs/user/fixture_run/candidate_sql/{case_id}__postgres.sql",
            "candidate_preflight_status": "passed",
            "candidate_preflight_passed": "true",
            "source_execution_status": "source_execution_success",
            "candidate_execution_status": "candidate_execution_success",
            "checker_status": "checker_success",
            "exact_status": "exact" if failure_bucket == "none" else "mismatch",
            "failure_bucket": failure_bucket,
            "artifact_path": f"runs/user/fixture_run/workspaces/{case_id}/postgres",
            "local_execution_only": "true",
            "official_metric_input": "false",
            "retained_evidence_input": "false",
        }
    )
    return row


def _write_fixture_run(root: Path, *, include_optional: bool = True) -> Path:
    run_dir = root / "runs" / "user" / "fixture_run"
    run_dir.mkdir(parents=True)
    (run_dir / "config.yaml").write_text(
        "\n".join(
            [
                "run_id: fixture_run",
                "created_at_utc: 2026-05-22T00:00:00+00:00",
                "case_set: common_core_v0",
                "engine: postgres",
                "adapter_command: \"python baselines/sqlglot/sqlglot_user_adapter.py --route noop\"",
                "timing_enabled: true",
                "",
            ]
        ),
        encoding="utf-8",
    )
    selected_rows = [
        {
            "run_id": "fixture_run",
            "case_id": "PERF_0006",
            "pool": "PERF",
            "engine": "postgres",
            "denominator_id": "track_a_same_engine:PERF_0006:postgres",
            "planned": "true",
            "case_path": "cases/PERF/PERF_0006",
            "source_sql_path": "cases/PERF/PERF_0006/sql/source.sql",
        }
    ]
    _write_csv(
        run_dir / "selected_cases.csv",
        selected_rows,
        [
            "run_id",
            "case_id",
            "pool",
            "engine",
            "denominator_id",
            "planned",
            "case_path",
            "source_sql_path",
        ],
    )
    ledger_rows = [_base_ledger_row("PERF_0006"), _base_ledger_row("PERF_0007", failure_bucket="mismatch")]
    _write_csv(run_dir / "ledger.csv", ledger_rows, LEDGER_FIELDS)
    _write_csv(
        run_dir / "failures.csv",
        [
            {
                "run_id": "fixture_run",
                "case_id": "PERF_0007",
                "pool": "PERF",
                "engine": "postgres",
                "denominator_id": "track_a_same_engine:PERF_0007:postgres",
                "failure_bucket": "mismatch",
                "artifact_path": "runs/user/fixture_run/workspaces/PERF_0007/postgres",
                "notes": "fixture mismatch",
            }
        ],
        [
            "run_id",
            "case_id",
            "pool",
            "engine",
            "denominator_id",
            "failure_bucket",
            "artifact_path",
            "notes",
        ],
    )
    (run_dir / "summary.json").write_text(
        json.dumps({"run_id": "fixture_run", "selected_rows": 2, "candidate_generated_rows": 2}),
        encoding="utf-8",
    )
    (run_dir / "quality_summary.json").write_text(
        json.dumps(
            {
                "funnel_counts": {
                    "selected_rows": 2,
                    "candidate_generated_rows": 2,
                    "exact_rows": 1,
                    "mismatch_rows": 1,
                }
            }
        ),
        encoding="utf-8",
    )
    if include_optional:
        candidate_dir = run_dir / "candidate_sql"
        candidate_dir.mkdir()
        (candidate_dir / "PERF_0006__postgres.sql").write_text("SELECT 1\n", encoding="utf-8")
        _write_csv(
            run_dir / "tag_slices.csv",
            [
                {
                    "axis": "rewrite_opportunity",
                    "tag": "predicate_pushdown",
                    "selected_rows": "2",
                    "exact_rows": "1",
                    "mismatch_rows": "1",
                }
            ],
            ["axis", "tag", "selected_rows", "exact_rows", "mismatch_rows"],
        )
        execution_dir = run_dir / "workspaces" / "PERF_0006" / "postgres" / "execution"
        checker_dir = run_dir / "workspaces" / "PERF_0006" / "postgres" / "checker"
        execution_dir.mkdir(parents=True)
        checker_dir.mkdir(parents=True)
        (execution_dir / "source_result.jsonl").write_text('{"x": 1}\n', encoding="utf-8")
        (checker_dir / "checker_result.json").write_text('{"exact": true}\n', encoding="utf-8")
        workspace = run_dir / "workspaces" / "PERF_0006" / "postgres"
        (workspace / "adapter_stdout.txt").write_text("adapter stdout\n", encoding="utf-8")
        (workspace / "adapter_stderr.txt").write_text("", encoding="utf-8")
        timing_dir = run_dir / "timing"
        timing_dir.mkdir()
        (timing_dir / "timing_policy.json").write_text(
            json.dumps({"timing_policy_id": "local_exact_gated_default_v0"}),
            encoding="utf-8",
        )
        (timing_dir / "timing_summary.json").write_text(
            json.dumps({"timed_rows": 1}),
            encoding="utf-8",
        )
        metrics_dir = run_dir / "metrics"
        metrics_dir.mkdir()
        (metrics_dir / "local_metrics_summary.json").write_text(
            json.dumps(
                {
                    "schema_version": "local_metrics_summary_v0",
                    "route_ids": ["sqlglot_noop"],
                    "method_ids": ["sqlglot"],
                    "overall": {
                        "counts": {
                            "selected": 2,
                            "candidate_generated": 2,
                            "candidate_executable": 2,
                            "exact": 1,
                        },
                        "rates": {
                            "generation_rate": 1.0,
                            "execution_coverage_rate": 1.0,
                            "result_consistency_rate": 0.5,
                        },
                    },
                }
            ),
            encoding="utf-8",
        )
    return run_dir


def _file_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): path.read_text(encoding="utf-8", errors="replace")
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class UserOutputWriterTests(unittest.TestCase):
    def test_output_path_construction_uses_d035_shape(self) -> None:
        paths = build_output_paths(Path("output"), "run_001")
        self.assertEqual(paths.result_root, Path("output/results/run_001"))
        self.assertEqual(paths.log_root, Path("output/logs/run_001"))
        self.assertEqual(paths.report_root, Path("output/reports/run_001"))

    def test_rejects_bad_run_id_and_top_level_reports_results(self) -> None:
        with self.assertRaises(ValueError):
            build_output_paths(Path("output"), "../bad")
        with self.assertRaises(ValueError):
            build_output_paths(Path("reports"), "run_001")
        with self.assertRaises(ValueError):
            build_output_paths(Path("results"), "run_001")

    def test_export_writes_manifest_boundary_and_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = _write_fixture_run(root)
            before = _file_snapshot(run_dir)
            exported = export_run_to_output(
                run_dir,
                root / "output",
                repo_root=root,
                git_commit="abc123",
            )
            after = _file_snapshot(run_dir)

            self.assertEqual(before, after)
            result_root = exported.paths.result_root
            log_root = exported.paths.log_root
            report_root = exported.paths.report_root
            self.assertTrue((result_root / "run_manifest.json").exists())
            manifest = json.loads((result_root / "run_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["run_id"], "fixture_run")
            self.assertEqual(manifest["git_commit"], "abc123")
            self.assertTrue(manifest["local_diagnostic_only"])
            self.assertFalse(manifest["official_metric_input"])
            self.assertFalse(manifest["paper_result_input"])
            self.assertFalse(manifest["retained_evidence_promoted"])
            self.assertFalse(manifest["leaderboard_input"])
            self.assertEqual(manifest["route_id"], "sqlglot_noop")
            self.assertEqual(manifest["method_id"], "sqlglot")
            self.assertEqual(manifest["timing_policy_id"], "local_exact_gated_default_v0")

            self.assertTrue((result_root / "ledger.csv").exists())
            self.assertTrue((result_root / "quality_summary.json").exists())
            self.assertTrue((result_root / "tag_slices.csv").exists())
            self.assertTrue((result_root / "failure_buckets.csv").exists())
            self.assertTrue((result_root / "candidates" / "PERF_0006__postgres.sql").exists())
            self.assertTrue((result_root / "execution" / "PERF_0006" / "postgres" / "source_result.jsonl").exists())
            self.assertTrue((result_root / "checker" / "PERF_0006" / "postgres" / "checker_result.json").exists())
            self.assertTrue((result_root / "timing" / "timing_policy.json").exists())
            self.assertTrue((result_root / "metrics" / "local_metrics_summary.json").exists())
            self.assertTrue((result_root / "verifier" / "verifier_status.json").exists())

            self.assertIn("adapter stdout", (log_root / "adapter_stdout.log").read_text(encoding="utf-8"))
            self.assertTrue((log_root / "command.log").exists())
            self.assertTrue((log_root / "engine_env.json").exists())
            self.assertTrue((log_root / "failures.log").exists())
            self.assertTrue((log_root / "timing.log").exists())
            self.assertTrue((log_root / "verifier.log").exists())

            boundary = (report_root / "boundary.md").read_text(encoding="utf-8")
            self.assertIn("local diagnostic output only", boundary)
            self.assertIn("not official metrics", boundary)
            self.assertIn("not paper results", boundary)
            self.assertIn("not retained evidence", boundary)
            self.assertIn("not leaderboard input", boundary)
            self.assertTrue((report_root / "summary.md").exists())
            self.assertTrue((report_root / "failure_buckets.md").exists())
            self.assertTrue((report_root / "tag_slices.md").exists())
            self.assertTrue((report_root / "metrics_summary.md").exists())
            self.assertTrue((report_root / "verifier_summary.md").exists())
            self.assertFalse((root / "reports").exists())
            self.assertFalse((root / "results").exists())

    def test_failure_buckets_are_derived_from_existing_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = _write_fixture_run(root)
            export_run_to_output(run_dir, root / "output", repo_root=root)
            with (root / "output" / "results" / "fixture_run" / "failure_buckets.csv").open(
                newline="", encoding="utf-8"
            ) as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["failure_bucket"], "mismatch")
        self.assertEqual(rows[0]["count"], "1")
        self.assertEqual(rows[0]["representative_cases"], "PERF_0007")

    def test_missing_optional_artifacts_create_na_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = _write_fixture_run(root, include_optional=False)
            exported = export_run_to_output(run_dir, root / "output", repo_root=root)
            result_root = exported.paths.result_root
            report_root = exported.paths.report_root

            self.assertFalse((result_root / "tag_slices.csv").exists())
            self.assertFalse((result_root / "metrics").exists())
            self.assertIn(
                "Tag slices are not available",
                (report_root / "tag_slices.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Local metrics were not computed",
                (report_root / "metrics_summary.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Verifier support was not run",
                (report_root / "verifier_summary.md").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
