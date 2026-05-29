#!/usr/bin/env python3
"""Run the bounded MySQL ARRAY_ANY fail-closed smoke.

This helper is audit-scoped. Runtime artifacts go under /tmp. It does not
collect timing, run verifiers, compute official metrics, or update paper
surfaces.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from sql_rewrite_bench.adapter_runner import run_adapter_for_case
from sql_rewrite_bench.case_package_resolver import resolve_case_package
from sql_rewrite_bench.case_selection import resolve_common_core_selection
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


TASK_ID = "sqlglot_optimize_schema_aware_mysql_array_any_fail_closed_v0"
RUN_ID = TASK_ID
ROUTE_ID = "sqlglot_optimize_schema_aware"
METHOD_ID = "sqlglot"
RUNTIME_ROOT = Path(f"/tmp/sqlrb_{TASK_ID}")
ROWS = [
    ("CONS_0005", "mysql", "target_mysql_array_any_blocker"),
    ("CONS_0005", "postgres", "postgres_control"),
    ("CONS_0005", "spark", "spark_semantic_mismatch_control"),
    ("PERF_0006", "mysql", "mysql_non_array_any_control"),
]

BEFORE = {
    ("CONS_0005", "mysql"): {
        "before_status": "candidate_execution_failed",
        "before_failure_bucket": "candidate_execution_failed",
        "before_exact_status": "not_exact_due_to_execution_failure",
    },
    ("CONS_0005", "postgres"): {
        "before_status": "exact",
        "before_failure_bucket": "none",
        "before_exact_status": "exact",
    },
    ("CONS_0005", "spark"): {
        "before_status": "mismatch",
        "before_failure_bucket": "mismatch",
        "before_exact_status": "mismatch",
    },
    ("PERF_0006", "mysql"): {
        "before_status": "exact",
        "before_failure_bucket": "none",
        "before_exact_status": "exact",
    },
}

FIELDS = [
    "case_id",
    "pool",
    "engine",
    "control_role",
    "method_id",
    "route_id",
    "before_status",
    "before_failure_bucket",
    "before_exact_status",
    "after_candidate_generated",
    "after_extraction_status",
    "after_candidate_preflight_status",
    "after_source_execution_status",
    "after_candidate_execution_status",
    "after_checker_status",
    "after_exact_status",
    "after_failure_bucket",
    "sqlglot_status_failure_bucket",
    "sqlglot_status_preflight_status",
    "db_execution_reached",
    "candidate_sql_path",
    "unsupported_candidate_sql_path",
    "notes",
    "local_only",
    "official_metric_input",
    "paper_result",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    audit_dir = Path(__file__).resolve().parent
    runtime_run_dir = RUNTIME_ROOT / "runtime" / RUN_ID
    runtime_run_dir.mkdir(parents=True, exist_ok=True)

    selected = []
    case_list = RUNTIME_ROOT / "case_ids.txt"
    case_list.write_text("CONS_0005\nPERF_0006\n", encoding="utf-8")
    wanted = {(case_id, engine): role for case_id, engine, role in ROWS}
    for engine in sorted({engine for _case_id, engine, _role in ROWS}):
        selected.extend(
            resolve_common_core_selection(
                repo_root=repo_root,
                case_set="common_core_v0",
                pool="all",
                engine=engine,
                case_list=case_list,
                smoke=False,
            )
        )
    selected = [row for row in selected if (row.case_id, row.engine) in wanted]
    selected.sort(
        key=lambda row: ROWS.index((row.case_id, row.engine, wanted[(row.case_id, row.engine)]))
    )
    if len(selected) != len(ROWS):
        raise RuntimeError(f"expected {len(ROWS)} selected rows, got {len(selected)}")

    adapter = repo_root / "baselines" / "sqlglot" / "sqlglot_user_adapter.py"
    adapter_command = f"{sys.executable} {adapter} --route optimize_schema_aware"
    output_rows: list[dict[str, str]] = []

    for row in selected:
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
            db_schema_prefix="sqlrb_schema_aware_array_any",
        )
        output_rows.append(_row_summary(row, ledger, adapter_result.workspace_dir, wanted))

    _write_csv(audit_dir / "before_after_status.csv", output_rows)
    summary = {
        "task": TASK_ID,
        "route_id": ROUTE_ID,
        "method_id": METHOD_ID,
        "smoke_rows": len(output_rows),
        "target_mysql_array_any_fail_closed": any(
            row["case_id"] == "CONS_0005"
            and row["engine"] == "mysql"
            and row["sqlglot_status_failure_bucket"] == "mysql_unsupported_array_any"
            and row["db_execution_reached"] == "false"
            for row in output_rows
        ),
        "postgres_cons0005_exact": any(
            row["case_id"] == "CONS_0005"
            and row["engine"] == "postgres"
            and row["after_exact_status"] == EXACT_STATUS_EXACT
            for row in output_rows
        ),
        "spark_cons0005_remains_mismatch": any(
            row["case_id"] == "CONS_0005"
            and row["engine"] == "spark"
            and row["after_exact_status"] == EXACT_STATUS_MISMATCH
            for row in output_rows
        ),
        "mysql_perf0006_exact": any(
            row["case_id"] == "PERF_0006"
            and row["engine"] == "mysql"
            and row["after_exact_status"] == EXACT_STATUS_EXACT
            for row in output_rows
        ),
        "official_metric_input": False,
        "paper_result": False,
    }
    (audit_dir / "diagnostic_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


def _row_summary(row, ledger: dict[str, object], workspace_dir: Path, wanted) -> dict[str, str]:
    status_path = workspace_dir / "sqlglot_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {}
    source_status = str(ledger.get("source_execution_status", ""))
    candidate_status = str(ledger.get("candidate_execution_status", ""))
    checker_status = str(ledger.get("checker_status", ""))
    candidate_generated = str(ledger.get("candidate_generated", "")) == "true"
    preflight_passed = ledger.get("candidate_preflight_status") == CANDIDATE_PREFLIGHT_STATUS_PASSED
    db_execution_reached = candidate_generated and preflight_passed
    if candidate_status == EXECUTION_STATUS_NOT_ENABLED:
        db_execution_reached = False
    before = BEFORE[(row.case_id, row.engine)]
    return {
        "case_id": row.case_id,
        "pool": row.pool,
        "engine": row.engine,
        "control_role": wanted[(row.case_id, row.engine)],
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "before_status": before["before_status"],
        "before_failure_bucket": before["before_failure_bucket"],
        "before_exact_status": before["before_exact_status"],
        "after_candidate_generated": _bool(candidate_generated),
        "after_extraction_status": str(ledger.get("extraction_status", "")),
        "after_candidate_preflight_status": str(ledger.get("candidate_preflight_status", "")),
        "after_source_execution_status": source_status,
        "after_candidate_execution_status": candidate_status,
        "after_checker_status": checker_status,
        "after_exact_status": str(ledger.get("exact_status", "")),
        "after_failure_bucket": str(ledger.get("failure_bucket", "")),
        "sqlglot_status_failure_bucket": str(status.get("failure_bucket", "")),
        "sqlglot_status_preflight_status": str(status.get("preflight_status", "")),
        "db_execution_reached": _bool(db_execution_reached),
        "candidate_sql_path": str(ledger.get("candidate_sql_path", "")),
        "unsupported_candidate_sql_path": str(status.get("unsupported_candidate_sql_path", "")),
        "notes": _notes(ledger, status, source_status, candidate_status, checker_status),
        "local_only": "true",
        "official_metric_input": "false",
        "paper_result": "false",
    }


def _notes(
    ledger: dict[str, object],
    status: dict[str, object],
    source_status: str,
    candidate_status: str,
    checker_status: str,
) -> str:
    parts = [" ".join(str(ledger.get("notes", "")).split())]
    if status.get("unsupported_reason"):
        parts.append(str(status["unsupported_reason"]))
    if source_status == EXECUTION_STATUS_SOURCE_SUCCESS:
        parts.append("source execution reached")
    if candidate_status == EXECUTION_STATUS_CANDIDATE_SUCCESS:
        parts.append("candidate execution reached")
    if checker_status not in {"", CHECKER_STATUS_NOT_ENABLED, CHECKER_STATUS_NON_DB}:
        parts.append("checker reached")
    return "; ".join(part for part in parts if part)


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
