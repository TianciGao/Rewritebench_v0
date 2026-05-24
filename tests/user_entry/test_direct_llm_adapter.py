import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTER = REPO_ROOT / "baselines" / "direct_llm_original" / "adapter.py"


def _load_adapter_module():
    spec = importlib.util.spec_from_file_location("direct_llm_adapter", ADAPTER)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load Direct LLM adapter module")
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
    source_path.write_text("SELECT a FROM table1 WHERE a > 0;\n", encoding="utf-8")
    schema_dir = temp_dir / "schema"
    schema_dir.mkdir()
    (schema_dir / "ddl_pg.sql").write_text(
        "CREATE TABLE table1 (a INTEGER, b INTEGER);\n",
        encoding="utf-8",
    )
    workspace = temp_dir / "workspace"
    return {
        **_pythonpath_env(),
        "SQLRB_RUN_ID": "test_run",
        "SQLRB_CASE_ID": "CONS_0036",
        "SQLRB_POOL": "CONS",
        "SQLRB_ENGINE": engine,
        "SQLRB_SOURCE_SQL_PATH": str(source_path),
        "SQLRB_CASE_DIR": str(temp_dir),
        "SQLRB_WORKSPACE_DIR": str(workspace),
        "SQLRB_CANDIDATE_SQL_PATH": str(workspace / "candidate.sql"),
    }


class DirectLlmAdapterTests(unittest.TestCase):
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

    def test_missing_api_key_fails_closed_without_secret_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env = _adapter_env(Path(temp_dir))
            env.update(
                {
                    "SQLRB_LLM_PROVIDER": "openai_compatible",
                    "SQLRB_LLM_BASE_URL": "https://api.gptsapi.net/v1",
                    "SQLRB_LLM_MODEL": "gpt-5.4",
                }
            )
            env.pop("SQLRB_LLM_API_KEY", None)
            env.pop("GPTSAPI_API_KEY", None)
            completed = subprocess.run(
                [sys.executable, str(ADAPTER)],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            workspace = Path(temp_dir) / "workspace"
            status = json.loads((workspace / "direct_llm_status.json").read_text(encoding="utf-8"))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse((workspace / "candidate.sql").exists())
        self.assertEqual(status["failure_bucket"], "missing_api_key")
        self.assertFalse(status["api_key_present"])
        self.assertNotIn("secret", json.dumps(status).lower())

    def test_provider_env_discovery_uses_gptsapi_aliases(self) -> None:
        module = _load_adapter_module()
        with patch.dict(
            os.environ,
            {
                "GPTSAPI_API_KEY": "secret-test-key",
                "GPTSAPI_BASE_URL": "https://api.gptsapi.net/v1",
                "GPTSAPI_MODEL": "gpt-5.4",
                "SQLRB_LLM_TEMPERATURE": "0",
                "SQLRB_LLM_TOP_P": "1",
            },
            clear=True,
        ):
            config = module.resolve_provider_config()

        self.assertEqual(config.provider, "openai_compatible")
        self.assertEqual(config.base_url_host, "api.gptsapi.net")
        self.assertEqual(config.model_id, "gpt-5.4")
        self.assertEqual(config.api_key_env_used, "GPTSAPI_API_KEY")
        self.assertEqual(config.temperature, 0.0)
        self.assertEqual(config.top_p, 1.0)

    def test_prompt_rendering_includes_sql_schema_and_target_dialect(self) -> None:
        module = _load_adapter_module()
        with patch.dict(os.environ, {"SQLRB_LLM_PROVIDER": "fake"}, clear=True):
            config = module.resolve_provider_config()
        env = {
            "SQLRB_CASE_ID": "PERF_0006",
            "SQLRB_POOL": "PERF",
            "SQLRB_ENGINE": "postgres",
            "SQLRB_SOURCE_SQL_PATH": "source.sql",
        }
        prompt = module.build_prompt(
            env=env,
            source_sql="SELECT a FROM table1;",
            schema_ddl="CREATE TABLE table1 (a INT);",
            config=config,
        )
        blob = json.dumps(prompt)
        self.assertIn("SELECT a FROM table1", blob)
        self.assertIn("CREATE TABLE table1", blob)
        self.assertIn("target dialect: postgres", blob)
        self.assertEqual(prompt["prompt_template_id"], "direct_llm_original_sql_only_v0")

    def test_one_sql_block_extraction_succeeds(self) -> None:
        module = _load_adapter_module()
        result = module.extract_sql_candidate("```sql\nSELECT a FROM table1\n```")
        self.assertEqual(result.status, "extracted")
        self.assertEqual(result.sql, "SELECT a FROM table1;\n")

    def test_multiple_sql_blocks_fail_closed(self) -> None:
        module = _load_adapter_module()
        result = module.extract_sql_candidate(
            "```sql\nSELECT a FROM table1;\n```\n```sql\nSELECT b FROM table1;\n```"
        )
        self.assertEqual(result.status, "multiple_sql_blocks_ambiguous")
        self.assertEqual(result.failure_bucket, "multiple_sql_blocks_ambiguous")

    def test_fake_provider_response_writes_candidate_sql(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env = _adapter_env(Path(temp_dir))
            env.update(
                {
                    "SQLRB_LLM_PROVIDER": "fake",
                    "SQLRB_LLM_FAKE_RESPONSE": "```sql\nSELECT a FROM table1 WHERE a > 0;\n```",
                    "SQLRB_LLM_API_KEY": "secret-should-not-be-written",
                }
            )
            completed = subprocess.run(
                [sys.executable, str(ADAPTER)],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            workspace = Path(temp_dir) / "workspace"
            status_text = (workspace / "direct_llm_status.json").read_text(encoding="utf-8")
            status = json.loads(status_text)
            candidate = (workspace / "candidate.sql").read_text(encoding="utf-8")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(candidate, "SELECT a FROM table1 WHERE a > 0;\n")
        self.assertTrue(status["candidate_generated"])
        self.assertEqual(status["failure_bucket"], "none")
        self.assertEqual(status["provider"], "fake")
        self.assertNotIn("secret-should-not-be-written", status_text)

    def test_direct_llm_original_does_not_repair_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env = _adapter_env(Path(temp_dir))
            env.update(
                {
                    "SQLRB_LLM_PROVIDER": "fake",
                    "SQLRB_LLM_FAKE_RESPONSE": "SELECT a FROM table1 WHERE a > 0",
                }
            )
            completed = subprocess.run(
                [sys.executable, str(ADAPTER)],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            workspace = Path(temp_dir) / "workspace"
            status = json.loads((workspace / "direct_llm_status.json").read_text(encoding="utf-8"))
            candidate = (workspace / "candidate.sql").read_text(encoding="utf-8")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(status["route_id"], "direct_llm_original")
        self.assertFalse(status["repair_attempted"])
        self.assertEqual(candidate, "SELECT a FROM table1 WHERE a > 0;\n")


if __name__ == "__main__":
    unittest.main()
