#!/usr/bin/env python3
"""PostgreSQL-only timing helper for exact Calcite HEP diagnostic rows.

This audit helper consumes the prior execution/checker ledger and times only
rows marked exact/result-consistent there. It writes runtime timing artifacts
under a caller-provided /tmp root and writes the audit CSV/JSON outputs into
this audit packet.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from sql_rewrite_bench.case_selection import resolve_common_core_selection  # noqa: E402
from sql_rewrite_bench.local_timing import (  # noqa: E402
    TimingPolicy,
    _collect_postgres_samples,
    _median,
    write_environment_metadata,
    write_timing_policy,
)


AUDIT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = (
    REPO_ROOT
    / "audits"
    / "calcite_hep_pg_execution_checker_diagnostic_v0"
    / "per_row_execution_checker_status.csv"
)
DEFAULT_OUTPUT_ROOT = Path("/tmp/sqlrb_calcite_hep_pg_exact_timing_diagnostic_v0")


FIELDNAMES = [
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "exact_gate_source",
    "generation_status",
    "candidate_origin",
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


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _samples_text(values: list[float]) -> str:
    return json.dumps([round(v, 6) for v in values], separators=(",", ":"))


def _float_text(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6f}"


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
    positive = [v for v in values if v > 0]
    if len(positive) != len(values) or not positive:
        return None
    return float(math.exp(sum(math.log(v) for v in positive) / len(positive)))


def _runtime_artifact_path(timing_dir: Path, case_id: str) -> Path:
    return timing_dir / "rows" / f"{case_id}__postgres__calcite_hep_fail_closed.json"


def _write_runtime_artifact(
    *,
    path: Path,
    row: dict[str, str],
    policy: TimingPolicy,
    timing_status: str,
    timing_failure_bucket: str,
    source_samples: list[float],
    candidate_samples: list[float],
    source_median: float | None,
    candidate_median: float | None,
    speedup_ratio: float | None,
    runtime_root: Path,
) -> None:
    payload = {
        "schema_version": "calcite_pg_exact_timing_row_artifact_v0",
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": "postgres",
        "method_id": "calcite_hep_fail_closed",
        "route_id": "calcite_hep_fail_closed",
        "exact_gate_source": "calcite_hep_pg_execution_checker_diagnostic_v0",
        "candidate_origin": row["candidate_origin"],
        "timing_status": timing_status,
        "timing_failure_bucket": timing_failure_bucket,
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
        "runtime_root": runtime_root.as_posix(),
        "source_sql_trace": row["source_sql_trace"],
        "candidate_sql_trace": row["candidate_sql_trace"],
        "local_only": True,
        "official_metric_input": False,
        "paper_result": False,
    }
    _write_json(path, payload)


def _summary(
    *,
    input_rows: list[dict[str, str]],
    output_rows: list[dict[str, str]],
    speedups: list[float],
    policy: TimingPolicy,
    run_id: str,
    output_root: Path,
) -> dict[str, Any]:
    selected = len(input_rows)
    generated = sum(row["generation_status"] == "generated" for row in input_rows)
    no_candidate = sum(row["generation_status"] == "no_candidate" for row in input_rows)
    exact = sum(row["exact"] == "true" for row in input_rows)
    attempted = sum(row["timing_attempted"] == "true" for row in output_rows)
    timed = sum(row["timing_status"] == "timed" for row in output_rows)
    failed = sum(row["timing_status"] == "timing_failed" for row in output_rows)
    prior_failure_counts = Counter(row["failure_bucket"] for row in input_rows)
    timing_failure_counts = Counter(
        row["timing_failure_bucket"] for row in output_rows if row["timing_failure_bucket"]
    )
    return {
        "schema_version": "calcite_pg_exact_timing_diagnostic_summary_v0",
        "run_id": run_id,
        "source_execution_checker_audit": "audits/calcite_hep_pg_execution_checker_diagnostic_v0/",
        "selected_rows": selected,
        "generated_candidate_rows": generated,
        "no_candidate_rows": no_candidate,
        "exact_rows": exact,
        "timing_attempted_rows": attempted,
        "timed_rows": timed,
        "timing_failed_rows": failed,
        "non_timed_not_exact_rows": selected - exact,
        "mismatch_rows": prior_failure_counts.get("mismatch", 0),
        "source_execution_failed_rows": prior_failure_counts.get("source_execution_failed", 0),
        "candidate_execution_failed_rows": prior_failure_counts.get("candidate_execution_failed", 0),
        "not_timed_no_candidate_rows": prior_failure_counts.get("no_candidate_sql", 0),
        "gm_speedup_diagnostic": _geomean(speedups),
        "median_speedup_diagnostic": statistics.median(speedups) if speedups else None,
        "speedup_percentiles_diagnostic": {
            "p10": _percentile(speedups, 10),
            "p25": _percentile(speedups, 25),
            "p50": _percentile(speedups, 50),
            "p75": _percentile(speedups, 75),
            "p90": _percentile(speedups, 90),
        },
        "win_tie_loss_diagnostic": None,
        "win_tie_loss_reason": "not_computed_no_existing_policy",
        "timing_policy": {
            "timing_policy_id": policy.timing_policy_id,
            "warmup_count": policy.warmup_count,
            "measured_repetitions": policy.measured_repetitions,
            "timeout_seconds": policy.timeout_seconds,
            "statistic": policy.statistic,
            "execution_order_policy": policy.execution_order_policy,
            "schema_setup_policy": policy.schema_setup_policy,
        },
        "timing_failure_bucket_counts": dict(sorted(timing_failure_counts.items())),
        "prior_failure_bucket_counts": dict(sorted(prior_failure_counts.items())),
        "runtime_output_root": output_root.as_posix(),
        "output_shape": {
            "results": (output_root / "output" / "results" / run_id).as_posix(),
            "logs": (output_root / "output" / "logs" / run_id).as_posix(),
            "reports": (output_root / "output" / "reports" / run_id).as_posix(),
        },
        "local_only": True,
        "official_metric_input": False,
        "paper_result": False,
        "leaderboard_output_created": False,
    }


def run(args: argparse.Namespace) -> int:
    input_rows = _read_csv(args.input_csv)
    selected_rows = resolve_common_core_selection(
        repo_root=REPO_ROOT,
        case_set="common_core_v0",
        pool="all",
        engine="postgres",
        case_list=None,
        smoke=False,
    )
    selected_by_case = {row.case_id: row for row in selected_rows}

    result_root = args.output_root / "output" / "results" / args.run_id
    log_root = args.output_root / "output" / "logs" / args.run_id
    report_root = args.output_root / "output" / "reports" / args.run_id
    timing_dir = result_root / "timing"
    for path in (result_root, log_root, report_root, timing_dir):
        path.mkdir(parents=True, exist_ok=True)

    policy = TimingPolicy(
        warmup_count=args.warmup,
        measured_repetitions=args.repetitions,
        timeout_seconds=args.timeout_seconds,
    )
    write_timing_policy(timing_dir, policy)
    write_environment_metadata(timing_dir, repo_root=REPO_ROOT, run_id=args.run_id)

    output_rows: list[dict[str, str]] = []
    speedups: list[float] = []
    for input_row in input_rows:
        case_id = input_row["case_id"]
        selected = selected_by_case.get(case_id)
        exact = input_row["exact"] == "true"
        timing_attempted = exact
        source_samples: list[float] = []
        candidate_samples: list[float] = []
        source_median: float | None = None
        candidate_median: float | None = None
        speedup_ratio: float | None = None
        timing_status = "not_timed"
        timing_failure_bucket = ""
        non_timing_reason = ""
        artifact_path = _runtime_artifact_path(timing_dir, case_id)

        if not exact:
            non_timing_reason = input_row["failure_bucket"] or "not_exact"
        elif selected is None:
            timing_status = "timing_failed"
            timing_failure_bucket = "selected_row_missing"
        else:
            candidate_path = Path(input_row["candidate_sql_trace"])
            if not candidate_path.exists():
                timing_status = "timing_failed"
                timing_failure_bucket = "candidate_sql_missing"
            else:
                try:
                    samples = _collect_postgres_samples(
                        repo_root=REPO_ROOT,
                        row=selected,
                        run_id=args.run_id,
                        candidate_sql_path=candidate_path,
                        policy=policy,
                        postgres_dsn_env=args.postgres_dsn_env,
                        db_schema_prefix=args.db_schema_prefix,
                        timing_dir=timing_dir,
                    )
                    source_samples = samples.source_runtime_samples_ms
                    candidate_samples = samples.candidate_runtime_samples_ms
                    source_median = _median(source_samples)
                    candidate_median = _median(candidate_samples)
                    if (
                        len(source_samples) == args.repetitions
                        and len(candidate_samples) == args.repetitions
                        and source_median is not None
                        and candidate_median is not None
                        and source_median > 0
                        and candidate_median > 0
                    ):
                        speedup_ratio = source_median / candidate_median
                        speedups.append(speedup_ratio)
                        timing_status = "timed"
                    else:
                        timing_status = "timing_failed"
                        timing_failure_bucket = "incomplete_or_non_positive_samples"
                except Exception as exc:  # keep rows visible and continue.
                    timing_status = "timing_failed"
                    timing_failure_bucket = f"{type(exc).__name__}"

        if timing_attempted:
            _write_runtime_artifact(
                path=artifact_path,
                row=input_row,
                policy=policy,
                timing_status=timing_status,
                timing_failure_bucket=timing_failure_bucket,
                source_samples=source_samples,
                candidate_samples=candidate_samples,
                source_median=source_median,
                candidate_median=candidate_median,
                speedup_ratio=speedup_ratio,
                runtime_root=args.output_root,
            )

        output_rows.append(
            {
                "case_id": case_id,
                "pool": input_row["pool"],
                "engine": "postgres",
                "method_id": "calcite_hep_fail_closed",
                "route_id": "calcite_hep_fail_closed",
                "exact_gate_source": "calcite_hep_pg_execution_checker_diagnostic_v0",
                "generation_status": input_row["generation_status"],
                "candidate_origin": input_row["candidate_origin"],
                "exact": input_row["exact"],
                "timing_attempted": _bool_text(timing_attempted),
                "source_timing_success": _bool_text(timing_status == "timed"),
                "candidate_timing_success": _bool_text(timing_status == "timed"),
                "timing_status": timing_status,
                "source_median_ms": _float_text(source_median),
                "candidate_median_ms": _float_text(candidate_median),
                "speedup_ratio": _float_text(speedup_ratio),
                "timing_failure_bucket": timing_failure_bucket,
                "non_timing_reason": non_timing_reason,
                "source_samples_ms": _samples_text(source_samples),
                "candidate_samples_ms": _samples_text(candidate_samples),
                "candidate_sql_sha256": input_row["candidate_sql_sha256"],
                "source_sql_trace": input_row["source_sql_trace"],
                "candidate_sql_trace": input_row["candidate_sql_trace"],
                "runtime_artifact_path": artifact_path.as_posix() if timing_attempted else "",
                "local_only": "true",
                "official_metric_input": "false",
                "paper_result": "false",
            }
        )

    _write_csv(args.audit_dir / "per_row_timing.csv", output_rows)
    _write_json(
        args.audit_dir / "diagnostic_summary.json",
        _summary(
            input_rows=input_rows,
            output_rows=output_rows,
            speedups=speedups,
            policy=policy,
            run_id=args.run_id,
            output_root=args.output_root,
        ),
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--audit-dir", type=Path, default=AUDIT_DIR)
    parser.add_argument("--run-id", default="calcite_hep_pg_exact_timing")
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument("--postgres-dsn-env", default="SQLRB_POSTGRES_DSN")
    parser.add_argument("--db-schema-prefix", default="sqlrb_calcite_pg_timing")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
