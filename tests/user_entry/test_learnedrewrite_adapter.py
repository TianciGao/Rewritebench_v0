import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTER = REPO_ROOT / "baselines" / "learnedrewrite" / "adapter.py"


def _load_adapter_module():
    spec = importlib.util.spec_from_file_location("learnedrewrite_adapter", ADAPTER)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load LearnedRewrite adapter module")
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
        "SQLRB_RUN_ID": "learnedrewrite_fixture_run",
        "SQLRB_CASE_ID": "PERF_0006",
        "SQLRB_POOL": "PERF",
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
    return json.loads((temp_dir / "workspace" / "learnedrewrite_status.json").read_text(encoding="utf-8"))


class _LearnedRewriteHTTPHandler(BaseHTTPRequestHandler):
    request_count = 0
    response_payload: dict[str, object] = {
        "status": True,
        "message": "SUCCESS",
        "data": {"rewritten_sql": "SELECT a FROM table1 WHERE a > 4"},
    }
    last_payload: dict[str, object] | None = None

    def log_message(self, format: str, *args: object) -> None:
        return

    def do_POST(self) -> None:
        type(self).request_count += 1
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        type(self).last_payload = json.loads(raw)
        body = json.dumps(type(self).response_payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class _HTTPServerContext:
    def __enter__(self) -> str:
        _LearnedRewriteHTTPHandler.request_count = 0
        _LearnedRewriteHTTPHandler.last_payload = None
        _LearnedRewriteHTTPHandler.response_payload = {
            "status": True,
            "message": "SUCCESS",
            "data": {"rewritten_sql": "SELECT a FROM table1 WHERE a > 4"},
        }
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _LearnedRewriteHTTPHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        host, port = self.server.server_address
        return f"http://{host}:{port}/rewriter"

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)


class LearnedRewriteAdapterTests(unittest.TestCase):
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
                    "SQLRB_LEARNEDREWRITE_MODE": "fake",
                    "SQLRB_LEARNEDREWRITE_FAKE_RESPONSE": json.dumps(
                        {"status": "ok", "rewritten_sql": "SELECT a FROM table1 WHERE a > 1"}
                    ),
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)
            candidate = (temp_dir / "workspace" / "candidate.sql").read_text(encoding="utf-8")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(candidate, "SELECT a FROM table1 WHERE a > 1;\n")
        self.assertTrue(status["candidate_generated"])
        self.assertEqual(status["failure_bucket"], "none")
        self.assertEqual(status["route_id"], "learnedrewrite")
        self.assertEqual(status["method_id"], "learnedrewrite")
        self.assertEqual(status["runtime_mode"], "fake")
        self.assertTrue(status["fake_runtime"])
        self.assertEqual(status["extraction_policy"], "single_sql_candidate_learnedrewrite_v0")
        self.assertTrue(status["local_diagnostic_only"])
        self.assertFalse(status["official_metric_input"])

    def test_fake_runtime_inline_sql_returns_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LEARNEDREWRITE_MODE": "fake",
                    "SQLRB_LEARNEDREWRITE_FAKE_SQL": "```sql\nSELECT a FROM table1 WHERE a > 2\n```",
                }
            )
            completed = _run_adapter(env)
            candidate = (temp_dir / "workspace" / "candidate.sql").read_text(encoding="utf-8")
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(candidate, "SELECT a FROM table1 WHERE a > 2;\n")
        self.assertTrue(status["candidate_generated"])

    def test_fake_runtime_multiple_statements_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LEARNEDREWRITE_MODE": "fake",
                    "SQLRB_LEARNEDREWRITE_FAKE_RESPONSE": json.dumps(
                        {"status": "ok", "rewritten_sql": "SELECT a FROM table1; SELECT b FROM table1;"}
                    ),
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse((temp_dir / "workspace" / "candidate.sql").exists())
        self.assertEqual(status["extraction_status"], "sql_extraction_failed")
        self.assertEqual(status["failure_bucket"], "multiple_sql_statements")

    def test_fake_runtime_prose_and_empty_fail_closed(self) -> None:
        fixtures = [
            ("Here is the rewrite: SELECT a FROM table1;", "response_not_sql"),
            ("   ", "response_empty"),
        ]
        for raw_response, expected_bucket in fixtures:
            with self.subTest(expected_bucket=expected_bucket):
                with tempfile.TemporaryDirectory() as temp_name:
                    temp_dir = Path(temp_name)
                    env = _adapter_env(temp_dir)
                    env.update(
                        {
                            "SQLRB_LEARNEDREWRITE_MODE": "fake",
                            "SQLRB_LEARNEDREWRITE_FAKE_RESPONSE": raw_response,
                        }
                    )
                    completed = _run_adapter(env)
                    status = _status(temp_dir)

                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(status["failure_bucket"], expected_bucket)
                self.assertFalse(status["candidate_generated"])

    def test_missing_runtime_config_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(status["runtime_status"], "runtime_unconfigured")
        self.assertEqual(status["failure_bucket"], "runtime_unconfigured")
        self.assertFalse(status["candidate_generated"])

    def test_malformed_json_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LEARNEDREWRITE_MODE": "fake",
                    "SQLRB_LEARNEDREWRITE_FAKE_RESPONSE": '{"status":"ok","rewritten_sql":',
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(status["runtime_status"], "runtime_invalid_json")
        self.assertEqual(status["failure_bucket"], "runtime_invalid_json")
        self.assertFalse(status["candidate_generated"])

    def test_unsupported_status_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LEARNEDREWRITE_MODE": "fake",
                    "SQLRB_LEARNEDREWRITE_FAKE_RESPONSE": json.dumps(
                        {"status": "unsupported", "reason": "window function unsupported"}
                    ),
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(status["runtime_status"], "runtime_unsupported")
        self.assertEqual(status["failure_bucket"], "unsupported")
        self.assertFalse((temp_dir / "workspace" / "candidate.sql").exists())

    def test_command_and_http_modes_fail_closed_without_invocation(self) -> None:
        fixtures = [
            ({"SQLRB_LEARNEDREWRITE_MODE": "command"}, "command_runtime_missing_env"),
            (
                {"SQLRB_LEARNEDREWRITE_MODE": "command", "SQLRB_LEARNEDREWRITE_CMD": "java -jar should-not-run.jar"},
                "external_runtime_not_implemented",
            ),
            ({"SQLRB_LEARNEDREWRITE_MODE": "http"}, "http_runtime_missing_env"),
            (
                {"SQLRB_LEARNEDREWRITE_MODE": "http", "SQLRB_LEARNEDREWRITE_URL": "http://127.0.0.1:6336/rewriter"},
                "runtime_not_allowed",
            ),
        ]
        for extra_env, expected_bucket in fixtures:
            with self.subTest(expected_bucket=expected_bucket):
                with tempfile.TemporaryDirectory() as temp_name:
                    temp_dir = Path(temp_name)
                    env = _adapter_env(temp_dir)
                    env.update(extra_env)
                    completed = _run_adapter(env)
                    status = _status(temp_dir)

                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(status["failure_bucket"], expected_bucket)
                self.assertFalse(status["java_runtime_invoked"])
                self.assertFalse(status["network_invoked"])
                self.assertFalse(status["candidate_generated"])

    def test_http_runtime_success_extracts_data_rewritten_sql(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name, _HTTPServerContext() as url:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LEARNEDREWRITE_MODE": "http",
                    "SQLRB_LEARNEDREWRITE_URL": url,
                    "SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME": "1",
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)
            candidate = (temp_dir / "workspace" / "candidate.sql").read_text(encoding="utf-8")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(_LearnedRewriteHTTPHandler.request_count, 1)
        self.assertEqual(candidate, "SELECT a FROM table1 WHERE a > 4;\n")
        self.assertTrue(status["candidate_generated"])
        self.assertEqual(status["runtime_mode"], "http")
        self.assertTrue(status["network_invoked"])
        self.assertTrue(status["http_runtime_invoked"])
        self.assertFalse(status["java_runtime_invoked"])
        self.assertEqual(status["runtime_status"], "http_runtime_success")
        self.assertEqual(status["schema_payload_status"], "ddl_derived_schema_json")
        self.assertEqual(status["schema_table_count"], 1)
        payload = _LearnedRewriteHTTPHandler.last_payload
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload["sql"], "SELECT a FROM table1 WHERE a > 0")
        self.assertIsInstance(payload["schema"], str)
        self.assertIn('"table":"table1"', payload["schema"])

    def test_http_runtime_status_false_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name, _HTTPServerContext() as url:
            _LearnedRewriteHTTPHandler.response_payload = {
                "status": False,
                "message": "Get Error",
            }
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LEARNEDREWRITE_MODE": "http",
                    "SQLRB_LEARNEDREWRITE_URL": url,
                    "SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME": "1",
                }
            )
            completed = _run_adapter(env)
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(_LearnedRewriteHTTPHandler.request_count, 1)
        self.assertEqual(status["failure_bucket"], "runtime_status_false")
        self.assertFalse(status["candidate_generated"])
        self.assertTrue(status["network_invoked"])

    def test_metadata_secret_hygiene_and_no_runtime_flags(self) -> None:
        secret_value = "fixture-secret-value-123"
        with tempfile.TemporaryDirectory() as temp_name:
            temp_dir = Path(temp_name)
            env = _adapter_env(temp_dir)
            env.update(
                {
                    "SQLRB_LEARNEDREWRITE_MODE": "fake",
                    "SQLRB_LEARNEDREWRITE_FAKE_RESPONSE": json.dumps(
                        {"status": "ok", "rewritten_sql": "SELECT a FROM table1 WHERE a > 3"}
                    ),
                    "SQLRB_LLM_API_KEY": secret_value,
                    "GPTSAPI_API_KEY": secret_value,
                    "OPENAI_API_KEY": secret_value,
                }
            )
            completed = _run_adapter(env)
            workspace = temp_dir / "workspace"
            written_text = "\n".join(path.read_text(encoding="utf-8") for path in workspace.rglob("*") if path.is_file())
            status = _status(temp_dir)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn(secret_value, written_text)
        self.assertTrue(status["no_upstream_source_or_jar_vendored"])
        self.assertFalse(status["java_runtime_invoked"])
        self.assertFalse(status["network_invoked"])
        self.assertFalse(status["db_execution_invoked"])
        self.assertFalse(status["checker_invoked"])
        self.assertFalse(status["timing_invoked"])
        self.assertFalse(status["local_metrics_invoked"])
        self.assertFalse(status["verifier_invoked"])
        self.assertFalse(status["paper_result"])
        self.assertFalse(status["retained_evidence_promoted"])
        self.assertFalse(status["leaderboard_input"])

    def test_mysql_and_spark_fail_closed_as_unsupported(self) -> None:
        for engine in ["mysql", "spark"]:
            with self.subTest(engine=engine):
                with tempfile.TemporaryDirectory() as temp_name:
                    temp_dir = Path(temp_name)
                    env = _adapter_env(temp_dir, engine=engine)
                    env.update(
                        {
                            "SQLRB_LEARNEDREWRITE_MODE": "fake",
                            "SQLRB_LEARNEDREWRITE_FAKE_RESPONSE": json.dumps(
                                {"status": "ok", "rewritten_sql": "SELECT a FROM table1"}
                            ),
                        }
                    )
                    completed = _run_adapter(env)
                    status = _status(temp_dir)

                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(status["failure_bucket"], "unsupported_engine")
                self.assertFalse(status["candidate_generated"])

    def test_extract_sql_candidate_rejects_prose(self) -> None:
        module = _load_adapter_module()
        result = module.extract_sql_candidate("The rewritten SQL is SELECT 1;")
        self.assertEqual(result.status, "sql_extraction_failed")
        self.assertEqual(result.failure_bucket, "response_not_sql")


if __name__ == "__main__":
    unittest.main()
