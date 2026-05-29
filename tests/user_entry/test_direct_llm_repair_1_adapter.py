import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTER = REPO_ROOT / "baselines" / "direct_llm_repair_1" / "adapter.py"


def _load_adapter_module():
    spec = importlib.util.spec_from_file_location("direct_llm_repair_1_adapter", ADAPTER)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load Direct LLM Repair-1 adapter module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _pythonpath_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    return env


def _adapter_env(temp_dir: Path, *, engine: str = "postgres") -> dict[str, str]:
    source_path = temp_dir / "source.sql"
    source_path.write_text("SELECT a, b FROM table1 WHERE a > 0;\n", encoding="utf-8")
    original_candidate_path = temp_dir / "original_candidate.sql"
    original_candidate_path.write_text("SELECT a FROM table1 WHERE a > 0;\n", encoding="utf-8")
    schema_dir = temp_dir / "schema"
    schema_dir.mkdir()
    (schema_dir / "ddl_pg.sql").write_text(
        "CREATE TABLE table1 (a INTEGER, b INTEGER);\n",
        encoding="utf-8",
    )
    workspace = temp_dir / "workspace"
    return {
        **_pythonpath_env(),
        "SQLRB_RUN_ID": "repair_1_fixture_run",
        "SQLRB_CASE_ID": "CONS_0005",
        "SQLRB_POOL": "CONS",
        "SQLRB_ENGINE": engine,
        "SQLRB_SOURCE_SQL_PATH": str(source_path),
        "SQLRB_CASE_DIR": str(temp_dir),
        "SQLRB_WORKSPACE_DIR": str(workspace),
        "SQLRB_CANDIDATE_SQL_PATH": str(workspace / "candidate.sql"),
        "SQLRB_REPAIR1_ORIGINAL_CANDIDATE_SQL_PATH": str(original_candidate_path),
        "SQLRB_REPAIR1_ORIGINAL_CANDIDATE_ID": "direct_llm_original_track_a_120_canonical_v0:CONS_0005:postgres:direct_llm_original",
        "SQLRB_REPAIR1_ORIGINAL_RUN_ID": "direct_llm_original_track_a_120_canonical_v0",
        "SQLRB_LLM_PROVIDER": "fake",
        "SQLRB_LLM_FAKE_RESPONSE": "SELECT a, b FROM table1 WHERE a > 0;",
    }


def _write_feedback(temp_dir: Path, payload: dict[str, object]) -> Path:
    path = temp_dir / "feedback.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _run_adapter(env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ADAPTER)],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


class DirectLlmRepair1AdapterTests(unittest.TestCase):
    def test_adapter_help_works(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ADAPTER), "--help"],
            cwd=REPO_ROOT,
            env=_pythonpath_env(),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--dry-run-prompt", completed.stdout)

    def test_mismatch_repair_prompt_construction(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            feedback_path = _write_feedback(
                temp_dir,
                {
                    "feedback_type": "checker_mismatch_feedback",
                    "source_executable": True,
                    "candidate_executable": True,
                    "checker_attempted": True,
                    "exact_status": "mismatch",
                    "failure_bucket": "mismatch",
                    "checker_or_error_summary": "checker_mismatch: candidate omitted column b",
                },
            )
            env["SQLRB_REPAIR1_FEEDBACK_PATH"] = str(feedback_path)
            completed = _run_adapter(env)
            workspace = temp_dir / "workspace"
            prompt_text = (workspace / "direct_llm_repair_1_prompt.json").read_text(encoding="utf-8")
            prompt = json.loads(prompt_text)
            status = json.loads((workspace / "direct_llm_repair_1_status.json").read_text(encoding="utf-8"))
            candidate = (workspace / "candidate.sql").read_text(encoding="utf-8")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(candidate, "SELECT a, b FROM table1 WHERE a > 0;\n")
        self.assertIn("checker_mismatch_feedback", prompt_text)
        self.assertIn("candidate omitted column b", prompt_text)
        self.assertIn("Original Direct LLM candidate SQL", prompt_text)
        self.assertEqual(prompt["prompt_template_id"], "direct_llm_repair_1_feedback_sql_only_v0")
        self.assertEqual(status["feedback_type"], "checker_mismatch_feedback")
        self.assertEqual(status["repair_prompt_template_id"], "direct_llm_repair_1_feedback_sql_only_v0")
        self.assertEqual(status["extraction_policy"], "single_sql_candidate_repair_v0")
        self.assertTrue(status["candidate_generated"])
        self.assertTrue(status["repair_attempted"])
        self.assertFalse(status["live_call"])
        self.assertEqual(status["failure_bucket"], "none")

    def test_candidate_execution_failed_repair_prompt_construction(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir, engine="spark")
            env["SQLRB_POOL"] = "LONGTAIL"
            env["SQLRB_CASE_ID"] = "LONGTAIL_0012"
            feedback_path = _write_feedback(
                temp_dir,
                {
                    "feedback_type": "candidate_execution_error_feedback",
                    "source_executable": True,
                    "candidate_executable": False,
                    "checker_attempted": False,
                    "exact_status": "not_attempted",
                    "failure_bucket": "candidate_execution_failed",
                    "execution_error_summary": "candidate_execution_failed_before_checker: unresolved column x",
                    "normalized_execution_error_class": "unresolved_column",
                },
            )
            env["SQLRB_REPAIR1_FEEDBACK_PATH"] = str(feedback_path)
            env["SQLRB_LLM_FAKE_RESPONSE"] = "```sql\nSELECT a, b FROM table1 WHERE a > 0\n```"
            completed = _run_adapter(env)
            workspace = temp_dir / "workspace"
            prompt_text = (workspace / "direct_llm_repair_1_prompt.json").read_text(encoding="utf-8")
            status = json.loads((workspace / "direct_llm_repair_1_status.json").read_text(encoding="utf-8"))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("candidate_execution_error_feedback", prompt_text)
        self.assertIn("unresolved column x", prompt_text)
        self.assertIn("normalized_execution_error_class: unresolved_column", prompt_text)
        self.assertEqual(status["feedback_type"], "candidate_execution_error_feedback")
        self.assertTrue(status["candidate_generated"])

    def test_unsupported_engine_row_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir, engine="spark")
            env["SQLRB_CASE_ID"] = "PORT_0008"
            env["SQLRB_POOL"] = "PORT"
            feedback_path = _write_feedback(
                temp_dir,
                {
                    "feedback_type": "unsupported_engine_boundary_feedback",
                    "source_executable": False,
                    "candidate_executable": False,
                    "checker_attempted": False,
                    "exact_status": "not_attempted",
                    "failure_bucket": "unsupported_engine",
                    "checker_or_error_summary": "source_engine_unsupported_fail_closed",
                },
            )
            env["SQLRB_REPAIR1_FEEDBACK_PATH"] = str(feedback_path)
            completed = _run_adapter(env)
            workspace = temp_dir / "workspace"
            status = json.loads((workspace / "direct_llm_repair_1_status.json").read_text(encoding="utf-8"))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse((workspace / "candidate.sql").exists())
        self.assertEqual(status["feedback_type"], "unsupported_engine_boundary_feedback")
        self.assertEqual(status["failure_bucket"], "unsupported_engine_boundary")
        self.assertFalse(status["repair_attempted"])
        self.assertFalse(status["call_attempted"])

    def test_missing_feedback_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.pop("SQLRB_REPAIR1_FEEDBACK_PATH", None)
            completed = _run_adapter(env)
            workspace = temp_dir / "workspace"
            status = json.loads((workspace / "direct_llm_repair_1_status.json").read_text(encoding="utf-8"))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse((workspace / "candidate.sql").exists())
        self.assertEqual(status["failure_bucket"], "missing_feedback")
        self.assertFalse(status["call_attempted"])

    def test_multiple_sql_extraction_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            feedback_path = _write_feedback(
                temp_dir,
                {
                    "feedback_type": "mismatch",
                    "source_executable": True,
                    "candidate_executable": True,
                    "checker_attempted": True,
                    "exact": False,
                    "failure_bucket": "mismatch",
                    "checker_error_summary": "checker_mismatch: row count changed",
                },
            )
            env["SQLRB_REPAIR1_FEEDBACK_PATH"] = str(feedback_path)
            env["SQLRB_LLM_FAKE_RESPONSE"] = "SELECT a FROM table1; SELECT b FROM table1;"
            completed = _run_adapter(env)
            workspace = temp_dir / "workspace"
            status = json.loads((workspace / "direct_llm_repair_1_status.json").read_text(encoding="utf-8"))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse((workspace / "candidate.sql").exists())
        self.assertEqual(status["extraction_status"], "sql_extraction_failed")
        self.assertEqual(status["failure_bucket"], "multiple_sql_statements_ambiguous")
        self.assertTrue(status["repair_attempted"])

    def test_secret_hygiene_for_fake_provider_outputs(self) -> None:
        secret_value = "fixture-api-key-value-123"
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            feedback_path = _write_feedback(
                temp_dir,
                {
                    "feedback_type": "checker_mismatch_feedback",
                    "source_executable": True,
                    "candidate_executable": True,
                    "checker_attempted": True,
                    "exact_status": "mismatch",
                    "failure_bucket": "mismatch",
                    "checker_or_error_summary": "checker_mismatch: expected two columns",
                },
            )
            env["SQLRB_REPAIR1_FEEDBACK_PATH"] = str(feedback_path)
            env["SQLRB_LLM_API_KEY"] = secret_value
            env["GPTSAPI_API_KEY"] = secret_value
            completed = _run_adapter(env)
            workspace = temp_dir / "workspace"
            written_text = "\n".join(path.read_text(encoding="utf-8") for path in workspace.rglob("*") if path.is_file())
            status = json.loads((workspace / "direct_llm_repair_1_status.json").read_text(encoding="utf-8"))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(status["api_key_present"])
        self.assertNotIn(secret_value, written_text)
        self.assertNotIn("api_key\": \"", written_text)

    def test_extraction_rejects_prose(self) -> None:
        module = _load_adapter_module()
        result = module.extract_sql_candidate("Here is the repaired query: SELECT 1;")
        self.assertEqual(result.status, "sql_extraction_failed")
        self.assertEqual(result.failure_bucket, "response_not_sql")


if __name__ == "__main__":
    unittest.main()
