#!/usr/bin/env python3
"""Fail-closed Calcite HEP baseline adapter for user-entry local runs.

The adapter follows the public ``sql_rewrite_bench.user_run`` environment
contract and writes a per-row status artifact into the provided workspace. It
does not vendor or assume an Apache Calcite runtime. When an external runtime
is configured through environment variables, the adapter invokes it and captures
candidate SQL. Otherwise, it remains a fail-closed local diagnostic route.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROUTE_ID = "calcite_hep_fail_closed"
METHOD_ID = "calcite_hep_fail_closed"
BASELINE_FAMILY = "calcite"
ROUTE_ROLE = "same_engine_rewrite"
ROUTE_POLICY = "fail_closed"

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

DISCOVERY_ENV_VARS = [
    "SQLRB_CALCITE_HEP_CMD",
    "SQLRB_CALCITE_HEP_JAR",
    "SQLRB_CALCITE_HEP_ROOT",
    "SQLRB_CALCITE_HEP_JAVA",
    "SQLRB_CALCITE_HEP_MODE",
    "SQLRB_CALCITE_HEP_TIMEOUT",
]

ENGINE_SCHEMA_DIR = {
    "postgres": "postgres",
    "pg": "postgres",
    "mysql": "mysql",
    "spark": "spark",
}

ENGINE_SCHEMA_SUFFIX = {
    "postgres": "pg",
    "pg": "pg",
    "mysql": "mysql",
    "spark": "spark",
}

DDL_CONSTRAINT_KEYWORDS = {
    "check",
    "constraint",
    "foreign",
    "primary",
    "unique",
}

NON_POSTGRES_DIALECT_GUARDS = {
    "mysql": [
        (
            re.compile(r'"[A-Za-z_][A-Za-z0-9_]*"'),
            "mysql_postgres_dialect_quoted_identifier",
            "Calcite emitted PostgreSQL-style double-quoted identifiers for MySQL.",
        ),
        (
            re.compile(r"\bDOUBLE\s+PRECISION\b", re.IGNORECASE),
            "mysql_postgres_dialect_double_precision",
            "Calcite emitted PostgreSQL DOUBLE PRECISION syntax for MySQL.",
        ),
    ],
    "spark": [
        (
            re.compile(r'"[A-Za-z_][A-Za-z0-9_]*"'),
            "spark_postgres_dialect_quoted_identifier",
            "Calcite emitted PostgreSQL-style double-quoted identifiers for Spark.",
        ),
        (
            re.compile(r"\bDOUBLE\s+PRECISION\b", re.IGNORECASE),
            "spark_postgres_dialect_double_precision",
            "Calcite emitted PostgreSQL DOUBLE PRECISION syntax for Spark.",
        ),
    ],
}


class AdapterError(Exception):
    """Expected adapter configuration error."""


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_env() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV_VARS if not os.environ.get(name)]
    if missing:
        raise AdapterError("missing required environment variables: " + ", ".join(missing))
    return {name: os.environ[name] for name in REQUIRED_ENV_VARS}


def _path_status(value: str) -> dict[str, object]:
    if not value:
        return {"configured": False, "exists": False, "path": ""}
    path = Path(value)
    return {
        "configured": True,
        "exists": path.exists(),
        "path": value,
    }


def _command_status(value: str) -> dict[str, object]:
    if not value:
        return {
            "configured": False,
            "exists": False,
            "command": "",
            "executable": "",
            "resolved_executable": "",
        }
    try:
        command = shlex.split(value)
    except ValueError:
        return {
            "configured": True,
            "exists": False,
            "command": value,
            "executable": "",
            "resolved_executable": "",
        }
    executable = command[0] if command else ""
    resolved = ""
    if executable:
        resolved = executable if Path(executable).is_absolute() else (shutil.which(executable) or "")
    exists = bool(resolved and (Path(resolved).exists() if Path(resolved).is_absolute() else True))
    return {
        "configured": True,
        "exists": exists,
        "command": value,
        "executable": executable,
        "resolved_executable": resolved,
    }


def discover_calcite_runtime() -> dict[str, object]:
    """Return Calcite HEP discovery metadata without invoking external tools."""

    java_value = os.environ.get("SQLRB_CALCITE_HEP_JAVA", "java")
    java_path = java_value if Path(java_value).is_absolute() else shutil.which(java_value)
    command = os.environ.get("SQLRB_CALCITE_HEP_CMD", "")
    jar = os.environ.get("SQLRB_CALCITE_HEP_JAR", "")
    root = os.environ.get("SQLRB_CALCITE_HEP_ROOT", "")
    return {
        "discovery_env_vars": {name: os.environ.get(name, "") for name in DISCOVERY_ENV_VARS},
        "java_command": java_value,
        "java_found": bool(java_path),
        "java_resolved_path": java_path or "",
        "calcite_command": _command_status(command),
        "calcite_command_configured": bool(command),
        "calcite_jar": _path_status(jar),
        "calcite_root": _path_status(root),
    }


def _preflight_status(discovery: dict[str, object]) -> tuple[str, str]:
    jar = discovery["calcite_jar"]
    root = discovery["calcite_root"]
    command = discovery["calcite_command"]
    command_configured = bool(command["configured"])
    command_exists = bool(command["exists"])
    java_found = bool(discovery["java_found"])
    jar_exists = bool(jar["exists"])
    root_exists = bool(root["exists"])

    if command_exists or (java_found and jar_exists):
        return (
            "calcite_runtime_available",
            "External Calcite HEP runtime configuration is available.",
        )
    if not java_found:
        return (
            "calcite_java_missing",
            "Java was not found; Calcite HEP cannot be invoked.",
        )
    if not command_configured and not jar_exists and not root_exists:
        return (
            "calcite_runtime_unavailable",
            "No SQLRB_CALCITE_HEP_CMD, SQLRB_CALCITE_HEP_JAR, or "
            "SQLRB_CALCITE_HEP_ROOT runtime is configured.",
        )
    return (
        "calcite_runtime_incomplete",
        "Calcite HEP runtime configuration is incomplete or points to missing paths.",
    )


def _repo_root() -> Path:
    return Path.cwd().resolve()


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


def _resolve_repo_path(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return (_repo_root() / path).resolve()


def _schema_profile_candidates(profile_path: Path, engine_dir: str) -> list[Path]:
    candidates: list[Path] = []
    raw_engine_asset = _yaml_engine_asset(profile_path, engine_dir)
    if raw_engine_asset:
        candidates.append(_resolve_repo_path(raw_engine_asset))
    if profile_path.exists():
        candidates.append((profile_path.parent / engine_dir / "ddl.sql").resolve())
    return candidates


def resolve_schema_ddl_path(env: dict[str, str]) -> Path | None:
    """Resolve the per-engine DDL path for the external Calcite runtime."""

    case_dir = Path(env["SQLRB_CASE_DIR"]).resolve()
    engine = env["SQLRB_ENGINE"]
    engine_dir = ENGINE_SCHEMA_DIR.get(engine, engine)
    engine_suffix = ENGINE_SCHEMA_SUFFIX.get(engine, engine)

    candidates: list[Path] = [
        case_dir / "schema" / f"ddl_{engine_suffix}.sql",
        case_dir / "schema" / engine_dir / "ddl.sql",
    ]

    case_profile = case_dir / "schema" / "schema_profile.yaml"
    candidates.extend(_schema_profile_candidates(case_profile, engine_dir))

    for key in ["external_schema_profile", "profile"]:
        external_raw = _yaml_scalar(case_profile, key)
        if external_raw.startswith("schemas/"):
            external_profile = _resolve_repo_path(external_raw)
            candidates.extend(_schema_profile_candidates(external_profile, engine_dir))

    manifest = case_dir / "manifest.yaml"
    external_raw = _yaml_scalar(manifest, "external_profile")
    if external_raw.startswith("schemas/"):
        external_profile = _resolve_repo_path(external_raw)
        candidates.extend(_schema_profile_candidates(external_profile, engine_dir))

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def _runtime_command(discovery: dict[str, object]) -> list[str]:
    command = discovery["calcite_command"]
    if command["configured"] and command["exists"]:
        return shlex.split(str(command["command"]))
    jar = discovery["calcite_jar"]
    if discovery["java_found"] and jar["exists"]:
        return [str(discovery["java_command"]), "-jar", str(jar["path"])]
    return []


def _runtime_cwd(discovery: dict[str, object]) -> Path:
    root = discovery["calcite_root"]
    if root["exists"]:
        return Path(str(root["path"])).resolve()
    return _repo_root()


def _runtime_timeout_seconds() -> int:
    raw = os.environ.get("SQLRB_CALCITE_HEP_TIMEOUT", "30").strip()
    try:
        value = int(raw)
    except ValueError:
        return 30
    return max(1, value)


def _runtime_mode() -> str:
    return os.environ.get("SQLRB_CALCITE_HEP_MODE", "real_route_canary").strip() or "real_route_canary"


def _runtime_target_engine(env: dict[str, str]) -> str:
    engine = env["SQLRB_ENGINE"].strip().lower()
    if engine == "pg":
        return "postgres"
    return engine


def _identifier_token_parts(token: str) -> tuple[str, bool]:
    stripped = token.strip()
    if stripped.startswith('"') and stripped.endswith('"') and len(stripped) >= 2:
        return stripped[1:-1].replace('""', '"'), True
    return stripped, False


def _split_top_level_csv(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    in_single = False
    in_double = False
    index = 0
    while index < len(text):
        char = text[index]
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif not in_single and not in_double:
            if char == "(":
                depth += 1
            elif char == ")" and depth > 0:
                depth -= 1
            elif char == "," and depth == 0:
                parts.append(text[start:index].strip())
                start = index + 1
        index += 1
    tail = text[start:].strip()
    if tail:
        parts.append(tail)
    return parts


def _postgres_folded_schema_identifiers(schema_ddl_path: Path) -> set[str]:
    """Return unquoted DDL identifiers that PostgreSQL folds to lowercase."""

    text = schema_ddl_path.read_text(encoding="utf-8")
    identifiers: set[str] = set()
    table_pattern = re.compile(
        r"\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?"
        r"(?P<table>(?:\"(?:[^\"]|\"\")+\"|[A-Za-z_][A-Za-z0-9_$]*)(?:\s*\.\s*(?:\"(?:[^\"]|\"\")+\"|[A-Za-z_][A-Za-z0-9_$]*))?)"
        r"\s*\((?P<body>.*?)\)\s*;",
        re.IGNORECASE | re.DOTALL,
    )
    token_pattern = re.compile(r'^\s*("[^"]+"|[A-Za-z_][A-Za-z0-9_$]*)')
    for match in table_pattern.finditer(text):
        table_token = match.group("table").split(".")[-1].strip()
        table_name, table_quoted = _identifier_token_parts(table_token)
        if not table_quoted and table_name:
            identifiers.add(table_name.lower())
        for column_def in _split_top_level_csv(match.group("body")):
            token_match = token_pattern.match(column_def)
            if not token_match:
                continue
            column_token = token_match.group(1)
            column_name, column_quoted = _identifier_token_parts(column_token)
            if column_quoted or column_name.lower() in DDL_CONSTRAINT_KEYWORDS:
                continue
            identifiers.add(column_name.lower())
    return identifiers


def normalize_postgres_calcite_identifiers(sql: str, schema_ddl_path: Path) -> tuple[str, dict[str, object]]:
    """Unquote/lowercase Calcite identifiers that match unquoted PostgreSQL DDL names.

    This is intentionally narrower than a SQL rewriter: only simple double-quoted
    identifiers whose lowercase form is present in the resolved PostgreSQL DDL
    are normalized. Calcite aliases and computed names not present in DDL remain
    unchanged.
    """

    ddl_identifiers = _postgres_folded_schema_identifiers(schema_ddl_path)
    replacements: dict[str, str] = {}
    replacement_count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal replacement_count
        raw = match.group(1)
        lowered = raw.lower()
        if lowered not in ddl_identifiers:
            return match.group(0)
        replacements[raw] = lowered
        replacement_count += 1
        return lowered

    normalized = re.sub(r'"([A-Za-z_][A-Za-z0-9_]*)"', replace, sql)
    return normalized, {
        "enabled": True,
        "ddl_identifier_count": len(ddl_identifiers),
        "replacement_count": replacement_count,
        "replacement_identifiers": dict(sorted(replacements.items())),
        "policy": "postgres_only_unquoted_ddl_identifier_fold_v0",
    }


def _postprocess_candidate_sql_if_needed(
    *,
    env: dict[str, str],
    schema_ddl_path: Path,
    candidate_path: Path,
) -> dict[str, object]:
    if env["SQLRB_ENGINE"] != "postgres":
        return {"enabled": False, "policy": "postgres_only"}
    original = candidate_path.read_text(encoding="utf-8")
    normalized, metadata = normalize_postgres_calcite_identifiers(original, schema_ddl_path)
    metadata["changed"] = normalized != original
    if normalized != original:
        candidate_path.write_text(normalized, encoding="utf-8")
    return metadata


def detect_non_postgres_target_dialect_block(sql: str, engine: str) -> dict[str, object]:
    """Detect Calcite PostgreSQL-dialect output that should fail closed elsewhere."""

    guards = NON_POSTGRES_DIALECT_GUARDS.get(engine, [])
    for pattern, bucket, reason in guards:
        match = pattern.search(sql)
        if match:
            return {
                "enabled": True,
                "blocked": True,
                "bucket": bucket,
                "reason": reason,
                "matched_text": match.group(0),
                "policy": "non_postgres_postgresql_dialect_fail_closed_v0",
            }
    return {
        "enabled": bool(guards),
        "blocked": False,
        "bucket": "",
        "reason": "",
        "matched_text": "",
        "policy": "non_postgres_postgresql_dialect_fail_closed_v0",
    }


def _fail_closed_for_unsupported_target_dialect_if_needed(
    *,
    env: dict[str, str],
    candidate_path: Path,
) -> dict[str, object]:
    engine = env["SQLRB_ENGINE"]
    if engine == "postgres":
        return {"enabled": False, "blocked": False, "policy": "postgres_supported"}
    if not candidate_path.exists():
        return {
            "enabled": engine in NON_POSTGRES_DIALECT_GUARDS,
            "blocked": False,
            "policy": "candidate_missing",
        }
    sql = candidate_path.read_text(encoding="utf-8")
    guard = detect_non_postgres_target_dialect_block(sql, engine)
    if not guard["blocked"]:
        return guard
    unsupported_path = candidate_path.parent / "unsupported_candidate.sql"
    unsupported_path.write_text(sql, encoding="utf-8")
    candidate_path.unlink()
    guard["unsupported_candidate_sql_path"] = str(unsupported_path)
    return guard


def invoke_calcite_runtime(
    *,
    env: dict[str, str],
    discovery: dict[str, object],
    schema_ddl_path: Path,
) -> dict[str, object]:
    """Invoke the external Calcite runtime and return fail-closed metadata."""

    workspace = Path(env["SQLRB_WORKSPACE_DIR"])
    candidate_path = Path(env["SQLRB_CANDIDATE_SQL_PATH"])
    stdout_path = workspace / "calcite_hep_runtime_stdout.txt"
    stderr_path = workspace / "calcite_hep_runtime_stderr.txt"
    if candidate_path.exists():
        candidate_path.unlink()

    command = _runtime_command(discovery)
    timeout_seconds = _runtime_timeout_seconds()
    target_engine = _runtime_target_engine(env)
    args = command + [
        "--case-id",
        env["SQLRB_CASE_ID"],
        "--source-sql",
        env["SQLRB_SOURCE_SQL_PATH"],
        "--ddl",
        str(schema_ddl_path),
        "--output-sql",
        str(candidate_path),
        "--mode",
        _runtime_mode(),
        "--engine",
        target_engine,
    ]
    command_shape = []
    for piece in args:
        if piece == env["SQLRB_SOURCE_SQL_PATH"]:
            command_shape.append("<source-sql>")
        elif piece == str(schema_ddl_path):
            command_shape.append("<schema-ddl>")
        elif piece == str(candidate_path):
            command_shape.append("<candidate-sql>")
        else:
            command_shape.append(piece)

    try:
        completed = subprocess.run(
            args,
            cwd=_runtime_cwd(discovery),
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text(str(exc.stdout or ""), encoding="utf-8")
        stderr_path.write_text(str(exc.stderr or ""), encoding="utf-8")
        return {
            "preflight_status": "calcite_invocation_timeout",
            "unsupported_reason": f"Calcite HEP invocation timed out after {timeout_seconds} seconds.",
            "candidate_generated": False,
            "failure_bucket": "no_candidate_sql",
            "runtime": {
                "command_shape": command_shape,
                "timeout_seconds": timeout_seconds,
                "exit_code": None,
                "target_engine": target_engine,
                "stdout_path": str(stdout_path),
                "stderr_path": str(stderr_path),
            },
        }

    stdout_path.write_text(completed.stdout or "", encoding="utf-8")
    stderr_path.write_text(completed.stderr or "", encoding="utf-8")
    runtime = {
        "command_shape": command_shape,
        "timeout_seconds": timeout_seconds,
        "exit_code": completed.returncode,
        "target_engine": target_engine,
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
    }
    if completed.returncode != 0:
        return {
            "preflight_status": "calcite_invocation_failed",
            "unsupported_reason": f"Calcite HEP invocation exited nonzero: {completed.returncode}.",
            "candidate_generated": False,
            "failure_bucket": "no_candidate_sql",
            "runtime": runtime,
        }
    if candidate_path.exists() and candidate_path.read_text(encoding="utf-8").strip():
        dialect_guard = _fail_closed_for_unsupported_target_dialect_if_needed(
            env=env,
            candidate_path=candidate_path,
        )
        if dialect_guard.get("blocked"):
            return {
                "preflight_status": "calcite_target_dialect_unsupported",
                "unsupported_reason": str(dialect_guard["reason"]),
                "candidate_generated": False,
                "failure_bucket": "no_candidate_sql",
                "runtime": runtime,
                "target_dialect_guard": dialect_guard,
            }
        postprocess = _postprocess_candidate_sql_if_needed(
            env=env,
            schema_ddl_path=schema_ddl_path,
            candidate_path=candidate_path,
        )
        return {
            "preflight_status": "calcite_invocation_succeeded",
            "unsupported_reason": "",
            "candidate_generated": True,
            "failure_bucket": "none",
            "runtime": runtime,
            "candidate_postprocess": postprocess,
            "target_dialect_guard": dialect_guard,
        }
    return {
        "preflight_status": "calcite_no_candidate_sql",
        "unsupported_reason": "Calcite HEP invocation succeeded but emitted no candidate SQL.",
        "candidate_generated": False,
        "failure_bucket": "no_candidate_sql",
        "runtime": runtime,
    }


def build_status_payload(env: dict[str, str]) -> dict[str, object]:
    source_path = Path(env["SQLRB_SOURCE_SQL_PATH"])
    discovery = discover_calcite_runtime()
    preflight_status, unsupported_reason = _preflight_status(discovery)
    schema_ddl_path = resolve_schema_ddl_path(env)
    return {
        "schema_version": "calcite_hep_fail_closed_adapter_status_v0",
        "created_at_utc": _utc_now_iso(),
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "baseline_family": BASELINE_FAMILY,
        "route_role": ROUTE_ROLE,
        "route_policy": ROUTE_POLICY,
        "run_id": env["SQLRB_RUN_ID"],
        "case_id": env["SQLRB_CASE_ID"],
        "pool": env["SQLRB_POOL"],
        "engine": env["SQLRB_ENGINE"],
        "runtime_target_engine": _runtime_target_engine(env),
        "source_sql_path": env["SQLRB_SOURCE_SQL_PATH"],
        "source_sql_exists": source_path.exists(),
        "schema_ddl_path": str(schema_ddl_path) if schema_ddl_path else "",
        "schema_ddl_exists": bool(schema_ddl_path),
        "candidate_sql_path": env["SQLRB_CANDIDATE_SQL_PATH"],
        "candidate_generated": False,
        "preflight_status": preflight_status,
        "unsupported_reason": unsupported_reason,
        "failure_bucket": "no_candidate_sql",
        "discovery": discovery,
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result_input": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
    }


def run() -> int:
    env = load_env()
    workspace = Path(env["SQLRB_WORKSPACE_DIR"])
    workspace.mkdir(parents=True, exist_ok=True)
    payload = build_status_payload(env)
    if payload["preflight_status"] == "calcite_runtime_available":
        if not payload["schema_ddl_exists"]:
            payload["preflight_status"] = "calcite_schema_unavailable"
            payload["unsupported_reason"] = "No per-engine schema DDL path could be resolved."
        else:
            invocation = invoke_calcite_runtime(
                env=env,
                discovery=payload["discovery"],
                schema_ddl_path=Path(str(payload["schema_ddl_path"])),
            )
            payload.update(invocation)
    (workspace / "calcite_hep_status.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if payload["candidate_generated"]:
        print(f"{ROUTE_ID}: candidate SQL generated via external runtime", file=sys.stderr)
    else:
        print(
            f"{ROUTE_ID} fail-closed: {payload['preflight_status']}; "
            "candidate SQL not generated",
            file=sys.stderr,
        )
    return 0


def main() -> int:
    try:
        return run()
    except AdapterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
