import csv
import json
import shutil
import sys
import tempfile
import unittest
import uuid
from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from sql_rewrite_bench.case_selection import SelectedCaseEngineRow
from sql_rewrite_bench.local_timing import (
    TIMING_STATUS_NOT_ELIGIBLE,
    TIMING_STATUS_PARTIAL_FAILURE,
    TIMING_STATUS_TIMED,
    TimingPolicy,
    TimingSamples,
    collect_timing_for_row,
    route_identity,
    write_environment_metadata,
)
from sql_rewrite_bench.user_run import run_user_benchmark
from sql_rewrite_bench.user_run_schema import (
    CANDIDATE_PREFLIGHT_STATUS_PASSED,
    CHECKER_STATUS_SUCCESS,
    DIAGNOSTIC_MODE_SAME_ENGINE,
    DIAGNOSTIC_MODE_UNSUPPORTED,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_MISMATCH,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    EXECUTION_STATUS_UNSUPPORTED,
    FAILURE_MISMATCH,
    FAILURE_NONE,
    FAILURE_UNSUPPORTED_ENGINE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _unique_out(name: str) -> Path:
    return Path("runs/user") / f"{name}_{uuid.uuid4().hex}"


def _case_list(tmp_path: Path, *case_ids: str) -> Path:
    path = tmp_path / "case_ids.txt"
    path.write_text("\n".join(case_ids) + "\n", encoding="utf-8")
    return path


def _user_args(out: Path, case_list: Path, adapter: Path) -> Namespace:
    return Namespace(
        case_set="common_core_v0",
        pool="PERF",
        engine="postgres",
        case_list=case_list,
        smoke=False,
        adapter_command=f"{sys.executable} {adapter}",
        out=out,
        run_id=None,
        adapter_timeout=30,
        dry_run=False,
        enable_db_execution=False,
        enable_checker=False,
        postgres_dsn_env="SQLRB_POSTGRES_DSN",
        execution_timeout_sec=30,
        db_schema_prefix="sqlrb_user",
    )


def _row(root: Path) -> SelectedCaseEngineRow:
    return SelectedCaseEngineRow(
        denominator_id="PERF_TEST__postgres",
        case_id="PERF_TEST",
        pool="PERF",
        engine="postgres",
        planned="true",
        case_path="cases/PERF/PERF_TEST",
        source_sql_path="cases/PERF/PERF_TEST/sql/source.sql",
    )


def _package(mode: str = DIAGNOSTIC_MODE_SAME_ENGINE) -> SimpleNamespace:
    return SimpleNamespace(
        diagnostic_mode=mode,
        source_reference_query_path=Path("unused.sql"),
    )


def _write_case_files(root: Path) -> tuple[SelectedCaseEngineRow, Path, Path]:
    row = _row(root)
    source = root / row.source_sql_path
    candidate = root / "runs" / "user" / "timing_test" / "candidate.sql"
    source.parent.mkdir(parents=True)
    candidate.parent.mkdir(parents=True)
    source.write_text("select 1;\n", encoding="utf-8")
    candidate.write_text("select 1;\n", encoding="utf-8")
    return row, source, candidate


def _base_ledger(candidate: Path, root: Path) -> dict[str, object]:
    return {
        "candidate_generated": "true",
        "candidate_sql_path": candidate.resolve().relative_to(root.resolve()).as_posix(),
        "candidate_preflight_status": CANDIDATE_PREFLIGHT_STATUS_PASSED,
        "source_execution_status": EXECUTION_STATUS_SOURCE_SUCCESS,
        "candidate_execution_status": EXECUTION_STATUS_CANDIDATE_SUCCESS,
        "checker_status": CHECKER_STATUS_SUCCESS,
        "exact_status": EXACT_STATUS_EXACT,
        "failure_bucket": FAILURE_NONE,
        "source_result_path": "runs/user/timing_test/source_result.jsonl",
        "candidate_result_path": "runs/user/timing_test/candidate_result.jsonl",
        "mismatch_artifact_path": "",
        "notes": "exact",
    }


class LocalTimingTests(unittest.TestCase):
    def test_timing_disabled_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _unique_out("unittest_timing_disabled")
            self.addCleanup(shutil.rmtree, REPO_ROOT / out, ignore_errors=True)
            adapter = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "dummy_adapter.py"
            summary = run_user_benchmark(_user_args(out, case_list, adapter), REPO_ROOT)

        self.assertFalse((REPO_ROOT / out / "timing").exists())
        self.assertFalse(summary["timing_enabled"])
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["timing_status"], "not_requested")
        self.assertEqual(rows[0]["speedup_ratio"], "")

    def test_exact_row_becomes_timing_eligible_and_writes_claim_flags(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row, _source, candidate = _write_case_files(root)
            timing_dir = root / "runs" / "user" / "timing_test" / "timing"
            environment = write_environment_metadata(timing_dir, repo_root=root, run_id="timing_test")
            policy = TimingPolicy(warmup_count=0, measured_repetitions=2)
            ledger = _base_ledger(candidate, root)
            with mock.patch(
                "sql_rewrite_bench.local_timing._collect_samples_for_engine",
                return_value=TimingSamples([4.0, 6.0], [2.0, 3.0], "test-engine"),
            ):
                result = collect_timing_for_row(
                    ledger=ledger,
                    row=row,
                    resolved_package=_package(),
                    repo_root=root,
                    out_dir=root / "runs" / "user" / "timing_test",
                    run_id="timing_test",
                    adapter_command="python baselines/sqlglot/sqlglot_user_adapter.py --route noop",
                    policy=policy,
                    postgres_dsn_env="SQLRB_POSTGRES_DSN",
                    db_schema_prefix="sqlrb_user",
                    timing_dir=timing_dir,
                    environment_metadata_path=environment,
                )
            payload = json.loads(result.timing_artifact_path.read_text(encoding="utf-8"))

        self.assertTrue(result.timing_eligible)
        self.assertEqual(result.timing_status, TIMING_STATUS_TIMED)
        self.assertEqual(payload["route_id"], "sqlglot_noop")
        self.assertEqual(payload["method_id"], "sqlglot")
        self.assertEqual(payload["timing_status"], TIMING_STATUS_TIMED)
        self.assertEqual(payload["source_median_ms"], 5.0)
        self.assertEqual(payload["candidate_median_ms"], 2.5)
        self.assertEqual(payload["speedup_ratio"], 2.0)
        self.assertEqual(len(payload["source_sql_hash"]), 64)
        self.assertEqual(len(payload["candidate_sql_hash"]), 64)
        self.assertEqual(payload["claim_boundary"], "local_diagnostic_only")
        self.assertTrue(payload["local_diagnostic_only"])
        self.assertFalse(payload["official_metric_input"])
        self.assertFalse(payload["paper_result_input"])
        self.assertFalse(payload["retained_evidence_promoted"])
        self.assertFalse(payload["leaderboard_input"])

    def test_mismatch_row_is_timing_ineligible(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row, _source, candidate = _write_case_files(root)
            timing_dir = root / "runs" / "user" / "timing_test" / "timing"
            environment = write_environment_metadata(timing_dir, repo_root=root, run_id="timing_test")
            ledger = _base_ledger(candidate, root)
            ledger["exact_status"] = EXACT_STATUS_MISMATCH
            ledger["failure_bucket"] = FAILURE_MISMATCH
            result = collect_timing_for_row(
                ledger=ledger,
                row=row,
                resolved_package=_package(),
                repo_root=root,
                out_dir=root / "runs" / "user" / "timing_test",
                run_id="timing_test",
                adapter_command="python adapter.py",
                policy=TimingPolicy(),
                postgres_dsn_env="SQLRB_POSTGRES_DSN",
                db_schema_prefix="sqlrb_user",
                timing_dir=timing_dir,
                environment_metadata_path=environment,
            )
            payload = json.loads(result.timing_artifact_path.read_text(encoding="utf-8"))

        self.assertFalse(result.timing_eligible)
        self.assertEqual(result.timing_status, TIMING_STATUS_NOT_ELIGIBLE)
        self.assertIsNone(payload["speedup_ratio"])
        self.assertEqual(payload["timing_na_reason"], "checker_mismatch")

    def test_label_only_mismatch_is_timing_ineligible_under_strict_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row, _source, candidate = _write_case_files(root)
            timing_dir = root / "runs" / "user" / "timing_test" / "timing"
            environment = write_environment_metadata(timing_dir, repo_root=root, run_id="timing_test")
            ledger = _base_ledger(candidate, root)
            ledger["exact_status"] = EXACT_STATUS_MISMATCH
            ledger["failure_bucket"] = FAILURE_MISMATCH
            ledger["notes"] = "checker mismatch; value_exact=true, label_exact=false, label_only_mismatch=true"
            result = collect_timing_for_row(
                ledger=ledger,
                row=row,
                resolved_package=_package(),
                repo_root=root,
                out_dir=root / "runs" / "user" / "timing_test",
                run_id="timing_test",
                adapter_command="python adapter.py",
                policy=TimingPolicy(),
                postgres_dsn_env="SQLRB_POSTGRES_DSN",
                db_schema_prefix="sqlrb_user",
                timing_dir=timing_dir,
                environment_metadata_path=environment,
            )
            payload = json.loads(result.timing_artifact_path.read_text(encoding="utf-8"))

        self.assertFalse(result.timing_eligible)
        self.assertEqual(payload["timing_na_reason"], "label_only_mismatch")
        self.assertTrue(payload["label_only_mismatch"])

    def test_unsupported_row_is_timing_ineligible(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row, _source, candidate = _write_case_files(root)
            timing_dir = root / "runs" / "user" / "timing_test" / "timing"
            environment = write_environment_metadata(timing_dir, repo_root=root, run_id="timing_test")
            ledger = _base_ledger(candidate, root)
            ledger["source_execution_status"] = EXECUTION_STATUS_UNSUPPORTED
            ledger["candidate_execution_status"] = EXECUTION_STATUS_UNSUPPORTED
            ledger["failure_bucket"] = FAILURE_UNSUPPORTED_ENGINE
            result = collect_timing_for_row(
                ledger=ledger,
                row=row,
                resolved_package=_package(DIAGNOSTIC_MODE_UNSUPPORTED),
                repo_root=root,
                out_dir=root / "runs" / "user" / "timing_test",
                run_id="timing_test",
                adapter_command="python adapter.py",
                policy=TimingPolicy(),
                postgres_dsn_env="SQLRB_POSTGRES_DSN",
                db_schema_prefix="sqlrb_user",
                timing_dir=timing_dir,
                environment_metadata_path=environment,
            )
            payload = json.loads(result.timing_artifact_path.read_text(encoding="utf-8"))

        self.assertFalse(result.timing_eligible)
        self.assertEqual(payload["timing_na_reason"], "unsupported_fail_closed")

    def test_partial_timing_failure_has_null_speedup(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row, _source, candidate = _write_case_files(root)
            timing_dir = root / "runs" / "user" / "timing_test" / "timing"
            environment = write_environment_metadata(timing_dir, repo_root=root, run_id="timing_test")
            policy = TimingPolicy(warmup_count=0, measured_repetitions=2)
            with mock.patch(
                "sql_rewrite_bench.local_timing._collect_samples_for_engine",
                return_value=TimingSamples([4.0, 6.0], [2.0], "test-engine"),
            ):
                result = collect_timing_for_row(
                    ledger=_base_ledger(candidate, root),
                    row=row,
                    resolved_package=_package(),
                    repo_root=root,
                    out_dir=root / "runs" / "user" / "timing_test",
                    run_id="timing_test",
                    adapter_command="python adapter.py",
                    policy=policy,
                    postgres_dsn_env="SQLRB_POSTGRES_DSN",
                    db_schema_prefix="sqlrb_user",
                    timing_dir=timing_dir,
                    environment_metadata_path=environment,
                )
            payload = json.loads(result.timing_artifact_path.read_text(encoding="utf-8"))

        self.assertTrue(result.timing_eligible)
        self.assertEqual(result.timing_status, TIMING_STATUS_PARTIAL_FAILURE)
        self.assertIsNone(payload["speedup_ratio"])
        self.assertEqual(payload["timing_na_reason"], "timing_partial_failure")

    def test_route_identity_prevents_route_mixing(self) -> None:
        self.assertEqual(
            route_identity("python baselines/sqlglot/sqlglot_user_adapter.py --route noop"),
            ("sqlglot_noop", "sqlglot"),
        )
        self.assertEqual(
            route_identity("python baselines/sqlglot/sqlglot_user_adapter.py --route optimize"),
            ("sqlglot_optimize", "sqlglot"),
        )
        self.assertEqual(
            route_identity(
                "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware"
            ),
            ("sqlglot_optimize_schema_aware", "sqlglot"),
        )


if __name__ == "__main__":
    unittest.main()
