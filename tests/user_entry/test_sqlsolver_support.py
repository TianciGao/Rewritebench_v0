import json
import sys
import tempfile
import unittest
from pathlib import Path

from sql_rewrite_bench.verifier_support.fixtures import synthetic_pair_record
from sql_rewrite_bench.verifier_support.sqlsolver import (
    detect_sqlsolver,
    normalize_sqlsolver_output,
    write_sqlsolver_smoke,
)
from sql_rewrite_bench.verifier_support.verieql import normalize_verieql_output


class SQLSolverSupportTests(unittest.TestCase):
    def test_unavailable_sqlsolver_fails_closed_without_fake_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = write_sqlsolver_smoke(
                output_root=Path(tmp) / "output",
                run_id="sqlsolver_unavailable",
                pair_records=[synthetic_pair_record(pair_id="p1", run_id="sqlsolver_unavailable", tool="sqlsolver")],
                command="/definitely/missing/sqlsolver",
                env={},
                search_path="",
            )

            self.assertFalse(output.tool_available)
            self.assertIsNone(output.tool_version)
            verdicts = _read_jsonl(output.verdicts_path)
            self.assertEqual(len(verdicts), 1)
            self.assertEqual(verdicts[0]["normalized_verdict"], "not_attempted")
            self.assertEqual(verdicts[0]["invocation_status"], "not_attempted")
            self.assertEqual(verdicts[0]["tool_version"], "unavailable")
            self.assertEqual(output.summary["semantic_equivalence_rate"], None)
            self.assertEqual(output.summary["na_reason"], "sqlsolver_unavailable")
            self.assertEqual(output.summary["decidable_count"], 0)
            self.assertTrue(output.summary["local_diagnostic_only"])
            self.assertFalse(output.summary["official_metric_input"])
            self.assertFalse(output.summary["paper_result_input"])
            self.assertFalse(output.summary["retained_evidence_promoted"])
            self.assertFalse(output.summary["leaderboard_input"])
            self.assertIn("tool_available=false", output.log_path.read_text(encoding="utf-8"))

    def test_detect_sqlsolver_reports_unavailable_without_installing(self) -> None:
        availability = detect_sqlsolver(command="/definitely/missing/sqlsolver", env={}, search_path="")
        self.assertFalse(availability.tool_available)
        self.assertEqual(availability.detection_reason, "sqlsolver_command_not_found")

    def test_sqlsolver_like_output_normalization(self) -> None:
        self.assertEqual(normalize_sqlsolver_output(stdout="Result: equivalent"), "equivalent")
        self.assertEqual(normalize_sqlsolver_output(stdout="PROVED: valid"), "equivalent")
        self.assertEqual(normalize_sqlsolver_output(stdout="Counterexample found"), "non_equivalent")
        self.assertEqual(normalize_sqlsolver_output(stdout="The query pair was refuted"), "non_equivalent")
        self.assertEqual(normalize_sqlsolver_output(stdout="unknown"), "unknown")
        self.assertEqual(normalize_sqlsolver_output(stdout="unsupported syntax"), "unsupported")
        self.assertEqual(normalize_sqlsolver_output(stdout="", timed_out=True), "timeout")
        self.assertEqual(normalize_sqlsolver_output(stdout="internal crash", returncode=1), "tool_error")

    def test_fake_available_command_writes_decidable_local_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake = tmp_path / "fake_sqlsolver.py"
            fake.write_text(
                "\n".join(
                    [
                        "import sys",
                        "if '--version' in sys.argv:",
                        "    print('SQLSolver synthetic 0.1')",
                        "else:",
                        "    print('Result: equivalent')",
                    ]
                ),
                encoding="utf-8",
            )
            source = tmp_path / "source.sql"
            candidate = tmp_path / "candidate.sql"
            source.write_text("SELECT 1\n", encoding="utf-8")
            candidate.write_text("SELECT 1\n", encoding="utf-8")
            pair = synthetic_pair_record(
                pair_id="p1",
                run_id="sqlsolver_fake",
                tool="sqlsolver",
                pair_type="support_pair_smoke",
                source_sql_path=source.as_posix(),
                candidate_sql_path=candidate.as_posix(),
            )

            output = write_sqlsolver_smoke(
                output_root=tmp_path / "output",
                run_id="sqlsolver_fake",
                pair_records=[pair],
                command=[sys.executable, fake.as_posix()],
                env={},
                result_consistent_pairs=1,
            )

            self.assertTrue(output.tool_available)
            self.assertEqual(output.tool_version, "SQLSolver synthetic 0.1")
            verdicts = _read_jsonl(output.verdicts_path)
            self.assertEqual(verdicts[0]["normalized_verdict"], "equivalent")
            self.assertEqual(verdicts[0]["verdict"], "equivalent")
            self.assertEqual(output.summary["semantic_equivalence_rate"], 1.0)
            self.assertEqual(output.summary["verifier_decidability_rate"], 1.0)
            self.assertFalse(output.summary["result_checker_exactness_used"])
            self.assertEqual(output.result_verifier_dir, tmp_path / "output" / "results" / "sqlsolver_fake" / "verifier")
            self.assertEqual(output.log_path, tmp_path / "output" / "logs" / "sqlsolver_fake" / "verifier.log")
            self.assertEqual(output.report_path, tmp_path / "output" / "reports" / "sqlsolver_fake" / "verifier_summary.md")

    def test_nonzero_counterexample_output_remains_non_equivalent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake = tmp_path / "fake_sqlsolver_counterexample.py"
            fake.write_text(
                "\n".join(
                    [
                        "import sys",
                        "if '--version' in sys.argv:",
                        "    print('SQLSolver synthetic 0.1')",
                        "else:",
                        "    print('counterexample found')",
                        "    raise SystemExit(1)",
                    ]
                ),
                encoding="utf-8",
            )
            source = tmp_path / "source.sql"
            candidate = tmp_path / "candidate.sql"
            source.write_text("SELECT 1\n", encoding="utf-8")
            candidate.write_text("SELECT 2\n", encoding="utf-8")
            pair = synthetic_pair_record(
                pair_id="p1",
                run_id="sqlsolver_counterexample",
                tool="sqlsolver",
                pair_type="support_pair_smoke",
                source_sql_path=source.as_posix(),
                candidate_sql_path=candidate.as_posix(),
            )

            output = write_sqlsolver_smoke(
                output_root=tmp_path / "output",
                run_id="sqlsolver_counterexample",
                pair_records=[pair],
                command=[sys.executable, fake.as_posix()],
                env={},
            )

            verdicts = _read_jsonl(output.verdicts_path)
            self.assertEqual(verdicts[0]["normalized_verdict"], "non_equivalent")
            self.assertEqual(verdicts[0]["invocation_status"], "completed")
            self.assertEqual(output.summary["semantic_equivalence_rate"], 0.0)

    def test_output_contract_has_no_leaderboard_or_ranking_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = write_sqlsolver_smoke(
                output_root=Path(tmp) / "output",
                run_id="sqlsolver_contract",
                pair_records=[synthetic_pair_record(pair_id="p1", run_id="sqlsolver_contract", tool="sqlsolver")],
                command="/definitely/missing/sqlsolver",
                env={},
                search_path="",
            )
            payload = output.summary_path.read_text(encoding="utf-8")
            verdict_payload = output.verdicts_path.read_text(encoding="utf-8")
            for token in ["winner", "best_method", "rank"]:
                self.assertNotIn(token, payload)
                self.assertNotIn(token, verdict_payload)
            summary = json.loads(payload)
            self.assertTrue(summary["local_diagnostic_only"])
            self.assertFalse(summary["leaderboard_input"])

    def test_verieql_normalization_is_unchanged_by_sqlsolver_addition(self) -> None:
        self.assertEqual(normalize_verieql_output(stdout="Result: equivalent"), "equivalent")
        self.assertEqual(normalize_verieql_output(stdout="Counterexample found"), "non_equivalent")


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


if __name__ == "__main__":
    unittest.main()
