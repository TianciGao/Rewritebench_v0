import csv
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest
import uuid
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


def _postgres_case_row(case_id: str):
    rows = resolve_common_core_selection(
        repo_root=REPO_ROOT,
        case_set="common_core_v0",
        engine="postgres",
    )
    for row in rows:
        if row.case_id == case_id:
            return row
    raise AssertionError(f"case not selected: {case_id}")


def _load_adapter_module():
    spec = importlib.util.spec_from_file_location("calcite_hep_fail_closed_adapter", ADAPTER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _clear_calcite_env() -> None:
    for name in [
        "SQLRB_CALCITE_HEP_CMD",
        "SQLRB_CALCITE_HEP_JAR",
        "SQLRB_CALCITE_HEP_ROOT",
        "SQLRB_CALCITE_HEP_JAVA",
        "SQLRB_CALCITE_HEP_MODE",
        "SQLRB_CALCITE_HEP_TIMEOUT",
    ]:
        os.environ.pop(name, None)


def _unique_user_out(name: str) -> Path:
    return Path("runs") / "user" / f"{name}_{uuid.uuid4().hex}"


class CalciteHepFailClosedRouteTests(unittest.TestCase):
    def test_postgres_identifier_normalization_unquotes_schema_identifiers_only(self) -> None:
        adapter = _load_adapter_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            ddl = Path(temp_dir) / "ddl.sql"
            ddl.write_text("CREATE TABLE DEPT (NAME VARCHAR(32));\n", encoding="utf-8")
            normalized, metadata = adapter.normalize_postgres_calcite_identifiers(
                'SELECT "NAME", COUNT(*) AS "C" FROM "DEPT" GROUP BY "NAME";\n',
                ddl,
            )

        self.assertEqual(
            normalized,
            'SELECT name, COUNT(*) AS "C" FROM dept GROUP BY name;\n',
        )
        self.assertTrue(metadata["enabled"])
        self.assertEqual(metadata["policy"], "postgres_only_unquoted_ddl_identifier_fold_v0")
        self.assertEqual(metadata["replacement_count"], 3)
        self.assertEqual(metadata["replacement_identifiers"], {"DEPT": "dept", "NAME": "name"})

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

    def test_adapter_invokes_configured_external_command(self) -> None:
        row = _postgres_smoke_row()
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {}, clear=False):
            runtime_script = Path(temp_dir) / "fake_calcite_runtime.py"
            runtime_script.write_text(
                "\n".join(
                    [
                        "import pathlib",
                        "import sys",
                        "args = dict(zip(sys.argv[1::2], sys.argv[2::2]))",
                        "assert pathlib.Path(args['--source-sql']).exists()",
                        "assert pathlib.Path(args['--ddl']).exists()",
                        "pathlib.Path(args['--output-sql']).write_text('SELECT 1;\\n', encoding='utf-8')",
                        "print('runtime_ok=true')",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            _clear_calcite_env()
            os.environ["SQLRB_CALCITE_HEP_CMD"] = f"{sys.executable} {runtime_script}"
            os.environ["SQLRB_CALCITE_HEP_ROOT"] = temp_dir
            result = run_adapter_for_case(
                run_id="calcite_external_runtime_unit",
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
        self.assertTrue(result.candidate_generated)
        self.assertEqual(result.candidate_capture_mode, "candidate_file")
        self.assertEqual(payload["preflight_status"], "calcite_invocation_succeeded")
        self.assertTrue(payload["candidate_generated"])
        self.assertEqual(payload["failure_bucket"], "none")
        self.assertTrue(payload["schema_ddl_exists"])
        self.assertFalse(payload["official_metric_input"])

    def test_adapter_postprocesses_calcite_quoted_postgres_schema_identifiers(self) -> None:
        row = _postgres_case_row("CONS_0036")
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {}, clear=False):
            runtime_script = Path(temp_dir) / "fake_calcite_runtime.py"
            runtime_script.write_text(
                "\n".join(
                    [
                        "import pathlib",
                        "import sys",
                        "args = dict(zip(sys.argv[1::2], sys.argv[2::2]))",
                        "assert pathlib.Path(args['--source-sql']).exists()",
                        "assert pathlib.Path(args['--ddl']).exists()",
                        "pathlib.Path(args['--output-sql']).write_text(",
                        "    'SELECT \"NAME\", COUNT(*) AS \"C\"\\nFROM \"DEPT\"\\nGROUP BY \"NAME\"\\n',",
                        "    encoding='utf-8',",
                        ")",
                        "print('runtime_ok=true')",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            _clear_calcite_env()
            os.environ["SQLRB_CALCITE_HEP_CMD"] = f"{sys.executable} {runtime_script}"
            os.environ["SQLRB_CALCITE_HEP_ROOT"] = temp_dir
            result = run_adapter_for_case(
                run_id="calcite_postgres_identifier_postprocess_unit",
                row=row,
                resolved_package=resolved,
                adapter_command=f"{sys.executable} {ADAPTER}",
                repo_root=REPO_ROOT,
                out_dir=Path(temp_dir) / "out",
                timeout=10,
            )
            candidate_sql = result.candidate_sql_path.read_text(encoding="utf-8")
            status_path = result.workspace_dir / "calcite_hep_status.json"
            payload = json.loads(status_path.read_text(encoding="utf-8"))

        self.assertTrue(result.candidate_generated)
        self.assertIn("FROM dept", candidate_sql)
        self.assertIn("GROUP BY name", candidate_sql)
        self.assertIn('AS "C"', candidate_sql)
        self.assertNotIn('"DEPT"', candidate_sql)
        self.assertNotIn('"NAME"', candidate_sql)
        postprocess = payload["candidate_postprocess"]
        self.assertTrue(postprocess["changed"])
        self.assertEqual(postprocess["policy"], "postgres_only_unquoted_ddl_identifier_fold_v0")
        self.assertEqual(postprocess["replacement_identifiers"], {"DEPT": "dept", "NAME": "name"})

    def test_adapter_fails_closed_for_mysql_postgres_dialect_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {}, clear=False):
            case_list = Path(temp_dir) / "cases.txt"
            case_list.write_text("CONS_0036\n", encoding="utf-8")
            row = resolve_common_core_selection(
                repo_root=REPO_ROOT,
                case_set="common_core_v0",
                engine="mysql",
                case_list=case_list,
            )[0]
            resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
            runtime_script = Path(temp_dir) / "fake_calcite_runtime.py"
            runtime_script.write_text(
                "\n".join(
                    [
                        "import pathlib",
                        "import sys",
                        "args = dict(zip(sys.argv[1::2], sys.argv[2::2]))",
                        "pathlib.Path(args['--output-sql']).write_text(",
                        "    'SELECT \"NAME\" FROM \"DEPT\"\\n',",
                        "    encoding='utf-8',",
                        ")",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            _clear_calcite_env()
            os.environ["SQLRB_CALCITE_HEP_CMD"] = f"{sys.executable} {runtime_script}"
            os.environ["SQLRB_CALCITE_HEP_ROOT"] = temp_dir
            result = run_adapter_for_case(
                run_id="calcite_mysql_target_dialect_guard_unit",
                row=row,
                resolved_package=resolved,
                adapter_command=f"{sys.executable} {ADAPTER}",
                repo_root=REPO_ROOT,
                out_dir=Path(temp_dir) / "out",
                timeout=10,
            )
            status_path = result.workspace_dir / "calcite_hep_status.json"
            payload = json.loads(status_path.read_text(encoding="utf-8"))
            unsupported_path_exists = Path(
                payload["target_dialect_guard"]["unsupported_candidate_sql_path"]
            ).exists()

        self.assertFalse(result.candidate_generated)
        self.assertIsNone(result.candidate_sql_path)
        self.assertFalse((result.workspace_dir / "candidate.sql").exists())
        self.assertEqual(payload["preflight_status"], "calcite_target_dialect_unsupported")
        guard = payload["target_dialect_guard"]
        self.assertTrue(guard["blocked"])
        self.assertEqual(guard["bucket"], "mysql_postgres_dialect_quoted_identifier")
        self.assertTrue(unsupported_path_exists)

    def test_adapter_fails_closed_for_spark_postgres_dialect_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {}, clear=False):
            case_list = Path(temp_dir) / "cases.txt"
            case_list.write_text("CONS_0036\n", encoding="utf-8")
            row = resolve_common_core_selection(
                repo_root=REPO_ROOT,
                case_set="common_core_v0",
                engine="spark",
                case_list=case_list,
            )[0]
            resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
            runtime_script = Path(temp_dir) / "fake_calcite_runtime.py"
            runtime_script.write_text(
                "\n".join(
                    [
                        "import pathlib",
                        "import sys",
                        "args = dict(zip(sys.argv[1::2], sys.argv[2::2]))",
                        "pathlib.Path(args['--output-sql']).write_text(",
                        "    'SELECT CAST(\"id\" AS DOUBLE PRECISION) FROM \"cards\"\\n',",
                        "    encoding='utf-8',",
                        ")",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            _clear_calcite_env()
            os.environ["SQLRB_CALCITE_HEP_CMD"] = f"{sys.executable} {runtime_script}"
            os.environ["SQLRB_CALCITE_HEP_ROOT"] = temp_dir
            result = run_adapter_for_case(
                run_id="calcite_spark_target_dialect_guard_unit",
                row=row,
                resolved_package=resolved,
                adapter_command=f"{sys.executable} {ADAPTER}",
                repo_root=REPO_ROOT,
                out_dir=Path(temp_dir) / "out",
                timeout=10,
            )
            status_path = result.workspace_dir / "calcite_hep_status.json"
            payload = json.loads(status_path.read_text(encoding="utf-8"))
            unsupported_path_exists = Path(
                payload["target_dialect_guard"]["unsupported_candidate_sql_path"]
            ).exists()

        self.assertFalse(result.candidate_generated)
        self.assertIsNone(result.candidate_sql_path)
        self.assertFalse((result.workspace_dir / "candidate.sql").exists())
        self.assertEqual(payload["preflight_status"], "calcite_target_dialect_unsupported")
        guard = payload["target_dialect_guard"]
        self.assertTrue(guard["blocked"])
        self.assertEqual(guard["bucket"], "spark_postgres_dialect_quoted_identifier")
        self.assertTrue(unsupported_path_exists)

    def test_adapter_fails_closed_when_external_command_fails(self) -> None:
        row = _postgres_smoke_row()
        resolved = resolve_case_package(repo_root=REPO_ROOT, row=row)
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {}, clear=False):
            runtime_script = Path(temp_dir) / "failing_calcite_runtime.py"
            runtime_script.write_text(
                "import sys\nprint('boom', file=sys.stderr)\nsys.exit(7)\n",
                encoding="utf-8",
            )
            _clear_calcite_env()
            os.environ["SQLRB_CALCITE_HEP_CMD"] = f"{sys.executable} {runtime_script}"
            os.environ["SQLRB_CALCITE_HEP_ROOT"] = temp_dir
            result = run_adapter_for_case(
                run_id="calcite_external_runtime_failure_unit",
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
        self.assertEqual(payload["preflight_status"], "calcite_invocation_failed")
        self.assertFalse(payload["candidate_generated"])
        self.assertEqual(payload["failure_bucket"], FAILURE_NO_CANDIDATE_SQL)
        self.assertEqual(payload["runtime"]["exit_code"], 7)

    def test_user_run_captures_calcite_fail_closed_rows(self) -> None:
        out = _unique_user_out("calcite_fail_closed_unit")
        try:
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
        finally:
            shutil.rmtree(REPO_ROOT / out, ignore_errors=True)

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
