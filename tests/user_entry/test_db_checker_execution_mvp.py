import csv
import json
import sys
import tempfile
import unittest
import uuid
from argparse import Namespace
from pathlib import Path

from sql_rewrite_bench.local_result_checker import run_local_checker
from sql_rewrite_bench.user_run import run_user_benchmark, validate_output_root
from sql_rewrite_bench.user_run_schema import (
    CHECKER_STATUS_CONFIG_MISSING,
    CHECKER_STATUS_NORMALIZATION_MISSING,
    CHECKER_STATUS_SUCCESS,
    CHECKER_STATUS_VALUES,
    EXACT_STATUS_CHECKER_MISSING,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_VALUES,
    EXECUTION_STATUS_NON_DB,
    EXECUTION_STATUS_VALUES,
    FAILURE_BUCKET_VALUES,
    FAILURE_MISMATCH,
    FAILURE_NONE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _case_list(tmp_path: Path, *case_ids: str) -> Path:
    path = tmp_path / "case_ids.txt"
    path.write_text("\n".join(case_ids) + "\n", encoding="utf-8")
    return path


def _unique_out(name: str) -> Path:
    return Path("runs/user") / f"{name}_{uuid.uuid4().hex}"


def _args(out: Path, case_list: Path, *, enable_checker: bool = False) -> Namespace:
    adapter = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "dummy_adapter.py"
    return Namespace(
        case_set="common_core_v0",
        pool="PERF",
        engine="postgres",
        case_list=case_list,
        adapter_command=f"{sys.executable} {adapter}",
        out=out,
        run_id=None,
        adapter_timeout=30,
        dry_run=False,
        enable_db_execution=False,
        enable_checker=enable_checker,
        postgres_dsn_env="SQLRB_POSTGRES_DSN",
        execution_timeout_sec=30,
        db_schema_prefix="sqlrb_user",
    )


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def _write_checker_configs(case_dir: Path, *, normalization: bool = True, compare: bool = True) -> None:
    checker_dir = case_dir / "checker"
    checker_dir.mkdir(parents=True, exist_ok=True)
    (checker_dir / "checker.yaml").write_text("case_id: TEST\n", encoding="utf-8")
    if normalization:
        (checker_dir / "normalization.yaml").write_text(
            "sort_rows: true\ntrim_whitespace: true\nnormalize_numeric_format: true\n",
            encoding="utf-8",
        )
    if compare:
        (checker_dir / "compare_config.yaml").write_text(
            "reference_engine: postgres\n", encoding="utf-8"
        )


class DbCheckerExecutionMvpTests(unittest.TestCase):
    def test_non_db_user_run_has_extended_ledger_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            out = _unique_out("unittest_db_checker_non_db")
            summary = run_user_benchmark(_args(out, case_list), REPO_ROOT)
        self.assertEqual(summary["selected_rows"], 1)
        self.assertIs(summary["db_execution_enabled"], False)
        self.assertIs(summary["checker_enabled"], False)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["execution_enabled"], "false")
        self.assertEqual(rows[0]["checker_enabled"], "false")
        self.assertEqual(rows[0]["source_execution_status"], EXECUTION_STATUS_NON_DB)
        self.assertEqual(rows[0]["candidate_execution_status"], EXECUTION_STATUS_NON_DB)
        self.assertEqual(rows[0]["local_execution_only"], "true")
        self.assertEqual(rows[0]["official_metric_input"], "false")
        self.assertEqual(rows[0]["retained_evidence_input"], "false")
        self.assertFalse((REPO_ROOT / out / "leaderboard.csv").exists())

    def test_checker_requires_db_execution_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "PERF_0006")
            args = _args(_unique_out("unittest_checker_without_db"), case_list, enable_checker=True)
            with self.assertRaisesRegex(ValueError, "--enable-checker requires"):
                run_user_benchmark(args, REPO_ROOT)

    def test_invalid_output_roots_still_rejected(self) -> None:
        for invalid in [
            Path("cases/PERF/PERF_0006/runs/demo"),
            Path("results/retained/demo"),
            Path("reports/evaluation/demo"),
            Path("/tmp/demo"),
            Path("../demo"),
        ]:
            with self.assertRaisesRegex(ValueError, "runs/user"):
                validate_output_root(invalid, REPO_ROOT)

    def test_status_vocabulary_contains_db_checker_values(self) -> None:
        self.assertIn("source_execution_success", EXECUTION_STATUS_VALUES)
        self.assertIn("candidate_execution_success", EXECUTION_STATUS_VALUES)
        self.assertIn("checker_success", CHECKER_STATUS_VALUES)
        self.assertIn("checker_mismatch", CHECKER_STATUS_VALUES)
        self.assertIn("exact", EXACT_STATUS_VALUES)
        self.assertIn(FAILURE_MISMATCH, FAILURE_BUCKET_VALUES)

    def test_local_checker_exact_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "case"
            _write_checker_configs(case_dir)
            source = root / "source.jsonl"
            candidate = root / "candidate.jsonl"
            rows = [{"a": "1.00", "b": " x "}, {"a": "2", "b": "y"}]
            _write_jsonl(source, rows)
            _write_jsonl(candidate, list(reversed(rows)))
            result = run_local_checker(
                case_dir=case_dir,
                source_result_path=source,
                candidate_result_path=candidate,
                checker_dir=root / "checker_out",
            )
        self.assertEqual(result.checker_status, CHECKER_STATUS_SUCCESS)
        self.assertEqual(result.exact_status, EXACT_STATUS_EXACT)
        self.assertEqual(result.failure_bucket, FAILURE_NONE)

    def test_local_checker_mismatch_writes_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "case"
            _write_checker_configs(case_dir)
            source = root / "source.jsonl"
            candidate = root / "candidate.jsonl"
            _write_jsonl(source, [{"a": "1"}])
            _write_jsonl(candidate, [{"a": "2"}])
            result = run_local_checker(
                case_dir=case_dir,
                source_result_path=source,
                candidate_result_path=candidate,
                checker_dir=root / "checker_out",
            )
            self.assertEqual(result.failure_bucket, FAILURE_MISMATCH)
            self.assertIsNotNone(result.mismatch_artifact_path)
            self.assertTrue(result.mismatch_artifact_path.exists())

    def test_missing_normalization_config_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "case"
            _write_checker_configs(case_dir, normalization=False)
            source = root / "source.jsonl"
            candidate = root / "candidate.jsonl"
            _write_jsonl(source, [{"a": "1"}])
            _write_jsonl(candidate, [{"a": "1"}])
            result = run_local_checker(
                case_dir=case_dir,
                source_result_path=source,
                candidate_result_path=candidate,
                checker_dir=root / "checker_out",
            )
        self.assertEqual(result.checker_status, CHECKER_STATUS_NORMALIZATION_MISSING)
        self.assertEqual(result.exact_status, EXACT_STATUS_CHECKER_MISSING)

    def test_missing_compare_config_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "case"
            _write_checker_configs(case_dir, compare=False)
            source = root / "source.jsonl"
            candidate = root / "candidate.jsonl"
            _write_jsonl(source, [{"a": "1"}])
            _write_jsonl(candidate, [{"a": "1"}])
            result = run_local_checker(
                case_dir=case_dir,
                source_result_path=source,
                candidate_result_path=candidate,
                checker_dir=root / "checker_out",
            )
        self.assertEqual(result.checker_status, CHECKER_STATUS_CONFIG_MISSING)
        self.assertEqual(result.exact_status, EXACT_STATUS_CHECKER_MISSING)


if __name__ == "__main__":
    unittest.main()
