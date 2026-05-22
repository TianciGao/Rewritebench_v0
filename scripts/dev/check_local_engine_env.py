#!/usr/bin/env python3
"""Report local SQL-RewriteBench engine environment readiness.

This helper is diagnostic-only. It writes no files, does not run benchmark
cases, does not run checkers, and does not compute metrics, timing, reports,
results, or leaderboard data.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from sql_rewrite_bench.spark_execution import inspect_spark_environment  # noqa: E402

POSTGRES_DSN_ENV = "SQLRB_POSTGRES_DSN"
POSTGRES_LIBPQ_REQUIRED = ("PGHOST", "PGPORT", "PGDATABASE", "PGUSER")
POSTGRES_LIBPQ_OPTIONAL = ("PGPASSWORD",)

MYSQL_REQUIRED = ("SQLRB_MYSQL_HOST", "SQLRB_MYSQL_PORT", "SQLRB_MYSQL_USER")
MYSQL_OPTIONAL = ("SQLRB_MYSQL_PASSWORD",)
SECRET_ENV_NAMES = (
    "SQLRB_POSTGRES_DSN",
    "PGPASSWORD",
    "SQLRB_MYSQL_PASSWORD",
    "MYSQL_PWD",
)


def _is_set(name: str, env: Mapping[str, str]) -> bool:
    return bool(env.get(name))


def _set_unset(name: str, env: Mapping[str, str]) -> str:
    return "set" if _is_set(name, env) else "unset"


def _which(name: str) -> str | None:
    return shutil.which(name)


def _redact(text: str, env: Mapping[str, str] | None) -> str:
    if not env:
        return text
    redacted = text
    for name in SECRET_ENV_NAMES:
        value = env.get(name)
        if value:
            redacted = redacted.replace(value, "<redacted>")
    return redacted


def _run(command: Sequence[str], *, env: Mapping[str, str] | None = None) -> tuple[str, str]:
    try:
        completed = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=8,
            check=False,
            env=dict(env) if env is not None else None,
        )
    except subprocess.TimeoutExpired:
        return "timeout", "command timed out after 8 seconds"

    if completed.returncode == 0:
        first_line = (completed.stdout or "").strip().splitlines()
        detail = first_line[0] if first_line else "command succeeded"
        return "ok", _redact(detail, env)
    detail = (completed.stderr or completed.stdout or "").strip().splitlines()
    message = detail[0] if detail else f"exit code {completed.returncode}"
    return "failed", _redact(message, env)


def _postgres_config_source(env: Mapping[str, str]) -> tuple[bool, str]:
    if _is_set(POSTGRES_DSN_ENV, env):
        return True, f"{POSTGRES_DSN_ENV}=set"
    missing = [name for name in POSTGRES_LIBPQ_REQUIRED if not _is_set(name, env)]
    if not missing:
        optional = " ".join(f"{name}={_set_unset(name, env)}" for name in POSTGRES_LIBPQ_OPTIONAL)
        return True, "libpq vars present (" + optional + ")"
    return False, "missing libpq vars: " + ", ".join(missing)


def _postgres_command(env: Mapping[str, str]) -> list[str]:
    command = ["psql"]
    dsn = env.get(POSTGRES_DSN_ENV)
    if dsn:
        command.append(dsn)
    command.extend(["-X", "-v", "ON_ERROR_STOP=1", "-q", "-t", "-A", "-c", "SELECT version();"])
    return command


def _mysql_config_source(env: Mapping[str, str]) -> tuple[bool, str]:
    missing = [name for name in MYSQL_REQUIRED if not _is_set(name, env)]
    optional = " ".join(f"{name}=set" if _is_set(name, env) else f"{name}=unset" for name in MYSQL_OPTIONAL)
    if not missing:
        return True, "required SQLRB_MYSQL_* vars present (" + optional + ")"
    return False, "missing vars: " + ", ".join(missing) + " (" + optional + ")"


def _mysql_command(env: Mapping[str, str]) -> list[str]:
    return [
        "mysql",
        "--batch",
        "--raw",
        "--quick",
        "--column-names",
        "--connect-timeout=5",
        "--protocol=TCP",
        "--host",
        env["SQLRB_MYSQL_HOST"],
        "--port",
        env["SQLRB_MYSQL_PORT"],
        "--user",
        env["SQLRB_MYSQL_USER"],
        "-e",
        "SELECT VERSION();",
    ]


def _mysql_env(env: Mapping[str, str]) -> dict[str, str]:
    child_env = dict(env)
    password = child_env.get("SQLRB_MYSQL_PASSWORD")
    if password:
        child_env["MYSQL_PWD"] = password
    return child_env


def _print_postgres(env: Mapping[str, str]) -> None:
    print("PostgreSQL")
    psql_path = _which("psql")
    print(f"  psql CLI: {'found at ' + psql_path if psql_path else 'not found'}")
    config_present, config_detail = _postgres_config_source(env)
    print(f"  config: {'present' if config_present else 'missing'} ({config_detail})")
    if not psql_path:
        print("  probe: skipped because psql is not available")
    elif not config_present:
        print("  probe: skipped because PostgreSQL config is missing")
    else:
        status, detail = _run(_postgres_command(env), env=env)
        print(f"  probe SELECT version(): {status} ({detail})")


def _print_mysql(env: Mapping[str, str]) -> None:
    print("MySQL")
    mysql_path = _which("mysql")
    print(f"  mysql CLI: {'found at ' + mysql_path if mysql_path else 'not found'}")
    config_present, config_detail = _mysql_config_source(env)
    print(f"  config: {'present' if config_present else 'missing'} ({config_detail})")
    if not mysql_path:
        print("  probe: skipped because mysql is not available")
    elif not config_present:
        print("  probe: skipped because SQLRB_MYSQL_* config is missing")
    else:
        status, detail = _run(_mysql_command(env), env=_mysql_env(env))
        print(f"  probe SELECT VERSION(): {status} ({detail})")


def _print_spark(env: Mapping[str, str]) -> None:
    print("Spark")
    status = inspect_spark_environment(env)
    print(f"  spark-sql CLI: {'found at ' + status.spark_sql_path if status.spark_sql_path else 'not found'}")
    print(f"  SPARK_LOCAL_IP: {_set_unset('SPARK_LOCAL_IP', env)}")
    print(f"  SPARK_HOME: {_set_unset('SPARK_HOME', env)}")
    print(f"  PYSPARK_PYTHON: {_set_unset('PYSPARK_PYTHON', env)}")
    print(f"  SQLRB_SPARK_MASTER: {_set_unset('SQLRB_SPARK_MASTER', env)}")
    print(f"  pyspark import: {'available' if status.pyspark_importable else 'unavailable'}")
    if status.pyspark_importable:
        print("  backend status: live local diagnostic backend available through PySpark")
        print("  probe: skipped; no Spark session is started by this environment checker")
    else:
        print(f"  backend status: fail-closed until PySpark is available ({status.failure_class})")
        print("  probe: skipped")


def main() -> int:
    env = os.environ
    print("SQL-RewriteBench local engine environment check")
    print("Passwords and DSN values are not printed.")
    _print_postgres(env)
    _print_mysql(env)
    _print_spark(env)
    print("Result: diagnostic report complete")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - protects script error semantics
        print(f"Script error: {exc}", file=sys.stderr)
        raise SystemExit(2)
