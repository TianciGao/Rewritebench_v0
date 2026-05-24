#!/usr/bin/env python3
"""Provider-agnostic Direct LLM original adapter for local user runs.

The adapter reads the public ``sql_rewrite_bench.user_run`` environment,
builds a deterministic SQL-only rewrite prompt, optionally calls an
OpenAI-compatible chat/completions endpoint, extracts exactly one SQL candidate,
and writes it to ``SQLRB_CANDIDATE_SQL_PATH``.

Expected fail-closed states return exit code 0 without writing candidate SQL so
the user runner records a denominator-visible no-candidate row rather than a
runner crash. Configuration and per-row status are written to the workspace.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


METHOD_ID = "direct_llm_original"
ROUTE_ID = "direct_llm_original"
BASELINE_FAMILY = "direct_llm"
PROMPT_TEMPLATE_ID = "direct_llm_original_sql_only_v0"
EXTRACTION_POLICY_ID = "single_sql_candidate_v0"
DEFAULT_BASE_URL = "https://api.gptsapi.net/v1"
DEFAULT_MODEL = "gpt-5.4"
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TIMEOUT_SECONDS = 60.0

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

SUPPORTED_ENGINES = {"postgres", "mysql", "spark"}

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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one Direct LLM original candidate SQL for a user-run row."
    )
    parser.add_argument(
        "--dry-run-prompt",
        action="store_true",
        help="Render prompt/status only; do not call a provider or write candidate SQL.",
    )
    return parser.parse_args(argv)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_env() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV_VARS if not os.environ.get(name)]
    if missing:
        raise AdapterError("missing required environment variables: " + ", ".join(missing))
    return {name: os.environ[name] for name in REQUIRED_ENV_VARS}


def _env_first(names: list[str], default: str = "") -> tuple[str, str]:
    for name in names:
        value = os.environ.get(name, "")
        if value:
            return value, name
    return default, "default" if default else "none"


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name, "")
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise AdapterError(f"{name} must be a float") from exc


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "")
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise AdapterError(f"{name} must be an integer") from exc
    if value <= 0:
        raise AdapterError(f"{name} must be positive")
    return value


def _host_from_url(base_url: str) -> str:
    parsed = urllib.parse.urlparse(base_url)
    return parsed.netloc or ""


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


def resolve_provider_config() -> ProviderConfig:
    provider = os.environ.get("SQLRB_LLM_PROVIDER", "openai_compatible").strip()
    base_url, base_url_env = _env_first(
        ["SQLRB_LLM_BASE_URL", "GPTSAPI_BASE_URL"],
        DEFAULT_BASE_URL,
    )
    api_key, api_key_env = _env_first(["SQLRB_LLM_API_KEY", "GPTSAPI_API_KEY"])
    model, model_env = _env_first(["SQLRB_LLM_MODEL", "GPTSAPI_MODEL"], DEFAULT_MODEL)
    auth_header = os.environ.get("SQLRB_LLM_AUTH_HEADER", "authorization_bearer").strip()
    if auth_header not in {"authorization_bearer", "x-api-key"}:
        raise AdapterError("SQLRB_LLM_AUTH_HEADER must be authorization_bearer or x-api-key")
    return ProviderConfig(
        provider=provider,
        base_url=base_url.rstrip("/"),
        base_url_host=_host_from_url(base_url),
        base_url_env_used=base_url_env,
        api_key=api_key,
        api_key_env_used=api_key_env,
        model_id=model,
        model_env_used=model_env,
        temperature=_env_float("SQLRB_LLM_TEMPERATURE", 0.0),
        top_p=_env_float("SQLRB_LLM_TOP_P", 1.0),
        max_tokens=_env_int("SQLRB_LLM_MAX_TOKENS", DEFAULT_MAX_TOKENS),
        timeout_seconds=_env_float("SQLRB_LLM_TIMEOUT", DEFAULT_TIMEOUT_SECONDS),
        allow_live=os.environ.get("SQLRB_LLM_ALLOW_LIVE", "") == "1",
        auth_header=auth_header,
        save_raw_response=os.environ.get("SQLRB_LLM_SAVE_RAW_RESPONSE", "") == "1",
    )


def resolve_schema_ddl_path(env: dict[str, str]) -> Path | None:
    case_dir = Path(env["SQLRB_CASE_DIR"])
    engine = env["SQLRB_ENGINE"]
    candidates = []
    for name in DDL_CANDIDATE_NAMES.get(engine, [f"ddl_{engine}.sql"]):
        candidates.append(case_dir / "schema" / name)
    candidates.append(case_dir / "schema" / engine / "ddl.sql")

    case_schema_profile = case_dir / "schema" / "schema_profile.yaml"
    candidates.extend(_schema_profile_candidates(case_schema_profile, engine))
    for key in [
        "external_schema_profile",
        "external_profile",
        "profile",
    ]:
        raw_profile = _yaml_scalar(case_schema_profile, key)
        if raw_profile.startswith("schemas/"):
            candidates.extend(_schema_profile_candidates(_resolve_repo_path(raw_profile), engine))

    manifest_path = case_dir / "manifest.yaml"
    for key in ["external_profile", "profile"]:
        raw_profile = _yaml_scalar(manifest_path, key)
        if raw_profile.startswith("schemas/"):
            candidates.extend(_schema_profile_candidates(_resolve_repo_path(raw_profile), engine))

    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return None


def load_schema_context(env: dict[str, str]) -> tuple[Path | None, str]:
    ddl_path = resolve_schema_ddl_path(env)
    if ddl_path is None:
        return None, ""
    return ddl_path, ddl_path.read_text(encoding="utf-8")


def build_prompt(
    *,
    env: dict[str, str],
    source_sql: str,
    schema_ddl: str,
    config: ProviderConfig,
) -> dict[str, Any]:
    target_dialect = env["SQLRB_ENGINE"]
    system_message = (
        "You are a SQL rewrite engine for SQL-RewriteBench.\n"
        "Return exactly one SQL query for the requested target dialect.\n"
        "Return SQL only: no markdown, no explanation, no commentary.\n"
        "Preserve the source query semantics, result columns, result labels, and row multiplicity.\n"
        "Use only tables and columns present in the provided schema.\n"
        "Do not emit DDL, DML, temp tables, indexes, stored procedures, UDFs, or multiple statements.\n"
        "If no safe rewrite is possible, return the original SQL unchanged."
    )
    user_message = (
        f"case_id: {env['SQLRB_CASE_ID']}\n"
        f"pool: {env['SQLRB_POOL']}\n"
        f"target dialect: {target_dialect}\n"
        f"model_id: {config.model_id}\n"
        "\n"
        "Schema / DDL context:\n"
        f"{schema_ddl.strip() if schema_ddl.strip() else '<schema unavailable>'}\n"
        "\n"
        "Source SQL:\n"
        f"{source_sql.strip()}\n"
        "\n"
        "Task: Produce one semantically equivalent SQL rewrite for the target same-engine dialect. "
        "Return SQL only."
    )
    prompt = {
        "prompt_template_id": PROMPT_TEMPLATE_ID,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        "metadata": {
            "route_id": ROUTE_ID,
            "method_id": METHOD_ID,
            "case_id": env["SQLRB_CASE_ID"],
            "pool": env["SQLRB_POOL"],
            "target_dialect": target_dialect,
            "source_sql_path": env["SQLRB_SOURCE_SQL_PATH"],
            "schema_context_status": "available" if schema_ddl.strip() else "unavailable",
            "model_id": config.model_id,
            "local_only": True,
            "official_metric_input": False,
        },
    }
    prompt["prompt_sha256"] = hashlib.sha256(
        json.dumps(prompt["messages"], sort_keys=True).encode("utf-8")
    ).hexdigest()
    return prompt


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
        sql = _strip_one_trailing_semicolon(blocks[0]) + ";\n"
        return ExtractionResult(
            status="extracted",
            sql=sql,
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
    content = os.environ.get("SQLRB_LLM_FAKE_RESPONSE", "SELECT 1 AS direct_llm_fake_smoke;")
    return {
        "id": "fake-direct-llm-response",
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
    headers = {"Content-Type": "application/json"}
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
    prompt: dict[str, Any],
    schema_ddl_path: Path | None,
) -> dict[str, Any]:
    return {
        "schema_version": "direct_llm_original_adapter_status_v0",
        "created_at_utc": _utc_now_iso(),
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "baseline_family": BASELINE_FAMILY,
        "run_id": env["SQLRB_RUN_ID"],
        "case_id": env["SQLRB_CASE_ID"],
        "pool": env["SQLRB_POOL"],
        "engine": env["SQLRB_ENGINE"],
        "source_sql_path": env["SQLRB_SOURCE_SQL_PATH"],
        "case_dir": env["SQLRB_CASE_DIR"],
        "candidate_sql_path": env["SQLRB_CANDIDATE_SQL_PATH"],
        "schema_ddl_path": str(schema_ddl_path) if schema_ddl_path else "",
        "schema_context_status": "available" if schema_ddl_path else "unavailable",
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
        "prompt_template_id": PROMPT_TEMPLATE_ID,
        "prompt_sha256": prompt["prompt_sha256"],
        "extraction_policy": EXTRACTION_POLICY_ID,
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


def run(*, dry_run_prompt: bool = False) -> int:
    env = load_env()
    if env["SQLRB_ENGINE"] not in SUPPORTED_ENGINES:
        raise AdapterError(f"unsupported SQLRB_ENGINE for Direct LLM adapter: {env['SQLRB_ENGINE']}")

    workspace = Path(env["SQLRB_WORKSPACE_DIR"])
    workspace.mkdir(parents=True, exist_ok=True)
    source_path = Path(env["SQLRB_SOURCE_SQL_PATH"])
    source_sql = source_path.read_text(encoding="utf-8")
    schema_ddl_path, schema_ddl = load_schema_context(env)
    config = resolve_provider_config()
    prompt = build_prompt(env=env, source_sql=source_sql, schema_ddl=schema_ddl, config=config)
    _write_json(workspace / "direct_llm_prompt.json", prompt)
    status = _base_status(env=env, config=config, prompt=prompt, schema_ddl_path=schema_ddl_path)

    if dry_run_prompt:
        _fail_closed(
            status,
            bucket="prompt_dry_run_only",
            reason="--dry-run-prompt rendered prompt and skipped provider call",
            call_status="not_requested",
        )
        _write_json(workspace / "direct_llm_status.json", status)
        return 0

    if config.provider == "fake":
        response = _fake_provider_response()
        status["call_attempted"] = True
        status["call_status"] = "fake_provider_success"
        status["request_timestamp"] = _utc_now_iso()
    else:
        if config.provider != "openai_compatible":
            _fail_closed(
                status,
                bucket="unsupported_provider",
                reason=f"unsupported provider: {config.provider}",
                call_status="not_attempted",
            )
            _write_json(workspace / "direct_llm_status.json", status)
            return 0
        if not config.api_key:
            _fail_closed(
                status,
                bucket="missing_api_key",
                reason="SQLRB_LLM_API_KEY or GPTSAPI_API_KEY is required",
                call_status="not_attempted",
            )
            _write_json(workspace / "direct_llm_status.json", status)
            return 0
        if not config.allow_live:
            _fail_closed(
                status,
                bucket="live_api_disabled",
                reason="set SQLRB_LLM_ALLOW_LIVE=1 to permit a live provider call",
                call_status="not_attempted",
            )
            _write_json(workspace / "direct_llm_status.json", status)
            return 0
        status["call_attempted"] = True
        status["request_timestamp"] = _utc_now_iso()
        try:
            response = _call_openai_compatible(prompt, config)
            status["call_status"] = "success"
        except Exception as exc:
            _fail_closed(status, bucket="request_failed", reason=str(exc), call_status="request_failed")
            _write_json(workspace / "direct_llm_status.json", status)
            return 0

    if config.save_raw_response or config.provider == "fake":
        raw_path = workspace / "direct_llm_raw_response.json"
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
        _write_json(workspace / "direct_llm_status.json", status)
        return 0

    candidate_path = Path(env["SQLRB_CANDIDATE_SQL_PATH"])
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(extraction.sql, encoding="utf-8")
    status["candidate_generated"] = True
    status["failure_bucket"] = "none"
    status["failure_reason"] = ""
    status["candidate_sql_sha256"] = hashlib.sha256(extraction.sql.encode("utf-8")).hexdigest()
    _write_json(workspace / "direct_llm_status.json", status)
    print(f"{ROUTE_ID}: candidate SQL generated for {env['SQLRB_CASE_ID']} on {env['SQLRB_ENGINE']}")
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
