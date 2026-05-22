import csv
import json
import tempfile
import unittest
from pathlib import Path

from sql_rewrite_bench.local_metrics import compute_and_write_local_metrics, compute_local_metrics
from sql_rewrite_bench.user_run_schema import LEDGER_FIELDS


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _base_row(case_id: str, *, pool: str = "PERF") -> dict[str, str]:
    row = {field: "" for field in LEDGER_FIELDS}
    row.update(
        {
            "run_id": "fixture_run",
            "case_id": case_id,
            "pool": pool,
            "engine": "postgres",
            "denominator_id": f"track_a_same_engine:{case_id}:postgres",
            "planned": "true",
            "selected": "true",
            "adapter_invoked": "true",
            "adapter_exit_code": "0",
            "candidate_generated": "true",
            "candidate_preflight_status": "passed",
            "candidate_preflight_passed": "true",
            "source_execution_status": "source_execution_success",
            "candidate_execution_status": "candidate_execution_success",
            "checker_status": "checker_success",
            "exact_status": "exact",
            "failure_bucket": "none",
            "timing_eligible": "false",
            "timing_status": "not_requested",
            "timed_status": "not_requested",
            "local_execution_only": "true",
            "official_metric_input": "false",
            "retained_evidence_input": "false",
        }
    )
    return row


def _write_timing_row(
    run_dir: Path,
    row: dict[str, str],
    *,
    speedup: float | None,
    route_id: str = "sqlglot_noop",
    timing_status: str = "timed",
    timing_eligible: bool = True,
    label_only: bool = False,
) -> str:
    rows_dir = run_dir / "timing" / "rows"
    rows_dir.mkdir(parents=True, exist_ok=True)
    path = rows_dir / f"{row['case_id']}__{row['engine']}__{route_id}.json"
    payload = {
        "schema_version": "timing_artifact_schema_v0",
        "route_id": route_id,
        "method_id": "sqlglot",
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "denominator_id": row["denominator_id"],
        "candidate_id": f"{row['case_id']}__candidate",
        "local_run_id": row["run_id"],
        "timing_policy_id": "local_exact_gated_default_v0",
        "exact_status": row["exact_status"],
        "failure_bucket": row["failure_bucket"],
        "label_only_mismatch": label_only,
        "timing_eligible": timing_eligible,
        "timing_status": timing_status,
        "timing_na_reason": None if timing_status == "timed" else timing_status,
        "source_runtime_samples_ms": [10.0, 12.0],
        "candidate_runtime_samples_ms": [5.0, 6.0],
        "source_median_ms": 11.0 if speedup is not None else None,
        "candidate_median_ms": (11.0 / speedup) if speedup else None,
        "speedup_ratio": speedup,
        "source_sql_hash": "a" * 64,
        "candidate_sql_hash": "b" * 64,
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result_input": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path.as_posix()


def _write_fixture_run(root: Path) -> Path:
    run_dir = root / "runs" / "user" / "fixture_run"
    run_dir.mkdir(parents=True)
    (run_dir / "config.yaml").write_text(
        "run_id: fixture_run\nadapter_command: python baselines/sqlglot/sqlglot_user_adapter.py --route noop\n",
        encoding="utf-8",
    )
    rows = []
    exact_a = _base_row("PERF_A")
    exact_b = _base_row("PERF_B")
    mismatch = _base_row("PERF_C")
    mismatch.update({"exact_status": "mismatch", "failure_bucket": "mismatch"})
    label_only = _base_row("PERF_D")
    label_only.update(
        {
            "exact_status": "mismatch",
            "failure_bucket": "mismatch",
            "notes": "value_exact=true, label_exact=false, label_only_mismatch=true",
        }
    )
    unsupported = _base_row("PERF_E")
    unsupported.update(
        {
            "candidate_generated": "false",
            "candidate_preflight_status": "not_run",
            "candidate_preflight_passed": "false",
            "source_execution_status": "execution_unsupported",
            "candidate_execution_status": "execution_unsupported",
            "checker_status": "checker_unsupported",
            "exact_status": "not_exact_due_to_execution_failure",
            "failure_bucket": "unsupported_engine",
        }
    )
    rows.extend([exact_a, exact_b, mismatch, label_only, unsupported])
    for row, speedup in [(exact_a, 2.0), (exact_b, 8.0)]:
        artifact = _write_timing_row(run_dir, row, speedup=speedup)
        row.update(
            {
                "timing_eligible": "true",
                "timing_status": "timed",
                "timed_status": "timed",
                "timing_artifact_path": artifact,
                "speedup_ratio": str(speedup),
            }
        )
    artifact = _write_timing_row(run_dir, label_only, speedup=None, timing_status="not_eligible", timing_eligible=False, label_only=True)
    label_only.update(
        {
            "timing_eligible": "false",
            "timing_status": "not_eligible",
            "timed_status": "not_eligible",
            "timing_artifact_path": artifact,
        }
    )
    _write_csv(run_dir / "ledger.csv", rows)
    return run_dir


class LocalMetricsTests(unittest.TestCase):
    def test_d033_rates_and_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = _write_fixture_run(Path(tmp))
            metrics = compute_local_metrics(run_dir)["summary"]

        overall = metrics["overall"]
        self.assertEqual(overall["counts"]["selected"], 5)
        self.assertEqual(overall["counts"]["candidate_generated"], 4)
        self.assertEqual(overall["rates"]["generation_rate"], 0.8)
        self.assertEqual(overall["counts"]["preflight_passed"], 4)
        self.assertFalse(overall["diagnostics"]["preflight_passed_is_metric_numerator"])
        self.assertEqual(overall["counts"]["candidate_executable"], 4)
        self.assertEqual(overall["rates"]["execution_coverage_rate"], 0.8)
        self.assertEqual(overall["counts"]["source_executable"], 4)
        self.assertFalse(overall["diagnostics"]["source_executable_is_metric_numerator"])
        self.assertEqual(overall["counts"]["exact"], 2)
        self.assertEqual(overall["rates"]["result_consistency_rate"], 0.4)
        self.assertEqual(overall["counts"]["unsupported_fail_closed"], 1)

    def test_exact_timed_rows_enter_speedup_metrics_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = _write_fixture_run(Path(tmp))
            payload = compute_local_metrics(run_dir)

        performance = payload["summary"]["overall"]["performance"]
        self.assertEqual(performance["speedup_denominator"], 2)
        self.assertEqual(performance["gm_speedup_ratio"], 4.0)
        self.assertAlmostEqual(performance["speedup_percentiles"]["p10"], 2.6)
        self.assertAlmostEqual(performance["speedup_percentiles"]["p25"], 3.5)
        self.assertAlmostEqual(performance["speedup_percentiles"]["p50"], 5.0)
        self.assertAlmostEqual(performance["speedup_percentiles"]["p75"], 6.5)
        self.assertAlmostEqual(performance["speedup_percentiles"]["p90"], 7.4)
        excluded = {
            row["case_id"]: row["exclusion_reason"]
            for row in payload["speedup_rows"]
            if row["included_in_performance"] == "false"
        }
        self.assertEqual(excluded["PERF_C"], "not_exact")
        self.assertEqual(excluded["PERF_D"], "not_exact")
        self.assertEqual(excluded["PERF_E"], "not_exact")

    def test_missing_timing_produces_na_performance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "runs" / "user" / "no_timing"
            run_dir.mkdir(parents=True)
            (run_dir / "config.yaml").write_text(
                "run_id: no_timing\nadapter_command: python adapter.py\n",
                encoding="utf-8",
            )
            _write_csv(run_dir / "ledger.csv", [_base_row("PERF_A")])
            metrics = compute_local_metrics(run_dir)["summary"]

        self.assertIsNone(metrics["overall"]["performance"]["gm_speedup_ratio"])
        self.assertEqual(metrics["overall"]["performance"]["performance_na_reason"], "no_exact_timed_rows")

    def test_partial_timing_failure_produces_na_performance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "runs" / "user" / "partial"
            run_dir.mkdir(parents=True)
            (run_dir / "config.yaml").write_text(
                "run_id: partial\nadapter_command: python adapter.py\n",
                encoding="utf-8",
            )
            row = _base_row("PERF_A")
            artifact = _write_timing_row(run_dir, row, speedup=None, timing_status="partial_failure")
            row.update({"timing_eligible": "true", "timing_status": "partial_failure", "timed_status": "partial_failure", "timing_artifact_path": artifact})
            _write_csv(run_dir / "ledger.csv", [row])
            payload = compute_local_metrics(run_dir)

        self.assertIsNone(payload["summary"]["overall"]["performance"]["gm_speedup_ratio"])
        self.assertEqual(payload["speedup_rows"][0]["exclusion_reason"], "timing_partial_failure")

    def test_route_grouping_prevents_route_mixing_and_no_leaderboard_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "runs" / "user" / "routes"
            run_dir.mkdir(parents=True)
            (run_dir / "config.yaml").write_text(
                "run_id: routes\nadapter_command: python adapter.py\n",
                encoding="utf-8",
            )
            row_a = _base_row("PERF_A")
            row_b = _base_row("PERF_B")
            row_b["denominator_id"] = "track_a_same_engine:PERF_B:postgres"
            for row, route in [(row_a, "sqlglot_noop"), (row_b, "sqlglot_optimize")]:
                artifact = _write_timing_row(run_dir, row, speedup=2.0, route_id=route)
                row.update({"timing_eligible": "true", "timing_status": "timed", "timed_status": "timed", "timing_artifact_path": artifact, "speedup_ratio": "2.0"})
            _write_csv(run_dir / "ledger.csv", [row_a, row_b])
            metrics = compute_local_metrics(run_dir)["summary"]

        self.assertEqual(metrics["route_ids"], ["sqlglot_noop", "sqlglot_optimize"])
        self.assertEqual(len(metrics["by_engine"]), 2)
        serialized = json.dumps(metrics)
        self.assertNotIn("winner", serialized)
        self.assertNotIn("best_method", serialized)
        self.assertFalse(metrics["prohibited_outputs"]["method_selection_output_emitted"])

    def test_deferred_metrics_and_boundaries_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = _write_fixture_run(Path(tmp))
            outputs = compute_and_write_local_metrics(run_dir)
            summary = json.loads(outputs.summary_path.read_text(encoding="utf-8"))
            self.assertTrue(outputs.by_engine_path.exists())
            self.assertTrue(outputs.by_pool_path.exists())
            self.assertTrue(outputs.speedup_rows_path.exists())
            self.assertTrue(outputs.boundary_path.exists())

        self.assertTrue(summary["local_diagnostic_only"])
        self.assertFalse(summary["official_metric_input"])
        self.assertFalse(summary["paper_result_input"])
        self.assertFalse(summary["retained_evidence_promoted"])
        self.assertFalse(summary["leaderboard_input"])
        self.assertEqual(summary["deferred_metrics"]["semantic_equivalence_rate"]["status"], "not_applicable")
        self.assertEqual(summary["deferred_metrics"]["cross_engine_gm_speedup_ratio"]["status"], "not_applicable")
        self.assertTrue(summary["deferred_metrics"]["positive_operation_coverage_rate"]["skill_adapter_pending"])


if __name__ == "__main__":
    unittest.main()
