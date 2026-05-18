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
import os
import sys
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

MISSING_SQLGLOT_MESSAGE = (
    "SQLGlot is not installed. Install optional SQLGlot support before using this adapter."
)


class AdapterError(Exception):
    """Expected adapter failure reported as a clean nonzero exit."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate candidate SQL with optional SQLGlot non-DB routes."
    )
    parser.add_argument(
        "--route",
        required=True,
        choices=["noop", "optimize"],
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


def generate_candidate(source_sql: str, *, route: str, dialect: str) -> str:
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

    raise AdapterError(f"unsupported SQLGlot route: {route}")


def run(route: str) -> int:
    env = load_env()
    source_path = Path(env["SQLRB_SOURCE_SQL_PATH"])
    if not source_path.exists():
        raise AdapterError(f"source SQL path does not exist: {source_path}")
    if not source_path.is_file():
        raise AdapterError(f"source SQL path is not a file: {source_path}")

    dialect = dialect_for_engine(env["SQLRB_ENGINE"])
    source_sql = source_path.read_text(encoding="utf-8")
    candidate_sql = generate_candidate(source_sql, route=route, dialect=dialect)

    candidate_path = Path(env["SQLRB_CANDIDATE_SQL_PATH"])
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(candidate_sql, encoding="utf-8")
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
