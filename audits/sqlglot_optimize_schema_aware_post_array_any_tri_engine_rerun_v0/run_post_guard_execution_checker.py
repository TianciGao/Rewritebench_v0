#!/usr/bin/env python3
"""Run post-ARRAY_ANY-guard schema-aware SQLGlot bounded checker smoke.

This helper is audit-scoped. Runtime artifacts go under /tmp and committed
outputs go only under this audit packet. It does not collect timing, run
verifiers, compute official metrics, or update paper surfaces.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from sql_rewrite_bench.adapter_runner import run_adapter_for_case
from sql_rewrite_bench.case_package_resolver import resolve_case_package
from sql_rewrite_bench.case_selection import resolve_common_core_selection
from sql_rewrite_bench.mysql_execution import execute_mysql_source_reference
from sql_rewrite_bench.user_ledger import ledger_from_adapter_result
from sql_rewrite_bench.user_run import _apply_candidate_preflight_for_row, _apply_db_checker_for_row
from sql_rewrite_bench.user_run_schema import (
    CANDIDATE_PREFLIGHT_STATUS_PASSED,
    CHECKER_STATUS_NOT_ENABLED,
    CHECKER_STATUS_NON_DB,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_MISMATCH,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    FAILURE_NONE,
)


TASK_ID = "sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0"
RUN_ID = TASK_ID
ROUTE_ID = "sqlglot_optimize_schema_aware"
METHOD_ID = "sqlglot"
CASES = ["CONS_0005", "PERF_0006", "CONS_0036"]
ENGINES = ["postgres", "mysql", "spark"]
RUNTIME_ROOT = Path(f"/tmp/sqlrb_{TASK_ID}")
FAIL_CLOSED_BUCKETS = {"mysql_unsupported_array_any", "sqlglot_unsupported_mysql_lambda"}

PRE_GUARD = {
    "planned_rows": 9,
    "generated_candidate_rows": 9,
    "preflight_passed_rows": 9,
    "fail_closed_rows": 0,
    "source_executable_rows": 9,
    "candidate_executable_rows": 8,
    "checker_attempted_rows": 8,
    "exact_rows": 6,
    "mismatch_rows": 2,
    "source_execution_failed_rows": 0,
    "candidate_execution_failed_rows": 1,
}

FIELDS = [
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "candidate_generated",
    "preflight_passed",
    "fail_closed",
    "fail_closed_bucket",
    "source_executable",
    "candidate_executable",
    "checker_attempted",
    "exact_result_consistent",
    "mismatch",
    "source_execution_failed",
    "candidate_execution_failed",
    "failure_bucket",
    "error_summary",
    "candidate_sql_sha256",
    "unsupported_candidate_sql_sha256",
    "source_sql_path",
    "candidate_sql_path",
    "unsupported_candidate_sql_path",
    "schema_context_status",
    "schema_ddl_path",
    "schema_context_tables",
    "checker_status",
    "exact_status",
    "source_execution_status",
    "candidate_execution_status",
    "mismatch_artifact_path",
    "db_artifact_dir",
    "local_only",
    "official_metric_input",
    "paper_result",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    audit_dir = Path(__file__).resolve().parent
    runtime_run_dir = RUNTIME_ROOT / "runtime" / RUN_ID
    runtime_run_dir.mkdir(parents=True, exist_ok=True)
    case_list = RUNTIME_ROOT / "case_ids.txt"
    case_list.write_text("\n".join(CASES) + "\n", encoding="utf-8")

    adapter = repo_root / "baselines" / "sqlglot" / "sqlglot_user_adapter.py"
    adapter_command = f"{sys.executable} {adapter} --route optimize_schema_aware"

    selected_rows = []
    for engine in ENGINES:
        selected_rows.extend(
            resolve_common_core_selection(
                repo_root=repo_root,
                case_set="common_core_v0",
                pool="all",
                engine=engine,
                case_list=case_list,
                smoke=False,
            )
        )

    selected_rows = [row for row in selected_rows if row.case_id in CASES]
    selected_rows.sort(key=lambda row: (CASES.index(row.case_id), ENGINES.index(row.engine)))
    if len(selected_rows) != 9:
        raise RuntimeError(f"expected 9 selected rows, got {len(selected_rows)}")

    rows: list[dict[str, str]] = []
    ledger_rows: list[dict[str, object]] = []

    for row in selected_rows:
        resolved = resolve_case_package(repo_root=repo_root, row=row)
        adapter_result = run_adapter_for_case(
            run_id=RUN_ID,
            row=row,
            resolved_package=resolved,
            adapter_command=adapter_command,
            repo_root=repo_root,
            out_dir=runtime_run_dir,
            timeout=120,
        )
        ledger = ledger_from_adapter_result(
            run_id=RUN_ID,
            row=row,
            adapter_result=adapter_result,
            repo_root=repo_root,
        )
        ledger = _apply_candidate_preflight_for_row(
            ledger=ledger,
            row=row,
            resolved_package=resolved,
            repo_root=repo_root,
        )
        status = _read_status(adapter_result.workspace_dir)
        fail_closed_bucket = _fail_closed_bucket(status)
        source_only_result: Any | None = None
        if fail_closed_bucket:
            if row.engine == "mysql":
                source_only_result = execute_mysql_source_reference(
                    repo_root=repo_root,
                    run_id=RUN_ID,
                    row=row,
                    resolved_package=resolved,
                    workspace_dir=adapter_result.workspace_dir,
                    timeout_sec=30,
                    schema_prefix="sqlrb_schema_aware_post_guard",
                )
        else:
            ledger = _apply_db_checker_for_row(
                ledger=ledger,
                run_id=RUN_ID,
                row=row,
                resolved_package=resolved,
                repo_root=repo_root,
                out_dir=runtime_run_dir,
                enable_checker=True,
                postgres_dsn_env="SQLRB_POSTGRES_DSN",
                execution_timeout_sec=30,
                db_schema_prefix="sqlrb_schema_aware_post_guard",
            )
        ledger_rows.append(ledger)
        rows.append(
            _row_summary(
                repo_root=repo_root,
                row=row,
                ledger=ledger,
                workspace_dir=adapter_result.workspace_dir,
                status=status,
                fail_closed_bucket=fail_closed_bucket,
                source_only_result=source_only_result,
            )
        )

    _write_csv(audit_dir / "per_row_execution_checker_status.csv", rows, FIELDS)
    (runtime_run_dir / "ledger_rows.json").write_text(
        json.dumps(ledger_rows, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = _summary(rows)
    (audit_dir / "diagnostic_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


def _read_status(workspace_dir: Path) -> dict[str, Any]:
    status_path = workspace_dir / "sqlglot_status.json"
    if not status_path.exists():
        return {}
    return json.loads(status_path.read_text(encoding="utf-8"))


def _fail_closed_bucket(status: dict[str, Any]) -> str:
    bucket = str(status.get("failure_bucket", ""))
    return bucket if bucket in FAIL_CLOSED_BUCKETS else ""


def _row_summary(
    *,
    repo_root: Path,
    row,
    ledger: dict[str, object],
    workspace_dir: Path,
    status: dict[str, Any],
    fail_closed_bucket: str,
    source_only_result: Any | None,
) -> dict[str, str]:
    candidate_path_text = str(ledger.get("candidate_sql_path", ""))
    candidate_path = Path(candidate_path_text) if candidate_path_text else None
    if candidate_path and not candidate_path.is_absolute():
        candidate_path = repo_root / candidate_path
    candidate_sql = candidate_path.read_text(encoding="utf-8") if candidate_path and candidate_path.exists() else ""
    unsupported_path_text = str(status.get("unsupported_candidate_sql_path", ""))
    unsupported_path = Path(unsupported_path_text) if unsupported_path_text else None
    unsupported_sql = unsupported_path.read_text(encoding="utf-8") if unsupported_path and unsupported_path.exists() else ""

    source_status = str(ledger.get("source_execution_status", ""))
    candidate_status = str(ledger.get("candidate_execution_status", ""))
    db_artifact_dir = str(ledger.get("db_artifact_dir", ""))
    if source_only_result is not None:
        source_status = source_only_result.source_execution_status
        candidate_status = source_only_result.candidate_execution_status
        db_artifact_dir = str(source_only_result.db_artifact_dir)

    checker_status = str(ledger.get("checker_status", ""))
    exact_status = str(ledger.get("exact_status", ""))
    failure_bucket = fail_closed_bucket or str(ledger.get("failure_bucket", ""))
    notes = " ".join(str(ledger.get("notes", "")).split())
    if status.get("unsupported_reason"):
        notes = f"{notes}; {status['unsupported_reason']}".strip("; ")
    if source_only_result is not None:
        notes = f"{notes}; source-only execution: {source_only_result.notes}".strip("; ")

    return {
        "case_id": row.case_id,
        "pool": row.pool,
        "engine": row.engine,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "candidate_generated": _bool(ledger.get("candidate_generated") == "true"),
        "preflight_passed": _bool(ledger.get("candidate_preflight_status") == CANDIDATE_PREFLIGHT_STATUS_PASSED),
        "fail_closed": _bool(bool(fail_closed_bucket)),
        "fail_closed_bucket": fail_closed_bucket,
        "source_executable": _bool(source_status == EXECUTION_STATUS_SOURCE_SUCCESS),
        "candidate_executable": _bool(candidate_status == EXECUTION_STATUS_CANDIDATE_SUCCESS),
        "checker_attempted": _bool(
            checker_status not in {"", CHECKER_STATUS_NOT_ENABLED, CHECKER_STATUS_NON_DB}
        ),
        "exact_result_consistent": _bool(exact_status == EXACT_STATUS_EXACT),
        "mismatch": _bool(exact_status == EXACT_STATUS_MISMATCH or failure_bucket == "mismatch"),
        "source_execution_failed": _bool(
            source_status not in {"", EXECUTION_STATUS_SOURCE_SUCCESS, EXECUTION_STATUS_NOT_ENABLED}
        ),
        "candidate_execution_failed": _bool(
            candidate_status not in {"", EXECUTION_STATUS_CANDIDATE_SUCCESS, EXECUTION_STATUS_NOT_ENABLED}
        ),
        "failure_bucket": failure_bucket,
        "error_summary": notes[:600],
        "candidate_sql_sha256": hashlib.sha256(candidate_sql.encode("utf-8")).hexdigest() if candidate_sql else "",
        "unsupported_candidate_sql_sha256": hashlib.sha256(unsupported_sql.encode("utf-8")).hexdigest() if unsupported_sql else "",
        "source_sql_path": str((repo_root / row.source_sql_path).resolve()),
        "candidate_sql_path": str(candidate_path) if candidate_path else "",
        "unsupported_candidate_sql_path": str(unsupported_path) if unsupported_path else "",
        "schema_context_status": "available" if status.get("schema_ddl_path") else "unavailable",
        "schema_ddl_path": str(status.get("schema_ddl_path", "")),
        "schema_context_tables": ";".join(status.get("schema_context_tables", [])),
        "checker_status": checker_status,
        "exact_status": exact_status,
        "source_execution_status": source_status,
        "candidate_execution_status": candidate_status,
        "mismatch_artifact_path": str(ledger.get("mismatch_artifact_path", "")),
        "db_artifact_dir": db_artifact_dir,
        "local_only": "true",
        "official_metric_input": "false",
        "paper_result": "false",
    }


def _summary(rows: list[dict[str, str]]) -> dict[str, object]:
    by_engine: dict[str, dict[str, int]] = {}
    by_case: dict[str, dict[str, int]] = {}
    for key, values in [("engine", by_engine), ("case_id", by_case)]:
        grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            grouped[row[key]].append(row)
        for value, group in grouped.items():
            values[value] = _counts(group)

    current = _counts(rows)
    comparison = {
        "candidate_execution_failed_before": PRE_GUARD["candidate_execution_failed_rows"],
        "candidate_execution_failed_after": current["candidate_execution_failed_rows"],
        "fail_closed_before": PRE_GUARD["fail_closed_rows"],
        "fail_closed_after": current["fail_closed_rows"],
        "exact_before": PRE_GUARD["exact_rows"],
        "exact_after": current["exact_rows"],
        "mismatch_before": PRE_GUARD["mismatch_rows"],
        "mismatch_after": current["mismatch_rows"],
    }
    return {
        "task": TASK_ID,
        "route_id": ROUTE_ID,
        "method_id": METHOD_ID,
        **current,
        "failure_buckets": dict(Counter(row["failure_bucket"] for row in rows)),
        "by_engine": by_engine,
        "by_case": by_case,
        "pre_guard_comparison": comparison,
        "all_rows_generated_or_fail_closed": current["generated_candidate_rows"] + current["fail_closed_rows"] == 9,
        "cons0005_mysql_fail_closed": any(
            row["case_id"] == "CONS_0005"
            and row["engine"] == "mysql"
            and row["fail_closed_bucket"] in FAIL_CLOSED_BUCKETS
            and row["candidate_execution_status"] == EXECUTION_STATUS_NOT_ENABLED
            for row in rows
        ),
        "postgres_remained_3_of_3_exact": by_engine.get("postgres", {}).get("exact_rows") == 3,
        "mysql_stable_except_cons0005_fail_closed": by_engine.get("mysql", {}).get("exact_rows") == 2
        and by_engine.get("mysql", {}).get("fail_closed_rows") == 1,
        "spark_blockers_remain": by_engine.get("spark", {}).get("mismatch_rows") == 2,
        "timing_collected": False,
        "verifier_run": False,
        "official_metric_input": False,
        "paper_result": False,
    }


def _counts(rows: list[dict[str, str]]) -> dict[str, int]:
    return {
        "planned_rows": len(rows),
        "generated_candidate_rows": _count_true(rows, "candidate_generated"),
        "preflight_passed_rows": _count_true(rows, "preflight_passed"),
        "fail_closed_rows": _count_true(rows, "fail_closed"),
        "source_executable_rows": _count_true(rows, "source_executable"),
        "candidate_executable_rows": _count_true(rows, "candidate_executable"),
        "checker_attempted_rows": _count_true(rows, "checker_attempted"),
        "exact_rows": _count_true(rows, "exact_result_consistent"),
        "mismatch_rows": _count_true(rows, "mismatch"),
        "source_execution_failed_rows": _count_true(rows, "source_execution_failed"),
        "candidate_execution_failed_rows": _count_true(rows, "candidate_execution_failed"),
    }


def _count_true(rows: list[dict[str, str]], field: str) -> int:
    return sum(row[field] == "true" for row in rows)


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
