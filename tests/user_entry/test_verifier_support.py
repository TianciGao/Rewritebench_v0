import csv
import json
import tempfile
import unittest
from pathlib import Path

from sql_rewrite_bench.verifier_support import (
    ALLOWED_VERDICTS,
    generate_semantic_equivalence_summary,
    normalize_verdict,
    validate_pair_record,
    validate_verdict_record,
)
from sql_rewrite_bench.verifier_support.fixtures import (
    synthetic_pair_record,
    write_synthetic_verifier_fixture,
)
from sql_rewrite_bench.verifier_support.pairs import PAIR_FIELDS, boundary_flags_as_csv


class VerifierSupportTests(unittest.TestCase):
    def test_verdict_normalization_vocabulary(self) -> None:
        examples = {
            "equivalent": ["equivalent", "valid", "proved"],
            "non_equivalent": ["non_equivalent", "counterexample", "not equivalent"],
            "unknown": ["unknown", "inconclusive", "undecidable"],
            "timeout": ["timeout", "timed_out"],
            "unsupported": ["unsupported", "not supported"],
            "tool_error": ["tool_error", "parse_error", "crash"],
            "not_attempted": ["not_attempted", "skipped", ""],
        }
        for expected, raw_values in examples.items():
            for raw in raw_values:
                self.assertEqual(normalize_verdict(raw), expected, raw)

    def test_unrecognized_raw_verdict_fails_visible_as_tool_error(self) -> None:
        self.assertEqual(normalize_verdict("definitely maybe equivalent"), "tool_error")
        self.assertEqual(normalize_verdict("unknown"), "unknown")

    def test_pair_and_verdict_validation_require_contract_fields_and_flags(self) -> None:
        pair = synthetic_pair_record(pair_id="p1", run_id="run1", tool="verieql")
        self.assertEqual(validate_pair_record(pair)["pair_type"], "source_vs_candidate")
        bad_pair = dict(pair)
        bad_pair["official_metric_input"] = "true"
        with self.assertRaises(ValueError):
            validate_pair_record(bad_pair)

        verdict = {
            "pair_id": "p1",
            "tool": "verieql",
            "tool_version": "synthetic",
            "invocation_status": "completed",
            "verdict": "equivalent",
            "raw_stdout_path": "output/results/run1/verifier/tools/verieql/p1/raw_stdout.txt",
            "raw_stderr_path": "output/results/run1/verifier/tools/verieql/p1/raw_stderr.txt",
            "runtime_ms": 1.0,
            "timeout_seconds": 30,
            "normalized_verdict": "equivalent",
            "verdict_reason": "fixture",
            "artifact_paths": {},
            "local_diagnostic_only": True,
            "official_metric_input": False,
            "paper_result_input": False,
            "retained_evidence_promoted": False,
            "leaderboard_input": False,
        }
        self.assertEqual(validate_verdict_record(verdict)["normalized_verdict"], "equivalent")
        bad_verdict = dict(verdict)
        bad_verdict["leaderboard_input"] = True
        with self.assertRaises(ValueError):
            validate_verdict_record(bad_verdict)

    def test_semantic_equivalence_summary_uses_only_decidable_verifier_outcomes(self) -> None:
        rows = [
            _verdict("p1", "equivalent"),
            _verdict("p2", "non_equivalent"),
            _verdict("p3", "equivalent"),
            _verdict("p4", "unknown"),
            _verdict("p5", "timeout"),
            _verdict("p6", "unsupported"),
            _verdict("p7", "tool_error"),
            _verdict("p8", "not_attempted"),
        ]
        summary = generate_semantic_equivalence_summary(
            run_id="run1",
            verdict_rows=rows,
            verifier_tools_requested=["verieql", "sqlsolver"],
            result_consistent_pairs=10,
        )

        self.assertEqual(summary["decidable_count"], 3)
        self.assertEqual(summary["equivalent_count"], 2)
        self.assertEqual(summary["non_equivalent_count"], 1)
        self.assertEqual(summary["semantic_equivalence_rate"], 2 / 3)
        self.assertEqual(summary["verifier_decidability_rate"], 0.3)
        self.assertEqual(summary["unknown_count"], 1)
        self.assertEqual(summary["timeout_count"], 1)
        self.assertEqual(summary["unsupported_count"], 1)
        self.assertEqual(summary["tool_error_count"], 1)
        self.assertEqual(summary["not_attempted_count"], 1)
        self.assertFalse(summary["result_checker_exactness_used"])
        self.assertTrue(summary["local_diagnostic_only"])
        self.assertFalse(summary["official_metric_input"])
        self.assertFalse(summary["paper_result_input"])
        self.assertFalse(summary["retained_evidence_promoted"])
        self.assertFalse(summary["leaderboard_input"])

    def test_semantic_equivalence_summary_is_na_when_no_decidable_outcomes(self) -> None:
        summary = generate_semantic_equivalence_summary(
            run_id="run1",
            verdict_rows=[_verdict("p1", "unknown"), _verdict("p2", "timeout")],
        )

        self.assertEqual(summary["decidable_count"], 0)
        self.assertIsNone(summary["semantic_equivalence_rate"])
        self.assertEqual(summary["semantic_equivalence_rate_status"], "not_applicable")
        self.assertEqual(summary["na_reason"], "no_decidable_verifier_outcomes")

    def test_synthetic_fixture_writes_output_contract_shape_and_no_prohibited_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "output"
            pairs = [
                synthetic_pair_record(pair_id="p1", run_id="run1", tool="verieql"),
                synthetic_pair_record(pair_id="p2", run_id="run1", tool="sqlsolver"),
                synthetic_pair_record(
                    pair_id="p3",
                    run_id="run1",
                    tool="verieql",
                    pair_type="source_vs_positive",
                    candidate_sql_path="",
                    positive_sql_path="output/results/run1/positive.sql",
                ),
                synthetic_pair_record(
                    pair_id="p4",
                    run_id="run1",
                    tool="sqlsolver",
                    pair_type="source_vs_hard_negative",
                    candidate_sql_path="",
                    negative_sql_path="output/results/run1/negative.sql",
                ),
            ]
            fixture = write_synthetic_verifier_fixture(
                output_root=output_root,
                run_id="run1",
                pair_records=pairs,
                raw_verdict_rows=[
                    {"pair_id": "p1", "raw_verdict": "equivalent"},
                    {"pair_id": "p2", "raw_verdict": "counterexample"},
                    {"pair_id": "p3", "raw_verdict": "unknown"},
                    {"pair_id": "p4", "invocation_status": "timeout", "raw_verdict": ""},
                ],
                result_consistent_pairs=4,
            )

            self.assertEqual(fixture.result_verifier_dir, output_root / "results" / "run1" / "verifier")
            self.assertEqual(fixture.log_path, output_root / "logs" / "run1" / "verifier.log")
            self.assertEqual(fixture.report_path, output_root / "reports" / "run1" / "verifier_summary.md")
            with fixture.pairs_path.open(newline="", encoding="utf-8") as handle:
                pair_rows = list(csv.DictReader(handle))
            self.assertEqual(handle_fieldnames(fixture.pairs_path), PAIR_FIELDS)
            self.assertEqual(len(pair_rows), 4)

            verdict_rows = [
                json.loads(line)
                for line in fixture.verdicts_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(len(verdict_rows), 4)
            for row in verdict_rows:
                self.assertIn(row["normalized_verdict"], ALLOWED_VERDICTS)
                self.assertTrue(row["local_diagnostic_only"])
                self.assertFalse(row["official_metric_input"])
                self.assertFalse(row["paper_result_input"])
                self.assertFalse(row["retained_evidence_promoted"])
                self.assertFalse(row["leaderboard_input"])
                for prohibited in ["winner", "best_method", "rank"]:
                    self.assertNotIn(prohibited, row)

            summary = json.loads(fixture.summary_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["pairs_planned"], 4)
            self.assertEqual(summary["pairs_attempted"], 4)
            self.assertEqual(summary["semantic_equivalence_rate"], 0.5)
            self.assertEqual(summary["verifier_tools_requested"], ["sqlsolver", "verieql"])
            self.assertIn("Synthetic verifier fixture only", fixture.log_path.read_text(encoding="utf-8"))
            self.assertIn("Semantic Equivalence Rate", fixture.report_path.read_text(encoding="utf-8"))
            for prohibited in ["winner", "best_method", "rank"]:
                self.assertNotIn(prohibited, json.dumps(summary))

    def test_output_schema_matches_required_verifier_contract_fields(self) -> None:
        pair = synthetic_pair_record(pair_id="p1", run_id="run1", tool="verieql")
        self.assertEqual(list(pair.keys()), PAIR_FIELDS)
        self.assertEqual(boundary_flags_as_csv()["local_diagnostic_only"], "true")
        verdict = _verdict("p1", "equivalent")
        required_verdict_fields = {
            "pair_id",
            "tool",
            "tool_version",
            "invocation_status",
            "verdict",
            "raw_stdout_path",
            "raw_stderr_path",
            "runtime_ms",
            "timeout_seconds",
            "normalized_verdict",
            "verdict_reason",
            "artifact_paths",
            "local_diagnostic_only",
            "official_metric_input",
            "paper_result_input",
            "retained_evidence_promoted",
            "leaderboard_input",
        }
        self.assertTrue(required_verdict_fields.issubset(verdict.keys()))


def _verdict(pair_id: str, normalized: str) -> dict[str, object]:
    return {
        "pair_id": pair_id,
        "tool": "verieql",
        "tool_version": "synthetic",
        "invocation_status": "not_attempted" if normalized == "not_attempted" else "completed",
        "verdict": normalized,
        "raw_stdout_path": f"output/results/run1/verifier/tools/verieql/{pair_id}/raw_stdout.txt",
        "raw_stderr_path": f"output/results/run1/verifier/tools/verieql/{pair_id}/raw_stderr.txt",
        "runtime_ms": None,
        "timeout_seconds": 30,
        "normalized_verdict": normalized,
        "verdict_reason": "fixture",
        "artifact_paths": {},
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result_input": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
    }


def handle_fieldnames(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or [])


if __name__ == "__main__":
    unittest.main()
