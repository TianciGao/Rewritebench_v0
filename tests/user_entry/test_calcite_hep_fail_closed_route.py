import csv
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sql_rewrite_bench.adapter_runner import run_adapter_for_case
from sql_rewrite_bench.case_package_resolver import resolve_case_package
from sql_rewrite_bench.case_selection import resolve_common_core_selection
from sql_rewrite_bench.local_timing import route_identity
from sql_rewrite_bench.user_run import run_user_benchmark
from sql_rewrite_bench.user_run_schema import EXTRACTION_NO_CANDIDATE_SQL, FAILURE_NO_CANDIDATE_SQL


REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTER = REPO_ROOT / "baselines" / "calcite_hep_fail_closed" / "adapter.py"


def _postgres_smoke_row():
    return resolve_common_core_selection(
        repo_root=REPO_ROOT,
        case_set="common_core_v0",
        engine="postgres",
        smoke=True,
    )[0]


def _clear_calcite_env() -> None:
    for name in [
        "SQLRB_CALCITE_HEP_CMD",
        "SQLRB_CALCITE_HEP_JAR",
        "SQLRB_CALCITE_HEP_ROOT",
        "SQLRB_CALCITE_HEP_JAVA",
    ]:
        os.environ.pop(name, None)


class CalciteHepFailClosedRouteTests(unittest.TestCase):
    def test_route_identity_recognizes_calcite_adapter(self) -> None:
        command = f"{sys.executable} {ADAPTER}"
        self.assertEqual(
            route_identity(command),
            ("calcite_hep_fail_closed", "calcite_hep_fail_closed"),
        )
        self.assertEqual(
            route_identity(f"{sys.executable} {REPO_ROOT / 'baselines' / 'calcite_hep_fail_closed' / 'adapter.py'}"),
            ("calcite_hep_fail_closed", "calcite_hep_fail_closed"),
        )

    def test_adapter_fails_closed_without_calcite_runtime(self) -> None:
        row = _postgres_smoke_row()
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {}, clear=False):
            _clear_calcite_env()
            result = run_adapter_for_case(
                run_id="calcite_fail_closed_unit",
                row=row,
                resolved_package=resolved,
                adapter_command=f"{sys.executable} {ADAPTER}",
                repo_root=REPO_ROOT,
                out_dir=Path(temp_dir) / "out",
                timeout=10,
            )
            status_path = result.workspace_dir / "calcite_hep_status.json"
            payload = json.loads(status_path.read_text(encoding="utf-8"))

        self.assertTrue(result.adapter_invoked)
        self.assertEqual(result.adapter_exit_code, 0)
        self.assertFalse(result.candidate_generated)
        self.assertEqual(result.extraction_status, EXTRACTION_NO_CANDIDATE_SQL)
        self.assertEqual(result.failure_bucket_hint, FAILURE_NO_CANDIDATE_SQL)
        self.assertEqual(payload["route_id"], "calcite_hep_fail_closed")
        self.assertEqual(payload["method_id"], "calcite_hep_fail_closed")
        self.assertEqual(payload["route_policy"], "fail_closed")
        self.assertFalse(payload["candidate_generated"])
        self.assertIn(payload["preflight_status"], {"calcite_runtime_unavailable", "calcite_java_missing"})
        self.assertFalse(payload["official_metric_input"])

    def test_user_run_captures_calcite_fail_closed_rows(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "runs" / "user") as temp_dir:
            out = Path(temp_dir).relative_to(REPO_ROOT)
            with patch.dict(os.environ, {}, clear=False):
                _clear_calcite_env()
                summary = run_user_benchmark(
                    argparse_namespace(
                        case_set="common_core_v0",
                        pool="all",
                        engine="postgres",
                        case_list=None,
                        smoke=True,
                        adapter_command=f"{sys.executable} {ADAPTER}",
                        out=out,
                        run_id="calcite_fail_closed_unit_run",
                        adapter_timeout=10,
                        dry_run=False,
                        enable_db_execution=False,
                        enable_checker=False,
                        collect_timing=False,
                    ),
                    REPO_ROOT,
                )
            with (REPO_ROOT / out / "ledger.csv").open(newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))

        self.assertEqual(summary["selected_rows"], 2)
        self.assertEqual(summary["adapter_invoked_rows"], 2)
        self.assertEqual(summary["candidate_generated_rows"], 0)
        self.assertEqual({row["failure_bucket"] for row in rows}, {FAILURE_NO_CANDIDATE_SQL})
        self.assertEqual({row["extraction_status"] for row in rows}, {EXTRACTION_NO_CANDIDATE_SQL})


def argparse_namespace(**kwargs):
    from argparse import Namespace

    return Namespace(**kwargs)


if __name__ == "__main__":
    unittest.main()
