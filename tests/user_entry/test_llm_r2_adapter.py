import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTER = REPO_ROOT / "baselines" / "llm_r2" / "adapter.py"


def _load_adapter_module():
    spec = importlib.util.spec_from_file_location("llm_r2_adapter", ADAPTER)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load LLM-R2 adapter module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _pythonpath_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    return env


def _adapter_env(temp_dir: Path, *, engine: str = "postgres", schema: bool = True) -> dict[str, str]:
    source_path = temp_dir / "source.sql"
    source_path.write_text("SELECT a FROM table1 WHERE a > 0;\n", encoding="utf-8")
    if schema:
        schema_dir = temp_dir / "schema"
        schema_dir.mkdir()
        (schema_dir / "ddl_pg.sql").write_text(
            "CREATE TABLE table1 (a INTEGER, b INTEGER);\n",
            encoding="utf-8",
        )
    workspace = temp_dir / "workspace"
    return {
        **_pythonpath_env(),
        "SQLRB_RUN_ID": "llm_r2_fixture_run",
        "SQLRB_CASE_ID": "CONS_0036",
        "SQLRB_POOL": "CONS",
        "SQLRB_ENGINE": engine,
        "SQLRB_SOURCE_SQL_PATH": str(source_path),
        "SQLRB_CASE_DIR": str(temp_dir),
        "SQLRB_WORKSPACE_DIR": str(workspace),
        "SQLRB_CANDIDATE_SQL_PATH": str(workspace / "candidate.sql"),
    }


def _run_adapter(env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ADAPTER)],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def _status(temp_dir: Path) -> dict[str, object]:
    return json.loads((temp_dir / "workspace" / "llm_r2_status.json").read_text(encoding="utf-8"))


class LLMR2AdapterTests(unittest.TestCase):
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
        self.assertIn("--dry-run-status", completed.stdout)

    def test_fake_runtime_json_returns_one_sql_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LLM_R2_MODE": "fake",
                    "SQLRB_LLM_R2_FAKE_RESPONSE": json.dumps(
                        {"status": "ok", "candidate_sql": "SELECT a FROM table1 WHERE a > 1"}
                    ),
                    "SQLRB_LLM_API_KEY": "secret-should-not-be-written",
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)
            status_text = json.dumps(status)
            candidate = (temp_dir / "workspace" / "candidate.sql").read_text(encoding="utf-8")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(candidate, "SELECT a FROM table1 WHERE a > 1;\n")
        self.assertTrue(status["candidate_generated"])
        self.assertEqual(status["route_id"], "llm_r2_gpt54_adapted")
        self.assertEqual(status["method_id"], "llm_r2")
        self.assertEqual(status["provider_policy"], "openai_compatible")
        self.assertEqual(status["model_policy"], "gpt-5.4")
        self.assertTrue(status["adapted_gpt54_local_diagnostic"])
        self.assertFalse(status["original_paper_reproduction"])
        self.assertFalse(status["official_llm_r2_stack"])
        self.assertTrue(status["fake_runtime"])
        self.assertFalse(status["live_call"])
        self.assertFalse(status["rule_system_runtime_used"])
        self.assertFalse(status["checkpoint_used"])
        self.assertFalse(status["demonstration_selector_used"])
        self.assertTrue(status["local_diagnostic_only"])
        self.assertNotIn("secret-should-not-be-written", status_text)

    def test_fake_rule_sequence_plus_sql_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LLM_R2_MODE": "fake",
                    "SQLRB_LLM_R2_FAKE_RESPONSE": json.dumps(
                        {
                            "status": "ok",
                            "content": "Rules:\n- FilterProjectTranspose\nSQL:\nSELECT a FROM table1 WHERE a > 2",
                            "rule_sequence": ["FilterProjectTranspose"],
                        }
                    ),
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)
            candidate = (temp_dir / "workspace" / "candidate.sql").read_text(encoding="utf-8")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(candidate, "SELECT a FROM table1 WHERE a > 2;\n")
        self.assertTrue(status["rule_sequence_present"])
        self.assertEqual(status["rule_sequence"], ["FilterProjectTranspose"])
        self.assertEqual(status["extraction_status"], "extracted")

    def test_fake_runtime_safe_sql_fence_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LLM_R2_MODE": "fake",
                    "SQLRB_LLM_R2_FAKE_SQL": "```sql\nWITH c AS (SELECT a FROM table1) SELECT a FROM c\n```",
                }
            )
            completed = _run_adapter(env)
            candidate = (temp_dir / "workspace" / "candidate.sql").read_text(encoding="utf-8")
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(candidate, "WITH c AS (SELECT a FROM table1) SELECT a FROM c;\n")
        self.assertEqual(status["extraction_status"], "extracted")

    def test_multiple_sql_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LLM_R2_MODE": "fake",
                    "SQLRB_LLM_R2_FAKE_RESPONSE": json.dumps(
                        {"status": "ok", "candidate_sql": "SELECT a FROM table1; SELECT b FROM table1;"}
                    ),
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse((temp_dir / "workspace" / "candidate.sql").exists())
        self.assertEqual(status["fail_closed_reason"], "multiple_sql_statements")

    def test_prose_empty_and_ambiguous_markdown_fail_closed(self) -> None:
        fixtures = [
            ("Here is the rewrite: SELECT a FROM table1;", "response_not_sql"),
            ("   ", "response_empty"),
            ("```python\nprint('not sql')\n```", "ambiguous_markdown"),
        ]
        for raw_response, expected_bucket in fixtures:
            with self.subTest(expected_bucket=expected_bucket):
                with tempfile.TemporaryDirectory() as temp_name:
                    temp_dir = Path(temp_name)
                    env = _adapter_env(temp_dir)
                    env.update(
                        {
                            "SQLRB_LLM_R2_MODE": "fake",
                            "SQLRB_LLM_R2_FAKE_RESPONSE": json.dumps(
                                {"status": "ok", "candidate_sql": raw_response}
                            ),
                        }
                    )
                    completed = _run_adapter(env)
                    status = _status(temp_dir)

                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertFalse(status["candidate_generated"])
                self.assertEqual(status["fail_closed_reason"], expected_bucket)

    def test_malformed_json_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update({"SQLRB_LLM_R2_MODE": "fake", "SQLRB_LLM_R2_FAKE_RESPONSE": '{"status":"ok"'})
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse(status["candidate_generated"])
        self.assertEqual(status["runtime_status"], "fake_runtime_malformed_json")
        self.assertEqual(status["fail_closed_reason"], "malformed_json")

    def test_rule_only_response_without_sql_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LLM_R2_MODE": "fake",
                    "SQLRB_LLM_R2_FAKE_RESPONSE": json.dumps(
                        {"status": "ok", "content": "Rules:\n- FilterMerge\n- ProjectMerge"}
                    ),
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse(status["candidate_generated"])
        self.assertEqual(status["fail_closed_reason"], "response_not_sql")

    def test_missing_source_and_schema_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            Path(env["SQLRB_SOURCE_SQL_PATH"]).unlink()
            env.update({"SQLRB_LLM_R2_MODE": "fake", "SQLRB_LLM_R2_FAKE_SQL": "SELECT a FROM table1"})
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(status["fail_closed_reason"], "missing_source_sql")

        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir, schema=False)
            env.update({"SQLRB_LLM_R2_MODE": "fake", "SQLRB_LLM_R2_FAKE_SQL": "SELECT a FROM table1"})
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(status["fail_closed_reason"], "missing_schema_context")

    def test_unsupported_engine_fails_closed_before_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir, engine="mysql")
            env.update({"SQLRB_LLM_R2_MODE": "fake", "SQLRB_LLM_R2_FAKE_SQL": "SELECT a FROM table1"})
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse(status["candidate_generated"])
        self.assertEqual(status["fail_closed_reason"], "unsupported_engine")
        self.assertEqual(status["runtime_status"], "not_attempted")

    def test_live_mode_without_gate_or_api_key_fails_closed_without_call(self) -> None:
        fixtures = [
            ({}, "live_gate_missing"),
            ({"SQLRB_LLM_ALLOW_LIVE": "1"}, "missing_api_key"),
        ]
        for extra_env, expected in fixtures:
            with self.subTest(expected=expected):
                with tempfile.TemporaryDirectory() as temp_name:
                    temp_dir = Path(temp_name)
                    env = _adapter_env(temp_dir)
                    env.update({"SQLRB_LLM_R2_MODE": "live"})
                    env.pop("SQLRB_LLM_API_KEY", None)
                    env.pop("GPTSAPI_API_KEY", None)
                    env.pop("SQLRB_LLM_ALLOW_LIVE", None)
                    env.update(extra_env)
                    completed = _run_adapter(env)
                    status = _status(temp_dir)

                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertFalse(status["candidate_generated"])
                self.assertEqual(status["fail_closed_reason"], expected)
                self.assertFalse(status["live_call"])

    def test_live_mode_with_gate_still_fails_closed_without_call(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LLM_R2_MODE": "live",
                    "SQLRB_LLM_PROVIDER": "openai_compatible",
                    "SQLRB_LLM_BASE_URL": "https://api.gptsapi.net/v1",
                    "SQLRB_LLM_MODEL": "gpt-5.4",
                    "SQLRB_LLM_API_KEY": "secret-live-test-key",
                    "SQLRB_LLM_ALLOW_LIVE": "1",
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)
            status_text = json.dumps(status)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse(status["candidate_generated"])
        self.assertFalse(status["live_call"])
        self.assertEqual(status["fail_closed_reason"], "live_not_implemented")
        self.assertNotIn("secret-live-test-key", status_text)

    def test_rule_system_required_but_unavailable_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LLM_R2_MODE": "fake",
                    "SQLRB_LLM_R2_REQUIRE_RULE_SYSTEM": "1",
                    "SQLRB_LLM_R2_FAKE_SQL": "SELECT a FROM table1",
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(status["fail_closed_reason"], "rule_system_runtime_unavailable")
        self.assertFalse(status["rule_system_runtime_used"])
        self.assertFalse(status["checkpoint_used"])
        self.assertFalse(status["demonstration_selector_used"])

    def test_checkpoint_and_demo_selector_required_fail_closed(self) -> None:
        fixtures = [
            ("SQLRB_LLM_R2_REQUIRE_CHECKPOINT", "checkpoint_unavailable"),
            ("SQLRB_LLM_R2_REQUIRE_DEMO_SELECTOR", "demonstration_selector_unavailable"),
        ]
        for env_flag, expected in fixtures:
            with self.subTest(expected=expected):
                with tempfile.TemporaryDirectory() as temp_name:
                    temp_dir = Path(temp_name)
                    env = _adapter_env(temp_dir)
                    env.update(
                        {
                            "SQLRB_LLM_R2_MODE": "fake",
                            env_flag: "1",
                            "SQLRB_LLM_R2_FAKE_SQL": "SELECT a FROM table1",
                        }
                    )
                    completed = _run_adapter(env)
                    status = _status(temp_dir)

                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(status["fail_closed_reason"], expected)

    def test_extraction_helper_rejects_multiple_blocks(self) -> None:
        module = _load_adapter_module()
        result = module.extract_sql_candidate(
            "```sql\nSELECT a FROM table1;\n```\n```sql\nSELECT b FROM table1;\n```"
        )
        self.assertEqual(result.failure_bucket, "multiple_sql_statements")


if __name__ == "__main__":
    unittest.main()
