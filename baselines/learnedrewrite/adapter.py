#!/usr/bin/env python3
"""Fixture-only LearnedRewrite external-wrapper adapter scaffold.

The adapter follows the public ``sql_rewrite_bench.user_run`` row environment
contract. In this scaffold task it supports fake runtime mode only. Command and
HTTP modes are deliberately fail-closed placeholders so this adapter cannot
accidentally run Java, open network connections, execute SQL, or call external
tools during fixture tests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROUTE_ID = "learnedrewrite"
METHOD_ID = "learnedrewrite"
BASELINE_FAMILY = "prior_method_external_wrapper"
ADAPTER_VERSION = "learnedrewrite_adapter_scaffold_v0"
WRAPPER_CONTRACT_ID = "learnedrewrite_external_wrapper_contract_v0"
EXTRACTION_POLICY_ID = "single_sql_candidate_learnedrewrite_v0"
SCHEMA_SERIALIZATION_POLICY = "schema_context_reference_only_v0"

REQUIRED_ENV_VARS = [
    "SQLRB_RUN_ID",
    "SQLRB_CASE_ID",
    "SQLRB_POOL",
    "SQLRB_ENGINE",
    "SQLRB_SOURCE_SQL_PATH",
    "SQLRB_CASE_DIR",
    "SQLRB_WORKSPACE_DIR",
    "SQLRB_CANDIDATE_SQL_PATH",
]

SUPPORTED_ENGINES = {"postgres"}
KNOWN_ENGINES = {"postgres", "mysql", "spark"}
RUNTIME_MODES = {"fake", "command", "cmd", "http"}

DDL_CANDIDATE_NAMES = {
    "postgres": ["ddl_pg.sql", "ddl_postgres.sql"],
    "mysql": ["ddl_mysql.sql"],
    "spark": ["ddl_spark.sql"],
}

SQL_START_PATTERN = re.compile(r"^\s*(SELECT|WITH)\b", re.IGNORECASE | re.DOTALL)
FENCED_BLOCK_PATTERN = re.compile(
    r"```(?P<lang>[A-Za-z0-9_-]*)\s*\n?(?P<body>.*?)```",
    re.DOTALL,
)


class AdapterError(Exception):
    """Unexpected adapter setup error."""


@dataclass(frozen=True)
class RuntimeConfig:
    mode: str
    command_configured: bool
    http_url_configured: bool
    fake_response_configured: bool
    fake_sql_configured: bool
    timeout_seconds: float
    allow_runtime: bool
    external_runtime_configured: bool


@dataclass(frozen=True)
class RuntimeResult:
    status: str
    raw_output: str
    failure_bucket: str
    reason: str
    runtime_attempted: bool


@dataclass(frozen=True)
class ExtractionResult:
    status: str
    sql: str
    failure_bucket: str
    reason: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one LearnedRewrite candidate SQL in fixture-only fake mode."
    )
    parser.add_argument(
        "--dry-run-status",
        action="store_true",
        help="Write status metadata only; do not parse fake runtime output or write candidate SQL.",
    )
    return parser.parse_args(argv)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _resolve_repo_path(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path.resolve()
    return (_repo_root() / path).resolve()


def _yaml_scalar(path: Path, key: str) -> str:
    if not path.exists():
        return ""
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*:\s*(.+?)\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.split("#", 1)[0].rstrip())
        if match:
            return match.group(1).strip().strip("'\"")
    return ""


def _yaml_engine_asset(path: Path, engine: str) -> str:
    if not path.exists():
        return ""
    pattern = re.compile(rf"^\s*{re.escape(engine)}\s*:\s*(.+?\.sql)\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.split("#", 1)[0].rstrip())
        if match:
            return match.group(1).strip().strip("'\"")
    return ""


def _schema_profile_candidates(profile_path: Path, engine: str) -> list[Path]:
    candidates: list[Path] = []
    raw_engine_asset = _yaml_engine_asset(profile_path, engine)
    if raw_engine_asset:
        candidates.append(_resolve_repo_path(raw_engine_asset))
    if profile_path.exists():
        candidates.append((profile_path.parent / engine / "ddl.sql").resolve())
    return candidates


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_env() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV_VARS if not os.environ.get(name)]
    if missing:
        raise AdapterError("missing required environment variables: " + ", ".join(missing))
    return {name: os.environ[name] for name in REQUIRED_ENV_VARS}


def resolve_runtime_config() -> RuntimeConfig:
    mode = os.environ.get("SQLRB_LEARNEDREWRITE_MODE", "").strip().lower()
    command_configured = bool(os.environ.get("SQLRB_LEARNEDREWRITE_CMD", "").strip())
    http_url_configured = bool(os.environ.get("SQLRB_LEARNEDREWRITE_URL", "").strip())
    fake_response_configured = "SQLRB_LEARNEDREWRITE_FAKE_RESPONSE" in os.environ
    fake_sql_configured = "SQLRB_LEARNEDREWRITE_FAKE_SQL" in os.environ
    raw_timeout = os.environ.get("SQLRB_LEARNEDREWRITE_TIMEOUT", "30").strip()
    try:
        timeout_seconds = float(raw_timeout)
    except ValueError as exc:
        raise AdapterError("SQLRB_LEARNEDREWRITE_TIMEOUT must be numeric") from exc
    if timeout_seconds <= 0:
        raise AdapterError("SQLRB_LEARNEDREWRITE_TIMEOUT must be positive")
    return RuntimeConfig(
        mode=mode,
        command_configured=command_configured,
        http_url_configured=http_url_configured,
        fake_response_configured=fake_response_configured,
        fake_sql_configured=fake_sql_configured,
        timeout_seconds=timeout_seconds,
        allow_runtime=os.environ.get("SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME", "") == "1",
        external_runtime_configured=command_configured or http_url_configured,
    )


def resolve_schema_context(env: dict[str, str]) -> tuple[str, str, str]:
    """Return schema status, schema ref, and a safe schema artifact path/status."""

    explicit_schema = os.environ.get("SQLRB_LEARNEDREWRITE_SCHEMA_JSON", "").strip()
    if explicit_schema:
        return "inline_schema_json_present", _sha256_text(explicit_schema), "inline"

    explicit_ref = os.environ.get("SQLRB_SCHEMA_REF", "").strip()
    case_dir = Path(env["SQLRB_CASE_DIR"]).resolve()
    engine = env["SQLRB_ENGINE"]
    candidates: list[Path] = []
    for name in DDL_CANDIDATE_NAMES.get(engine, [f"ddl_{engine}.sql"]):
        candidates.append(case_dir / "schema" / name)
    candidates.append(case_dir / "schema" / engine / "ddl.sql")

    case_schema_profile = case_dir / "schema" / "schema_profile.yaml"
    candidates.extend(_schema_profile_candidates(case_schema_profile, engine))
    for key in ["external_schema_profile", "external_profile", "profile"]:
        raw_profile = _yaml_scalar(case_schema_profile, key)
        if raw_profile.startswith("schemas/"):
            candidates.extend(_schema_profile_candidates(_resolve_repo_path(raw_profile), engine))
            explicit_ref = explicit_ref or raw_profile

    manifest_path = case_dir / "manifest.yaml"
    for key in ["schema_ref", "external_profile", "profile"]:
        raw_profile = _yaml_scalar(manifest_path, key)
        if raw_profile:
            explicit_ref = explicit_ref or raw_profile
        if raw_profile.startswith("schemas/"):
            candidates.extend(_schema_profile_candidates(_resolve_repo_path(raw_profile), engine))

    for candidate in candidates:
        if candidate.is_file():
            return "schema_context_available", explicit_ref or str(candidate), str(candidate)
    return "schema_context_unavailable", explicit_ref, ""


def _strip_one_trailing_semicolon(sql: str) -> str:
    stripped = sql.strip()
    if stripped.endswith(";"):
        return stripped[:-1].rstrip()
    return stripped


def _statement_semicolon_count(sql: str) -> int:
    in_single = False
    in_double = False
    in_line_comment = False
    in_block_comment = False
    count = 0
    index = 0
    while index < len(sql):
        char = sql[index]
        nxt = sql[index + 1] if index + 1 < len(sql) else ""
        if in_line_comment:
            if char == "\n":
                in_line_comment = False
            index += 1
            continue
        if in_block_comment:
            if char == "*" and nxt == "/":
                in_block_comment = False
                index += 2
                continue
            index += 1
            continue
        if in_single:
            if char == "'" and nxt == "'":
                index += 2
                continue
            if char == "'":
                in_single = False
            index += 1
            continue
        if in_double:
            if char == '"' and nxt == '"':
                index += 2
                continue
            if char == '"':
                in_double = False
            index += 1
            continue
        if char == "-" and nxt == "-":
            in_line_comment = True
            index += 2
            continue
        if char == "/" and nxt == "*":
            in_block_comment = True
            index += 2
            continue
        if char == "'":
            in_single = True
        elif char == '"':
            in_double = True
        elif char == ";":
            count += 1
        index += 1
    return count


def _looks_like_single_sql_statement(text: str) -> tuple[bool, str]:
    stripped = text.strip()
    if not stripped:
        return False, "response_empty"
    if not SQL_START_PATTERN.match(stripped):
        return False, "response_not_sql"
    semicolons = _statement_semicolon_count(stripped)
    if semicolons > 1:
        return False, "multiple_sql_statements"
    if semicolons == 1 and not stripped.endswith(";"):
        return False, "multiple_sql_statements"
    return True, ""


def extract_sql_candidate(raw_response: str) -> ExtractionResult:
    if not raw_response.strip():
        return ExtractionResult(
            status="response_empty",
            sql="",
            failure_bucket="response_empty",
            reason="runtime response was empty",
        )

    blocks = []
    for match in FENCED_BLOCK_PATTERN.finditer(raw_response):
        lang = match.group("lang").strip().lower()
        body = match.group("body").strip()
        ok, _reason = _looks_like_single_sql_statement(body)
        if ok and lang in {"", "sql"}:
            blocks.append(body)

    if len(blocks) > 1:
        return ExtractionResult(
            status="multiple_sql_blocks",
            sql="",
            failure_bucket="multiple_sql_statements",
            reason="multiple SQL code blocks were present",
        )
    if len(blocks) == 1:
        return ExtractionResult(
            status="extracted",
            sql=_strip_one_trailing_semicolon(blocks[0]) + ";\n",
            failure_bucket="none",
            reason="extracted one fenced SQL block",
        )

    ok, reason = _looks_like_single_sql_statement(raw_response)
    if not ok:
        return ExtractionResult(
            status="sql_extraction_failed",
            sql="",
            failure_bucket=reason,
            reason=reason,
        )
    return ExtractionResult(
        status="extracted",
        sql=_strip_one_trailing_semicolon(raw_response) + ";\n",
        failure_bucket="none",
        reason="full response looked like one SQL statement",
    )


def _fake_runtime_response() -> RuntimeResult:
    if "SQLRB_LEARNEDREWRITE_FAKE_SQL" in os.environ:
        raw_sql = os.environ.get("SQLRB_LEARNEDREWRITE_FAKE_SQL", "")
        return RuntimeResult(
            status="fake_runtime_success",
            raw_output=raw_sql,
            failure_bucket="none",
            reason="fake SQL response supplied",
            runtime_attempted=True,
        )

    raw = os.environ.get("SQLRB_LEARNEDREWRITE_FAKE_RESPONSE", "")
    if not raw.strip():
        return RuntimeResult(
            status="fake_response_empty",
            raw_output="",
            failure_bucket="response_empty",
            reason="SQLRB_LEARNEDREWRITE_FAKE_RESPONSE was empty",
            runtime_attempted=True,
        )

    stripped = raw.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            return RuntimeResult(
                status="runtime_invalid_json",
                raw_output="",
                failure_bucket="runtime_invalid_json",
                reason=f"fake response JSON could not be parsed: {exc.msg}",
                runtime_attempted=True,
            )
        if not isinstance(payload, dict):
            return RuntimeResult(
                status="runtime_invalid_json",
                raw_output="",
                failure_bucket="runtime_invalid_json",
                reason="fake response JSON must be an object",
                runtime_attempted=True,
            )
        status = str(payload.get("status", "ok")).strip().lower()
        if status in {"unsupported", "no_verifier_support"}:
            return RuntimeResult(
                status="runtime_unsupported",
                raw_output="",
                failure_bucket="unsupported",
                reason=str(payload.get("reason") or "fake runtime status was unsupported"),
                runtime_attempted=True,
            )
        if status in {"timeout", "timed_out"}:
            return RuntimeResult(
                status="runtime_timeout",
                raw_output="",
                failure_bucket="runtime_timeout",
                reason=str(payload.get("reason") or "fake runtime status was timeout"),
                runtime_attempted=True,
            )
        if status in {"error", "failed", "runtime_failed"}:
            return RuntimeResult(
                status="runtime_failed",
                raw_output="",
                failure_bucket="runtime_failed",
                reason=str(payload.get("reason") or "fake runtime status was failed"),
                runtime_attempted=True,
            )
        rewritten = payload.get("rewritten_sql", payload.get("candidate_sql", payload.get("sql", "")))
        if not isinstance(rewritten, str):
            return RuntimeResult(
                status="no_rewritten_sql",
                raw_output="",
                failure_bucket="no_rewritten_sql",
                reason="rewritten_sql was missing or not a string",
                runtime_attempted=True,
            )
        if not rewritten.strip():
            return RuntimeResult(
                status="empty_candidate_sql",
                raw_output="",
                failure_bucket="empty_candidate_sql",
                reason="rewritten_sql was empty",
                runtime_attempted=True,
            )
        return RuntimeResult(
            status="fake_runtime_success",
            raw_output=rewritten,
            failure_bucket="none",
            reason="fake JSON response supplied rewritten_sql",
            runtime_attempted=True,
        )

    return RuntimeResult(
        status="fake_runtime_success",
        raw_output=raw,
        failure_bucket="none",
        reason="inline fake response supplied",
        runtime_attempted=True,
    )


def _runtime_fail_closed(config: RuntimeConfig) -> RuntimeResult:
    if not config.mode:
        return RuntimeResult(
            status="runtime_unconfigured",
            raw_output="",
            failure_bucket="runtime_unconfigured",
            reason="set SQLRB_LEARNEDREWRITE_MODE=fake for fixture mode",
            runtime_attempted=False,
        )
    if config.mode not in RUNTIME_MODES:
        return RuntimeResult(
            status="unsupported_runtime_mode",
            raw_output="",
            failure_bucket="unsupported_runtime_mode",
            reason=f"unsupported SQLRB_LEARNEDREWRITE_MODE: {config.mode}",
            runtime_attempted=False,
        )
    if config.mode in {"command", "cmd"}:
        if not config.command_configured:
            return RuntimeResult(
                status="command_runtime_missing_env",
                raw_output="",
                failure_bucket="command_runtime_missing_env",
                reason="SQLRB_LEARNEDREWRITE_CMD is required for command mode",
                runtime_attempted=False,
            )
        return RuntimeResult(
            status="external_runtime_not_implemented",
            raw_output="",
            failure_bucket="external_runtime_not_implemented",
            reason="command mode is a future hook; this scaffold runs fake mode only",
            runtime_attempted=False,
        )
    if config.mode == "http":
        if not config.http_url_configured:
            return RuntimeResult(
                status="http_runtime_missing_env",
                raw_output="",
                failure_bucket="http_runtime_missing_env",
                reason="SQLRB_LEARNEDREWRITE_URL is required for HTTP mode",
                runtime_attempted=False,
            )
        return RuntimeResult(
            status="external_runtime_not_implemented",
            raw_output="",
            failure_bucket="external_runtime_not_implemented",
            reason="HTTP mode is a future hook; this scaffold runs fake mode only",
            runtime_attempted=False,
        )
    if not config.fake_response_configured and not config.fake_sql_configured:
        return RuntimeResult(
            status="fake_runtime_missing_response",
            raw_output="",
            failure_bucket="fake_runtime_missing_response",
            reason="fake mode requires SQLRB_LEARNEDREWRITE_FAKE_RESPONSE or SQLRB_LEARNEDREWRITE_FAKE_SQL",
            runtime_attempted=False,
        )
    return _fake_runtime_response()


def _base_status(
    *,
    env: dict[str, str],
    config: RuntimeConfig,
    source_sql_sha256: str,
    schema_status: str,
    schema_ref: str,
    schema_artifact: str,
) -> dict[str, Any]:
    return {
        "schema_version": "learnedrewrite_adapter_status_v0",
        "created_at_utc": _utc_now_iso(),
        "route_id": ROUTE_ID,
        "method_id": METHOD_ID,
        "baseline_family": BASELINE_FAMILY,
        "adapter_version": ADAPTER_VERSION,
        "wrapper_contract_id": WRAPPER_CONTRACT_ID,
        "run_id": env["SQLRB_RUN_ID"],
        "case_id": env["SQLRB_CASE_ID"],
        "pool": env["SQLRB_POOL"],
        "target_engine": env["SQLRB_ENGINE"],
        "source_sql_path": env["SQLRB_SOURCE_SQL_PATH"],
        "source_sql_sha256": source_sql_sha256,
        "case_dir": env["SQLRB_CASE_DIR"],
        "candidate_sql_path": env["SQLRB_CANDIDATE_SQL_PATH"],
        "schema_context_status": schema_status,
        "schema_ref": schema_ref,
        "schema_artifact": schema_artifact,
        "schema_serialization_policy": SCHEMA_SERIALIZATION_POLICY,
        "runtime_mode": config.mode or "unconfigured",
        "runtime_timeout_seconds": config.timeout_seconds,
        "external_runtime_configured": config.external_runtime_configured,
        "external_command_configured": config.command_configured,
        "external_http_url_configured": config.http_url_configured,
        "fake_runtime": config.mode == "fake",
        "fake_runtime_response_configured": config.fake_response_configured or config.fake_sql_configured,
        "java_runtime_invoked": False,
        "network_invoked": False,
        "db_execution_invoked": False,
        "checker_invoked": False,
        "timing_invoked": False,
        "local_metrics_invoked": False,
        "verifier_invoked": False,
        "extraction_policy": EXTRACTION_POLICY_ID,
        "runtime_status": "not_attempted",
        "runtime_attempted": False,
        "extraction_status": "not_attempted",
        "candidate_generated": False,
        "candidate_sql_sha256": "",
        "source_like_status": "not_evaluated",
        "failure_bucket": "no_candidate_sql",
        "fail_closed_reason": "",
        "no_upstream_source_or_jar_vendored": True,
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result": False,
        "paper_result_input": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _fail_closed(
    status: dict[str, Any],
    *,
    bucket: str,
    reason: str,
    runtime_status: str,
    runtime_attempted: bool = False,
) -> int:
    status["failure_bucket"] = bucket
    status["fail_closed_reason"] = reason
    status["runtime_status"] = runtime_status
    status["runtime_attempted"] = runtime_attempted
    status["candidate_generated"] = False
    return 0


def run(*, dry_run_status: bool = False) -> int:
    env = load_env()
    workspace = Path(env["SQLRB_WORKSPACE_DIR"])
    workspace.mkdir(parents=True, exist_ok=True)

    source_path = Path(env["SQLRB_SOURCE_SQL_PATH"])
    if not source_path.is_file():
        raise AdapterError(f"source SQL path does not exist: {source_path}")
    source_sql = source_path.read_text(encoding="utf-8")
    config = resolve_runtime_config()
    schema_status, schema_ref, schema_artifact = resolve_schema_context(env)
    status = _base_status(
        env=env,
        config=config,
        source_sql_sha256=_sha256_text(source_sql),
        schema_status=schema_status,
        schema_ref=schema_ref,
        schema_artifact=schema_artifact,
    )

    if dry_run_status:
        _fail_closed(
            status,
            bucket="status_dry_run_only",
            reason="--dry-run-status wrote metadata and skipped runtime/extraction",
            runtime_status="not_requested",
        )
        _write_json(workspace / "learnedrewrite_status.json", status)
        return 0

    if env["SQLRB_ENGINE"] not in KNOWN_ENGINES:
        _fail_closed(
            status,
            bucket="unsupported_engine",
            reason=f"unknown SQLRB_ENGINE: {env['SQLRB_ENGINE']}",
            runtime_status="not_attempted",
        )
        _write_json(workspace / "learnedrewrite_status.json", status)
        return 0
    if env["SQLRB_ENGINE"] not in SUPPORTED_ENGINES:
        _fail_closed(
            status,
            bucket="unsupported_engine",
            reason=f"{env['SQLRB_ENGINE']} is not enabled for the LearnedRewrite scaffold",
            runtime_status="not_attempted",
        )
        _write_json(workspace / "learnedrewrite_status.json", status)
        return 0
    if schema_status == "schema_context_unavailable":
        _fail_closed(
            status,
            bucket="schema_context_unavailable",
            reason="no schema context or schema_ref could be resolved for LearnedRewrite",
            runtime_status="not_attempted",
        )
        _write_json(workspace / "learnedrewrite_status.json", status)
        return 0

    runtime = _runtime_fail_closed(config)
    status["runtime_status"] = runtime.status
    status["runtime_attempted"] = runtime.runtime_attempted
    if runtime.failure_bucket != "none":
        _fail_closed(
            status,
            bucket=runtime.failure_bucket,
            reason=runtime.reason,
            runtime_status=runtime.status,
            runtime_attempted=runtime.runtime_attempted,
        )
        _write_json(workspace / "learnedrewrite_status.json", status)
        return 0

    extraction = extract_sql_candidate(runtime.raw_output)
    status["extraction_status"] = extraction.status
    if extraction.status != "extracted":
        _fail_closed(
            status,
            bucket=extraction.failure_bucket,
            reason=extraction.reason,
            runtime_status=runtime.status,
            runtime_attempted=runtime.runtime_attempted,
        )
        _write_json(workspace / "learnedrewrite_status.json", status)
        return 0

    candidate_path = Path(env["SQLRB_CANDIDATE_SQL_PATH"])
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(extraction.sql, encoding="utf-8")
    status["candidate_generated"] = True
    status["candidate_sql_sha256"] = _sha256_text(extraction.sql)
    status["source_like_status"] = (
        "source_like" if _strip_one_trailing_semicolon(extraction.sql).casefold() == _strip_one_trailing_semicolon(source_sql).casefold() else "not_source_like"
    )
    status["failure_bucket"] = "none"
    status["fail_closed_reason"] = ""
    _write_json(workspace / "learnedrewrite_status.json", status)
    print(f"{ROUTE_ID}: fake runtime candidate SQL generated for {env['SQLRB_CASE_ID']}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run(dry_run_status=args.dry_run_status)
    except AdapterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
