#!/usr/bin/env python3
"""SQLGlot noop PostgreSQL local diagnostic route-card refresh.

This audit-local helper runs the PostgreSQL-only SQLGlot noop diagnostic chain:

1. candidate generation for all Common-core v0 PostgreSQL rows;
2. execution/checker for generated candidates;
3. exact-gated timing for exact rows only;
4. local diagnostic route-card projection.

Runtime artifacts are written under the caller-provided /tmp output root. The
committed outputs are the audit CSV/JSON files written next to this script.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from sql_rewrite_bench.adapter_runner import run_adapter_for_case  # noqa: E402
from sql_rewrite_bench.case_package_resolver import (  # noqa: E402
    DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE,
    DIAGNOSTIC_MODE_SAME_ENGINE,
    LOCAL_DIAGNOSTIC_COMPARISON,
    resolve_case_package,
)
from sql_rewrite_bench.case_selection import resolve_common_core_selection  # noqa: E402
from sql_rewrite_bench.engine_execution import execute_engine_case  # noqa: E402
from sql_rewrite_bench.local_result_checker import run_local_checker  # noqa: E402
from sql_rewrite_bench.local_timing import (  # noqa: E402
    TimingPolicy,
    _collect_postgres_samples,
    _median,
    write_environment_metadata,
    write_timing_policy,
)


AUDIT_DIR = Path(__file__).resolve().parent
ADAPTER = REPO_ROOT / "baselines/sqlglot/sqlglot_user_adapter.py"


CANDIDATE_FIELDS = [
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "source_sql_path",
    "schema_path",
    "candidate_generated",
    "candidate_origin",
    "candidate_sql_path",
    "candidate_sql_sha256",
    "candidate_sql_bytes",
    "failure_bucket",
    "adapter_status",
    "adapter_exit_code",
    "candidate_capture_mode",
    "stdout_trace_path",
    "stderr_trace_path",
    "local_only",
    "official_metric_input",
    "paper_result",
]


EXECUTION_FIELDS = [
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "generation_status",
    "candidate_origin",
    "diagnostic_mode",
    "execution_attempted",
    "source_executable",
    "candidate_executable",
    "checker_attempted",
    "exact",
    "result_consistent",
    "mismatch",
    "source_execution_status",
    "candidate_execution_status",
    "checker_status",
    "execution_error",
    "failure_bucket",
    "candidate_sql_sha256",
    "source_sql_trace",
    "candidate_sql_trace",
    "source_result_trace",
    "candidate_result_trace",
    "checker_output_trace",
    "mismatch_artifact_path",
    "execution_artifact_dir",
    "local_only",
    "official_metric_input",
    "paper_result",
]


TIMING_FIELDS = [
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "exact_gate_source",
    "generation_status",
    "candidate_origin",
    "diagnostic_mode",
    "exact",
    "timing_attempted",
    "source_timing_success",
    "candidate_timing_success",
    "timing_status",
    "source_median_ms",
    "candidate_median_ms",
    "speedup_ratio",
    "timing_failure_bucket",
    "non_timing_reason",
    "source_samples_ms",
    "candidate_samples_ms",
    "candidate_sql_sha256",
    "source_sql_trace",
    "candidate_sql_trace",
    "runtime_artifact_path",
    "local_only",
    "official_metric_input",
    "paper_result",
]


ROUTE_CARD_FIELDS = [
    "method_id",
    "route_id",
    "baseline_family",
    "engine",
    "selected_rows",
    "generated_candidate_rows",
    "no_candidate_rows",
    "execution_attempted_rows",
    "source_executable_rows",
    "candidate_executable_rows",
    "checker_attempted_rows",
    "exact_rows",
    "mismatch_rows",
    "source_execution_failed_rows",
    "candidate_execution_failed_rows",
    "timing_attempted_rows",
    "timed_exact_rows",
    "timing_failed_rows",
    "local_generation_rate",
    "local_execution_coverage_rate",
    "local_result_consistency_rate",
    "diagnostic_gm_speedup",
    "diagnostic_speedup_p10",
    "diagnostic_speedup_p25",
    "diagnostic_speedup_p50",
    "diagnostic_speedup_p75",
    "diagnostic_speedup_p90",
    "diagnostic_median_speedup",
    "official_metric_input",
    "paper_result",
    "leaderboard_output_created",
]


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _float_text(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6f}"


def _sha256(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bytes(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return str(path.stat().st_size)


def _rel(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _percentile(values: list[float], percentile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    rank = (percentile / 100.0) * (len(ordered) - 1)
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return float(ordered[lower])
    weight = rank - lower
    return float(ordered[lower] * (1.0 - weight) + ordered[upper] * weight)


def _geomean(values: list[float]) -> float | None:
    if not values:
        return None
    if any(value <= 0 for value in values):
        return None
    return float(math.exp(sum(math.log(value) for value in values) / len(values)))


def _samples_text(values: list[float]) -> str:
    return json.dumps([round(value, 6) for value in values], separators=(",", ":"))


def _cross_dialect_checker_normalization_enabled(resolved: Any) -> bool:
    return (
        resolved.diagnostic_mode == DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE
        and resolved.checker_comparison == LOCAL_DIAGNOSTIC_COMPARISON
    )


def _mysql_to_spark_numeric_equivalence_enabled(resolved: Any) -> bool:
    return (
        _cross_dialect_checker_normalization_enabled(resolved)
        and resolved.source_reference_engine == "mysql"
        and resolved.target_candidate_engine == "spark"
    )


def _source_trace(resolved: Any, row: Any) -> str:
    if resolved.diagnostic_mode == DIAGNOSTIC_MODE_CROSS_DIALECT_REFERENCE:
        return _rel(resolved.source_reference_query_path)
    return row.source_sql_path


def _stage_candidate_generation(
    *,
    rows: list[Any],
    resolved_by_case: dict[str, Any],
    run_id: str,
    result_root: Path,
    adapter_timeout_sec: int,
) -> list[dict[str, str]]:
    candidate_rows: list[dict[str, str]] = []
    adapter_command = f"{sys.executable} {ADAPTER} --route noop"
    for row in rows:
        resolved = resolved_by_case[row.case_id]
        result = run_adapter_for_case(
            run_id=run_id,
            row=row,
            resolved_package=resolved,
            adapter_command=adapter_command,
            repo_root=REPO_ROOT,
            out_dir=result_root,
            timeout=adapter_timeout_sec,
        )
        generated = result.candidate_generated
        candidate_rows.append(
            {
                "case_id": row.case_id,
                "pool": row.pool,
                "engine": "postgres",
                "method_id": "sqlglot_noop",
                "route_id": "sqlglot_noop",
                "source_sql_path": row.source_sql_path,
                "schema_path": _rel(resolved.schema_external_profile_path),
                "candidate_generated": _bool_text(generated),
                "candidate_origin": "sqlglot_noop" if generated else "no_candidate",
                "candidate_sql_path": _rel(result.candidate_sql_path),
                "candidate_sql_sha256": _sha256(result.candidate_sql_path),
                "candidate_sql_bytes": _bytes(result.candidate_sql_path),
                "failure_bucket": "none" if generated else result.failure_bucket_hint,
                "adapter_status": result.adapter_status,
                "adapter_exit_code": ""
                if result.adapter_exit_code is None
                else str(result.adapter_exit_code),
                "candidate_capture_mode": result.candidate_capture_mode,
                "stdout_trace_path": _rel(result.adapter_stdout_path),
                "stderr_trace_path": _rel(result.adapter_stderr_path),
                "local_only": "true",
                "official_metric_input": "false",
                "paper_result": "false",
            }
        )
    return candidate_rows


def _stage_execution_checker(
    *,
    selected_by_case: dict[str, Any],
    resolved_by_case: dict[str, Any],
    candidate_rows: list[dict[str, str]],
    run_id: str,
    result_root: Path,
    execution_timeout_sec: int,
    db_schema_prefix: str,
    postgres_dsn_env: str,
) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    for candidate in candidate_rows:
        case_id = candidate["case_id"]
        row = selected_by_case[case_id]
        resolved = resolved_by_case[case_id]
        generated = candidate["candidate_generated"] == "true"
        workspace = result_root / "workspaces" / case_id / "postgres"
        execution = None
        checker = None
        execution_attempted = generated
        failure_bucket = candidate["failure_bucket"]
        if execution_attempted:
            execution = execute_engine_case(
                repo_root=REPO_ROOT,
                run_id=run_id,
                row=row,
                candidate_sql_path=Path(candidate["candidate_sql_path"]),
                workspace_dir=workspace,
                timeout_sec=execution_timeout_sec,
                schema_prefix=db_schema_prefix,
                postgres_dsn_env=postgres_dsn_env,
                resolved_package=resolved,
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
                    enable_cross_dialect_normalization=_cross_dialect_checker_normalization_enabled(
                        resolved
                    ),
                    enable_mixed_numeric_equivalence=_mysql_to_spark_numeric_equivalence_enabled(
                        resolved
                    ),
                )
                failure_bucket = checker.failure_bucket

        source_ok = bool(execution and execution.source_executable)
        candidate_ok = bool(execution and execution.candidate_executable)
        source_status = execution.source_execution_status if execution else "not_attempted"
        candidate_status = execution.candidate_execution_status if execution else "not_attempted"
        checker_status = checker.checker_status if checker else "not_attempted"
        exact = checker is not None and checker.exact_status == "exact"
        mismatch = checker is not None and checker.exact_status == "mismatch"
        output_rows.append(
            {
                "case_id": case_id,
                "pool": candidate["pool"],
                "engine": "postgres",
                "method_id": "sqlglot_noop",
                "route_id": "sqlglot_noop",
                "generation_status": "generated" if generated else "no_candidate",
                "candidate_origin": candidate["candidate_origin"],
                "diagnostic_mode": resolved.diagnostic_mode,
                "execution_attempted": _bool_text(execution_attempted),
                "source_executable": _bool_text(source_ok),
                "candidate_executable": _bool_text(candidate_ok),
                "checker_attempted": _bool_text(checker is not None),
                "exact": _bool_text(exact),
                "result_consistent": _bool_text(exact),
                "mismatch": _bool_text(mismatch),
                "source_execution_status": source_status,
                "candidate_execution_status": candidate_status,
                "checker_status": checker_status,
                "execution_error": execution.execution_failure_class if execution else "",
                "failure_bucket": failure_bucket,
                "candidate_sql_sha256": candidate["candidate_sql_sha256"],
                "source_sql_trace": _source_trace(resolved, row),
                "candidate_sql_trace": candidate["candidate_sql_path"],
                "source_result_trace": _rel(execution.source_result_path) if execution else "",
                "candidate_result_trace": _rel(execution.candidate_result_path)
                if execution
                else "",
                "checker_output_trace": _rel(workspace / "checker" / "checker_result.json")
                if checker
                else "",
                "mismatch_artifact_path": _rel(checker.mismatch_artifact_path)
                if checker and checker.mismatch_artifact_path
                else "",
                "execution_artifact_dir": _rel(execution.db_artifact_dir)
                if execution
                else "",
                "local_only": "true",
                "official_metric_input": "false",
                "paper_result": "false",
            }
        )
    return output_rows


def _timing_runtime_artifact_path(timing_dir: Path, case_id: str) -> Path:
    return timing_dir / "rows" / f"{case_id}__postgres__sqlglot_noop.json"


def _write_timing_artifact(
    *,
    path: Path,
    execution_row: dict[str, str],
    policy: TimingPolicy,
    status: str,
    failure_bucket: str,
    source_samples: list[float],
    candidate_samples: list[float],
    source_median: float | None,
    candidate_median: float | None,
    speedup_ratio: float | None,
    output_root: Path,
) -> None:
    _write_json(
        path,
        {
            "schema_version": "sqlglot_noop_pg_timing_row_artifact_v0",
            "case_id": execution_row["case_id"],
            "pool": execution_row["pool"],
            "engine": "postgres",
            "method_id": "sqlglot_noop",
            "route_id": "sqlglot_noop",
            "exact_gate_source": "sqlglot_noop_pg_current_execution_checker_stage",
            "candidate_origin": execution_row["candidate_origin"],
            "timing_status": status,
            "timing_failure_bucket": failure_bucket,
            "source_runtime_samples_ms": source_samples,
            "candidate_runtime_samples_ms": candidate_samples,
            "source_median_ms": source_median,
            "candidate_median_ms": candidate_median,
            "speedup_ratio": speedup_ratio,
            "timing_policy": {
                "timing_policy_id": policy.timing_policy_id,
                "warmup_count": policy.warmup_count,
                "measured_repetitions": policy.measured_repetitions,
                "timeout_seconds": policy.timeout_seconds,
                "statistic": policy.statistic,
                "execution_order_policy": policy.execution_order_policy,
                "schema_setup_policy": policy.schema_setup_policy,
            },
            "output_root": output_root.as_posix(),
            "source_sql_trace": execution_row["source_sql_trace"],
            "candidate_sql_trace": execution_row["candidate_sql_trace"],
            "local_only": True,
            "official_metric_input": False,
            "paper_result": False,
        },
    )


def _stage_timing(
    *,
    selected_by_case: dict[str, Any],
    resolved_by_case: dict[str, Any],
    execution_rows: list[dict[str, str]],
    run_id: str,
    output_root: Path,
    result_root: Path,
    timing_timeout_sec: float,
    db_schema_prefix: str,
    postgres_dsn_env: str,
) -> list[dict[str, str]]:
    timing_dir = result_root / "timing"
    policy = TimingPolicy(
        warmup_count=1,
        measured_repetitions=5,
        timeout_seconds=timing_timeout_sec,
    )
    write_timing_policy(timing_dir, policy)
    write_environment_metadata(timing_dir, repo_root=REPO_ROOT, run_id=run_id)
    output_rows: list[dict[str, str]] = []
    for execution_row in execution_rows:
        case_id = execution_row["case_id"]
        resolved = resolved_by_case[case_id]
        exact = execution_row["exact"] == "true"
        timing_attempted = exact and resolved.diagnostic_mode == DIAGNOSTIC_MODE_SAME_ENGINE
        source_samples: list[float] = []
        candidate_samples: list[float] = []
        source_median: float | None = None
        candidate_median: float | None = None
        speedup_ratio: float | None = None
        timing_status = "not_attempted"
        failure_bucket = ""
        non_timing_reason = ""
        artifact_path = _timing_runtime_artifact_path(timing_dir, case_id)
        if timing_attempted:
            row = selected_by_case[case_id]
            try:
                samples = _collect_postgres_samples(
                    repo_root=REPO_ROOT,
                    row=row,
                    run_id=run_id,
                    candidate_sql_path=Path(execution_row["candidate_sql_trace"]),
                    policy=policy,
                    postgres_dsn_env=postgres_dsn_env,
                    db_schema_prefix=db_schema_prefix,
                    timing_dir=timing_dir,
                )
                source_samples = samples.source_runtime_samples_ms
                candidate_samples = samples.candidate_runtime_samples_ms
                source_median = _median(source_samples)
                candidate_median = _median(candidate_samples)
                if source_median and candidate_median and source_median > 0 and candidate_median > 0:
                    speedup_ratio = source_median / candidate_median
                    timing_status = "timed"
                else:
                    timing_status = "timing_failed"
                    failure_bucket = "non_positive_median"
            except Exception as exc:
                timing_status = "timing_failed"
                failure_bucket = f"timing_failed_{type(exc).__name__}"
        else:
            if execution_row["generation_status"] == "no_candidate":
                non_timing_reason = "no_candidate"
            elif execution_row["source_executable"] != "true":
                non_timing_reason = "source_execution_failed"
            elif execution_row["candidate_executable"] != "true":
                non_timing_reason = "candidate_execution_failed"
            elif execution_row["mismatch"] == "true":
                non_timing_reason = "checker_mismatch"
            elif exact and resolved.diagnostic_mode != DIAGNOSTIC_MODE_SAME_ENGINE:
                non_timing_reason = "timing_scope_not_supported"
            else:
                non_timing_reason = "not_exact"
        if timing_attempted:
            _write_timing_artifact(
                path=artifact_path,
                execution_row=execution_row,
                policy=policy,
                status=timing_status,
                failure_bucket=failure_bucket,
                source_samples=source_samples,
                candidate_samples=candidate_samples,
                source_median=source_median,
                candidate_median=candidate_median,
                speedup_ratio=speedup_ratio,
                output_root=output_root,
            )
        output_rows.append(
            {
                "case_id": case_id,
                "pool": execution_row["pool"],
                "engine": "postgres",
                "method_id": "sqlglot_noop",
                "route_id": "sqlglot_noop",
                "exact_gate_source": "sqlglot_noop_pg_current_execution_checker_stage",
                "generation_status": execution_row["generation_status"],
                "candidate_origin": execution_row["candidate_origin"],
                "diagnostic_mode": resolved.diagnostic_mode,
                "exact": execution_row["exact"],
                "timing_attempted": _bool_text(timing_attempted),
                "source_timing_success": _bool_text(timing_status == "timed"),
                "candidate_timing_success": _bool_text(timing_status == "timed"),
                "timing_status": timing_status,
                "source_median_ms": _float_text(source_median),
                "candidate_median_ms": _float_text(candidate_median),
                "speedup_ratio": _float_text(speedup_ratio),
                "timing_failure_bucket": failure_bucket,
                "non_timing_reason": non_timing_reason,
                "source_samples_ms": _samples_text(source_samples),
                "candidate_samples_ms": _samples_text(candidate_samples),
                "candidate_sql_sha256": execution_row["candidate_sql_sha256"],
                "source_sql_trace": execution_row["source_sql_trace"],
                "candidate_sql_trace": execution_row["candidate_sql_trace"],
                "runtime_artifact_path": _rel(artifact_path) if timing_attempted else "",
                "local_only": "true",
                "official_metric_input": "false",
                "paper_result": "false",
            }
        )
    return output_rows


def _route_card(
    *,
    candidate_rows: list[dict[str, str]],
    execution_rows: list[dict[str, str]],
    timing_rows: list[dict[str, str]],
) -> dict[str, Any]:
    selected = len(candidate_rows)
    generated = sum(row["candidate_generated"] == "true" for row in candidate_rows)
    no_candidate = sum(row["candidate_generated"] != "true" for row in candidate_rows)
    execution_attempted = sum(row["execution_attempted"] == "true" for row in execution_rows)
    source_ok = sum(row["source_executable"] == "true" for row in execution_rows)
    candidate_ok = sum(row["candidate_executable"] == "true" for row in execution_rows)
    checker_attempted = sum(row["checker_attempted"] == "true" for row in execution_rows)
    exact = sum(row["exact"] == "true" for row in execution_rows)
    mismatch = sum(row["mismatch"] == "true" for row in execution_rows)
    source_failed = sum(
        row["execution_attempted"] == "true" and row["source_executable"] != "true"
        for row in execution_rows
    )
    candidate_failed = sum(
        row["source_executable"] == "true" and row["candidate_executable"] != "true"
        for row in execution_rows
    )
    timing_attempted = sum(row["timing_attempted"] == "true" for row in timing_rows)
    timed = sum(row["timing_status"] == "timed" for row in timing_rows)
    timing_failed = sum(row["timing_status"] == "timing_failed" for row in timing_rows)
    speedups = [float(row["speedup_ratio"]) for row in timing_rows if row["speedup_ratio"]]
    return {
        "schema_version": "sqlglot_noop_pg_current_route_card_v0",
        "method_id": "sqlglot_noop",
        "route_id": "sqlglot_noop",
        "baseline_family": "sqlglot",
        "engine": "postgres",
        "selected_rows": selected,
        "generated_candidate_rows": generated,
        "no_candidate_rows": no_candidate,
        "execution_attempted_rows": execution_attempted,
        "source_executable_rows": source_ok,
        "candidate_executable_rows": candidate_ok,
        "checker_attempted_rows": checker_attempted,
        "exact_rows": exact,
        "mismatch_rows": mismatch,
        "source_execution_failed_rows": source_failed,
        "candidate_execution_failed_rows": candidate_failed,
        "timing_attempted_rows": timing_attempted,
        "timed_exact_rows": timed,
        "timing_failed_rows": timing_failed,
        "local_generation_rate": generated / selected if selected else None,
        "local_execution_coverage_rate": candidate_ok / selected if selected else None,
        "local_result_consistency_rate": exact / selected if selected else None,
        "diagnostic_gm_speedup": _geomean(speedups),
        "diagnostic_speedup_p10": _percentile(speedups, 10),
        "diagnostic_speedup_p25": _percentile(speedups, 25),
        "diagnostic_speedup_p50": _percentile(speedups, 50),
        "diagnostic_speedup_p75": _percentile(speedups, 75),
        "diagnostic_speedup_p90": _percentile(speedups, 90),
        "diagnostic_median_speedup": statistics.median(speedups) if speedups else None,
        "official_metric_input": False,
        "paper_result": False,
        "leaderboard_output_created": False,
    }


def _route_card_csv_row(card: dict[str, Any]) -> dict[str, str]:
    row: dict[str, str] = {}
    for field in ROUTE_CARD_FIELDS:
        value = card.get(field)
        if isinstance(value, bool):
            row[field] = _bool_text(value)
        elif isinstance(value, float):
            row[field] = f"{value:.6f}"
        elif value is None:
            row[field] = ""
        else:
            row[field] = str(value)
    return row


def _summary(card: dict[str, Any], run_id: str, output_root: Path) -> dict[str, Any]:
    return {
        "schema_version": "sqlglot_noop_pg_current_route_card_summary_v0",
        "run_id": run_id,
        "runtime_root": output_root.as_posix(),
        **card,
        "local_only": True,
        "official_metric_input": False,
        "paper_result": False,
        "leaderboard_output_created": False,
        "timing_policy": {
            "warmup": 1,
            "measured_repetitions": 5,
            "timeout_seconds": 30,
            "statistic": "median",
        },
    }


def run(args: argparse.Namespace) -> int:
    selected = resolve_common_core_selection(
        repo_root=REPO_ROOT,
        case_set="common_core_v0",
        pool="all",
        engine="postgres",
        case_list=None,
        smoke=False,
    )
    selected_by_case = {row.case_id: row for row in selected}
    resolved_by_case = {
        row.case_id: resolve_case_package(repo_root=REPO_ROOT, row=row) for row in selected
    }
    result_root = args.output_root / "output" / "results" / args.run_id
    log_root = args.output_root / "output" / "logs" / args.run_id
    report_root = args.output_root / "output" / "reports" / args.run_id
    for path in (result_root, log_root, report_root):
        path.mkdir(parents=True, exist_ok=True)

    candidate_rows = _stage_candidate_generation(
        rows=selected,
        resolved_by_case=resolved_by_case,
        run_id=args.run_id,
        result_root=result_root,
        adapter_timeout_sec=args.adapter_timeout_sec,
    )
    execution_rows = _stage_execution_checker(
        selected_by_case=selected_by_case,
        resolved_by_case=resolved_by_case,
        candidate_rows=candidate_rows,
        run_id=args.run_id,
        result_root=result_root,
        execution_timeout_sec=args.execution_timeout_sec,
        db_schema_prefix=args.db_schema_prefix,
        postgres_dsn_env=args.postgres_dsn_env,
    )
    timing_rows = _stage_timing(
        selected_by_case=selected_by_case,
        resolved_by_case=resolved_by_case,
        execution_rows=execution_rows,
        run_id=args.run_id,
        output_root=args.output_root,
        result_root=result_root,
        timing_timeout_sec=args.timing_timeout_sec,
        db_schema_prefix=args.db_schema_prefix,
        postgres_dsn_env=args.postgres_dsn_env,
    )
    card = _route_card(
        candidate_rows=candidate_rows,
        execution_rows=execution_rows,
        timing_rows=timing_rows,
    )
    summary = _summary(card, args.run_id, args.output_root)

    _write_csv(AUDIT_DIR / "per_row_candidate_status.csv", candidate_rows, CANDIDATE_FIELDS)
    _write_csv(AUDIT_DIR / "per_row_execution_checker_status.csv", execution_rows, EXECUTION_FIELDS)
    _write_csv(AUDIT_DIR / "per_row_timing.csv", timing_rows, TIMING_FIELDS)
    _write_json(AUDIT_DIR / "route_card.json", card)
    _write_csv(AUDIT_DIR / "route_card.csv", [_route_card_csv_row(card)], ROUTE_CARD_FIELDS)
    _write_json(AUDIT_DIR / "diagnostic_summary.json", summary)
    _write_json(
        log_root / "run_config.json",
        {key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()},
    )
    (report_root / "README.md").write_text(
        "# SQLGlot noop PostgreSQL current route-card refresh\n\n"
        "Local diagnostic runtime artifacts only. No official metrics or paper results.\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--run-id", default="sqlglot_noop_pg_current_route_card")
    parser.add_argument("--adapter-timeout-sec", type=int, default=40)
    parser.add_argument("--execution-timeout-sec", type=int, default=40)
    parser.add_argument("--timing-timeout-sec", type=float, default=30.0)
    parser.add_argument("--db-schema-prefix", default="sqlrb_sqlglot_noop_pg_current")
    parser.add_argument("--postgres-dsn-env", default="SQLRB_POSTGRES_DSN")
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
