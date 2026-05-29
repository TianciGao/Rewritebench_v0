#!/usr/bin/env python3
"""Run the bounded schema-aware SQLGlot optimize execution/checker smoke.

This helper is audit-scoped. It writes runtime artifacts under /tmp and audit
summary files under this audit packet. It does not collect timing, run
verifiers, compute official metrics, or touch paper/report/result surfaces.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
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
    CHECKER_STATUS_SUCCESS,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_MISMATCH,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    FAILURE_NONE,
)


TASK_ID = "sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0"
RUN_ID = TASK_ID
ROUTE_ID = "sqlglot_optimize_schema_aware"
METHOD_ID = "sqlglot"
CASES = ["CONS_0005", "PERF_0006", "CONS_0036"]
ENGINES = ["postgres", "mysql", "spark"]
RUNTIME_ROOT = Path(f"/tmp/sqlrb_{TASK_ID}")
INVALID_QUALIFICATIONS = ['"table1"."table2"."i"', "`table1`.`table2`.`i`"]


FIELDS = [
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "candidate_generated",
    "preflight_passed",
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
    "source_sql_path",
    "candidate_sql_path",
    "schema_context_status",
    "schema_ddl_path",
    "schema_context_tables",
    "invalid_cons0005_qualification_present",
    "mysql_array_any_warning",
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

    rows: list[dict[str, str]] = []
    ledger_rows: list[dict[str, object]] = []
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
            db_schema_prefix="sqlrb_schema_aware",
        )
        ledger_rows.append(ledger)
        rows.append(_row_summary(repo_root, row, ledger, adapter_result.workspace_dir))

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


def _row_summary(
    repo_root: Path,
    row,
    ledger: dict[str, object],
    workspace_dir: Path,
) -> dict[str, str]:
    candidate_path_text = str(ledger.get("candidate_sql_path", ""))
    candidate_path = Path(candidate_path_text) if candidate_path_text else None
    if candidate_path and not candidate_path.is_absolute():
        candidate_path = repo_root / candidate_path
    candidate_sql = candidate_path.read_text(encoding="utf-8") if candidate_path and candidate_path.exists() else ""
    status_path = workspace_dir / "sqlglot_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {}
    adapter_stderr_path = workspace_dir / "adapter_stderr.txt"
    adapter_stderr = adapter_stderr_path.read_text(encoding="utf-8") if adapter_stderr_path.exists() else ""
    source_status = str(ledger.get("source_execution_status", ""))
    candidate_status = str(ledger.get("candidate_execution_status", ""))
    checker_status = str(ledger.get("checker_status", ""))
    exact_status = str(ledger.get("exact_status", ""))
    failure_bucket = str(ledger.get("failure_bucket", ""))
    notes = " ".join(str(ledger.get("notes", "")).split())
    if adapter_stderr.strip():
        notes = f"{notes}; adapter_stderr={adapter_stderr.strip()}"

    return {
        "case_id": row.case_id,
        "pool": row.pool,
        "engine": row.engine,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "candidate_generated": _bool(ledger.get("candidate_generated") == "true"),
        "preflight_passed": _bool(ledger.get("candidate_preflight_status") == CANDIDATE_PREFLIGHT_STATUS_PASSED),
        "source_executable": _bool(source_status == EXECUTION_STATUS_SOURCE_SUCCESS),
        "candidate_executable": _bool(candidate_status == EXECUTION_STATUS_CANDIDATE_SUCCESS),
        "checker_attempted": _bool(
            checker_status not in {"", CHECKER_STATUS_NOT_ENABLED, CHECKER_STATUS_NON_DB}
        ),
        "exact_result_consistent": _bool(exact_status == EXACT_STATUS_EXACT),
        "mismatch": _bool(exact_status == EXACT_STATUS_MISMATCH or failure_bucket == "mismatch"),
        "source_execution_failed": _bool(source_status != EXECUTION_STATUS_SOURCE_SUCCESS),
        "candidate_execution_failed": _bool(
            source_status == EXECUTION_STATUS_SOURCE_SUCCESS
            and candidate_status != EXECUTION_STATUS_CANDIDATE_SUCCESS
        ),
        "failure_bucket": failure_bucket,
        "error_summary": notes[:500],
        "candidate_sql_sha256": hashlib.sha256(candidate_sql.encode("utf-8")).hexdigest() if candidate_sql else "",
        "source_sql_path": str((repo_root / row.source_sql_path).resolve()),
        "candidate_sql_path": str(candidate_path) if candidate_path else "",
        "schema_context_status": "available" if status.get("schema_ddl_path") else "unavailable",
        "schema_ddl_path": str(status.get("schema_ddl_path", "")),
        "schema_context_tables": ";".join(status.get("schema_context_tables", [])),
        "invalid_cons0005_qualification_present": _bool(any(token in candidate_sql for token in INVALID_QUALIFICATIONS)),
        "mysql_array_any_warning": _bool("ARRAY_ANY is unsupported" in adapter_stderr),
        "checker_status": checker_status,
        "exact_status": exact_status,
        "source_execution_status": source_status,
        "candidate_execution_status": candidate_status,
        "mismatch_artifact_path": str(ledger.get("mismatch_artifact_path", "")),
        "db_artifact_dir": str(ledger.get("db_artifact_dir", "")),
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
    return {
        "task": TASK_ID,
        "route_id": ROUTE_ID,
        "method_id": METHOD_ID,
        "planned_rows": 9,
        "generated_candidate_rows": _count_true(rows, "candidate_generated"),
        "preflight_passed_rows": _count_true(rows, "preflight_passed"),
        "source_executable_rows": _count_true(rows, "source_executable"),
        "candidate_executable_rows": _count_true(rows, "candidate_executable"),
        "checker_attempted_rows": _count_true(rows, "checker_attempted"),
        "exact_rows": _count_true(rows, "exact_result_consistent"),
        "mismatch_rows": _count_true(rows, "mismatch"),
        "source_execution_failed_rows": _count_true(rows, "source_execution_failed"),
        "candidate_execution_failed_rows": _count_true(rows, "candidate_execution_failed"),
        "invalid_cons0005_qualification_rows": _count_true(rows, "invalid_cons0005_qualification_present"),
        "mysql_array_any_warning_rows": _count_true(rows, "mysql_array_any_warning"),
        "failure_buckets": dict(Counter(row["failure_bucket"] for row in rows)),
        "by_engine": by_engine,
        "by_case": by_case,
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
