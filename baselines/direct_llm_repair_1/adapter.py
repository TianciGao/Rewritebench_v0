#!/usr/bin/env python3
"""Direct LLM Repair-1 adapter scaffold.

This adapter consumes an original Direct LLM candidate plus local
execution/checker feedback and asks a provider for one repaired SQL statement.
The scaffold supports fake-provider fixture tests and keeps live provider calls
behind the same explicit environment gate as the original Direct LLM route.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


METHOD_ID = "direct_llm_repair_1"
ROUTE_ID = "direct_llm_repair_1"
BASELINE_FAMILY = "direct_llm"
ORIGINAL_ROUTE_ID = "direct_llm_original"
ORIGINAL_METHOD_ID = "direct_llm_original"
REPAIR_PROMPT_TEMPLATE_ID = "direct_llm_repair_1_feedback_sql_only_v0"
EXTRACTION_POLICY_ID = "single_sql_candidate_repair_v0"
DEFAULT_BASE_URL = "https://api.gptsapi.net/v1"
DEFAULT_MODEL = "gpt-5.4"
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TIMEOUT_SECONDS = 60.0
DEFAULT_USER_AGENT = "SQL-RewriteBench/0.1"
SUPPORTED_ENGINES = {"postgres", "mysql", "spark"}
SUPPORTED_FEEDBACK_TYPES = {
    "checker_mismatch_feedback",
    "candidate_execution_error_feedback",
}
EXCLUDED_FEEDBACK_TYPES = {
    "unsupported_engine_boundary_feedback",
}

REQUIRED_ENV = [
    "SQLRB_RUN_ID",
    "SQLRB_CASE_ID",
    "SQLRB_POOL",
    "SQLRB_ENGINE",
    "SQLRB_SOURCE_SQL_PATH",
    "SQLRB_CASE_DIR",
    "SQLRB_WORKSPACE_DIR",
    "SQLRB_CANDIDATE_SQL_PATH",
]

FENCED_BLOCK_PATTERN = re.compile(
    r"```(?P<lang>[a-zA-Z0-9_-]*)\s*\n(?P<body>.*?)```",
    re.DOTALL,
)
SQL_START_PATTERN = re.compile(r"^\s*(?:WITH|SELECT)\b", re.IGNORECASE | re.DOTALL)


class AdapterError(RuntimeError):
    """Raised when required adapter invocation context is malformed."""


@dataclass(frozen=True)
class ProviderConfig:
    provider: str
    base_url: str
    base_url_host: str
    base_url_env_used: str
    api_key: str
    api_key_env_used: str
    model_id: str
    model_env_used: str
    temperature: float
    top_p: float
    max_tokens: int
    timeout_seconds: float
    allow_live: bool
    auth_header: str
    save_raw_response: bool


@dataclass(frozen=True)
class ExtractionResult:
    status: str
    sql: str
    failure_bucket: str
    reason: str


@dataclass(frozen=True)
class RepairFeedback:
    feedback_type: str
    source_feedback_type: str
    source_executable: bool | None
    candidate_executable: bool | None
    checker_attempted: bool | None
    exact_status: str
    failure_bucket: str
    checker_or_error_summary: str
    normalized_execution_error_class: str
    raw: dict[str, Any]


def _utc_now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Direct LLM Repair-1 adapter scaffold")
    parser.add_argument(
        "--dry-run-prompt",
        action="store_true",
        help="render Repair-1 prompt/status and skip provider call",
    )
    return parser.parse_args(argv)


def load_env() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        raise AdapterError(f"missing required environment variables: {', '.join(missing)}")
    env = {name: os.environ[name] for name in REQUIRED_ENV}
    for optional in [
        "SQLRB_REPAIR1_ORIGINAL_CANDIDATE_SQL_PATH",
        "SQLRB_ORIGINAL_CANDIDATE_SQL_PATH",
        "SQLRB_REPAIR1_FEEDBACK_PATH",
        "SQLRB_REPAIR_FEEDBACK_PATH",
        "SQLRB_FEEDBACK_PATH",
        "SQLRB_REPAIR1_ORIGINAL_CANDIDATE_ID",
        "SQLRB_REPAIR1_ORIGINAL_RUN_ID",
    ]:
        if os.environ.get(optional):
            env[optional] = os.environ[optional]
    return env


def _float_env(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise AdapterError(f"{name} must be a float") from exc


def _int_env(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise AdapterError(f"{name} must be an integer") from exc


def _first_env(names: list[str], default: str = "") -> tuple[str, str]:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value, name
    return default, ""


def resolve_provider_config() -> ProviderConfig:
    provider = os.environ.get("SQLRB_LLM_PROVIDER", "openai_compatible").strip() or "openai_compatible"
    base_url, base_url_env = _first_env(["SQLRB_LLM_BASE_URL", "GPTSAPI_BASE_URL"], DEFAULT_BASE_URL)
    api_key, api_key_env = _first_env(["SQLRB_LLM_API_KEY", "GPTSAPI_API_KEY"], "")
    model_id, model_env = _first_env(["SQLRB_LLM_MODEL", "GPTSAPI_MODEL"], DEFAULT_MODEL)
    parsed = urllib.parse.urlparse(base_url)
    auth_header = os.environ.get("SQLRB_LLM_AUTH_HEADER", "authorization_bearer").strip().lower()
    if auth_header not in {"authorization_bearer", "x-api-key"}:
        raise AdapterError("SQLRB_LLM_AUTH_HEADER must be authorization_bearer or x-api-key")
    return ProviderConfig(
        provider=provider,
        base_url=base_url,
        base_url_host=parsed.netloc,
        base_url_env_used=base_url_env or "default",
        api_key=api_key,
        api_key_env_used=api_key_env,
        model_id=model_id,
        model_env_used=model_env or "default",
        temperature=_float_env("SQLRB_LLM_TEMPERATURE", 0.0),
        top_p=_float_env("SQLRB_LLM_TOP_P", 1.0),
        max_tokens=_int_env("SQLRB_LLM_MAX_TOKENS", DEFAULT_MAX_TOKENS),
        timeout_seconds=_float_env("SQLRB_LLM_TIMEOUT", DEFAULT_TIMEOUT_SECONDS),
        allow_live=os.environ.get("SQLRB_LLM_ALLOW_LIVE") == "1",
        auth_header=auth_header,
        save_raw_response=os.environ.get("SQLRB_LLM_SAVE_RAW_RESPONSE") == "1",
    )


def resolve_schema_ddl_path(env: dict[str, str]) -> Path | None:
    case_dir = Path(env["SQLRB_CASE_DIR"])
    engine = env["SQLRB_ENGINE"]
    candidates = [
        case_dir / "schema" / f"ddl_{engine}.sql",
        case_dir / "schema" / f"{engine}.sql",
        case_dir / "schema" / "ddl.sql",
        case_dir / "schema.sql",
    ]
    if engine == "postgres":
        candidates.insert(0, case_dir / "schema" / "ddl_pg.sql")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def load_schema_context(env: dict[str, str]) -> tuple[Path | None, str]:
    ddl_path = resolve_schema_ddl_path(env)
    if ddl_path is None:
        return None, ""
    return ddl_path, ddl_path.read_text(encoding="utf-8")


def _resolve_context_path(env: dict[str, str], names: list[str]) -> tuple[Path | None, str]:
    for name in names:
        value = env.get(name) or os.environ.get(name)
        if value:
            return Path(value), name
    return None, ""


def resolve_original_candidate_path(env: dict[str, str]) -> tuple[Path | None, str]:
    return _resolve_context_path(
        env,
        [
            "SQLRB_REPAIR1_ORIGINAL_CANDIDATE_SQL_PATH",
            "SQLRB_ORIGINAL_CANDIDATE_SQL_PATH",
        ],
    )


def resolve_feedback_path(env: dict[str, str]) -> tuple[Path | None, str]:
    return _resolve_context_path(
        env,
        [
            "SQLRB_REPAIR1_FEEDBACK_PATH",
            "SQLRB_REPAIR_FEEDBACK_PATH",
            "SQLRB_FEEDBACK_PATH",
        ],
    )


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _coerce_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
    return None


def _feedback_summary(payload: dict[str, Any]) -> str:
    for key in [
        "checker_or_error_summary",
        "checker_error_summary",
        "execution_error_summary",
        "error_summary",
        "feedback_summary",
        "safe_error_excerpt",
    ]:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def normalize_feedback_type(payload: dict[str, Any]) -> tuple[str, str]:
    raw = (
        payload.get("feedback_type")
        or payload.get("likely_repair1_feedback_type")
        or payload.get("failure_bucket")
        or ""
    )
    source = str(raw).strip()
    lowered = source.lower()
    mapping = {
        "mismatch": "checker_mismatch_feedback",
        "checker_mismatch": "checker_mismatch_feedback",
        "checker_mismatch_feedback": "checker_mismatch_feedback",
        "candidate_execution_failed": "candidate_execution_error_feedback",
        "candidate_execution_failed_before_checker": "candidate_execution_error_feedback",
        "candidate_execution_error": "candidate_execution_error_feedback",
        "candidate_execution_error_feedback": "candidate_execution_error_feedback",
        "unsupported_engine": "unsupported_engine_boundary_feedback",
        "source_engine_unsupported_fail_closed": "unsupported_engine_boundary_feedback",
        "unsupported_engine_boundary_feedback": "unsupported_engine_boundary_feedback",
    }
    return mapping.get(lowered, lowered), source


def load_feedback(path: Path) -> RepairFeedback:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AdapterError(f"feedback JSON is malformed: {path}") from exc
    if not isinstance(payload, dict):
        raise AdapterError("feedback JSON must be an object")
    feedback_type, source_feedback_type = normalize_feedback_type(payload)
    exact_value = payload.get("exact_status", payload.get("exact", ""))
    return RepairFeedback(
        feedback_type=feedback_type,
        source_feedback_type=source_feedback_type,
        source_executable=_coerce_bool(payload.get("source_executable")),
        candidate_executable=_coerce_bool(payload.get("candidate_executable")),
        checker_attempted=_coerce_bool(payload.get("checker_attempted")),
        exact_status=str(exact_value),
        failure_bucket=str(payload.get("failure_bucket", "")).strip(),
        checker_or_error_summary=_feedback_summary(payload),
        normalized_execution_error_class=str(payload.get("normalized_execution_error_class", "")).strip(),
        raw=payload,
    )


def build_prompt(
    *,
    env: dict[str, str],
    source_sql: str,
    original_candidate_sql: str,
    original_candidate_id: str,
    original_candidate_sha256: str,
    feedback: RepairFeedback,
    schema_ddl: str,
    config: ProviderConfig,
) -> dict[str, Any]:
    target_dialect = env["SQLRB_ENGINE"]
    system_message = (
        "You are a SQL Repair-1 rewrite engine for SQL-RewriteBench.\n"
        "Repair the original candidate using only the provided local feedback.\n"
        "Return exactly one SQL query for the requested target dialect.\n"
        "Return SQL only: no markdown, no explanation, no commentary.\n"
        "Preserve source-query semantics, result columns, result labels, and row multiplicity.\n"
        "Use only tables and columns present in the provided schema.\n"
        "Do not emit DDL, DML, temp tables, indexes, stored procedures, UDFs, or multiple statements.\n"
        "If no safe repair is possible, return the original candidate SQL unchanged."
    )
    user_message = (
        f"case_id: {env['SQLRB_CASE_ID']}\n"
        f"pool: {env['SQLRB_POOL']}\n"
        f"target dialect: {target_dialect}\n"
        f"model_id: {config.model_id}\n"
        f"original_candidate_id: {original_candidate_id}\n"
        f"original_candidate_sql_sha256: {original_candidate_sha256}\n"
        f"feedback_type: {feedback.feedback_type}\n"
        f"failure_bucket: {feedback.failure_bucket or '<unavailable>'}\n"
        f"source_executable: {_format_optional_bool(feedback.source_executable)}\n"
        f"candidate_executable: {_format_optional_bool(feedback.candidate_executable)}\n"
        f"checker_attempted: {_format_optional_bool(feedback.checker_attempted)}\n"
        f"exact_status: {feedback.exact_status or '<unavailable>'}\n"
        f"normalized_execution_error_class: {feedback.normalized_execution_error_class or '<none>'}\n"
        "\n"
        "Schema / DDL context:\n"
        f"{schema_ddl.strip() if schema_ddl.strip() else '<schema unavailable>'}\n"
        "\n"
        "Source SQL:\n"
        f"{source_sql.strip()}\n"
        "\n"
        "Original Direct LLM candidate SQL:\n"
        f"{original_candidate_sql.strip()}\n"
        "\n"
        "Local execution/checker feedback summary:\n"
        f"{feedback.checker_or_error_summary}\n"
        "\n"
        "Task: Produce one repaired, semantically equivalent SQL candidate for the target same-engine "
        "dialect. Return SQL only."
    )
    prompt = {
        "prompt_template_id": REPAIR_PROMPT_TEMPLATE_ID,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        "metadata": {
            "route_id": ROUTE_ID,
            "method_id": METHOD_ID,
            "original_route_id": ORIGINAL_ROUTE_ID,
            "original_method_id": ORIGINAL_METHOD_ID,
            "case_id": env["SQLRB_CASE_ID"],
            "pool": env["SQLRB_POOL"],
            "target_dialect": target_dialect,
            "source_sql_path": env["SQLRB_SOURCE_SQL_PATH"],
            "original_candidate_id": original_candidate_id,
            "original_candidate_sql_sha256": original_candidate_sha256,
            "feedback_type": feedback.feedback_type,
            "repair_prompt_template_id": REPAIR_PROMPT_TEMPLATE_ID,
            "schema_context_status": "available" if schema_ddl.strip() else "unavailable",
            "model_id": config.model_id,
            "local_only": True,
            "official_metric_input": False,
            "paper_result": False,
        },
    }
    prompt["prompt_sha256"] = _sha256_text(json.dumps(prompt["messages"], sort_keys=True))
    return prompt


def _format_optional_bool(value: bool | None) -> str:
    if value is None:
        return "<unavailable>"
    return "true" if value else "false"


def _strip_one_trailing_semicolon(sql: str) -> str:
    stripped = sql.strip()
    if stripped.endswith(";"):
        return stripped[:-1].rstrip()
    return stripped


def _looks_like_single_sql_statement(text: str) -> tuple[bool, str]:
    stripped = text.strip()
    if not stripped:
        return False, "response_empty"
    if not SQL_START_PATTERN.match(stripped):
        return False, "response_not_sql"
    without_final = _strip_one_trailing_semicolon(stripped)
    if ";" in without_final:
        return False, "multiple_sql_statements_ambiguous"
    return True, ""


def extract_sql_candidate(raw_response: str) -> ExtractionResult:
    if not raw_response.strip():
        return ExtractionResult(
            status="response_empty",
            sql="",
            failure_bucket="response_empty",
            reason="provider response was empty",
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
            status="multiple_sql_blocks_ambiguous",
            sql="",
            failure_bucket="multiple_sql_blocks_ambiguous",
            reason="multiple SQL code blocks were present",
        )
    if len(blocks) == 1:
        return ExtractionResult(
            status="extracted",
            sql=_strip_one_trailing_semicolon(blocks[0]) + ";\n",
            failure_bucket="none",
            reason="extracted one fenced SQL block",
        )

    raw = raw_response.strip()
    ok, reason = _looks_like_single_sql_statement(raw)
    if not ok:
        return ExtractionResult(
            status="sql_extraction_failed",
            sql="",
            failure_bucket=reason,
            reason=reason,
        )
    return ExtractionResult(
        status="extracted",
        sql=_strip_one_trailing_semicolon(raw) + ";\n",
        failure_bucket="none",
        reason="full response looked like one SQL statement",
    )


def _fake_provider_response() -> dict[str, Any]:
    content = os.environ.get(
        "SQLRB_REPAIR1_FAKE_RESPONSE",
        os.environ.get("SQLRB_LLM_FAKE_RESPONSE", "SELECT 1 AS direct_llm_repair_1_fake_smoke;"),
    )
    return {
        "id": "fake-direct-llm-repair-1-response",
        "choices": [{"message": {"content": content}}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


def _call_openai_compatible(prompt: dict[str, Any], config: ProviderConfig) -> dict[str, Any]:
    url = config.base_url.rstrip("/") + "/chat/completions"
    body = {
        "model": config.model_id,
        "messages": prompt["messages"],
        "temperature": config.temperature,
        "top_p": config.top_p,
        "max_tokens": config.max_tokens,
    }
    headers = {"Content-Type": "application/json", "User-Agent": DEFAULT_USER_AGENT}
    if config.auth_header == "x-api-key":
        headers["x-api-key"] = config.api_key
    else:
        headers["Authorization"] = f"Bearer {config.api_key}"
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.timeout_seconds) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AdapterError(f"request_failed: HTTP {exc.code}: {detail[:500]}") from exc
    except urllib.error.URLError as exc:
        raise AdapterError(f"request_failed: {exc.reason}") from exc
    return json.loads(payload)


def _response_content(response: dict[str, Any]) -> str:
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""
    first = choices[0]
    if not isinstance(first, dict):
        return ""
    message = first.get("message")
    if isinstance(message, dict) and isinstance(message.get("content"), str):
        return message["content"]
    text = first.get("text")
    if isinstance(text, str):
        return text
    return ""


def _base_status(
    *,
    env: dict[str, str],
    config: ProviderConfig,
    schema_ddl_path: Path | None,
    original_candidate_path: Path | None,
    original_candidate_path_env_used: str,
    feedback_path: Path | None,
    feedback_path_env_used: str,
) -> dict[str, Any]:
    return {
        "schema_version": "direct_llm_repair_1_adapter_status_v0",
        "created_at_utc": _utc_now_iso(),
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "baseline_family": BASELINE_FAMILY,
        "original_route_id": ORIGINAL_ROUTE_ID,
        "original_method_id": ORIGINAL_METHOD_ID,
        "run_id": env["SQLRB_RUN_ID"],
        "case_id": env["SQLRB_CASE_ID"],
        "pool": env["SQLRB_POOL"],
        "engine": env["SQLRB_ENGINE"],
        "source_sql_path": env["SQLRB_SOURCE_SQL_PATH"],
        "case_dir": env["SQLRB_CASE_DIR"],
        "candidate_sql_path": env["SQLRB_CANDIDATE_SQL_PATH"],
        "schema_ddl_path": str(schema_ddl_path) if schema_ddl_path else "",
        "schema_context_status": "available" if schema_ddl_path else "unavailable",
        "original_run_id": env.get("SQLRB_REPAIR1_ORIGINAL_RUN_ID", ""),
        "original_candidate_id": env.get("SQLRB_REPAIR1_ORIGINAL_CANDIDATE_ID", ""),
        "original_candidate_sql_path": str(original_candidate_path) if original_candidate_path else "",
        "original_candidate_sql_path_env_used": original_candidate_path_env_used,
        "original_candidate_sql_sha256": "",
        "feedback_path": str(feedback_path) if feedback_path else "",
        "feedback_path_env_used": feedback_path_env_used,
        "feedback_type": "",
        "source_feedback_type": "",
        "repair_prompt_template_id": REPAIR_PROMPT_TEMPLATE_ID,
        "prompt_template_id": REPAIR_PROMPT_TEMPLATE_ID,
        "prompt_sha256": "",
        "repaired_candidate_id": "",
        "extraction_policy": EXTRACTION_POLICY_ID,
        "provider": config.provider,
        "base_url_host": config.base_url_host,
        "base_url_env_used": config.base_url_env_used,
        "api_key_present": bool(config.api_key),
        "api_key_env_used": config.api_key_env_used,
        "model_id": config.model_id,
        "model_env_used": config.model_env_used,
        "temperature": config.temperature,
        "top_p": config.top_p,
        "max_tokens": config.max_tokens,
        "timeout_seconds": config.timeout_seconds,
        "user_agent": DEFAULT_USER_AGENT,
        "live_call": False,
        "request_timestamp": "",
        "raw_response_saved": False,
        "raw_response_path": "",
        "candidate_generated": False,
        "call_attempted": False,
        "call_status": "not_attempted",
        "extraction_status": "not_attempted",
        "failure_bucket": "no_candidate_sql",
        "failure_reason": "",
        "token_usage": {},
        "repair_attempted": False,
        "local_only": True,
        "official_metric_input": False,
        "paper_result": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _fail_closed(status: dict[str, Any], *, bucket: str, reason: str, call_status: str) -> int:
    status["failure_bucket"] = bucket
    status["failure_reason"] = reason
    status["call_status"] = call_status
    status["candidate_generated"] = False
    return 0


def _default_original_candidate_id(env: dict[str, str], feedback: RepairFeedback | None) -> str:
    if env.get("SQLRB_REPAIR1_ORIGINAL_CANDIDATE_ID"):
        return env["SQLRB_REPAIR1_ORIGINAL_CANDIDATE_ID"]
    if feedback is not None and isinstance(feedback.raw.get("original_candidate_id"), str):
        return feedback.raw["original_candidate_id"]
    original_run_id = env.get("SQLRB_REPAIR1_ORIGINAL_RUN_ID") or "direct_llm_original_track_a_120_canonical_v0"
    return f"{original_run_id}:{env['SQLRB_CASE_ID']}:{env['SQLRB_ENGINE']}:direct_llm_original"


def _write_status(workspace: Path, status: dict[str, Any]) -> None:
    _write_json(workspace / "direct_llm_repair_1_status.json", status)


def run(*, dry_run_prompt: bool = False) -> int:
    env = load_env()
    if env["SQLRB_ENGINE"] not in SUPPORTED_ENGINES:
        raise AdapterError(f"unsupported SQLRB_ENGINE for Direct LLM Repair-1 adapter: {env['SQLRB_ENGINE']}")

    workspace = Path(env["SQLRB_WORKSPACE_DIR"])
    workspace.mkdir(parents=True, exist_ok=True)
    source_path = Path(env["SQLRB_SOURCE_SQL_PATH"])
    source_sql = source_path.read_text(encoding="utf-8")
    schema_ddl_path, schema_ddl = load_schema_context(env)
    config = resolve_provider_config()
    original_candidate_path, original_candidate_path_env = resolve_original_candidate_path(env)
    feedback_path, feedback_path_env = resolve_feedback_path(env)
    status = _base_status(
        env=env,
        config=config,
        schema_ddl_path=schema_ddl_path,
        original_candidate_path=original_candidate_path,
        original_candidate_path_env_used=original_candidate_path_env,
        feedback_path=feedback_path,
        feedback_path_env_used=feedback_path_env,
    )

    if original_candidate_path is None:
        _fail_closed(
            status,
            bucket="missing_original_candidate",
            reason="SQLRB_REPAIR1_ORIGINAL_CANDIDATE_SQL_PATH or SQLRB_ORIGINAL_CANDIDATE_SQL_PATH is required",
            call_status="not_attempted",
        )
        _write_status(workspace, status)
        return 0
    if not original_candidate_path.exists():
        _fail_closed(
            status,
            bucket="missing_original_candidate",
            reason=f"original candidate SQL path does not exist: {original_candidate_path}",
            call_status="not_attempted",
        )
        _write_status(workspace, status)
        return 0
    original_candidate_sql = original_candidate_path.read_text(encoding="utf-8")
    if not original_candidate_sql.strip():
        _fail_closed(
            status,
            bucket="missing_original_candidate",
            reason="original candidate SQL is empty",
            call_status="not_attempted",
        )
        _write_status(workspace, status)
        return 0
    status["original_candidate_sql_sha256"] = _sha256_file(original_candidate_path)

    if feedback_path is None:
        _fail_closed(
            status,
            bucket="missing_feedback",
            reason="SQLRB_REPAIR1_FEEDBACK_PATH, SQLRB_REPAIR_FEEDBACK_PATH, or SQLRB_FEEDBACK_PATH is required",
            call_status="not_attempted",
        )
        _write_status(workspace, status)
        return 0
    if not feedback_path.exists():
        _fail_closed(
            status,
            bucket="missing_feedback",
            reason=f"feedback path does not exist: {feedback_path}",
            call_status="not_attempted",
        )
        _write_status(workspace, status)
        return 0

    try:
        feedback = load_feedback(feedback_path)
    except AdapterError as exc:
        _fail_closed(status, bucket="missing_feedback", reason=str(exc), call_status="not_attempted")
        _write_status(workspace, status)
        return 0

    status["feedback_type"] = feedback.feedback_type
    status["source_feedback_type"] = feedback.source_feedback_type
    original_candidate_id = _default_original_candidate_id(env, feedback)
    status["original_candidate_id"] = original_candidate_id
    status["original_run_id"] = (
        env.get("SQLRB_REPAIR1_ORIGINAL_RUN_ID")
        or str(feedback.raw.get("original_run_id", "direct_llm_original_track_a_120_canonical_v0"))
    )
    status["repaired_candidate_id"] = f"{original_candidate_id}:repair_1"

    if feedback.feedback_type in EXCLUDED_FEEDBACK_TYPES:
        _fail_closed(
            status,
            bucket="unsupported_engine_boundary",
            reason="unsupported_engine rows are excluded from Repair-1 attempts",
            call_status="not_attempted",
        )
        _write_status(workspace, status)
        return 0
    if feedback.feedback_type not in SUPPORTED_FEEDBACK_TYPES:
        _fail_closed(
            status,
            bucket="unsupported_feedback",
            reason=f"unsupported Repair-1 feedback type: {feedback.source_feedback_type or feedback.feedback_type}",
            call_status="not_attempted",
        )
        _write_status(workspace, status)
        return 0
    if not feedback.checker_or_error_summary:
        _fail_closed(
            status,
            bucket="missing_feedback",
            reason="feedback payload did not include a checker/error summary",
            call_status="not_attempted",
        )
        _write_status(workspace, status)
        return 0

    prompt = build_prompt(
        env=env,
        source_sql=source_sql,
        original_candidate_sql=original_candidate_sql,
        original_candidate_id=original_candidate_id,
        original_candidate_sha256=status["original_candidate_sql_sha256"],
        feedback=feedback,
        schema_ddl=schema_ddl,
        config=config,
    )
    status["prompt_sha256"] = prompt["prompt_sha256"]
    _write_json(workspace / "direct_llm_repair_1_prompt.json", prompt)

    if dry_run_prompt:
        _fail_closed(
            status,
            bucket="prompt_dry_run_only",
            reason="--dry-run-prompt rendered Repair-1 prompt and skipped provider call",
            call_status="not_requested",
        )
        _write_status(workspace, status)
        return 0

    if config.provider == "fake":
        response = _fake_provider_response()
        status["call_attempted"] = True
        status["call_status"] = "fake_provider_success"
        status["request_timestamp"] = _utc_now_iso()
        status["repair_attempted"] = True
    else:
        if config.provider != "openai_compatible":
            _fail_closed(
                status,
                bucket="unsupported_provider",
                reason=f"unsupported provider: {config.provider}",
                call_status="not_attempted",
            )
            _write_status(workspace, status)
            return 0
        if not config.api_key:
            _fail_closed(
                status,
                bucket="missing_api_key",
                reason="SQLRB_LLM_API_KEY or GPTSAPI_API_KEY is required",
                call_status="not_attempted",
            )
            _write_status(workspace, status)
            return 0
        if not config.allow_live:
            _fail_closed(
                status,
                bucket="live_api_disabled",
                reason="set SQLRB_LLM_ALLOW_LIVE=1 to permit a live Repair-1 provider call",
                call_status="not_attempted",
            )
            _write_status(workspace, status)
            return 0
        status["call_attempted"] = True
        status["live_call"] = True
        status["request_timestamp"] = _utc_now_iso()
        status["repair_attempted"] = True
        try:
            response = _call_openai_compatible(prompt, config)
            status["call_status"] = "success"
        except Exception as exc:
            _fail_closed(status, bucket="request_failed", reason=str(exc), call_status="request_failed")
            _write_status(workspace, status)
            return 0

    if config.save_raw_response or config.provider == "fake":
        raw_path = workspace / "direct_llm_repair_1_raw_response.json"
        _write_json(raw_path, response)
        status["raw_response_saved"] = True
        status["raw_response_path"] = str(raw_path)

    if isinstance(response.get("usage"), dict):
        status["token_usage"] = response["usage"]

    extraction = extract_sql_candidate(_response_content(response))
    status["extraction_status"] = extraction.status
    if extraction.status != "extracted":
        _fail_closed(
            status,
            bucket=extraction.failure_bucket,
            reason=extraction.reason,
            call_status=status["call_status"],
        )
        _write_status(workspace, status)
        return 0

    candidate_path = Path(env["SQLRB_CANDIDATE_SQL_PATH"])
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(extraction.sql, encoding="utf-8")
    status["candidate_generated"] = True
    status["failure_bucket"] = "none"
    status["failure_reason"] = ""
    status["repaired_candidate_sql_sha256"] = _sha256_text(extraction.sql)
    _write_status(workspace, status)
    print(f"{ROUTE_ID}: repaired candidate SQL generated for {env['SQLRB_CASE_ID']} on {env['SQLRB_ENGINE']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run(dry_run_prompt=args.dry_run_prompt)
    except AdapterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
