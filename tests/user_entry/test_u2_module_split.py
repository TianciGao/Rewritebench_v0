import csv
import json
import sys
import tempfile
import unittest
import uuid
from argparse import Namespace
from pathlib import Path

from sql_rewrite_bench.adapter_runner import run_adapter_for_case
from sql_rewrite_bench.case_package_resolver import resolve_case_package
from sql_rewrite_bench.case_selection import (
    SelectedCaseEngineRow,
    resolve_common_core_selection,
)
from sql_rewrite_bench.user_ledger import (
    dry_run_ledger_for_row,
    failure_rows_from_ledger,
    ledger_from_adapter_result,
    write_failures,
    write_ledger,
)
from sql_rewrite_bench.user_run import run_user_benchmark
from sql_rewrite_bench.user_run_schema import FAILURE_FIELDS, LEDGER_FIELDS


REPO_ROOT = Path(__file__).resolve().parents[2]


def _smoke_rows() -> list[SelectedCaseEngineRow]:
    return resolve_common_core_selection(
        repo_root=REPO_ROOT,
        case_set="common_core_v0",
        engine="postgres",
        smoke=True,
    )


def _unique_out(name: str) -> Path:
    return Path("runs/user") / f"{name}_{uuid.uuid4().hex}"


class U2ModuleSplitTests(unittest.TestCase):
    def test_resolver_resolves_smoke_cases(self) -> None:
        rows = _smoke_rows()
        self.assertEqual([row.case_id for row in rows], ["PERF_0006", "CONS_0005"])
        for row in rows:
            resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
            self.assertEqual(resolved.case_id, row.case_id)
            self.assertEqual(resolved.pool, row.pool)
            self.assertTrue(resolved.manifest_path.exists())
            self.assertTrue(resolved.source_sql_path.exists())
            self.assertTrue(resolved.schema_profile_path.exists())
            self.assertIsNotNone(resolved.schema_external_profile_path)
            self.assertTrue(resolved.schema_external_profile_path.exists())
            self.assertTrue(resolved.checker_config_path.exists())
            self.assertTrue(resolved.normalization_config_path.exists())
            self.assertTrue(resolved.compare_config_path.exists())
            self.assertEqual(resolved.resolution_status, "ok")

    def test_resolver_fails_closed_on_missing_required_package_asset(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "cases" / "PERF" / "PERF_TEST"
            case_dir.mkdir(parents=True)
            (case_dir / "manifest.yaml").write_text(
                "\n".join(
                    [
                        "case_id: PERF_TEST",
                        "pool: PERF",
                        "package_path: cases/PERF/PERF_TEST",
                        "sql:",
                        "  source: sql/source.sql",
                        "schema:",
                        "  profile: schema/schema_profile.yaml",
                        "checker:",
                        "  checker: checker/checker.yaml",
                        "  normalization: checker/normalization.yaml",
                        "  compare_config: checker/compare_config.yaml",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            row = SelectedCaseEngineRow(
                denominator_id="track_a_same_engine:PERF_TEST:postgres",
                case_id="PERF_TEST",
                pool="PERF",
                engine="postgres",
                planned="true",
                case_path="cases/PERF/PERF_TEST",
                source_sql_path="cases/PERF/PERF_TEST/sql/source.sql",
            )
            with self.assertRaisesRegex(FileNotFoundError, "sql.source"):
                resolve_case_package(repo_root=root, row=row)

    def test_adapter_runner_exposes_required_environment_variables(self) -> None:
        row = _smoke_rows()[0]
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            adapter = temp / "adapter.py"
            adapter.write_text(
                "\n".join(
                    [
                        "import json, os",
                        "from pathlib import Path",
                        "workspace = Path(os.environ['SQLRB_WORKSPACE_DIR'])",
                        "workspace.mkdir(parents=True, exist_ok=True)",
                        "keys = [",
                        "  'SQLRB_RUN_ID', 'SQLRB_CASE_ID', 'SQLRB_POOL', 'SQLRB_ENGINE',",
                        "  'SQLRB_CASE_DIR', 'SQLRB_SOURCE_SQL_PATH', 'SQLRB_WORKSPACE_DIR',",
                        "  'SQLRB_CANDIDATE_SQL_PATH'",
                        "]",
                        "(workspace / 'env.json').write_text(json.dumps({k: os.environ[k] for k in keys}, sort_keys=True))",
                        "Path(os.environ['SQLRB_CANDIDATE_SQL_PATH']).write_text('select 1 as value;\\n')",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            result = run_adapter_for_case(
                run_id="u2_env_test",
                row=row,
                resolved_package=resolved,
                adapter_command=f"{sys.executable} {adapter}",
                repo_root=REPO_ROOT,
                out_dir=temp / "out",
                timeout=10,
            )
            payload = json.loads((result.workspace_dir / "env.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["SQLRB_RUN_ID"], "u2_env_test")
        self.assertEqual(payload["SQLRB_CASE_ID"], row.case_id)
        self.assertEqual(payload["SQLRB_POOL"], row.pool)
        self.assertEqual(payload["SQLRB_ENGINE"], row.engine)
        self.assertEqual(payload["SQLRB_SOURCE_SQL_PATH"], str(resolved.source_sql_path))
        self.assertEqual(payload["SQLRB_CASE_DIR"], str(resolved.case_dir))
        self.assertEqual(result.candidate_generated, True)

    def test_adapter_runner_prefers_workspace_candidate_over_stdout(self) -> None:
        row = _smoke_rows()[0]
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            adapter = temp / "adapter.py"
            adapter.write_text(
                "\n".join(
                    [
                        "import os",
                        "from pathlib import Path",
                        "Path(os.environ['SQLRB_CANDIDATE_SQL_PATH']).write_text('select 111 as chosen;\\n')",
                        "print('select 222 as ignored;')",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            result = run_adapter_for_case(
                run_id="u2_priority_test",
                row=row,
                resolved_package=resolved,
                adapter_command=f"{sys.executable} {adapter}",
                repo_root=REPO_ROOT,
                out_dir=temp / "out",
                timeout=10,
            )
            captured = result.candidate_sql_path.read_text(encoding="utf-8")
        self.assertEqual(result.extraction_status, "captured_from_candidate_file")
        self.assertIn("select 111 as chosen", captured)
        self.assertNotIn("select 222 as ignored", captured)

    def test_adapter_runner_records_failure_and_timeout_statuses(self) -> None:
        row = _smoke_rows()[0]
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        failing = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "failing_adapter.py"
        slow = REPO_ROOT / "tests" / "user_entry" / "fixtures" / "slow_adapter.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            failed = run_adapter_for_case(
                run_id="u2_failed_test",
                row=row,
                resolved_package=resolved,
                adapter_command=f"{sys.executable} {failing}",
                repo_root=REPO_ROOT,
                out_dir=temp / "failed",
                timeout=10,
            )
            timed_out = run_adapter_for_case(
                run_id="u2_timeout_test",
                row=row,
                resolved_package=resolved,
                adapter_command=f"{sys.executable} {slow}",
                repo_root=REPO_ROOT,
                out_dir=temp / "timeout",
                timeout=1,
            )
        self.assertEqual(failed.adapter_exit_code, 7)
        self.assertEqual(failed.extraction_status, "adapter_failed")
        self.assertEqual(failed.failure_bucket_hint, "adapter_failed")
        self.assertIsNone(timed_out.adapter_exit_code)
        self.assertEqual(timed_out.extraction_status, "adapter_failed")
        self.assertEqual(timed_out.failure_bucket_hint, "adapter_timeout")

    def test_ledger_writer_preserves_current_columns(self) -> None:
        row = _smoke_rows()[0]
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            ledger = dry_run_ledger_for_row(
                run_id="u2_ledger_test",
                row=row,
                repo_root=REPO_ROOT,
                out_dir=temp / "out",
            )
            ledger_path = temp / "ledger.csv"
            failures_path = temp / "failures.csv"
            write_ledger(ledger_path, [ledger])
            write_failures(failures_path, failure_rows_from_ledger([ledger]))
            with ledger_path.open(newline="", encoding="utf-8") as f:
                ledger_reader = csv.DictReader(f)
                ledger_rows = list(ledger_reader)
            with failures_path.open(newline="", encoding="utf-8") as f:
                failure_reader = csv.DictReader(f)
                failure_rows = list(failure_reader)
        self.assertEqual(ledger_reader.fieldnames, LEDGER_FIELDS)
        self.assertEqual(failure_reader.fieldnames, FAILURE_FIELDS)
        self.assertEqual(ledger_rows[0]["extraction_status"], "skipped_dry_run")
        self.assertEqual(failure_rows, [])

    def test_user_run_public_smoke_dry_run_behavior_unchanged(self) -> None:
        out = _unique_out("unittest_u2_public_smoke_dry_run")
        adapter = REPO_ROOT / "examples" / "user" / "noop_adapter.py"
        args = Namespace(
            case_set="common_core_v0",
            pool="all",
            engine="postgres",
            case_list=None,
            smoke=True,
            adapter_command=f"{sys.executable} {adapter}",
            out=out,
            run_id=None,
            adapter_timeout=30,
            dry_run=True,
        )
        summary = run_user_benchmark(args, REPO_ROOT)
        self.assertEqual(summary["selected_rows"], 2)
        self.assertEqual(summary["adapter_invoked_rows"], 0)
        self.assertEqual(summary["candidate_generated_rows"], 0)
        with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual([row["case_id"] for row in rows], ["PERF_0006", "CONS_0005"])
        self.assertEqual({row["extraction_status"] for row in rows}, {"skipped_dry_run"})


if __name__ == "__main__":
    unittest.main()
