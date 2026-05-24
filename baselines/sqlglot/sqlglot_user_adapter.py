#!/usr/bin/env python3
"""Optional SQLGlot adapter for the non-DB user-entry runner.

The adapter reads source SQL from the environment supplied by
``sql_rewrite_bench.user_run`` and writes candidate SQL to
``SQLRB_CANDIDATE_SQL_PATH``. It does not execute SQL, run checkers, collect
timing, compute official metrics, update retained evidence, or create
leaderboard output.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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

DIALECT_BY_ENGINE = {
    "postgres": "postgres",
    "mysql": "mysql",
    "spark": "spark",
}

ROUTE_IDS = {
    "noop": "sqlglot_noop",
    "optimize": "sqlglot_optimize",
    "optimize_schema_aware": "sqlglot_optimize_schema_aware",
}

METHOD_ID = "sqlglot"
BASELINE_FAMILY = "sqlglot"

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

DDL_TYPE_STOP_KEYWORDS = {
    "check",
    "collate",
    "constraint",
    "default",
    "generated",
    "not",
    "null",
    "primary",
    "references",
    "unique",
}

MISSING_SQLGLOT_MESSAGE = (
    "SQLGlot is not installed. Install optional SQLGlot support before using this adapter."
)
MYSQL_UNSUPPORTED_ARRAY_ANY_BUCKET = "mysql_unsupported_array_any"
MYSQL_UNSUPPORTED_LAMBDA_BUCKET = "sqlglot_unsupported_mysql_lambda"


class AdapterError(Exception):
    """Expected adapter failure reported as a clean nonzero exit."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate candidate SQL with optional SQLGlot non-DB routes."
    )
    parser.add_argument(
        "--route",
        required=True,
        choices=sorted(ROUTE_IDS),
        help="SQLGlot candidate-generation route to run.",
    )
    return parser.parse_args(argv)


def load_env() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV_VARS if not os.environ.get(name)]
    if missing:
        raise AdapterError("missing required environment variables: " + ", ".join(missing))
    return {name: os.environ[name] for name in REQUIRED_ENV_VARS}


def load_sqlglot() -> Any:
    try:
        import sqlglot
    except ImportError as exc:
        raise AdapterError(MISSING_SQLGLOT_MESSAGE) from exc
    return sqlglot


def dialect_for_engine(engine: str) -> str:
    try:
        return DIALECT_BY_ENGINE[engine]
    except KeyError as exc:
        raise AdapterError(f"unsupported SQLRB_ENGINE for SQLGlot adapter: {engine}") from exc


def ensure_candidate_sql(sql: str) -> str:
    cleaned = sql.strip()
    if not cleaned:
        raise AdapterError("SQLGlot emitted empty candidate SQL")
    if not cleaned.endswith(";"):
        cleaned += ";"
    return cleaned + "\n"


def unsupported_mysql_schema_aware_output_bucket(
    *, route: str, dialect: str, candidate_sql: str
) -> str | None:
    """Return the fail-closed bucket for known MySQL-unsupported optimize output."""

    if route != "optimize_schema_aware" or dialect != "mysql":
        return None
    if re.search(r"\bARRAY_ANY\s*\(", candidate_sql, re.IGNORECASE):
        return MYSQL_UNSUPPORTED_ARRAY_ANY_BUCKET
    if re.search(r"(?:`_[A-Za-z][A-Za-z0-9_]*`|_[A-Za-z][A-Za-z0-9_]*)\s*->", candidate_sql):
        return MYSQL_UNSUPPORTED_LAMBDA_BUCKET
    return None


def _unsupported_mysql_output_reason(bucket: str) -> str:
    if bucket == MYSQL_UNSUPPORTED_ARRAY_ANY_BUCKET:
        return (
            "SQLGlot emitted ARRAY_ANY / lambda-style SQL that is unsupported "
            "by the MySQL route."
        )
    return "SQLGlot emitted lambda-style SQL that is unsupported by the MySQL route."


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _repo_root() -> Path:
    return Path.cwd().resolve()


def _simple_yaml_mapping(path: Path) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("-") or ":" not in stripped:
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
            continue
        parent[key] = value.strip("'\"")
    return root


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception:
        return _simple_yaml_mapping(path)

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AdapterError(f"YAML root must be a mapping: {path}")
    return data


def _resolve_path(raw: str, *, base: Path) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path.resolve()
    return (base / path).resolve()


def _engine_asset_from_profile(profile_path: Path, engine_dir: str) -> Path | None:
    try:
        profile = _load_yaml_mapping(profile_path)
    except Exception:
        return None
    engines = profile.get("engines")
    if not isinstance(engines, dict):
        return None
    engine_config = engines.get(engine_dir)
    if not isinstance(engine_config, dict):
        return None
    raw = engine_config.get("ddl")
    if not isinstance(raw, str) or not raw.strip():
        return None
    return _resolve_path(raw.strip(), base=_repo_root())


def _schema_profile_candidates(profile_path: Path, engine_dir: str) -> list[Path]:
    candidates: list[Path] = []
    if profile_path.exists():
        engine_asset = _engine_asset_from_profile(profile_path, engine_dir)
        if engine_asset is not None:
            candidates.append(engine_asset)
        candidates.append((profile_path.parent / engine_dir / "ddl.sql").resolve())
    return candidates


def resolve_schema_ddl_path(env: dict[str, str]) -> Path | None:
    """Resolve the selected case's per-engine DDL for schema-aware optimize."""

    case_dir = _resolve_path(env["SQLRB_CASE_DIR"], base=_repo_root())
    engine_dir = ENGINE_SCHEMA_DIR.get(env["SQLRB_ENGINE"], env["SQLRB_ENGINE"])
    engine_suffix = ENGINE_SCHEMA_SUFFIX.get(env["SQLRB_ENGINE"], env["SQLRB_ENGINE"])
    candidates: list[Path] = [
        case_dir / "schema" / f"ddl_{engine_suffix}.sql",
        case_dir / "schema" / engine_dir / "ddl.sql",
    ]

    case_profile = case_dir / "schema" / "schema_profile.yaml"
    candidates.extend(_schema_profile_candidates(case_profile, engine_dir))

    for profile_path in [case_profile, case_dir / "manifest.yaml"]:
        if not profile_path.exists():
            continue
        try:
            profile = _load_yaml_mapping(profile_path)
        except Exception:
            continue
        for raw in _external_profile_references(profile):
            if raw.startswith("schemas/"):
                candidates.extend(_schema_profile_candidates(_resolve_path(raw, base=_repo_root()), engine_dir))

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def _external_profile_references(mapping: dict[str, Any]) -> list[str]:
    references: list[str] = []
    for key in ["external_schema_profile", "external_profile", "profile"]:
        value = mapping.get(key)
        if isinstance(value, str) and value.strip():
            references.append(value.strip())
    schema = mapping.get("schema")
    if isinstance(schema, dict):
        value = schema.get("external_profile")
        if isinstance(value, str) and value.strip():
            references.append(value.strip())
    external_resolution = mapping.get("external_schema_resolution")
    if isinstance(external_resolution, dict):
        value = external_resolution.get("profile")
        if isinstance(value, str) and value.strip():
            references.append(value.strip())
    return references


def _identifier_token_parts(token: str) -> tuple[str, bool]:
    stripped = token.strip()
    if stripped.startswith('"') and stripped.endswith('"') and len(stripped) >= 2:
        return stripped[1:-1].replace('""', '"'), True
    if stripped.startswith("`") and stripped.endswith("`") and len(stripped) >= 2:
        return stripped[1:-1].replace("``", "`"), True
    if stripped.startswith("[") and stripped.endswith("]") and len(stripped) >= 2:
        return stripped[1:-1], True
    return stripped, False


def _split_top_level_csv(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    index = 0
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if quote is not None:
            if char == quote:
                if next_char == quote:
                    index += 2
                    continue
                quote = None
            index += 1
            continue
        if char in {"'", '"', "`"}:
            quote = char
            index += 1
            continue
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


def _table_name_from_token(token: str) -> str:
    last_part = token.split(".")[-1].strip()
    name, _quoted = _identifier_token_parts(last_part)
    return name


def _column_type_from_definition(rest: str) -> str:
    tokens = rest.strip().split()
    if not tokens:
        return "UNKNOWN"
    type_tokens: list[str] = []
    for token in tokens:
        normalized = token.rstrip(",").lower()
        if normalized in DDL_TYPE_STOP_KEYWORDS:
            break
        type_tokens.append(token.rstrip(","))
    if not type_tokens:
        return "UNKNOWN"
    return " ".join(type_tokens)


def schema_context_from_ddl(schema_ddl_path: Path) -> dict[str, dict[str, str]]:
    """Build the simple table/column type mapping SQLGlot optimize expects."""

    text = schema_ddl_path.read_text(encoding="utf-8")
    schema: dict[str, dict[str, str]] = {}
    table_pattern = re.compile(
        r"\bCREATE\s+(?:TEMPORARY\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?"
        r"(?P<table>(?:\"(?:[^\"]|\"\")+\"|`[^`]+`|\[[^\]]+\]|[A-Za-z_][A-Za-z0-9_$]*)(?:\s*\.\s*(?:\"(?:[^\"]|\"\")+\"|`[^`]+`|\[[^\]]+\]|[A-Za-z_][A-Za-z0-9_$]*))?)"
        r"\s*\((?P<body>.*?)\)\s*(?:USING\s+[A-Za-z_][A-Za-z0-9_]*)?\s*;",
        re.IGNORECASE | re.DOTALL,
    )
    column_pattern = re.compile(
        r'^\s*("[^"]+"|`[^`]+`|\[[^\]]+\]|[A-Za-z_][A-Za-z0-9_$]*)\s+(?P<rest>.+)$',
        re.DOTALL,
    )

    for match in table_pattern.finditer(text):
        table_name = _table_name_from_token(match.group("table"))
        if not table_name:
            continue
        columns: dict[str, str] = {}
        for column_def in _split_top_level_csv(match.group("body")):
            token_match = column_pattern.match(column_def)
            if not token_match:
                continue
            column_name, _quoted = _identifier_token_parts(token_match.group(1))
            if not column_name or column_name.lower() in DDL_CONSTRAINT_KEYWORDS:
                continue
            columns[column_name] = _column_type_from_definition(token_match.group("rest"))
        if columns:
            schema[table_name] = columns

    if not schema:
        raise AdapterError(f"sqlglot_schema_parse_failed: no CREATE TABLE columns found in {schema_ddl_path}")
    return schema


def generate_candidate(
    source_sql: str,
    *,
    route: str,
    dialect: str,
    schema_context: dict[str, dict[str, str]] | None = None,
) -> str:
    sqlglot = load_sqlglot()
    try:
        expression = sqlglot.parse_one(source_sql, read=dialect)
    except Exception as exc:
        raise AdapterError(f"SQLGlot parse failed: {exc}") from exc

    if route == "noop":
        try:
            return ensure_candidate_sql(expression.sql(dialect=dialect))
        except Exception as exc:
            raise AdapterError(f"SQLGlot no-op emit failed: {exc}") from exc

    if route == "optimize":
        try:
            from sqlglot.optimizer import optimize

            optimized = optimize(expression)
            return ensure_candidate_sql(optimized.sql(dialect=dialect))
        except Exception as exc:
            raise AdapterError(f"SQLGlot optimize failed: {exc}") from exc

    if route == "optimize_schema_aware":
        if not schema_context:
            raise AdapterError("schema_context_unavailable: schema-aware optimize requires per-engine DDL")
        try:
            from sqlglot.optimizer import optimize

            optimized = optimize(expression, schema=schema_context, dialect=dialect)
            return ensure_candidate_sql(optimized.sql(dialect=dialect))
        except Exception as exc:
            raise AdapterError(f"sqlglot_optimize_failed: {exc}") from exc

    raise AdapterError(f"unsupported SQLGlot route: {route}")


def _base_status_payload(
    *,
    env: dict[str, str],
    route: str,
    dialect: str,
    schema_ddl_path: Path | None,
    schema_context: dict[str, dict[str, str]] | None,
) -> dict[str, Any]:
    return {
        "schema_version": "sqlglot_adapter_status_v0",
        "created_at_utc": _utc_now_iso(),
        "method_id": METHOD_ID,
        "route_id": ROUTE_IDS.get(route, f"sqlglot_{route}"),
        "baseline_family": BASELINE_FAMILY,
        "route": route,
        "optimizer_mode": "schema_aware" if route == "optimize_schema_aware" else route,
        "run_id": env["SQLRB_RUN_ID"],
        "case_id": env["SQLRB_CASE_ID"],
        "pool": env["SQLRB_POOL"],
        "engine": env["SQLRB_ENGINE"],
        "dialect": dialect,
        "source_sql_path": env["SQLRB_SOURCE_SQL_PATH"],
        "case_dir": env["SQLRB_CASE_DIR"],
        "candidate_sql_path": env["SQLRB_CANDIDATE_SQL_PATH"],
        "schema_ddl_path": str(schema_ddl_path) if schema_ddl_path else "",
        "schema_context_tables": sorted(schema_context or {}),
        "candidate_generated": False,
        "preflight_status": "not_attempted",
        "failure_bucket": "",
        "unsupported_reason": "",
        "local_diagnostic_only": True,
        "official_metric_input": False,
        "paper_result_input": False,
        "retained_evidence_promoted": False,
        "leaderboard_input": False,
    }


def _failure_bucket_for_error(message: str) -> str:
    if message.startswith("schema_context_unavailable"):
        return "schema_context_unavailable"
    if message.startswith("sqlglot_schema_parse_failed"):
        return "sqlglot_schema_parse_failed"
    if message.startswith("sqlglot_optimize_failed"):
        return "sqlglot_optimize_failed"
    if message.startswith("SQLGlot parse failed"):
        return "sqlglot_parse_failed"
    return "candidate_generation_failed"


def _write_status(workspace: Path, payload: dict[str, Any]) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "sqlglot_status.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run(route: str) -> int:
    env = load_env()
    workspace = Path(env["SQLRB_WORKSPACE_DIR"])
    source_path = Path(env["SQLRB_SOURCE_SQL_PATH"])
    if not source_path.exists():
        raise AdapterError(f"source SQL path does not exist: {source_path}")
    if not source_path.is_file():
        raise AdapterError(f"source SQL path is not a file: {source_path}")

    dialect = dialect_for_engine(env["SQLRB_ENGINE"])
    source_sql = source_path.read_text(encoding="utf-8")
    schema_ddl_path: Path | None = None
    schema_context: dict[str, dict[str, str]] | None = None
    if route == "optimize_schema_aware":
        schema_ddl_path = resolve_schema_ddl_path(env)
        if schema_ddl_path is None:
            payload = _base_status_payload(
                env=env,
                route=route,
                dialect=dialect,
                schema_ddl_path=None,
                schema_context=None,
            )
            payload["preflight_status"] = "schema_context_unavailable"
            payload["failure_bucket"] = "schema_context_unavailable"
            payload["unsupported_reason"] = "No per-engine schema DDL path could be resolved."
            _write_status(workspace, payload)
            raise AdapterError("schema_context_unavailable: no per-engine schema DDL path could be resolved")
        try:
            schema_context = schema_context_from_ddl(schema_ddl_path)
        except AdapterError as exc:
            payload = _base_status_payload(
                env=env,
                route=route,
                dialect=dialect,
                schema_ddl_path=schema_ddl_path,
                schema_context=None,
            )
            payload["preflight_status"] = "schema_context_unavailable"
            payload["failure_bucket"] = "sqlglot_schema_parse_failed"
            payload["unsupported_reason"] = str(exc)
            _write_status(workspace, payload)
            raise

    payload = _base_status_payload(
        env=env,
        route=route,
        dialect=dialect,
        schema_ddl_path=schema_ddl_path,
        schema_context=schema_context,
    )
    try:
        candidate_sql = generate_candidate(
            source_sql,
            route=route,
            dialect=dialect,
            schema_context=schema_context,
        )
    except AdapterError as exc:
        message = str(exc)
        payload["preflight_status"] = "candidate_generation_failed"
        payload["failure_bucket"] = _failure_bucket_for_error(message)
        payload["unsupported_reason"] = message
        _write_status(workspace, payload)
        raise

    unsupported_bucket = unsupported_mysql_schema_aware_output_bucket(
        route=route,
        dialect=dialect,
        candidate_sql=candidate_sql,
    )
    if unsupported_bucket is not None:
        workspace.mkdir(parents=True, exist_ok=True)
        unsupported_candidate_path = workspace / "unsupported_candidate.sql"
        unsupported_candidate_path.write_text(candidate_sql, encoding="utf-8")
        payload["candidate_generated"] = False
        payload["preflight_status"] = unsupported_bucket
        payload["failure_bucket"] = unsupported_bucket
        payload["unsupported_reason"] = _unsupported_mysql_output_reason(unsupported_bucket)
        payload["unsupported_candidate_sql_path"] = str(unsupported_candidate_path)
        payload["sqlglot_warning"] = (
            "ARRAY_ANY is unsupported"
            if unsupported_bucket == MYSQL_UNSUPPORTED_ARRAY_ANY_BUCKET
            else ""
        )
        _write_status(workspace, payload)
        print(f"warning: {payload['unsupported_reason']}", file=sys.stderr)
        return 0

    candidate_path = Path(env["SQLRB_CANDIDATE_SQL_PATH"])
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(candidate_sql, encoding="utf-8")
    payload["candidate_generated"] = True
    payload["preflight_status"] = "candidate_generated"
    payload["failure_bucket"] = "none"
    _write_status(workspace, payload)
    print(
        f"sqlglot_{route} candidate written for "
        f"{env['SQLRB_CASE_ID']} on {env['SQLRB_ENGINE']}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run(args.route)
    except AdapterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
