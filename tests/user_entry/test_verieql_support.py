import json
import sys
import tempfile
import unittest
from pathlib import Path

from sql_rewrite_bench.verifier_support.fixtures import synthetic_pair_record
from sql_rewrite_bench.verifier_support.verieql import (
    build_verieql_batch_command,
    detect_verieql,
    normalize_verieql_jsonl_record,
    normalize_verieql_output,
    parse_verieql_output_file,
    write_verieql_pair_jsonl,
    write_verieql_canary,
)


class VeriEQLSupportTests(unittest.TestCase):
    def test_unavailable_verieql_fails_closed_without_fake_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = write_verieql_canary(
                output_root=Path(tmp) / "output",
                run_id="verieql_unavailable",
                pair_records=[synthetic_pair_record(pair_id="p1", run_id="verieql_unavailable", tool="verieql")],
                command="/definitely/missing/verieql",
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
            self.assertEqual(output.summary["na_reason"], "verieql_unavailable")
            self.assertEqual(output.summary["decidable_count"], 0)
            self.assertTrue(output.summary["local_diagnostic_only"])
            self.assertFalse(output.summary["official_metric_input"])
            self.assertFalse(output.summary["paper_result_input"])
            self.assertFalse(output.summary["retained_evidence_promoted"])
            self.assertFalse(output.summary["leaderboard_input"])
            self.assertIn("tool_available=false", output.log_path.read_text(encoding="utf-8"))

    def test_detect_verieql_reports_unavailable_without_installing(self) -> None:
        availability = detect_verieql(command="/definitely/missing/verieql", env={}, search_path="")
        self.assertFalse(availability.tool_available)
        self.assertEqual(availability.detection_reason, "verieql_command_not_found")

    def test_detect_verieql_root_uses_jsonl_batch_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _fake_verieql_root(Path(tmp))
            availability = detect_verieql(env={"SQLRB_VERIEQL_ROOT": root.as_posix()}, search_path="")

            self.assertTrue(availability.tool_available)
            self.assertEqual(availability.detection_reason, "verieql_root_available")
            self.assertEqual(availability.invocation_mode, "jsonl_batch")
            self.assertEqual(availability.verieql_root, root.as_posix())
            self.assertIn("parallel.cli_within_timeout", availability.command or ())

    def test_missing_verieql_root_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = write_verieql_canary(
                output_root=Path(tmp) / "output",
                run_id="missing_root",
                pair_records=[synthetic_pair_record(pair_id="p1", run_id="missing_root", tool="verieql")],
                env={"SQLRB_VERIEQL_ROOT": (Path(tmp) / "missing").as_posix()},
                search_path="",
            )

            self.assertFalse(output.tool_available)
            self.assertEqual(output.summary["detection_reason"], "verieql_root_not_found")
            self.assertEqual(output.summary["na_reason"], "verieql_unavailable")
            verdicts = _read_jsonl(output.verdicts_path)
            self.assertEqual(verdicts[0]["normalized_verdict"], "not_attempted")

    def test_verieql_like_output_normalization(self) -> None:
        self.assertEqual(normalize_verieql_output(stdout="Result: equivalent"), "equivalent")
        self.assertEqual(normalize_verieql_output(stdout="VERIFIED: valid"), "equivalent")
        self.assertEqual(normalize_verieql_output(stdout="Counterexample found"), "non_equivalent")
        self.assertEqual(normalize_verieql_output(stdout="The claim was refuted"), "non_equivalent")
        self.assertEqual(normalize_verieql_output(stdout="unknown"), "unknown")
        self.assertEqual(normalize_verieql_output(stdout="unsupported syntax"), "unsupported")
        self.assertEqual(normalize_verieql_output(stdout="", timed_out=True), "timeout")
        self.assertEqual(normalize_verieql_output(stdout="internal crash", returncode=1), "tool_error")

    def test_verieql_jsonl_output_normalization(self) -> None:
        self.assertEqual(normalize_verieql_jsonl_record({"states": ["EQU"]}), "equivalent")
        self.assertEqual(normalize_verieql_jsonl_record({"states": ["EQU", "NEQ"], "counterexample": "rows"}), "non_equivalent")
        self.assertEqual(normalize_verieql_jsonl_record({"states": ["NSE"], "err": "Not supported feature: EXISTS"}), "unsupported")
        self.assertEqual(normalize_verieql_jsonl_record({"states": ["TMO"]}), "timeout")
        self.assertEqual(normalize_verieql_jsonl_record({"err": "parser crashed"}), "tool_error")
        self.assertEqual(normalize_verieql_jsonl_record({"states": []}), "unknown")

    def test_jsonl_pair_file_generation_and_command_construction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source.sql"
            candidate = tmp_path / "candidate.sql"
            schema = tmp_path / "schema.sql"
            source.write_text("SELECT 1\n", encoding="utf-8")
            candidate.write_text("SELECT 1\n", encoding="utf-8")
            schema.write_text("CREATE TABLE t (id BIGINT, name VARCHAR(10));\n", encoding="utf-8")
            pair = synthetic_pair_record(
                pair_id="p1",
                run_id="jsonl",
                tool="verieql",
                pair_type="support_pair_smoke",
                source_sql_path=source.as_posix(),
                candidate_sql_path=candidate.as_posix(),
                schema_context_path=schema.as_posix(),
            )
            output_jsonl = tmp_path / "pairs.jsonl"

            records = write_verieql_pair_jsonl([pair], output_jsonl)
            parsed = json.loads(output_jsonl.read_text(encoding="utf-8"))
            command = build_verieql_batch_command(
                [sys.executable, "-m", "parallel.cli_within_timeout"],
                input_jsonl=output_jsonl,
                output_jsonl=tmp_path / "out.jsonl",
                timeout_seconds=30,
            )

            self.assertEqual(records[0]["pair"], ["SELECT 1\n", "SELECT 1\n"])
            self.assertEqual(records[0]["pair_role"], "support_pair_smoke")
            self.assertEqual(parsed["schema"]["T"]["ID"], "BIGINT")
            self.assertEqual(command[-6:], ["parallel.cli_within_timeout", "-f", output_jsonl.as_posix(), "-t", "30", "-o", (tmp_path / "out.jsonl").as_posix()][-6:])

    def test_jsonl_dry_run_records_cons0007_plan_without_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            root = _fake_verieql_root(tmp_path / "verieql")
            source = tmp_path / "source.sql"
            positive = tmp_path / "rewrite_pos_01.sql"
            source.write_text("SELECT * FROM tmp_emps\n", encoding="utf-8")
            positive.write_text("SELECT * FROM tmp_emps\n", encoding="utf-8")
            pair = synthetic_pair_record(
                pair_id="cons0007_source_positive",
                run_id="cons0007_plan",
                tool="verieql",
                case_id="CONS_0007",
                pool="CONS",
                pair_type="source_vs_positive",
                source_sql_path=source.as_posix(),
                candidate_sql_path="",
                positive_sql_path=positive.as_posix(),
            )

            output = write_verieql_canary(
                output_root=tmp_path / "output",
                run_id="cons0007_plan",
                pair_records=[pair],
                env={"SQLRB_VERIEQL_ROOT": root.as_posix()},
                dry_run=True,
            )

            self.assertEqual(output.summary["na_reason"], "verieql_dry_run_not_executed")
            self.assertEqual(output.summary["semantic_equivalence_rate"], None)
            self.assertIsNotNone(output.jsonl_input_path)
            jsonl_record = json.loads(output.jsonl_input_path.read_text(encoding="utf-8"))
            self.assertEqual(jsonl_record["case_id"], "CONS_0007")
            self.assertEqual(jsonl_record["pair_role"], "source_positive")
            verdicts = _read_jsonl(output.verdicts_path)
            self.assertEqual(verdicts[0]["normalized_verdict"], "not_attempted")

    def test_missing_dependency_batch_failure_is_local_na(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            root = _fake_verieql_root(
                tmp_path / "verieql",
                body=[
                    "import sys",
                    "print(\"ModuleNotFoundError: No module named 'ujson'\", file=sys.stderr)",
                    "raise SystemExit(1)",
                ],
            )
            source = tmp_path / "source.sql"
            candidate = tmp_path / "candidate.sql"
            source.write_text("SELECT 1\n", encoding="utf-8")
            candidate.write_text("SELECT 1\n", encoding="utf-8")
            pair = synthetic_pair_record(
                pair_id="p1",
                run_id="dep_missing",
                tool="verieql",
                source_sql_path=source.as_posix(),
                candidate_sql_path=candidate.as_posix(),
            )

            output = write_verieql_canary(
                output_root=tmp_path / "output",
                run_id="dep_missing",
                pair_records=[pair],
                env={"SQLRB_VERIEQL_ROOT": root.as_posix()},
                timeout_seconds=1,
            )

            verdicts = _read_jsonl(output.verdicts_path)
            self.assertEqual(verdicts[0]["normalized_verdict"], "tool_error")
            self.assertEqual(output.summary["semantic_equivalence_rate"], None)
            self.assertEqual(output.summary["na_reason"], "verieql_dependency_missing")
            self.assertTrue(verdicts[0]["artifact_paths"]["dependency_missing"])

    def test_parse_verieql_output_file_by_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "output.jsonl"
            path.write_text('{"index": 2, "states": ["NEQ"]}\n{"index": 1, "states": ["EQU"]}\n', encoding="utf-8")

            parsed = parse_verieql_output_file(path)

            self.assertEqual(normalize_verieql_jsonl_record(parsed[1]), "equivalent")
            self.assertEqual(normalize_verieql_jsonl_record(parsed[2]), "non_equivalent")

    def test_fake_available_command_writes_decidable_local_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake = tmp_path / "fake_verieql.py"
            fake.write_text(
                "\n".join(
                    [
                        "import sys",
                        "if '--version' in sys.argv:",
                        "    print('VeriEQL synthetic 0.1')",
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
                run_id="verieql_fake",
                tool="verieql",
                pair_type="support_pair_smoke",
                source_sql_path=source.as_posix(),
                candidate_sql_path=candidate.as_posix(),
            )

            output = write_verieql_canary(
                output_root=tmp_path / "output",
                run_id="verieql_fake",
                pair_records=[pair],
                command=[sys.executable, fake.as_posix()],
                env={},
                result_consistent_pairs=1,
            )

            self.assertTrue(output.tool_available)
            self.assertEqual(output.tool_version, "VeriEQL synthetic 0.1")
            verdicts = _read_jsonl(output.verdicts_path)
            self.assertEqual(verdicts[0]["normalized_verdict"], "equivalent")
            self.assertEqual(verdicts[0]["verdict"], "equivalent")
            self.assertEqual(output.summary["semantic_equivalence_rate"], 1.0)
            self.assertEqual(output.summary["verifier_decidability_rate"], 1.0)
            self.assertFalse(output.summary["result_checker_exactness_used"])
            self.assertEqual(output.result_verifier_dir, tmp_path / "output" / "results" / "verieql_fake" / "verifier")
            self.assertEqual(output.log_path, tmp_path / "output" / "logs" / "verieql_fake" / "verifier.log")
            self.assertEqual(output.report_path, tmp_path / "output" / "reports" / "verieql_fake" / "verifier_summary.md")

    def test_nonzero_counterexample_output_remains_non_equivalent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake = tmp_path / "fake_verieql_counterexample.py"
            fake.write_text(
                "\n".join(
                    [
                        "import sys",
                        "if '--version' in sys.argv:",
                        "    print('VeriEQL synthetic 0.1')",
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
                run_id="verieql_counterexample",
                tool="verieql",
                pair_type="support_pair_smoke",
                source_sql_path=source.as_posix(),
                candidate_sql_path=candidate.as_posix(),
            )

            output = write_verieql_canary(
                output_root=tmp_path / "output",
                run_id="verieql_counterexample",
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
            output = write_verieql_canary(
                output_root=Path(tmp) / "output",
                run_id="verieql_contract",
                pair_records=[synthetic_pair_record(pair_id="p1", run_id="verieql_contract", tool="verieql")],
                command="/definitely/missing/verieql",
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


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _fake_verieql_root(path: Path, body: list[str] | None = None) -> Path:
    root = path
    module_dir = root / "parallel"
    module_dir.mkdir(parents=True, exist_ok=True)
    (module_dir / "__init__.py").write_text("", encoding="utf-8")
    (root / "README.md").write_text("fake VeriEQL root\n", encoding="utf-8")
    (module_dir / "cli_within_timeout.py").write_text(
        "\n".join(
            body
            or [
                "import argparse",
                "parser = argparse.ArgumentParser()",
                "parser.add_argument('-f')",
                "parser.add_argument('-t')",
                "parser.add_argument('-o')",
                "args = parser.parse_args()",
                "open(args.o, 'w', encoding='utf-8').write('{\"index\": 1, \"states\": [\"EQU\"]}\\n')",
            ]
        ),
        encoding="utf-8",
    )
    return root


if __name__ == "__main__":
    unittest.main()
