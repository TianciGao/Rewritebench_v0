import tempfile
import unittest
from pathlib import Path

from sql_rewrite_bench.case_selection import resolve_common_core_selection


REPO_ROOT = Path(__file__).resolve().parents[2]


class CaseSelectionTests(unittest.TestCase):
    def test_resolves_perf_postgres_common_core_rows(self) -> None:
        rows = resolve_common_core_selection(
            repo_root=REPO_ROOT,
            case_set="common_core_v0",
            pool="PERF",
            engine="postgres",
        )
        self.assertEqual(len(rows), 16)
        self.assertEqual({row.pool for row in rows}, {"PERF"})
        self.assertEqual({row.engine for row in rows}, {"postgres"})
        self.assertTrue(rows[0].source_sql_path.endswith("/sql/source.sql"))

    def test_engine_all_expands_three_rows_for_one_case(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = Path(temp_dir) / "cases.txt"
            case_list.write_text("PERF_0006\n", encoding="utf-8")
            rows = resolve_common_core_selection(
                repo_root=REPO_ROOT,
                case_set="common_core_v0",
                pool="PERF",
                engine="all",
                case_list=case_list,
            )
        self.assertEqual(len(rows), 3)
        self.assertEqual({row.engine for row in rows}, {"postgres", "mysql", "spark"})

    def test_rejects_non_common_core_case_set(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported case set"):
            resolve_common_core_selection(
                repo_root=REPO_ROOT,
                case_set="staged_backlog_v0",
                pool="all",
                engine="postgres",
            )


if __name__ == "__main__":
    unittest.main()
