#!/usr/bin/env python3
"""LLM-R2 adapted GPT-5.4 wrapper scaffold.

This adapter follows the public ``sql_rewrite_bench.user_run`` row
environment contract. It is an adapted local diagnostic scaffold for an
LLM-R2-like GPT-5.4 route, not an official LLM-R2 paper reproduction.

Fake fixture mode is used for tests. Live mode uses only the shared
OpenAI-compatible GPT-5.4 provider policy; it does not invoke the official
LLM-R2 runtime, Java/rule-system execution, checkpoint inference, or a
demonstration selector.
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


ROUTE_ID = "llm_r2_gpt54_adapted"
METHOD_ID = "llm_r2"
BASELINE_FAMILY = "prior_method_adapted_llm_rule_wrapper"
ADAPTER_VERSION = "llm_r2_gpt54_adapter_live_v0"
PROMPT_TEMPLATE_ID = "llm_r2_gpt54_adapted_rule_sql_only_v0"
EXTRACTION_POLICY_ID = "single_select_or_with_sql_llm_r2_gpt54_v0"
PROVIDER_POLICY = "openai_compatible"
MODEL_POLICY = "gpt-5.4"
DEFAULT_BASE_URL = "https://api.gptsapi.net/v1"
DEFAULT_TIMEOUT_SECONDS = 60.0
DEFAULT_MAX_TOKENS = 2048
DEFAULT_USER_AGENT = "SQL-RewriteBench/0.1"

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

SUPPORTED_FAKE_ENGINES = {"postgres"}
KNOWN_ENGINES = {"postgres", "mysql", "spark"}

DDL_CANDIDATE_NAMES = {
    "postgres": ["ddl_pg.sql", "ddl_postgres.sql", "ddl.sql"],
    "mysql": ["ddl_mysql.sql", "ddl.sql"],
    "spark": ["ddl_spark.sql", "ddl.sql"],
}

SQL_START_PATTERN = re.compile(r"^\s*(SELECT|WITH)\b", re.IGNORECASE | re.DOTALL)
FENCED_BLOCK_PATTERN = re.compile(
    r"```(?P<lang>[A-Za-z0-9_-]*)\s*\n?(?P<body>.*?)```",
    re.DOTALL,
)
LABELED_SQL_PATTERN = re.compile(
    r"(?:^|\n)\s*(?:candidate_sql|rewritten_sql|sql)\s*:\s*(?P<sql>(?:SELECT|WITH)\b.*)\s*$",
    re.IGNORECASE | re.DOTALL,
)


class AdapterError(RuntimeError):
    """Raised when adapter invocation context is malformed."""


@dataclass(frozen=True)
class ProviderConfig:
    provider: str
    base_url: str
    base_url_host: str
    base_url_env_used: str
    api_key: str
    api_key_present: bool
    api_key_env_used: str
    model_id: str
    model_env_used: str
    temperature: float
    top_p: float
    max_tokens: int
    allow_live: bool
    auth_header: str
    save_raw_response: bool
    timeout_seconds: float


@dataclass(frozen=True)
class RuntimeConfig:
    mode: str
    fake_response_configured: bool
    fake_sql_configured: bool
    fake_rule_sequence_configured: bool
    rule_system_required: bool
    rule_system_configured: bool
    checkpoint_required: bool
    checkpoint_configured: bool
    demonstration_selector_required: bool
    demonstration_selector_configured: bool


@dataclass(frozen=True)
class RuntimeResult:
    status: str
    raw_output: str
    failure_bucket: str
    reason: str
    fake_runtime: bool
    live_call: bool
    rule_system_runtime_used: bool
    checkpoint_used: bool
    demonstration_selector_used: bool
    rule_sequence: list[str]
    token_usage: dict[str, Any] | None = None
    prompt_sha256: str = ""
    raw_response_saved: bool = False
    raw_response_path: str = ""


@dataclass(frozen=True)
class ExtractionResult:
    status: str
    sql: str
    failure_bucket: str
    reason: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one LLM-R2 adapted GPT-5.4 candidate SQL."
    )
    parser.add_argument(
        "--dry-run-status",
        action="store_true",
        help="Write status metadata only; do not parse fake output or write candidate SQL.",
    )
    return parser.parse_args(argv)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _resolve_repo_path(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path.resolve()
    return (_repo_root() / path).resolve()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _env_first(names: list[str], default: str = "") -> tuple[str, str]:
    for name in names:
        value = os.environ.get(name, "")
        if value:
            return value, name
    return default, "default" if default else ""


def _env_timeout() -> float:
    raw = os.environ.get("SQLRB_LLM_R2_TIMEOUT", os.environ.get("SQLRB_LLM_TIMEOUT", str(DEFAULT_TIMEOUT_SECONDS)))
    try:
        value = float(raw)
    except ValueError as exc:
        raise AdapterError("SQLRB_LLM_R2_TIMEOUT/SQLRB_LLM_TIMEOUT must be numeric") from exc
    if value <= 0:
        raise AdapterError("SQLRB_LLM_R2_TIMEOUT/SQLRB_LLM_TIMEOUT must be positive")
    return value


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise AdapterError(f"{name} must be numeric") from exc


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise AdapterError(f"{name} must be an integer") from exc
    if value <= 0:
        raise AdapterError(f"{name} must be positive")
    return value


def load_env() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        raise AdapterError("missing required environment variables: " + ", ".join(missing))
    return {name: os.environ[name] for name in REQUIRED_ENV}


def resolve_provider_config() -> ProviderConfig:
    provider = os.environ.get("SQLRB_LLM_PROVIDER", PROVIDER_POLICY).strip() or PROVIDER_POLICY
    base_url, base_url_env = _env_first(["SQLRB_LLM_BASE_URL", "GPTSAPI_BASE_URL"], DEFAULT_BASE_URL)
    api_key, api_key_env = _env_first(["SQLRB_LLM_API_KEY", "GPTSAPI_API_KEY"])
    model_id, model_env = _env_first(["SQLRB_LLM_MODEL", "GPTSAPI_MODEL"], MODEL_POLICY)
    auth_header = os.environ.get("SQLRB_LLM_AUTH_HEADER", "authorization_bearer").strip().lower()
    if auth_header not in {"authorization_bearer", "x-api-key"}:
        raise AdapterError("SQLRB_LLM_AUTH_HEADER must be authorization_bearer or x-api-key")
    parsed = urllib.parse.urlparse(base_url)
    return ProviderConfig(
        provider=provider,
        base_url=base_url.rstrip("/"),
        base_url_host=parsed.netloc,
        base_url_env_used=base_url_env,
        api_key=api_key,
        api_key_present=bool(api_key),
        api_key_env_used=api_key_env,
        model_id=model_id,
        model_env_used=model_env,
        temperature=_env_float("SQLRB_LLM_TEMPERATURE", 0.0),
        top_p=_env_float("SQLRB_LLM_TOP_P", 1.0),
        max_tokens=_env_int("SQLRB_LLM_MAX_TOKENS", DEFAULT_MAX_TOKENS),
        allow_live=os.environ.get("SQLRB_LLM_ALLOW_LIVE") == "1",
        auth_header=auth_header,
        save_raw_response=os.environ.get("SQLRB_LLM_SAVE_RAW_RESPONSE") == "1",
        timeout_seconds=_env_timeout(),
    )


def resolve_runtime_config() -> RuntimeConfig:
    mode = os.environ.get("SQLRB_LLM_R2_MODE", "").strip().lower()
    fake_response_configured = "SQLRB_LLM_R2_FAKE_RESPONSE" in os.environ
    fake_sql_configured = "SQLRB_LLM_R2_FAKE_SQL" in os.environ
    fake_rule_sequence_configured = "SQLRB_LLM_R2_FAKE_RULE_SEQUENCE" in os.environ
    if not mode and (fake_response_configured or fake_sql_configured):
        mode = "fake"
    return RuntimeConfig(
        mode=mode,
        fake_response_configured=fake_response_configured,
        fake_sql_configured=fake_sql_configured,
        fake_rule_sequence_configured=fake_rule_sequence_configured,
        rule_system_required=os.environ.get("SQLRB_LLM_R2_REQUIRE_RULE_SYSTEM") == "1",
        rule_system_configured=bool(os.environ.get("SQLRB_LLM_R2_RULE_SYSTEM_CMD", "").strip()),
        checkpoint_required=os.environ.get("SQLRB_LLM_R2_REQUIRE_CHECKPOINT") == "1",
        checkpoint_configured=bool(os.environ.get("SQLRB_LLM_R2_CHECKPOINT_PATH", "").strip()),
        demonstration_selector_required=os.environ.get("SQLRB_LLM_R2_REQUIRE_DEMO_SELECTOR") == "1",
        demonstration_selector_configured=bool(os.environ.get("SQLRB_LLM_R2_DEMO_SELECTOR_PATH", "").strip()),
    )


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


def resolve_schema_context(env: dict[str, str]) -> tuple[str, str, str]:
    explicit_schema = os.environ.get("SQLRB_LLM_R2_SCHEMA_CONTEXT", "").strip()
    if explicit_schema:
        return "inline_schema_context_present", _sha256_text(explicit_schema), "inline"

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


def load_schema_text(schema_artifact: str) -> str:
    inline = os.environ.get("SQLRB_LLM_R2_SCHEMA_CONTEXT", "").strip()
    if inline:
        return inline
    if not schema_artifact:
        return ""
    path = Path(schema_artifact)
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


def build_prompt(
    *,
    env: dict[str, str],
    provider: ProviderConfig,
    source_sql: str,
    schema_text: str,
    schema_ref: str,
) -> dict[str, Any]:
    system = (
        "You are an adapted LLM-R2-style SQL rewrite generator for a local "
        "diagnostic benchmark route. This is not the official LLM-R2 stack and "
        "does not use Java/rule-system execution, checkpoint inference, or a "
        "demonstration selector. You may reason about common relational rewrite "
        "rules internally, but return exactly one PostgreSQL SELECT or WITH query "
        "and no prose, no markdown, no rule list, no comments, no DDL, no DML, "
        "no temporary tables, no UDFs, and no multiple statements. Preserve SQL "
        "semantics, output columns, column aliases, duplicate behavior, ordering "
        "requirements, and NULL behavior. If no safe rewrite is apparent, return "
        "the original query unchanged."
    )
    user = (
        f"route_id: {ROUTE_ID}\n"
        f"method_id: {METHOD_ID}\n"
        f"provider_policy: {PROVIDER_POLICY}\n"
        f"model_policy: {provider.model_id}\n"
        f"case_id: {env['SQLRB_CASE_ID']}\n"
        f"pool: {env['SQLRB_POOL']}\n"
        f"target_engine: {env['SQLRB_ENGINE']}\n"
        f"schema_ref: {schema_ref or 'unknown'}\n\n"
        "Schema context:\n"
        f"{schema_text.strip()}\n\n"
        "Source SQL:\n"
        f"{source_sql.strip()}\n\n"
        "Task: produce exactly one semantically equivalent rewritten PostgreSQL SQL query."
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    prompt_payload = {
        "prompt_template_id": PROMPT_TEMPLATE_ID,
        "messages": messages,
    }
    prompt_payload["prompt_sha256"] = _sha256_text(
        json.dumps(prompt_payload, sort_keys=True, separators=(",", ":"))
    )
    return prompt_payload


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


def _candidate_text_from_rule_labeled_response(raw_response: str) -> str:
    match = LABELED_SQL_PATTERN.search(raw_response)
    if not match:
        return ""
    candidate = match.group("sql").strip()
    if "\nrule" in candidate.lower():
        candidate = re.split(r"\n\s*rules?\s*:", candidate, maxsplit=1, flags=re.IGNORECASE)[0].strip()
    return candidate


def extract_sql_candidate(raw_response: str) -> ExtractionResult:
    if not raw_response.strip():
        return ExtractionResult("response_empty", "", "response_empty", "runtime response was empty")

    blocks: list[str] = []
    for match in FENCED_BLOCK_PATTERN.finditer(raw_response):
        lang = match.group("lang").strip().lower()
        body = match.group("body").strip()
        ok, _reason = _looks_like_single_sql_statement(body)
        if ok and lang in {"", "sql"}:
            blocks.append(body)

    if len(blocks) > 1:
        return ExtractionResult(
            "multiple_sql_blocks_ambiguous",
            "",
            "multiple_sql_statements",
            "multiple SQL code blocks were present",
        )
    if len(blocks) == 1:
        return ExtractionResult(
            "extracted",
            _strip_one_trailing_semicolon(blocks[0]) + ";\n",
            "none",
            "extracted one fenced SQL block",
        )
    if "```" in raw_response:
        return ExtractionResult(
            "ambiguous_markdown",
            "",
            "ambiguous_markdown",
            "markdown/code fence did not contain exactly one SQL statement",
        )

    labeled_candidate = _candidate_text_from_rule_labeled_response(raw_response)
    if labeled_candidate:
        ok, reason = _looks_like_single_sql_statement(labeled_candidate)
        if ok:
            return ExtractionResult(
                "extracted",
                _strip_one_trailing_semicolon(labeled_candidate) + ";\n",
                "none",
                "extracted SQL from labeled rule-sequence response",
            )
        return ExtractionResult("sql_extraction_failed", "", reason, reason)

    ok, reason = _looks_like_single_sql_statement(raw_response)
    if not ok:
        return ExtractionResult("sql_extraction_failed", "", reason, reason)
    return ExtractionResult(
        "extracted",
        _strip_one_trailing_semicolon(raw_response) + ";\n",
        "none",
        "extracted one raw SQL statement",
    )


def _rule_sequence_from_value(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            return [part.strip() for part in re.split(r"[,>\n]", stripped) if part.strip()]
        return _rule_sequence_from_value(parsed)
    return [str(value)]


def _fake_response_text() -> RuntimeResult:
    inline_rules = _rule_sequence_from_value(os.environ.get("SQLRB_LLM_R2_FAKE_RULE_SEQUENCE"))
    if "SQLRB_LLM_R2_FAKE_SQL" in os.environ:
        return RuntimeResult(
            status="fake_runtime_ok",
            raw_output=os.environ.get("SQLRB_LLM_R2_FAKE_SQL", ""),
            failure_bucket="none",
            reason="using inline fake SQL",
            fake_runtime=True,
            live_call=False,
            rule_system_runtime_used=False,
            checkpoint_used=False,
            demonstration_selector_used=False,
            rule_sequence=inline_rules,
        )

    raw = os.environ.get("SQLRB_LLM_R2_FAKE_RESPONSE", "")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return RuntimeResult(
            status="fake_runtime_malformed_json",
            raw_output="",
            failure_bucket="malformed_json",
            reason="SQLRB_LLM_R2_FAKE_RESPONSE was not valid JSON",
            fake_runtime=True,
            live_call=False,
            rule_system_runtime_used=False,
            checkpoint_used=False,
            demonstration_selector_used=False,
            rule_sequence=inline_rules,
        )
    if not isinstance(payload, dict):
        return RuntimeResult(
            status="fake_runtime_malformed_json",
            raw_output="",
            failure_bucket="malformed_json",
            reason="fake response JSON must be an object",
            fake_runtime=True,
            live_call=False,
            rule_system_runtime_used=False,
            checkpoint_used=False,
            demonstration_selector_used=False,
            rule_sequence=inline_rules,
        )
    status = str(payload.get("status", "ok")).lower()
    rules = _rule_sequence_from_value(payload.get("rule_sequence") or payload.get("rules")) or inline_rules
    if status in {"unsupported", "not_supported"}:
        return RuntimeResult(
            status="fake_runtime_unsupported",
            raw_output="",
            failure_bucket="unsupported",
            reason="fake runtime returned unsupported status",
            fake_runtime=True,
            live_call=False,
            rule_system_runtime_used=False,
            checkpoint_used=False,
            demonstration_selector_used=False,
            rule_sequence=rules,
        )
    if status not in {"ok", "success", "true"}:
        return RuntimeResult(
            status="fake_runtime_failed",
            raw_output="",
            failure_bucket="runtime_failed",
            reason=f"fake runtime returned status={status}",
            fake_runtime=True,
            live_call=False,
            rule_system_runtime_used=False,
            checkpoint_used=False,
            demonstration_selector_used=False,
            rule_sequence=rules,
        )
    for key in ["candidate_sql", "rewritten_sql", "output_sql", "sql", "content"]:
        value = payload.get(key)
        if isinstance(value, str):
            return RuntimeResult(
                status="fake_runtime_ok",
                raw_output=value,
                failure_bucket="none",
                reason=f"fake runtime returned {key}",
                fake_runtime=True,
                live_call=False,
                rule_system_runtime_used=False,
                checkpoint_used=False,
                demonstration_selector_used=False,
                rule_sequence=rules,
            )
    return RuntimeResult(
        status="fake_runtime_empty",
        raw_output="",
        failure_bucket="response_empty",
        reason="fake response had no candidate SQL field",
        fake_runtime=True,
        live_call=False,
        rule_system_runtime_used=False,
        checkpoint_used=False,
        demonstration_selector_used=False,
        rule_sequence=rules,
    )


def _call_openai_compatible(prompt: dict[str, Any], provider: ProviderConfig) -> dict[str, Any]:
    url = provider.base_url.rstrip("/") + "/chat/completions"
    body = {
        "model": provider.model_id,
        "messages": prompt["messages"],
        "temperature": provider.temperature,
        "top_p": provider.top_p,
        "max_tokens": provider.max_tokens,
    }
    headers = {"Content-Type": "application/json", "User-Agent": DEFAULT_USER_AGENT}
    if provider.auth_header == "x-api-key":
        headers["x-api-key"] = provider.api_key
    else:
        headers["Authorization"] = f"Bearer {provider.api_key}"
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=provider.timeout_seconds) as response:
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


def _live_provider_response(
    *,
    provider: ProviderConfig,
    prompt: dict[str, Any] | None,
    workspace: Path,
) -> RuntimeResult:
    if prompt is None:
        return RuntimeResult(
            status="missing_prompt",
            raw_output="",
            failure_bucket="missing_prompt",
            reason="live mode requires a prompt payload",
            fake_runtime=False,
            live_call=False,
            rule_system_runtime_used=False,
            checkpoint_used=False,
            demonstration_selector_used=False,
            rule_sequence=[],
        )
    try:
        response = _call_openai_compatible(prompt, provider)
    except json.JSONDecodeError as exc:
        return RuntimeResult(
            status="malformed_response",
            raw_output="",
            failure_bucket="malformed_response",
            reason=f"provider response was not valid JSON: {exc}",
            fake_runtime=False,
            live_call=True,
            rule_system_runtime_used=False,
            checkpoint_used=False,
            demonstration_selector_used=False,
            rule_sequence=[],
            prompt_sha256=str(prompt.get("prompt_sha256", "")),
        )
    except AdapterError as exc:
        message = str(exc)
        bucket = "timeout" if "timed out" in message.lower() else "provider_error"
        return RuntimeResult(
            status="provider_error",
            raw_output="",
            failure_bucket=bucket,
            reason=message,
            fake_runtime=False,
            live_call=True,
            rule_system_runtime_used=False,
            checkpoint_used=False,
            demonstration_selector_used=False,
            rule_sequence=[],
            prompt_sha256=str(prompt.get("prompt_sha256", "")),
        )

    if not isinstance(response, dict):
        return RuntimeResult(
            status="malformed_response",
            raw_output="",
            failure_bucket="malformed_response",
            reason="provider response JSON was not an object",
            fake_runtime=False,
            live_call=True,
            rule_system_runtime_used=False,
            checkpoint_used=False,
            demonstration_selector_used=False,
            rule_sequence=[],
            prompt_sha256=str(prompt.get("prompt_sha256", "")),
        )

    raw_response_path = ""
    raw_response_saved = False
    if provider.save_raw_response:
        workspace.mkdir(parents=True, exist_ok=True)
        raw_path = workspace / "llm_r2_raw_response.json"
        raw_path.write_text(json.dumps(response, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raw_response_path = str(raw_path)
        raw_response_saved = True

    usage = response.get("usage") if isinstance(response.get("usage"), dict) else None
    return RuntimeResult(
        status="live_provider_success",
        raw_output=_response_content(response),
        failure_bucket="none",
        reason="provider returned a chat completion response",
        fake_runtime=False,
        live_call=True,
        rule_system_runtime_used=False,
        checkpoint_used=False,
        demonstration_selector_used=False,
        rule_sequence=[],
        token_usage=usage,
        prompt_sha256=str(prompt.get("prompt_sha256", "")),
        raw_response_saved=raw_response_saved,
        raw_response_path=raw_response_path,
    )


def run_runtime(
    config: RuntimeConfig,
    provider: ProviderConfig,
    *,
    prompt: dict[str, Any] | None = None,
    workspace: Path | None = None,
) -> RuntimeResult:
    if config.rule_system_required and not config.rule_system_configured:
        return RuntimeResult(
            "rule_system_runtime_unavailable",
            "",
            "rule_system_runtime_unavailable",
            "rule-system runtime was required but SQLRB_LLM_R2_RULE_SYSTEM_CMD was not configured",
            False,
            False,
            False,
            False,
            False,
            [],
        )
    if config.checkpoint_required and not config.checkpoint_configured:
        return RuntimeResult(
            "checkpoint_unavailable",
            "",
            "checkpoint_unavailable",
            "checkpoint was required but SQLRB_LLM_R2_CHECKPOINT_PATH was not configured",
            False,
            False,
            False,
            False,
            False,
            [],
        )
    if config.demonstration_selector_required and not config.demonstration_selector_configured:
        return RuntimeResult(
            "demonstration_selector_unavailable",
            "",
            "demonstration_selector_unavailable",
            "demonstration selector was required but SQLRB_LLM_R2_DEMO_SELECTOR_PATH was not configured",
            False,
            False,
            False,
            False,
            False,
            [],
        )
    if config.mode == "fake":
        if not (config.fake_response_configured or config.fake_sql_configured):
            return RuntimeResult(
                "fake_runtime_unconfigured",
                "",
                "runtime_unconfigured",
                "fake mode requires SQLRB_LLM_R2_FAKE_RESPONSE or SQLRB_LLM_R2_FAKE_SQL",
                True,
                False,
                False,
                False,
                False,
                [],
            )
        return _fake_response_text()
    if config.mode in {"live", "gpt54", "openai_compatible"}:
        if not provider.allow_live:
            return RuntimeResult(
                "live_gate_missing",
                "",
                "live_gate_missing",
                "live mode requires SQLRB_LLM_ALLOW_LIVE=1",
                False,
                False,
                False,
                False,
                False,
                [],
            )
        if not provider.api_key_present:
            return RuntimeResult(
                "missing_api_key",
                "",
                "missing_api_key",
                "live mode requires SQLRB_LLM_API_KEY or GPTSAPI_API_KEY",
                False,
                False,
                False,
                False,
                False,
                [],
            )
        if provider.provider != PROVIDER_POLICY or not provider.base_url_host or not provider.model_id:
            return RuntimeResult(
                "provider_policy_incomplete",
                "",
                "provider_policy_incomplete",
                "live mode requires openai_compatible provider, base URL, and model",
                False,
                False,
                False,
                False,
                False,
                [],
            )
        return _live_provider_response(
            provider=provider,
            prompt=prompt,
            workspace=workspace or Path.cwd(),
        )
    return RuntimeResult(
        "runtime_unconfigured",
        "",
        "runtime_unconfigured",
        "set SQLRB_LLM_R2_MODE=fake or live; official rule-system/checkpoint/demo paths remain disabled",
        False,
        False,
        False,
        False,
        False,
        [],
    )


def _safe_metadata(
    *,
    env: dict[str, str],
    provider: ProviderConfig,
    runtime_config: RuntimeConfig,
    schema_status: str,
    schema_ref: str,
    schema_artifact: str,
    source_sql: str,
    runtime: RuntimeResult,
    extraction: ExtractionResult | None,
    candidate_generated: bool,
    fail_closed_reason: str,
) -> dict[str, Any]:
    source_path = Path(env["SQLRB_SOURCE_SQL_PATH"])
    source_hash = _sha256_file(source_path) if source_path.is_file() else _sha256_text(source_sql)
    rule_sequence = runtime.rule_sequence
    return {
        "schema_version": "llm_r2_gpt54_adapter_status_v0",
        "created_at": _utc_now_iso(),
        "route_id": ROUTE_ID,
        "method_id": METHOD_ID,
        "baseline_family": BASELINE_FAMILY,
        "adapter_version": ADAPTER_VERSION,
        "prompt_template_id": PROMPT_TEMPLATE_ID,
        "run_id": env["SQLRB_RUN_ID"],
        "case_id": env["SQLRB_CASE_ID"],
        "pool": env["SQLRB_POOL"],
        "target_engine": env["SQLRB_ENGINE"],
        "provider_policy": PROVIDER_POLICY,
        "model_policy": MODEL_POLICY,
        "provider": provider.provider,
        "model": provider.model_id,
        "model_id": provider.model_id,
        "provider_config": {
            "provider": provider.provider,
            "base_url_host": provider.base_url_host,
            "base_url_env_used": provider.base_url_env_used,
            "api_key_present": provider.api_key_present,
            "api_key_env_used": provider.api_key_env_used,
            "model_id": provider.model_id,
            "model_env_used": provider.model_env_used,
            "temperature": provider.temperature,
            "top_p": provider.top_p,
            "max_tokens": provider.max_tokens,
            "allow_live": provider.allow_live,
            "auth_header": provider.auth_header,
            "save_raw_response": provider.save_raw_response,
            "timeout_seconds": provider.timeout_seconds,
        },
        "adapted_gpt54_local_diagnostic": True,
        "original_paper_reproduction": False,
        "official_llm_r2_stack": False,
        "fake_runtime": runtime.fake_runtime,
        "runtime_mode": runtime_config.mode or "unconfigured",
        "live_call": runtime.live_call,
        "rule_system_runtime_used": runtime.rule_system_runtime_used,
        "checkpoint_used": runtime.checkpoint_used,
        "demonstration_selector_used": runtime.demonstration_selector_used,
        "rule_system_required": runtime_config.rule_system_required,
        "rule_system_configured": runtime_config.rule_system_configured,
        "checkpoint_required": runtime_config.checkpoint_required,
        "checkpoint_configured": runtime_config.checkpoint_configured,
        "demonstration_selector_required": runtime_config.demonstration_selector_required,
        "demonstration_selector_configured": runtime_config.demonstration_selector_configured,
        "rule_sequence_present": bool(rule_sequence),
        "rule_sequence": rule_sequence,
        "source_sql_path": str(source_path),
        "source_sql_sha256": source_hash,
        "schema_status": schema_status,
        "schema_ref": schema_ref,
        "schema_artifact": schema_artifact,
        "schema_context_required": True,
        "extraction_policy": EXTRACTION_POLICY_ID,
        "runtime_status": runtime.status,
        "provider_status": runtime.status,
        "call_status": runtime.status,
        "prompt_sha256": runtime.prompt_sha256,
        "token_usage": runtime.token_usage,
        "raw_response_saved": runtime.raw_response_saved,
        "raw_response_path": runtime.raw_response_path,
        "extraction_status": extraction.status if extraction else "not_attempted",
        "candidate_generated": candidate_generated,
        "fail_closed_reason": fail_closed_reason,
        "failure_bucket": "none" if candidate_generated else fail_closed_reason,
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result_input": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
        "no_secret_values": True,
    }


def write_status(workspace: Path, metadata: dict[str, Any]) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "llm_r2_status.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        env = load_env()
        provider = resolve_provider_config()
        runtime_config = resolve_runtime_config()
        workspace = Path(env["SQLRB_WORKSPACE_DIR"])
        candidate_path = Path(env["SQLRB_CANDIDATE_SQL_PATH"])
        source_path = Path(env["SQLRB_SOURCE_SQL_PATH"])
        source_sql = source_path.read_text(encoding="utf-8") if source_path.is_file() else ""
        schema_status, schema_ref, schema_artifact = resolve_schema_context(env)

        runtime = RuntimeResult(
            "not_attempted",
            "",
            "not_attempted",
            "runtime not attempted",
            False,
            False,
            False,
            False,
            False,
            [],
        )
        extraction: ExtractionResult | None = None
        candidate_generated = False
        fail_closed_reason = ""

        if args.dry_run_status:
            fail_closed_reason = "dry_run_status_only"
        elif not source_sql.strip():
            fail_closed_reason = "missing_source_sql"
        elif env["SQLRB_ENGINE"] not in KNOWN_ENGINES:
            fail_closed_reason = "unsupported_engine"
        elif env["SQLRB_ENGINE"] not in SUPPORTED_FAKE_ENGINES:
            fail_closed_reason = "unsupported_engine"
        elif schema_status == "schema_context_unavailable":
            fail_closed_reason = "missing_schema_context"
        else:
            prompt = None
            if runtime_config.mode in {"live", "gpt54", "openai_compatible"}:
                schema_text = load_schema_text(schema_artifact)
                prompt = build_prompt(
                    env=env,
                    provider=provider,
                    source_sql=source_sql,
                    schema_text=schema_text,
                    schema_ref=schema_ref,
                )
            runtime = run_runtime(runtime_config, provider, prompt=prompt, workspace=workspace)
            if runtime.failure_bucket != "none":
                fail_closed_reason = runtime.failure_bucket
            else:
                extraction = extract_sql_candidate(runtime.raw_output)
                if extraction.failure_bucket != "none":
                    fail_closed_reason = extraction.failure_bucket
                else:
                    candidate_path.parent.mkdir(parents=True, exist_ok=True)
                    candidate_path.write_text(extraction.sql, encoding="utf-8")
                    candidate_generated = True
                    fail_closed_reason = "none"

        metadata = _safe_metadata(
            env=env,
            provider=provider,
            runtime_config=runtime_config,
            schema_status=schema_status,
            schema_ref=schema_ref,
            schema_artifact=schema_artifact,
            source_sql=source_sql,
            runtime=runtime,
            extraction=extraction,
            candidate_generated=candidate_generated,
            fail_closed_reason=fail_closed_reason,
        )
        write_status(workspace, metadata)
        return 0
    except AdapterError as exc:
        workspace_raw = os.environ.get("SQLRB_WORKSPACE_DIR")
        if workspace_raw:
            workspace = Path(workspace_raw)
            metadata = {
                "schema_version": "llm_r2_gpt54_adapter_status_v0",
                "created_at": _utc_now_iso(),
                "route_id": ROUTE_ID,
                "method_id": METHOD_ID,
                "adapter_version": ADAPTER_VERSION,
                "candidate_generated": False,
                "failure_bucket": "adapter_configuration_error",
                "fail_closed_reason": "adapter_configuration_error",
                "adapter_error": str(exc),
                "provider_policy": PROVIDER_POLICY,
                "model_policy": MODEL_POLICY,
                "adapted_gpt54_local_diagnostic": True,
                "original_paper_reproduction": False,
                "official_llm_r2_stack": False,
                "fake_runtime": False,
                "live_call": False,
                "rule_system_runtime_used": False,
                "checkpoint_used": False,
                "demonstration_selector_used": False,
                "rule_sequence_present": False,
                "local_diagnostic_only": True,
                "official_metric_input": False,
                "paper_result_input": False,
                "retained_evidence_promoted": False,
                "leaderboard_input": False,
                "no_secret_values": True,
            }
            write_status(workspace, metadata)
            return 0
        print(f"llm_r2 adapter configuration error: {exc}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
