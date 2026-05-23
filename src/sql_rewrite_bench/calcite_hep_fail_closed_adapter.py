#!/usr/bin/env python3
"""Fail-closed Calcite HEP adapter scaffold for user-entry local runs.

The adapter follows the public ``sql_rewrite_bench.user_run`` environment
contract and writes a per-row status artifact into the provided workspace. It
does not vendor, invoke, or assume an Apache Calcite runtime. Until a bounded
Calcite HEP backend is separately authorized, this route emits no candidate SQL
and therefore remains a fail-closed local diagnostic route.
"""

from __future__ import annotations

import json
import os
import shutil
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
]


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
        "calcite_command_configured": bool(command),
        "calcite_jar": _path_status(jar),
        "calcite_root": _path_status(root),
    }


def _preflight_status(discovery: dict[str, object]) -> tuple[str, str]:
    jar = discovery["calcite_jar"]
    root = discovery["calcite_root"]
    command_configured = bool(discovery["calcite_command_configured"])
    java_found = bool(discovery["java_found"])
    jar_exists = bool(jar["exists"])
    root_exists = bool(root["exists"])

    if command_configured or (java_found and jar_exists):
        return (
            "calcite_backend_not_implemented",
            "Calcite runtime discovery found a possible backend, but this scaffold "
            "does not yet implement an authorized HEP invocation contract.",
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


def build_status_payload(env: dict[str, str]) -> dict[str, object]:
    source_path = Path(env["SQLRB_SOURCE_SQL_PATH"])
    discovery = discover_calcite_runtime()
    preflight_status, unsupported_reason = _preflight_status(discovery)
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
        "source_sql_path": env["SQLRB_SOURCE_SQL_PATH"],
        "source_sql_exists": source_path.exists(),
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
    (workspace / "calcite_hep_status.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
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
