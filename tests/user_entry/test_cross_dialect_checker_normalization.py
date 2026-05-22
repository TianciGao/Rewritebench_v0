import json
import tempfile
import unittest
from pathlib import Path

from sql_rewrite_bench.case_package_resolver import resolve_case_package
from sql_rewrite_bench.case_selection import resolve_common_core_selection
from sql_rewrite_bench.local_result_checker import run_local_checker
from sql_rewrite_bench.user_run import (
    _cross_dialect_checker_normalization_enabled,
    _mysql_to_spark_numeric_equivalence_enabled,
)
from sql_rewrite_bench.user_run_schema import (
    CHECKER_STATUS_MISMATCH,
    CHECKER_STATUS_SUCCESS,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_MISMATCH,
    FAILURE_MISMATCH,
    FAILURE_NONE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def _write_checker_configs(case_dir: Path, *, normalize_numeric: bool = True) -> None:
    checker_dir = case_dir / "checker"
    checker_dir.mkdir(parents=True, exist_ok=True)
    (checker_dir / "checker.yaml").write_text("case_id: TEST\n", encoding="utf-8")
    normalization = "sort_rows: true\ntrim_whitespace: true\n"
    if normalize_numeric:
        normalization += "normalize_numeric_format: true\n"
    (checker_dir / "normalization.yaml").write_text(normalization, encoding="utf-8")
    (checker_dir / "compare_config.yaml").write_text(
        "reference_engine: postgres\n", encoding="utf-8"
    )


def _case_list(tmp_path: Path, case_id: str) -> Path:
    path = tmp_path / "case_ids.txt"
    path.write_text(case_id + "\n", encoding="utf-8")
    return path


def _selected_row(case_id: str, *, engine: str = "postgres"):
    with tempfile.TemporaryDirectory() as temp_dir:
        rows = resolve_common_core_selection(
            repo_root=REPO_ROOT,
            case_set="common_core_v0",
            engine=engine,
            case_list=_case_list(Path(temp_dir), case_id),
        )
    if len(rows) != 1:
        raise AssertionError(f"expected one selected row for {case_id}")
    return rows[0]


class CrossDialectCheckerNormalizationTests(unittest.TestCase):
    def _run_synthetic_checker(
        self,
        source_rows: list[dict[str, object]],
        candidate_rows: list[dict[str, object]],
        *,
        enable_cross_dialect_normalization: bool,
        enable_mixed_numeric_equivalence: bool = False,
        normalize_numeric: bool = True,
    ):
        root = Path(self.enterContext(tempfile.TemporaryDirectory()))
        case_dir = root / "case"
        _write_checker_configs(case_dir, normalize_numeric=normalize_numeric)
        source = root / "source.jsonl"
        candidate = root / "candidate.jsonl"
        _write_jsonl(source, source_rows)
        _write_jsonl(candidate, candidate_rows)
        return run_local_checker(
            case_dir=case_dir,
            source_result_path=source,
            candidate_result_path=candidate,
            checker_dir=root / "checker_out",
            enable_cross_dialect_normalization=enable_cross_dialect_normalization,
            enable_mixed_numeric_equivalence=enable_mixed_numeric_equivalence,
        )

    def test_cross_dialect_single_column_different_labels_can_match(self) -> None:
        result = self._run_synthetic_checker(
            [{"mysql_expr": "50"}],
            [{"?column?": "50"}],
            enable_cross_dialect_normalization=True,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_SUCCESS)
        self.assertEqual(result.exact_status, EXACT_STATUS_EXACT)
        self.assertEqual(result.failure_bucket, FAILURE_NONE)
        self.assertTrue(result.details["cross_dialect_normalization_active"])
        self.assertTrue(result.details["positional_column_comparison_used"])

    def test_cross_dialect_multi_column_compares_by_position(self) -> None:
        result = self._run_synthetic_checker(
            [{"source_first": "1", "source_second": "x"}],
            [{"target_first": "1", "target_second": "x"}],
            enable_cross_dialect_normalization=True,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_SUCCESS)
        self.assertTrue(result.details["positional_column_comparison_used"])

    def test_cross_dialect_decimal_strings_can_match(self) -> None:
        result = self._run_synthetic_checker(
            [{"mysql_expr": "1.0"}],
            [{"?column?": "1.000000"}],
            enable_cross_dialect_normalization=True,
            normalize_numeric=False,
        )

        self.assertEqual(result.exact_status, EXACT_STATUS_EXACT)
        self.assertTrue(result.details["decimal_string_equivalence_used"])

    def test_mysql_spark_mixed_numeric_equivalence_can_match_when_opted_in(self) -> None:
        result = self._run_synthetic_checker(
            [{"mysql_expr": "4.80"}],
            [{"spark_expr": 4.8}],
            enable_cross_dialect_normalization=True,
            enable_mixed_numeric_equivalence=True,
            normalize_numeric=False,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_SUCCESS)
        self.assertEqual(result.exact_status, EXACT_STATUS_EXACT)
        self.assertTrue(result.details["mixed_numeric_equivalence_enabled"])
        self.assertTrue(result.details["mixed_numeric_equivalence_used"])

    def test_mixed_numeric_equivalence_requires_explicit_opt_in(self) -> None:
        result = self._run_synthetic_checker(
            [{"mysql_expr": "4.80"}],
            [{"spark_expr": 4.8}],
            enable_cross_dialect_normalization=True,
            enable_mixed_numeric_equivalence=False,
            normalize_numeric=False,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_MISMATCH)
        self.assertFalse(result.details["mixed_numeric_equivalence_enabled"])
        self.assertFalse(result.details["mixed_numeric_equivalence_used"])

    def test_same_engine_mixed_numeric_representation_remains_strict(self) -> None:
        result = self._run_synthetic_checker(
            [{"source_label": "4.80"}],
            [{"source_label": 4.8}],
            enable_cross_dialect_normalization=False,
            enable_mixed_numeric_equivalence=True,
            normalize_numeric=False,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_MISMATCH)
        self.assertFalse(result.details["cross_dialect_normalization_active"])

    def test_mixed_numeric_equivalence_does_not_coerce_booleans(self) -> None:
        result = self._run_synthetic_checker(
            [{"mysql_expr": "1"}],
            [{"spark_expr": True}],
            enable_cross_dialect_normalization=True,
            enable_mixed_numeric_equivalence=True,
            normalize_numeric=False,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_MISMATCH)
        self.assertEqual(result.details["mismatch_reason"], "value_mismatch")
        self.assertFalse(result.details["mixed_numeric_equivalence_used"])

    def test_mixed_numeric_equivalence_does_not_coerce_nonnumeric_strings(self) -> None:
        result = self._run_synthetic_checker(
            [{"mysql_expr": "ALICE"}],
            [{"spark_expr": 0}],
            enable_cross_dialect_normalization=True,
            enable_mixed_numeric_equivalence=True,
            normalize_numeric=False,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_MISMATCH)
        self.assertEqual(result.details["mismatch_reason"], "value_mismatch")
        self.assertFalse(result.details["mixed_numeric_equivalence_used"])

    def test_cross_dialect_true_value_difference_remains_mismatch(self) -> None:
        result = self._run_synthetic_checker(
            [{"mysql_expr": "1"}],
            [{"?column?": "2"}],
            enable_cross_dialect_normalization=True,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_MISMATCH)
        self.assertEqual(result.exact_status, EXACT_STATUS_MISMATCH)
        self.assertEqual(result.failure_bucket, FAILURE_MISMATCH)
        self.assertEqual(result.details["mismatch_reason"], "value_mismatch")

    def test_cross_dialect_different_column_counts_remain_mismatch(self) -> None:
        result = self._run_synthetic_checker(
            [{"a": "1", "b": "2"}],
            [{"x": "1"}],
            enable_cross_dialect_normalization=True,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_MISMATCH)
        self.assertEqual(result.details["mismatch_reason"], "column_count_mismatch")
        payload = json.loads(result.mismatch_artifact_path.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["cross_dialect_normalization"]["mismatch_reason"],
            "column_count_mismatch",
        )

    def test_cross_dialect_different_row_counts_remain_mismatch(self) -> None:
        result = self._run_synthetic_checker(
            [{"a": "1"}, {"a": "2"}],
            [{"x": "1"}],
            enable_cross_dialect_normalization=True,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_MISMATCH)
        self.assertEqual(result.details["mismatch_reason"], "row_count_mismatch")

    def test_same_engine_perf_like_comparison_still_respects_labels(self) -> None:
        result = self._run_synthetic_checker(
            [{"source_label": "1"}],
            [{"target_label": "1"}],
            enable_cross_dialect_normalization=False,
        )

        self.assertEqual(result.checker_status, CHECKER_STATUS_MISMATCH)
        self.assertFalse(result.details["cross_dialect_normalization_active"])

    def _assert_real_case_same_engine_label_mismatch(self, case_id: str) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.jsonl"
            candidate = root / "candidate.jsonl"
            _write_jsonl(source, [{"source_label": "1"}])
            _write_jsonl(candidate, [{"target_label": "1"}])
            result = run_local_checker(
                case_dir=REPO_ROOT / "cases" / case_id.split("_")[0] / case_id,
                source_result_path=source,
                candidate_result_path=candidate,
                checker_dir=root / "checker_out",
                enable_cross_dialect_normalization=False,
            )
        self.assertEqual(result.checker_status, CHECKER_STATUS_MISMATCH)

    def test_perf_0006_same_engine_behavior_unaffected(self) -> None:
        self._assert_real_case_same_engine_label_mismatch("PERF_0006")

    def test_cons_0005_same_engine_behavior_unaffected(self) -> None:
        self._assert_real_case_same_engine_label_mismatch("CONS_0005")

    def test_longtail_0011_same_engine_behavior_unaffected(self) -> None:
        self._assert_real_case_same_engine_label_mismatch("LONGTAIL_0011")

    def test_same_engine_port_cases_do_not_enable_positional_comparison(self) -> None:
        row = _selected_row("PORT_0003")
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        self.assertFalse(_cross_dialect_checker_normalization_enabled(resolved))

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.jsonl"
            candidate = root / "candidate.jsonl"
            _write_jsonl(source, [{"source_label": "1"}])
            _write_jsonl(candidate, [{"target_label": "1"}])
            result = run_local_checker(
                case_dir=REPO_ROOT / "cases" / "PORT" / "PORT_0003",
                source_result_path=source,
                candidate_result_path=candidate,
                checker_dir=root / "checker_out",
                enable_cross_dialect_normalization=_cross_dialect_checker_normalization_enabled(
                    resolved
                ),
            )
        self.assertEqual(result.checker_status, CHECKER_STATUS_MISMATCH)

    def test_cross_dialect_gating_comes_from_manifest_metadata(self) -> None:
        row = _selected_row("PORT_0004")
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        self.assertTrue(_cross_dialect_checker_normalization_enabled(resolved))
        self.assertFalse(_mysql_to_spark_numeric_equivalence_enabled(resolved))

        spark_row = _selected_row("PORT_0004", engine="spark")
        spark_resolved = resolve_case_package(repo_root=REPO_ROOT, row=spark_row)
        self.assertTrue(_cross_dialect_checker_normalization_enabled(spark_resolved))
        self.assertTrue(_mysql_to_spark_numeric_equivalence_enabled(spark_resolved))

        mysql_row = _selected_row("PORT_0003", engine="mysql")
        mysql_resolved = resolve_case_package(repo_root=REPO_ROOT, row=mysql_row)
        self.assertTrue(_cross_dialect_checker_normalization_enabled(mysql_resolved))
        self.assertFalse(_mysql_to_spark_numeric_equivalence_enabled(mysql_resolved))

    def test_checker_details_do_not_add_official_metric_fields_or_reports(self) -> None:
        result = self._run_synthetic_checker(
            [{"mysql_expr": "1"}],
            [{"?column?": "1"}],
            enable_cross_dialect_normalization=True,
        )

        self.assertEqual(result.exact_status, EXACT_STATUS_EXACT)
        self.assertNotIn("official_metric", result.details)
        self.assertNotIn("timing", result.details)


if __name__ == "__main__":
    unittest.main()
