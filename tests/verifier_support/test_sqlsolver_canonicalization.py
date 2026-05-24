import json
import sys
import tempfile
import unittest
from pathlib import Path

from sql_rewrite_bench.verifier_support.fixtures import synthetic_pair_record
from sql_rewrite_bench.verifier_support.sqlsolver import (
    canonicalize_sqlsolver_query,
    canonicalize_sqlsolver_schema,
    classify_sqlsolver_guard,
    sqlsolver_support_scope_decision,
    write_sqlsolver_smoke,
)


class SQLSolverCanonicalizationTests(unittest.TestCase):
    def test_leading_line_comments_and_date_literal_shape_to_one_line(self) -> None:
        result = canonicalize_sqlsolver_query(
            "-- provenance comment\n"
            "SELECT COUNT(*)\n"
            "FROM lineitem\n"
            "WHERE l_shipdate <= DATE '1998-08-27';\n"
        )

        self.assertTrue(result.safe_for_sqlsolver)
        self.assertNotIn("--", result.canonical_text)
        self.assertEqual(result.canonical_text.count("\n"), 0)
        self.assertEqual(
            result.canonical_text,
            "SELECT COUNT(*) FROM lineitem WHERE l_shipdate <= DATE '1998-08-27'",
        )
        self.assertIn("wrapper_input_format_gap", result.guard_categories)
        self.assertIn("query_normalization_gap", result.guard_categories)

    def test_date_interval_arithmetic_is_classified_not_silently_hidden(self) -> None:
        result = canonicalize_sqlsolver_query(
            "SELECT SUM(l_extendedprice) FROM lineitem "
            "WHERE l_shipdate < DATE '1995-01-01' + INTERVAL '1' YEAR"
        )

        self.assertTrue(result.safe_for_sqlsolver)
        self.assertIn("unsupported_postgres_dialect", result.guard_categories)
        self.assertIn("query_normalization_gap", result.guard_categories)

    def test_schema_strips_inline_comments_and_normalizes_common_types(self) -> None:
        result = canonicalize_sqlsolver_schema(
            "DROP TABLE IF EXISTS schools;\n"
            "CREATE TABLE schools (\n"
            "  id NUMERIC(10,0) PRIMARY KEY,\n"
            "  longitude DOUBLE PRECISION -- inline comment\n"
            ");\n"
        )

        self.assertTrue(result.safe_for_sqlsolver)
        self.assertNotIn("DROP TABLE", result.canonical_text.upper())
        self.assertNotIn("--", result.canonical_text)
        self.assertIn("longitude DOUBLE", result.canonical_text)
        self.assertIn("id DECIMAL(10,0) PRIMARY KEY", result.canonical_text)
        self.assertIn("schema_canonicalization_gap", result.guard_categories)

    def test_quoted_identifiers_and_null_ordering_are_guarded(self) -> None:
        result = canonicalize_sqlsolver_query(
            'SELECT "nationality" FROM "drivers" '
            'WHERE NOT "dob" IS NULL ORDER BY "dob" ASC NULLS FIRST LIMIT 1'
        )

        self.assertTrue(result.safe_for_sqlsolver)
        self.assertIn("unsupported_postgres_dialect", result.guard_categories)
        self.assertIn('"nationality"', result.canonical_text)
        self.assertIn("NULLS FIRST", result.canonical_text)
        decision = sqlsolver_support_scope_decision(result.canonical_text)
        self.assertFalse(decision.sqlsolver_invocation_allowed)
        self.assertEqual(decision.family, "quoted_identifier_null_ordering")
        self.assertEqual(decision.support_scope_verdict, "no_verifier_support")

    def test_dense_rank_cte_ranking_is_guarded(self) -> None:
        result = canonicalize_sqlsolver_query(
            "WITH ranked AS ("
            "SELECT id, DENSE_RANK() OVER (PARTITION BY owner_id ORDER BY score DESC) AS r "
            "FROM posts) SELECT id FROM ranked WHERE r = 1"
        )

        self.assertTrue(result.safe_for_sqlsolver)
        self.assertIn("unsupported_sql_feature", result.guard_categories)
        decision = sqlsolver_support_scope_decision(result.canonical_text)
        self.assertFalse(decision.sqlsolver_invocation_allowed)
        self.assertEqual(decision.family, "dense_rank_cte_ranking")
        self.assertEqual(decision.support_scope_verdict, "no_verifier_support")

    def test_terminal_semicolon_and_whitespace_policy(self) -> None:
        result = canonicalize_sqlsolver_query("  SELECT   a,\n b   FROM t ;\n")

        self.assertTrue(result.safe_for_sqlsolver)
        self.assertEqual(result.canonical_text, "SELECT a, b FROM t")
        self.assertIn("terminal_semicolon_normalized", result.notes)

    def test_block_and_line_comments_do_not_modify_string_literals(self) -> None:
        result = canonicalize_sqlsolver_query(
            "/* header */ SELECT '--not a comment' AS marker, col FROM t -- trailer\n"
        )

        self.assertTrue(result.safe_for_sqlsolver)
        self.assertEqual(result.canonical_text, "SELECT '--not a comment' AS marker, col FROM t")
        self.assertIn("block_comment_stripped", result.notes)
        self.assertIn("line_comment_stripped", result.notes)

    def test_unsafe_multi_statement_fails_closed(self) -> None:
        result = canonicalize_sqlsolver_query("SELECT 1; SELECT 2;")

        self.assertFalse(result.safe_for_sqlsolver)
        self.assertEqual(result.fail_closed_reason, "expected_exactly_one_sql_statement")
        self.assertIn("wrapper_input_format_gap", result.guard_categories)

    def test_guard_classifier_reports_known_categories(self) -> None:
        categories = classify_sqlsolver_guard(
            "WITH ranked AS (SELECT DENSE_RANK() OVER (ORDER BY score) AS r FROM posts) "
            "SELECT * FROM ranked WHERE r = 1",
            "CREATE TABLE posts (title TEXT, score NUMERIC);",
        )

        self.assertIn("unsupported_sql_feature", categories)
        self.assertIn("schema_canonicalization_gap", categories)

    def test_jar_runner_uses_canonicalized_temp_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            root = tmp_path / "external" / "SQLSolver"
            jar = root / "build" / "libs" / "sqlsolver.jar"
            lib = root / "lib"
            jar.parent.mkdir(parents=True)
            lib.mkdir(parents=True)
            jar.write_text("fake jar\n", encoding="utf-8")
            fake_java = _write_canonicalization_asserting_java(tmp_path)
            source = tmp_path / "source.sql"
            candidate = tmp_path / "candidate.sql"
            schema = tmp_path / "schema.sql"
            source.write_text("-- provenance\nSELECT longitude FROM schools;\n", encoding="utf-8")
            candidate.write_text("/* same */ SELECT longitude FROM schools;\n", encoding="utf-8")
            schema.write_text(
                "DROP TABLE IF EXISTS schools;\n"
                "CREATE TABLE schools (longitude DOUBLE PRECISION -- inline comment\n);\n",
                encoding="utf-8",
            )
            pair = synthetic_pair_record(
                pair_id="canonicalization_pair",
                run_id="sqlsolver_canonicalization",
                tool="sqlsolver",
                pair_type="support_pair_smoke",
                source_sql_path=source.as_posix(),
                candidate_sql_path=candidate.as_posix(),
                schema_context_path=schema.as_posix(),
            )

            output = write_sqlsolver_smoke(
                output_root=tmp_path / "output",
                run_id="sqlsolver_canonicalization",
                pair_records=[pair],
                env={
                    "SQLRB_SQLSOLVER_JAR": jar.as_posix(),
                    "SQLRB_SQLSOLVER_JAVA": fake_java.as_posix(),
                    "SQLRB_SQLSOLVER_LD_LIBRARY_PATH": lib.as_posix(),
                },
                search_path="",
                result_consistent_pairs=1,
            )

            verdicts = _read_jsonl(output.verdicts_path)
            self.assertEqual(verdicts[0]["normalized_verdict"], "equivalent")
            artifacts = verdicts[0]["artifact_paths"]
            self.assertTrue(artifacts["canonicalization_applied"])
            self.assertIn("wrapper_input_format_gap", artifacts["source_guard_categories"])
            self.assertIn("schema_canonicalization_gap", artifacts["schema_guard_categories"])

    def test_jar_runner_blocks_quoted_null_ordering_before_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            root = tmp_path / "external" / "SQLSolver"
            jar = root / "build" / "libs" / "sqlsolver.jar"
            lib = root / "lib"
            marker = tmp_path / "actual_invocation_marker.txt"
            jar.parent.mkdir(parents=True)
            lib.mkdir(parents=True)
            jar.write_text("fake jar\n", encoding="utf-8")
            fake_java = _write_failing_if_actual_java(tmp_path, marker)
            source = tmp_path / "source.sql"
            candidate = tmp_path / "candidate.sql"
            schema = tmp_path / "schema.sql"
            query = (
                'SELECT "nationality" FROM "drivers" '
                'WHERE NOT "dob" IS NULL ORDER BY "dob" ASC NULLS FIRST LIMIT 1;\n'
            )
            source.write_text(query, encoding="utf-8")
            candidate.write_text(query, encoding="utf-8")
            schema.write_text("CREATE TABLE drivers (nationality TEXT, dob TIMESTAMP);\n", encoding="utf-8")
            pair = synthetic_pair_record(
                pair_id="quoted_null_ordering",
                run_id="sqlsolver_support_scope_guard",
                tool="sqlsolver",
                pair_type="support_pair_smoke",
                source_sql_path=source.as_posix(),
                candidate_sql_path=candidate.as_posix(),
                schema_context_path=schema.as_posix(),
            )

            output = write_sqlsolver_smoke(
                output_root=tmp_path / "output",
                run_id="sqlsolver_support_scope_guard",
                pair_records=[pair],
                env={
                    "SQLRB_SQLSOLVER_JAR": jar.as_posix(),
                    "SQLRB_SQLSOLVER_JAVA": fake_java.as_posix(),
                    "SQLRB_SQLSOLVER_LD_LIBRARY_PATH": lib.as_posix(),
                },
                search_path="",
                result_consistent_pairs=1,
            )

            verdicts = _read_jsonl(output.verdicts_path)
            self.assertFalse(marker.exists())
            self.assertEqual(verdicts[0]["normalized_verdict"], "unsupported")
            self.assertEqual(output.summary["semantic_equivalence_rate"], None)
            artifacts = verdicts[0]["artifact_paths"]
            self.assertTrue(artifacts["support_scope_guarded"])
            self.assertEqual(artifacts["support_scope_family"], "quoted_identifier_null_ordering")
            self.assertEqual(artifacts["support_scope_verdict"], "no_verifier_support")
            self.assertFalse(artifacts["result_checker_exactness_used"])
            self.assertFalse(verdicts[0]["official_metric_input"])

    def test_jar_runner_blocks_dense_rank_cte_before_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            root = tmp_path / "external" / "SQLSolver"
            jar = root / "build" / "libs" / "sqlsolver.jar"
            lib = root / "lib"
            marker = tmp_path / "actual_invocation_marker.txt"
            jar.parent.mkdir(parents=True)
            lib.mkdir(parents=True)
            jar.write_text("fake jar\n", encoding="utf-8")
            fake_java = _write_failing_if_actual_java(tmp_path, marker)
            source = tmp_path / "source.sql"
            candidate = tmp_path / "candidate.sql"
            schema = tmp_path / "schema.sql"
            query = (
                "WITH ranked AS ("
                "SELECT id, DENSE_RANK() OVER (PARTITION BY owner_id ORDER BY score DESC) AS r "
                "FROM posts) SELECT id FROM ranked WHERE r = 1;\n"
            )
            source.write_text(query, encoding="utf-8")
            candidate.write_text(query, encoding="utf-8")
            schema.write_text("CREATE TABLE posts (id INT, owner_id INT, score INT);\n", encoding="utf-8")
            pair = synthetic_pair_record(
                pair_id="dense_rank_cte",
                run_id="sqlsolver_support_scope_guard_dense",
                tool="sqlsolver",
                pair_type="support_pair_smoke",
                source_sql_path=source.as_posix(),
                candidate_sql_path=candidate.as_posix(),
                schema_context_path=schema.as_posix(),
            )

            output = write_sqlsolver_smoke(
                output_root=tmp_path / "output",
                run_id="sqlsolver_support_scope_guard_dense",
                pair_records=[pair],
                env={
                    "SQLRB_SQLSOLVER_JAR": jar.as_posix(),
                    "SQLRB_SQLSOLVER_JAVA": fake_java.as_posix(),
                    "SQLRB_SQLSOLVER_LD_LIBRARY_PATH": lib.as_posix(),
                },
                search_path="",
                result_consistent_pairs=1,
            )

            verdicts = _read_jsonl(output.verdicts_path)
            self.assertFalse(marker.exists())
            self.assertEqual(verdicts[0]["normalized_verdict"], "unsupported")
            artifacts = verdicts[0]["artifact_paths"]
            self.assertTrue(artifacts["support_scope_guarded"])
            self.assertEqual(artifacts["support_scope_family"], "dense_rank_cte_ranking")
            self.assertEqual(artifacts["support_scope_verdict"], "no_verifier_support")
            self.assertFalse(artifacts["result_checker_exactness_used"])


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_canonicalization_asserting_java(tmp_path: Path) -> Path:
    fake_java = tmp_path / "fake_java.py"
    fake_java.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import sys",
                "from pathlib import Path",
                "if '-help' in sys.argv:",
                "    print('java -jar sqlsolver.jar [-help] -sql1=<path> -sql2=<path> -schema=<path> [-output=<path>]')",
                "    raise SystemExit(0)",
                "args = {arg.split('=', 1)[0]: arg.split('=', 1)[1] for arg in sys.argv if '=' in arg}",
                "sql1 = Path(args['-sql1']).read_text(encoding='utf-8')",
                "sql2 = Path(args['-sql2']).read_text(encoding='utf-8')",
                "schema = Path(args['-schema']).read_text(encoding='utf-8')",
                "assert '--' not in sql1 and '/*' not in sql2",
                "assert len(sql1.strip().splitlines()) == 1",
                "assert len(sql2.strip().splitlines()) == 1",
                "assert 'DROP TABLE' not in schema.upper()",
                "assert 'DOUBLE PRECISION' not in schema.upper()",
                "assert '--' not in schema",
                "Path(args['-output']).write_text('EQ\\n', encoding='utf-8')",
                "print('fake SQLSolver completed')",
            ]
        ),
        encoding="utf-8",
    )
    fake_java.chmod(0o755)
    return fake_java


def _write_failing_if_actual_java(tmp_path: Path, marker: Path) -> Path:
    fake_java = tmp_path / "fake_java_fail_actual.py"
    fake_java.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import sys",
                "from pathlib import Path",
                "if '-help' in sys.argv:",
                "    print('java -jar sqlsolver.jar [-help] -sql1=<path> -sql2=<path> -schema=<path> [-output=<path>]')",
                "    raise SystemExit(0)",
                f"Path({marker.as_posix()!r}).write_text('actual invocation happened\\n', encoding='utf-8')",
                "raise SystemExit(99)",
            ]
        ),
        encoding="utf-8",
    )
    fake_java.chmod(0o755)
    return fake_java


if __name__ == "__main__":
    unittest.main()
