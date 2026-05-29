import csv
import sys
import tempfile
import unittest
import uuid
from argparse import Namespace
from pathlib import Path
from unittest import mock

from sql_rewrite_bench.candidate_preflight import (
    run_candidate_preflight,
    split_sql_statements_comment_aware,
)
from sql_rewrite_bench.spark_execution import _split_sql_statements as split_spark_statements
from sql_rewrite_bench.user_run import run_user_benchmark
from sql_rewrite_bench.user_run_schema import (
    CANDIDATE_PREFLIGHT_FAILURE_EMPTY_CANDIDATE,
    CANDIDATE_PREFLIGHT_FAILURE_MULTI_STATEMENT,
    CANDIDATE_PREFLIGHT_FAILURE_UNSAFE_SQL,
    CANDIDATE_PREFLIGHT_FAILURE_UNSUPPORTED_STATEMENT_TYPE,
    CANDIDATE_PREFLIGHT_STATUS_FAILED,
    CANDIDATE_PREFLIGHT_STATUS_PASSED,
    CANDIDATE_PREFLIGHT_STATUS_VALUES,
    CANDIDATE_SAFETY_STATUS_SAFE,
    FAILURE_CANDIDATE_PREFLIGHT_FAILED,
    FAILURE_BUCKET_VALUES,
    SOURCE_LIKE_STATUS_CHANGED,
    SOURCE_LIKE_STATUS_SOURCE_LIKE,
)


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
    enable_db_execution: bool = False,
    enable_checker: bool = False,
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
        enable_db_execution=enable_db_execution,
        enable_checker=enable_checker,
        postgres_dsn_env="SQLRB_POSTGRES_DSN",
        execution_timeout_sec=30,
        db_schema_prefix="sqlrb_user",
    )


def _write_adapter(path: Path, candidate_sql: str) -> None:
    path.write_text(
        "\n".join(
            [
                "import os",
                "from pathlib import Path",
                "candidate = Path(os.environ['SQLRB_CANDIDATE_SQL_PATH'])",
                "candidate.parent.mkdir(parents=True, exist_ok=True)",
                f"candidate.write_text({candidate_sql!r})",
                "",
            ]
        ),
        encoding="utf-8",
    )


class CandidatePreflightTests(unittest.TestCase):
    def assert_preflight_and_spark_single_statement(self, sql: str) -> None:
        result = run_candidate_preflight(source_sql_text="select 1;", candidate_sql_text=sql)
        self.assertEqual(result.candidate_preflight_status, CANDIDATE_PREFLIGHT_STATUS_PASSED)
        self.assertEqual(len(split_sql_statements_comment_aware(sql)), 1)
        self.assertEqual(len(split_spark_statements(sql)), 1)

    def test_valid_select_candidate_passes(self) -> None:
        result = run_candidate_preflight(
            source_sql_text="select 1;",
            candidate_sql_text="select 2;",
            dialect="postgres",
        )
        self.assertEqual(result.candidate_preflight_status, CANDIDATE_PREFLIGHT_STATUS_PASSED)
        self.assertEqual(result.candidate_preflight_passed, "true")
        self.assertEqual(result.candidate_safety_status, CANDIDATE_SAFETY_STATUS_SAFE)
        self.assertEqual(result.source_like_status, SOURCE_LIKE_STATUS_CHANGED)

    def test_valid_with_candidate_passes(self) -> None:
        result = run_candidate_preflight(
            source_sql_text="select 1;",
            candidate_sql_text="with x as (select 1) select * from x",
        )
        self.assertEqual(result.candidate_preflight_status, CANDIDATE_PREFLIGHT_STATUS_PASSED)

    def test_empty_candidate_fails(self) -> None:
        result = run_candidate_preflight(source_sql_text="select 1;", candidate_sql_text="   ")
        self.assertEqual(result.candidate_preflight_status, CANDIDATE_PREFLIGHT_STATUS_FAILED)
        self.assertEqual(
            result.candidate_preflight_failure_class,
            CANDIDATE_PREFLIGHT_FAILURE_EMPTY_CANDIDATE,
        )

    def test_unsafe_candidate_fails(self) -> None:
        result = run_candidate_preflight(
            source_sql_text="select 1;", candidate_sql_text="drop table demo;"
        )
        self.assertEqual(
            result.candidate_preflight_failure_class,
            CANDIDATE_PREFLIGHT_FAILURE_UNSAFE_SQL,
        )

    def test_multiple_statements_fail(self) -> None:
        result = run_candidate_preflight(
            source_sql_text="select 1;", candidate_sql_text="select 1; select 2;"
        )
        self.assertEqual(
            result.candidate_preflight_failure_class,
            CANDIDATE_PREFLIGHT_FAILURE_MULTI_STATEMENT,
        )
        self.assertEqual(len(split_spark_statements("select 1; select 2;")), 2)

    def test_with_followed_by_unsafe_second_statement_fails(self) -> None:
        candidate = "with x as (select 1) select * from x; drop table demo;"
        result = run_candidate_preflight(source_sql_text="select 1;", candidate_sql_text=candidate)
        self.assertEqual(
            result.candidate_preflight_failure_class,
            CANDIDATE_PREFLIGHT_FAILURE_MULTI_STATEMENT,
        )
        self.assertEqual(len(split_spark_statements(candidate)), 2)

    def test_block_comment_semicolon_before_statement_is_single_statement(self) -> None:
        self.assert_preflight_and_spark_single_statement(
            "/* comment; still comment */ SELECT 1"
        )

    def test_block_comment_semicolon_after_statement_is_single_statement(self) -> None:
        self.assert_preflight_and_spark_single_statement(
            "SELECT 1 /* comment; still comment */"
        )

    def test_line_comment_semicolon_before_statement_is_single_statement(self) -> None:
        self.assert_preflight_and_spark_single_statement(
            "-- comment; still comment\nSELECT 1"
        )

    def test_string_literal_semicolon_is_single_statement(self) -> None:
        self.assert_preflight_and_spark_single_statement("SELECT 'a;b'")

    def test_backtick_identifier_semicolon_is_single_statement(self) -> None:
        self.assert_preflight_and_spark_single_statement("SELECT `a;b` FROM demo")

    def test_quoted_identifier_semicolon_is_single_statement(self) -> None:
        self.assert_preflight_and_spark_single_statement('SELECT "a;b" FROM demo')

    def test_non_query_top_level_statement_fails(self) -> None:
        result = run_candidate_preflight(
            source_sql_text="select 1;", candidate_sql_text="explain select 1;"
        )
        self.assertEqual(
            result.candidate_preflight_failure_class,
            CANDIDATE_PREFLIGHT_FAILURE_UNSUPPORTED_STATEMENT_TYPE,
        )

    def test_trailing_semicolon_is_accepted(self) -> None:
        result = run_candidate_preflight(source_sql_text="select 1", candidate_sql_text="select 1;")
        self.assertEqual(result.candidate_preflight_status, CANDIDATE_PREFLIGHT_STATUS_PASSED)

    def test_source_like_candidate_is_diagnostic_only(self) -> None:
        result = run_candidate_preflight(
            source_sql_text="select  1;",
            candidate_sql_text=" select 1 ; ",
        )
        self.assertEqual(result.candidate_preflight_status, CANDIDATE_PREFLIGHT_STATUS_PASSED)
        self.assertEqual(result.source_like_status, SOURCE_LIKE_STATUS_SOURCE_LIKE)

    def test_changed_candidate_is_flagged(self) -> None:
        result = run_candidate_preflight(
            source_sql_text="select 1;",
            candidate_sql_text="select 2;",
        )
        self.assertEqual(result.source_like_status, SOURCE_LIKE_STATUS_CHANGED)

    def test_status_vocabulary_contains_preflight_values(self) -> None:
        self.assertIn(CANDIDATE_PREFLIGHT_STATUS_PASSED, CANDIDATE_PREFLIGHT_STATUS_VALUES)
        self.assertIn(FAILURE_CANDIDATE_PREFLIGHT_FAILED, FAILURE_BUCKET_VALUES)

    def test_preflight_failure_prevents_optional_db_checker_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            case_list = _case_list(temp, "PERF_0006")
            adapter = temp / "unsafe_adapter.py"
            _write_adapter(adapter, "drop table demo;\n")
            out = _unique_out("unittest_u3_preflight_blocks_db")
            with mock.patch("sql_rewrite_bench.user_run.execute_engine_case") as execute:
                summary = run_user_benchmark(
                    _args(
                        out,
                        case_list,
                        adapter,
                        enable_db_execution=True,
                        enable_checker=True,
                    ),
                    REPO_ROOT,
                )
                execute.assert_not_called()

        self.assertEqual(summary["selected_rows"], 1)
        self.assertEqual(summary["candidate_generated_rows"], 1)
        self.assertEqual(summary["candidate_preflight_failed_rows"], 1)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["candidate_preflight_status"], "failed")
        self.assertEqual(rows[0]["candidate_preflight_failure_class"], "unsafe_sql")
        self.assertEqual(rows[0]["failure_bucket"], FAILURE_CANDIDATE_PREFLIGHT_FAILED)
        self.assertEqual(rows[0]["execution_status"], "execution_not_enabled")
        self.assertEqual(rows[0]["checker_status"], "checker_not_enabled")

    def test_ledger_includes_preflight_fields_for_public_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "IGNORED_FOR_SMOKE")
            out = _unique_out("unittest_u3_public_smoke_preflight")
            adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
            summary = run_user_benchmark(_args(out, case_list, adapter, smoke=True), REPO_ROOT)

        self.assertEqual(summary["selected_rows"], 2)
        self.assertEqual(summary["candidate_generated_rows"], 2)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual({row["candidate_preflight_status"] for row in rows}, {"passed"})
        self.assertEqual({row["candidate_preflight_passed"] for row in rows}, {"true"})
        self.assertEqual({row["source_like_status"] for row in rows}, {"source_like"})

    def test_public_smoke_dry_run_behavior_remains_correct(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            case_list = _case_list(Path(temp_dir), "IGNORED_FOR_SMOKE")
            out = _unique_out("unittest_u3_public_smoke_dry_run")
            adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
            summary = run_user_benchmark(
                _args(out, case_list, adapter, dry_run=True, smoke=True),
                REPO_ROOT,
            )

        self.assertEqual(summary["selected_rows"], 2)
        self.assertEqual(summary["adapter_invoked_rows"], 0)
        self.assertEqual(summary["candidate_generated_rows"], 0)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual({row["candidate_preflight_status"] for row in rows}, {"not_run"})


if __name__ == "__main__":
    unittest.main()
