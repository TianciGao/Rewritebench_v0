#!/usr/bin/env python3
"""PostgreSQL-only execution/checker helper for prior Calcite candidates.

This audit helper consumes `calcite_hep_pg_bounded_candidate_generation_v0`
candidate metadata and executes only generated candidates against PostgreSQL.
It avoids user-entry PORT cross-dialect source-reference routing so this audit
remains a PostgreSQL-only diagnostic pass.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from sql_rewrite_bench.case_selection import resolve_common_core_selection  # noqa: E402
from sql_rewrite_bench.local_result_checker import run_local_checker  # noqa: E402
from sql_rewrite_bench.postgres_execution import execute_postgres_case  # noqa: E402


DEFAULT_INPUT = (
    REPO_ROOT
    / "audits"
    / "calcite_hep_pg_bounded_candidate_generation_v0"
    / "per_row_candidate_status.csv"
)


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _origin(row: dict[str, str]) -> str:
    if row.get("candidate_generated") != "true":
        return "no_candidate"
    if row.get("candidate_review_status") == "generated_parse_only_schema_fallback_review":
        return "calcite_parse_only_schema_fallback"
    return "calcite_rel_to_sql"


def _rel(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_prior_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _summary(rows: list[dict[str, str]], *, run_id: str, input_csv: Path) -> dict[str, object]:
    selected = len(rows)
    generated = sum(row["generation_status"] == "generated" for row in rows)
    no_candidate = sum(row["generation_status"] == "no_candidate" for row in rows)
    attempted = sum(row["execution_attempted"] == "true" for row in rows)
    source_ok = sum(row["source_executable"] == "true" for row in rows)
    candidate_ok = sum(row["candidate_executable"] == "true" for row in rows)
    checker_attempted = sum(row["checker_attempted"] == "true" for row in rows)
    exact = sum(row["exact"] == "true" for row in rows)
    mismatch = sum(row["mismatch"] == "true" for row in rows)
    source_failed = sum(row["source_execution_status"] == "source_execution_failed" for row in rows)
    candidate_failed = sum(
        row["candidate_execution_status"] == "candidate_execution_failed" for row in rows
    )
    schema_fallback = [
        row for row in rows if row["candidate_origin"] == "calcite_parse_only_schema_fallback"
    ]
    return {
        "schema_version": "calcite_pg_execution_checker_diagnostic_summary_v0",
        "run_id": run_id,
        "source_candidate_generation_audit": "audits/calcite_hep_pg_bounded_candidate_generation_v0/",
        "input_candidate_csv": input_csv.as_posix(),
        "selected_rows": selected,
        "generated_candidate_rows": generated,
        "no_candidate_rows": no_candidate,
        "execution_attempted_rows": attempted,
        "source_executable_rows": source_ok,
        "candidate_executable_rows": candidate_ok,
        "checker_attempted_rows": checker_attempted,
        "exact_rows": exact,
        "mismatch_rows": mismatch,
        "source_execution_failed_rows": source_failed,
        "candidate_execution_failed_rows": candidate_failed,
        "schema_fallback_rows": len(schema_fallback),
        "schema_fallback_exact_rows": sum(row["exact"] == "true" for row in schema_fallback),
        "schema_fallback_failed_rows": sum(
            row["failure_bucket"] != "none" for row in schema_fallback
        ),
        "not_attempted_no_candidate_rows": no_candidate,
        "not_attempted_manual_review_rows": 0,
        "failure_bucket_counts": dict(sorted(Counter(row["failure_bucket"] for row in rows).items())),
        "candidate_origin_counts": dict(sorted(Counter(row["candidate_origin"] for row in rows).items())),
        "local_result_consistency_rate_diagnostic": exact / selected if selected else None,
        "db_execution_engine": "postgres",
        "timing_collected": False,
        "verifier_run": False,
        "official_metric_input": False,
        "paper_result": False,
        "local_only": True,
    }


def run(args: argparse.Namespace) -> int:
    prior_rows = _read_prior_rows(args.input_csv)
    selected = resolve_common_core_selection(
        repo_root=REPO_ROOT,
        case_set="common_core_v0",
        pool="all",
        engine="postgres",
        case_list=None,
        smoke=False,
    )
    selected_by_case = {row.case_id: row for row in selected}
    result_root = args.output_root / "output" / "results" / args.run_id
    log_root = args.output_root / "output" / "logs" / args.run_id
    report_root = args.output_root / "output" / "reports" / args.run_id
    workspace_root = result_root / "workspaces"
    for path in (result_root, log_root, report_root, workspace_root):
        path.mkdir(parents=True, exist_ok=True)

    output_rows: list[dict[str, str]] = []
    for prior in prior_rows:
        case_id = prior["case_id"]
        row = selected_by_case[case_id]
        origin = _origin(prior)
        generated = prior.get("candidate_generated") == "true"
        candidate_path = Path(prior.get("candidate_sql_path", ""))
        workspace = workspace_root / case_id / "postgres"
        failure_bucket = "no_candidate_sql" if not generated else "not_run"
        execution = None
        checker = None

        if generated:
            execution = execute_postgres_case(
                repo_root=REPO_ROOT,
                run_id=args.run_id,
                row=row,
                candidate_sql_path=candidate_path,
                workspace_dir=workspace,
                timeout_sec=args.execution_timeout_sec,
                schema_prefix=args.db_schema_prefix,
                dsn_env=args.postgres_dsn_env,
            )
            failure_bucket = execution.failure_bucket
            if (
                execution.source_result_path is not None
                and execution.candidate_result_path is not None
                and execution.failure_bucket == "none"
            ):
                checker = run_local_checker(
                    case_dir=REPO_ROOT / row.case_path,
                    source_result_path=execution.source_result_path,
                    candidate_result_path=execution.candidate_result_path,
                    checker_dir=workspace / "checker",
                    enable_cross_dialect_normalization=False,
                    enable_mixed_numeric_equivalence=False,
                )
                failure_bucket = checker.failure_bucket

        source_status = execution.source_execution_status if execution else "not_attempted"
        candidate_status = execution.candidate_execution_status if execution else "not_attempted"
        checker_status = checker.checker_status if checker else "not_attempted"
        exact = checker is not None and checker.exact_status == "exact"
        mismatch = checker is not None and checker.exact_status == "mismatch"
        output_rows.append(
            {
                "case_id": case_id,
                "pool": prior["pool"],
                "engine": "postgres",
                "method_id": "calcite_hep_fail_closed",
                "route_id": "calcite_hep_fail_closed",
                "generation_status": "generated" if generated else "no_candidate",
                "candidate_origin": origin,
                "execution_attempted": _bool_text(generated),
                "source_executable": _bool_text(source_status == "source_execution_success"),
                "candidate_executable": _bool_text(candidate_status == "candidate_execution_success"),
                "checker_attempted": _bool_text(checker is not None),
                "exact": _bool_text(exact),
                "result_consistent": _bool_text(exact),
                "mismatch": _bool_text(mismatch),
                "source_execution_status": source_status,
                "candidate_execution_status": candidate_status,
                "checker_status": checker_status,
                "execution_error": execution.execution_failure_class if execution else "",
                "failure_bucket": failure_bucket,
                "fail_closed_reason": prior.get("fail_closed_reason", ""),
                "candidate_sql_sha256": prior.get("candidate_sql_sha256", ""),
                "source_sql_trace": row.source_sql_path,
                "candidate_sql_trace": prior.get("candidate_sql_path", ""),
                "checker_output_trace": _rel(workspace / "checker" / "checker_result.json")
                if checker
                else "",
                "mismatch_artifact_path": _rel(checker.mismatch_artifact_path)
                if checker and checker.mismatch_artifact_path
                else "",
                "execution_artifact_dir": _rel(execution.db_artifact_dir) if execution else "",
                "local_only": "true",
                "official_metric_input": "false",
                "paper_result": "false",
            }
        )

    _write_csv(result_root / "per_row_execution_checker_status.csv", output_rows)
    payload = _summary(output_rows, run_id=args.run_id, input_csv=args.input_csv)
    (result_root / "diagnostic_summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (report_root / "README.md").write_text(
        "# Calcite HEP PostgreSQL execution/checker diagnostic\n\n"
        "Local diagnostic output only. No timing, verifier, official metrics, paper result, "
        "retained evidence, or leaderboard output was produced.\n",
        encoding="utf-8",
    )
    (log_root / "run_config.json").write_text(
        json.dumps(
            {
                "run_id": args.run_id,
                "input_csv": args.input_csv.as_posix(),
                "postgres_dsn_env": args.postgres_dsn_env,
                "execution_timeout_sec": args.execution_timeout_sec,
                "db_schema_prefix": args.db_schema_prefix,
                "local_only": True,
                "official_metric_input": False,
                "paper_result": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--postgres-dsn-env", default="SQLRB_POSTGRES_DSN")
    parser.add_argument("--execution-timeout-sec", type=int, default=40)
    parser.add_argument("--db-schema-prefix", default="sqlrb_calcite_pg_exec")
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
