#!/usr/bin/env python3
"""Run SQLGlot schema-aware optimize Track A 120 checker diagnostic.

This helper is audit-scoped. It uses the same user-entry adapter, preflight,
execution, and checker internals, but writes all runtime artifacts under /tmp
instead of repository-level runs/user or output directories.
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
    CHECKER_STATUS_SUCCESS,
    EXACT_STATUS_EXACT,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    FAILURE_NONE,
)


TASK_ID = "sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0"
RUN_ID = TASK_ID
METHOD_ID = "sqlglot"
ROUTE_ID = "sqlglot_optimize_schema_aware"
ENGINES = ("postgres", "mysql", "spark")
RUNTIME_ROOT = Path(f"/tmp/sqlrb_{TASK_ID}")
OUTPUT_ROOT = RUNTIME_ROOT / "output"
RESULT_ROOT = OUTPUT_ROOT / "results" / RUN_ID
LOG_ROOT = OUTPUT_ROOT / "logs" / RUN_ID
REPORT_ROOT = OUTPUT_ROOT / "reports" / RUN_ID
EXECUTION_TIMEOUT_SEC = 30
ADAPTER_TIMEOUT_SEC = 120
DB_SCHEMA_PREFIX = "sqlrb_schema_aware_track_a_120"

FIELDS = [
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "selected",
    "candidate_generated",
    "candidate_sql_sha256",
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
    "schema_context_status",
    "schema_ddl_path",
    "schema_context_tables",
    "candidate_sql_path",
    "unsupported_candidate_sql_sha256",
    "unsupported_candidate_sql_path",
    "source_sql_path",
    "checker_status",
    "exact_status",
    "source_execution_status",
    "candidate_execution_status",
    "mismatch_artifact_path",
    "mismatch_class",
    "label_only_mismatch",
    "semantic_mismatch",
    "local_only",
    "official_metric_input",
    "paper_result",
]

ROUTE_CARD_FIELDS = [
    "method_id",
    "route_id",
    "engine_scope",
    "planned_rows",
    "selected_rows",
    "candidate_generated_rows",
    "fail_closed_rows",
    "source_executable_rows",
    "candidate_executable_rows",
    "checker_attempted_rows",
    "exact_rows",
    "mismatch_rows",
    "source_execution_failed_rows",
    "candidate_execution_failed_rows",
    "no_candidate_rows",
    "unsupported_rows",
    "label_only_mismatch_count",
    "semantic_mismatch_count",
    "official_metric_input",
    "paper_result",
    "leaderboard_output_created",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    audit_dir = Path(__file__).resolve().parent
    for path in [RESULT_ROOT, LOG_ROOT, REPORT_ROOT]:
        path.mkdir(parents=True, exist_ok=True)
    runtime_source_run = RESULT_ROOT / "source_run"
    runtime_source_run.mkdir(parents=True, exist_ok=True)

    adapter = repo_root / "baselines" / "sqlglot" / "sqlglot_user_adapter.py"
    adapter_command = f"{sys.executable} {adapter} --route optimize_schema_aware"

    selected = resolve_common_core_selection(
        repo_root=repo_root,
        case_set="common_core_v0",
        pool="all",
        engine="all",
        case_list=None,
        smoke=False,
    )
    selected.sort(key=lambda row: (row.case_id, ENGINES.index(row.engine)))
    if len(selected) != 120:
        raise RuntimeError(f"expected 120 selected rows, got {len(selected)}")

    raw_ledger_rows: list[dict[str, object]] = []
    rows: list[dict[str, str]] = []
    for index, row in enumerate(selected, start=1):
        print(f"[{index:03d}/120] {row.case_id} / {row.engine}", flush=True)
        resolved = resolve_case_package(repo_root=repo_root, row=row)
        adapter_result = run_adapter_for_case(
            run_id=RUN_ID,
            row=row,
            resolved_package=resolved,
            adapter_command=adapter_command,
            repo_root=repo_root,
            out_dir=runtime_source_run,
            timeout=ADAPTER_TIMEOUT_SEC,
        )
        ledger = ledger_from_adapter_result(
            run_id=RUN_ID,
            row=row,
            adapter_result=adapter_result,
            repo_root=repo_root,
        )
        status = _read_status(adapter_result.workspace_dir)
        fail_closed_bucket = _fail_closed_bucket(status)
        if fail_closed_bucket:
            ledger["failure_bucket"] = fail_closed_bucket
            ledger["notes"] = _append_note(ledger, str(status.get("unsupported_reason", "")))
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
            out_dir=runtime_source_run,
            enable_checker=True,
            postgres_dsn_env="SQLRB_POSTGRES_DSN",
            execution_timeout_sec=EXECUTION_TIMEOUT_SEC,
            db_schema_prefix=DB_SCHEMA_PREFIX,
        )
        source_only_result: Any | None = None
        if fail_closed_bucket and row.engine == "mysql":
            source_only_result = execute_mysql_source_reference(
                repo_root=repo_root,
                run_id=RUN_ID,
                row=row,
                resolved_package=resolved,
                workspace_dir=adapter_result.workspace_dir,
                timeout_sec=EXECUTION_TIMEOUT_SEC,
                schema_prefix=DB_SCHEMA_PREFIX,
            )
            ledger["source_execution_status"] = source_only_result.source_execution_status
            ledger["candidate_execution_status"] = source_only_result.candidate_execution_status
            ledger["source_result_path"] = (
                str(source_only_result.source_result_path)
                if source_only_result.source_result_path
                else ""
            )
            ledger["execution_failure_class"] = source_only_result.execution_failure_class
            ledger["db_artifact_dir"] = str(source_only_result.db_artifact_dir)
            ledger["notes"] = _append_note(
                ledger,
                "source-only execution after fail-closed candidate: "
                + source_only_result.notes,
            )
        if fail_closed_bucket and ledger.get("failure_bucket") in {"no_candidate_sql", "none"}:
            ledger["failure_bucket"] = fail_closed_bucket
        raw_ledger_rows.append(ledger)
        rows.append(
            _row_summary(
                repo_root=repo_root,
                row=row,
                ledger=ledger,
                status=status,
                fail_closed_bucket=fail_closed_bucket,
                source_only_result=source_only_result,
            )
        )

    _write_csv(audit_dir / "per_row_execution_checker_status.csv", rows, FIELDS)
    (RESULT_ROOT / "ledger_rows.json").write_text(
        json.dumps(raw_ledger_rows, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = _summary(rows)
    (audit_dir / "diagnostic_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    route_card = _route_card(summary)
    _write_csv(audit_dir / "route_card.csv", [route_card], ROUTE_CARD_FIELDS)
    (audit_dir / "route_card.json").write_text(
        json.dumps(route_card, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_runtime_manifest(adapter_command, summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


def _append_note(ledger: dict[str, object], note: str) -> str:
    existing = str(ledger.get("notes", ""))
    if not note:
        return existing
    return existing + "; " + note if existing else note


def _read_status(workspace_dir: Path) -> dict[str, Any]:
    status_path = workspace_dir / "sqlglot_status.json"
    if not status_path.exists():
        return {}
    return json.loads(status_path.read_text(encoding="utf-8"))


def _fail_closed_bucket(status: dict[str, Any]) -> str:
    bucket = str(status.get("failure_bucket", ""))
    if bucket in {
        "mysql_unsupported_array_any",
        "sqlglot_unsupported_mysql_lambda",
        "schema_context_unavailable",
        "sqlglot_schema_parse_failed",
        "sqlglot_optimize_failed",
        "sqlglot_parse_failed",
        "candidate_generation_failed",
    }:
        return bucket
    return ""


def _sha256(path_text: str) -> str:
    if not path_text:
        return ""
    path = Path(path_text)
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _is_success(value: object, expected: str) -> bool:
    return str(value) == expected


def _row_summary(
    *,
    repo_root: Path,
    row,
    ledger: dict[str, object],
    status: dict[str, Any],
    fail_closed_bucket: str,
    source_only_result: Any | None,
) -> dict[str, str]:
    candidate_path = str(ledger.get("candidate_sql_path", ""))
    unsupported_path = str(status.get("unsupported_candidate_sql_path", ""))
    mismatch_path = str(ledger.get("mismatch_artifact_path", ""))
    mismatch = _mismatch_class(mismatch_path)
    failure_bucket = str(ledger.get("failure_bucket", ""))
    source_status = str(ledger.get("source_execution_status", ""))
    candidate_status = str(ledger.get("candidate_execution_status", ""))
    if source_only_result is not None:
        source_status = source_only_result.source_execution_status
        candidate_status = source_only_result.candidate_execution_status or EXECUTION_STATUS_NOT_ENABLED
    exact_status = str(ledger.get("exact_status", ""))
    checker_status = str(ledger.get("checker_status", ""))
    return {
        "case_id": row.case_id,
        "pool": row.pool,
        "engine": row.engine,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "selected": "true",
        "candidate_generated": _bool(str(ledger.get("candidate_generated", "")) == "true"),
        "candidate_sql_sha256": _sha256(candidate_path),
        "preflight_passed": _bool(str(ledger.get("candidate_preflight_status", "")) == CANDIDATE_PREFLIGHT_STATUS_PASSED),
        "fail_closed": _bool(bool(fail_closed_bucket) or failure_bucket in {"unsupported_engine", "no_candidate_sql"}),
        "fail_closed_bucket": fail_closed_bucket,
        "source_executable": _bool(_is_success(source_status, EXECUTION_STATUS_SOURCE_SUCCESS)),
        "candidate_executable": _bool(_is_success(candidate_status, EXECUTION_STATUS_CANDIDATE_SUCCESS)),
        "checker_attempted": _bool(checker_status in {CHECKER_STATUS_SUCCESS, "checker_mismatch"}),
        "exact_result_consistent": _bool(exact_status == EXACT_STATUS_EXACT),
        "mismatch": _bool(failure_bucket == "mismatch" or exact_status == "mismatch"),
        "source_execution_failed": _bool(str(source_status).startswith("source_") and source_status != EXECUTION_STATUS_SOURCE_SUCCESS),
        "candidate_execution_failed": _bool(candidate_status == "candidate_execution_failed"),
        "failure_bucket": failure_bucket,
        "error_summary": str(ledger.get("notes", "")),
        "schema_context_status": "available" if status.get("schema_ddl_path") else ("not_recorded" if not status else "unavailable"),
        "schema_ddl_path": str(status.get("schema_ddl_path", "")),
        "schema_context_tables": ";".join(status.get("schema_context_tables", []) or []),
        "candidate_sql_path": candidate_path,
        "unsupported_candidate_sql_sha256": _sha256(unsupported_path),
        "unsupported_candidate_sql_path": unsupported_path,
        "source_sql_path": str((repo_root / row.source_sql_path).resolve()),
        "checker_status": checker_status,
        "exact_status": exact_status,
        "source_execution_status": source_status,
        "candidate_execution_status": candidate_status,
        "mismatch_artifact_path": mismatch_path,
        "mismatch_class": mismatch["class"],
        "label_only_mismatch": _bool(mismatch["label_only"]),
        "semantic_mismatch": _bool(mismatch["semantic"]),
        "local_only": "true",
        "official_metric_input": "false",
        "paper_result": "false",
    }


def _mismatch_class(path_text: str) -> dict[str, Any]:
    result = {"class": "", "label_only": False, "semantic": False}
    if not path_text:
        return result
    path = Path(path_text)
    if not path.exists():
        return result
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return result
    diagnostics = payload.get("label_diagnostics") or payload.get("cross_dialect_normalization") or {}
    label_only = bool(diagnostics.get("label_only_mismatch"))
    value_exact = bool(diagnostics.get("value_exact"))
    value_reason = str(diagnostics.get("value_mismatch_reason", ""))
    source_count = payload.get("source_row_count")
    candidate_count = payload.get("candidate_row_count")
    if label_only and value_exact:
        return {"class": "label_only_mismatch", "label_only": True, "semantic": False}
    if value_reason == "row_count_mismatch" or source_count != candidate_count or not value_exact:
        return {"class": "semantic_mismatch", "label_only": False, "semantic": True}
    return result


def _summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    def count(field: str, value: str = "true") -> int:
        return sum(row[field] == value for row in rows)

    by_engine = _group_counts(rows, "engine")
    by_pool = _group_counts(rows, "pool")
    frontier = Counter(row["failure_bucket"] or "none" for row in rows)
    return {
        "task": TASK_ID,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "planned_rows": 120,
        "selected_rows": len(rows),
        "candidate_generated_rows": count("candidate_generated"),
        "fail_closed_rows": count("fail_closed"),
        "source_executable_rows": count("source_executable"),
        "candidate_executable_rows": count("candidate_executable"),
        "checker_attempted_rows": count("checker_attempted"),
        "exact_rows": count("exact_result_consistent"),
        "mismatch_rows": count("mismatch"),
        "source_execution_failed_rows": count("source_execution_failed"),
        "candidate_execution_failed_rows": count("candidate_execution_failed"),
        "no_candidate_rows": sum(
            row["candidate_generated"] == "false" for row in rows
        ),
        "unsupported_rows": sum(
            row["failure_bucket"] == "unsupported_engine" for row in rows
        ),
        "by_engine": by_engine,
        "by_pool": by_pool,
        "frontier_bucket_counts": dict(sorted(frontier.items())),
        "label_only_mismatch_count": count("label_only_mismatch"),
        "semantic_mismatch_count": count("semantic_mismatch"),
        "known_policy_rows": {
            "cons0005_spark_semantic_mismatch": _row_matches(rows, "CONS_0005", "spark", "semantic_mismatch"),
            "cons0036_spark_label_only_mismatch": _row_matches(rows, "CONS_0036", "spark", "label_only_mismatch"),
            "mysql_array_any_fail_closed_rows": [
                row["case_id"]
                for row in rows
                if row["engine"] == "mysql"
                and row["fail_closed_bucket"] in {"mysql_unsupported_array_any", "sqlglot_unsupported_mysql_lambda"}
            ],
        },
        "timing_collected": False,
        "verifier_run": False,
        "official_metric_input": False,
        "paper_result": False,
        "leaderboard_output_created": False,
    }


def _row_matches(rows: list[dict[str, str]], case_id: str, engine: str, field: str) -> bool:
    for row in rows:
        if row["case_id"] == case_id and row["engine"] == engine:
            return row[field] == "true"
    return False


def _group_counts(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, int]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row[key]].append(row)
    output: dict[str, dict[str, int]] = {}
    for name, subset in sorted(grouped.items()):
        output[name] = {
            "planned_rows": len(subset),
            "selected_rows": len(subset),
            "candidate_generated_rows": sum(row["candidate_generated"] == "true" for row in subset),
            "fail_closed_rows": sum(row["fail_closed"] == "true" for row in subset),
            "source_executable_rows": sum(row["source_executable"] == "true" for row in subset),
            "candidate_executable_rows": sum(row["candidate_executable"] == "true" for row in subset),
            "checker_attempted_rows": sum(row["checker_attempted"] == "true" for row in subset),
            "exact_rows": sum(row["exact_result_consistent"] == "true" for row in subset),
            "mismatch_rows": sum(row["mismatch"] == "true" for row in subset),
            "source_execution_failed_rows": sum(row["source_execution_failed"] == "true" for row in subset),
            "candidate_execution_failed_rows": sum(row["candidate_execution_failed"] == "true" for row in subset),
            "no_candidate_rows": sum(row["candidate_generated"] == "false" for row in subset),
            "unsupported_rows": sum(row["failure_bucket"] == "unsupported_engine" for row in subset),
        }
    return output


def _route_card(summary: dict[str, Any]) -> dict[str, str]:
    return {
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "engine_scope": "postgres,mysql,spark",
        "planned_rows": str(summary["planned_rows"]),
        "selected_rows": str(summary["selected_rows"]),
        "candidate_generated_rows": str(summary["candidate_generated_rows"]),
        "fail_closed_rows": str(summary["fail_closed_rows"]),
        "source_executable_rows": str(summary["source_executable_rows"]),
        "candidate_executable_rows": str(summary["candidate_executable_rows"]),
        "checker_attempted_rows": str(summary["checker_attempted_rows"]),
        "exact_rows": str(summary["exact_rows"]),
        "mismatch_rows": str(summary["mismatch_rows"]),
        "source_execution_failed_rows": str(summary["source_execution_failed_rows"]),
        "candidate_execution_failed_rows": str(summary["candidate_execution_failed_rows"]),
        "no_candidate_rows": str(summary["no_candidate_rows"]),
        "unsupported_rows": str(summary["unsupported_rows"]),
        "label_only_mismatch_count": str(summary["label_only_mismatch_count"]),
        "semantic_mismatch_count": str(summary["semantic_mismatch_count"]),
        "official_metric_input": "false",
        "paper_result": "false",
        "leaderboard_output_created": "false",
    }


def _write_runtime_manifest(adapter_command: str, summary: dict[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "task": TASK_ID,
        "adapter_command": adapter_command,
        "output_root": str(OUTPUT_ROOT),
        "result_root": str(RESULT_ROOT),
        "log_root": str(LOG_ROOT),
        "report_root": str(REPORT_ROOT),
        "summary": summary,
        "local_only": True,
        "official_metric_input": False,
        "paper_result": False,
        "leaderboard_output_created": False,
    }
    (RESULT_ROOT / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (REPORT_ROOT / "boundary.md").write_text(
        "# Boundary\n\nThis is a local diagnostic run only. No timing, verifier, official metric, paper result, retained evidence, or leaderboard output was created.\n",
        encoding="utf-8",
    )


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
