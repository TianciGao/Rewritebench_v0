#!/usr/bin/env python3
"""Time exact SQLGlot schema-aware optimize Track A diagnostic rows.

This audit helper consumes the prior 120-row execution/checker audit and times
only rows marked exact/result-consistent there. Runtime artifacts go under
/tmp using the D035 output/results|logs|reports shape. The committed outputs
remain limited to this audit packet.
"""

from __future__ import annotations

import csv
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from sql_rewrite_bench.case_package_resolver import resolve_case_package  # noqa: E402
from sql_rewrite_bench.case_selection import resolve_common_core_selection  # noqa: E402
from sql_rewrite_bench.local_timing import (  # noqa: E402
    TimingPolicy,
    collect_timing_for_row,
    write_environment_metadata,
    write_timing_policy,
)
from sql_rewrite_bench.user_run_schema import (  # noqa: E402
    CANDIDATE_PREFLIGHT_STATUS_PASSED,
    CHECKER_STATUS_SUCCESS,
    EXACT_STATUS_EXACT,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    FAILURE_NONE,
)


TASK_ID = "sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0"
RUN_ID = TASK_ID
METHOD_ID = "sqlglot"
ROUTE_ID = "sqlglot_optimize_schema_aware"
EXACT_GATE_SOURCE = "sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0"
RUNTIME_ROOT = Path(f"/tmp/sqlrb_{TASK_ID}")
OUTPUT_ROOT = RUNTIME_ROOT / "output"
RESULT_ROOT = OUTPUT_ROOT / "results" / RUN_ID
LOG_ROOT = OUTPUT_ROOT / "logs" / RUN_ID
REPORT_ROOT = OUTPUT_ROOT / "reports" / RUN_ID
TIMING_DIR = RESULT_ROOT / "timing"
SOURCE_AUDIT = REPO_ROOT / "audits" / EXACT_GATE_SOURCE / "per_row_execution_checker_status.csv"
AUDIT_DIR = Path(__file__).resolve().parent
ENGINE_ORDER = ("postgres", "mysql", "spark")

PER_ROW_FIELDS = [
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "exact_gate_source",
    "exact_result_consistent",
    "timing_attempted",
    "timing_success",
    "source_timing_success",
    "candidate_timing_success",
    "source_median_ms",
    "candidate_median_ms",
    "speedup_ratio",
    "timing_failure_bucket",
    "non_timing_reason",
    "source_samples_ms",
    "candidate_samples_ms",
    "runtime_artifact_path",
    "candidate_sql_path",
    "local_only",
    "official_metric_input",
    "paper_result",
]


def main() -> int:
    _prepare_runtime_dirs()
    source_rows = _read_csv(SOURCE_AUDIT)
    if len(source_rows) != 120:
        raise RuntimeError(f"expected 120 source rows, got {len(source_rows)}")

    selected = resolve_common_core_selection(
        repo_root=REPO_ROOT,
        case_set="common_core_v0",
        pool="all",
        engine="all",
        case_list=None,
        smoke=False,
    )
    selected_by_key = {(row.case_id, row.engine): row for row in selected}
    adapter = REPO_ROOT / "baselines" / "sqlglot" / "sqlglot_user_adapter.py"
    adapter_command = f"{sys.executable} {adapter} --route optimize_schema_aware"

    policy = TimingPolicy(warmup_count=1, measured_repetitions=5, timeout_seconds=30.0)
    write_timing_policy(TIMING_DIR, policy)
    environment_metadata_path = write_environment_metadata(
        TIMING_DIR, repo_root=REPO_ROOT, run_id=RUN_ID
    )

    per_row: list[dict[str, str]] = []
    for index, source_row in enumerate(_sort_source_rows(source_rows), start=1):
        case_id = source_row["case_id"]
        engine = source_row["engine"]
        exact = source_row["exact_result_consistent"] == "true"
        print(f"[{index:03d}/120] {case_id} / {engine} exact={exact}", flush=True)

        timing_row = _base_timing_row(source_row)
        if not exact:
            timing_row["non_timing_reason"] = _frontier_reason(source_row)
            per_row.append(timing_row)
            continue

        selected_row = selected_by_key.get((case_id, engine))
        if selected_row is None:
            timing_row.update(
                {
                    "timing_attempted": "true",
                    "timing_failure_bucket": "selected_row_missing",
                }
            )
            per_row.append(timing_row)
            continue

        candidate_sql_path = Path(source_row["candidate_sql_path"])
        if not candidate_sql_path.exists():
            timing_row.update(
                {
                    "timing_attempted": "true",
                    "timing_failure_bucket": "candidate_sql_missing",
                }
            )
            per_row.append(timing_row)
            continue

        resolved = resolve_case_package(repo_root=REPO_ROOT, row=selected_row)
        ledger = _ledger_from_source_row(source_row)
        result = collect_timing_for_row(
            ledger=ledger,
            row=selected_row,
            resolved_package=resolved,
            repo_root=REPO_ROOT,
            out_dir=RESULT_ROOT / "source_run",
            run_id=RUN_ID,
            adapter_command=adapter_command,
            policy=policy,
            postgres_dsn_env="SQLRB_POSTGRES_DSN",
            db_schema_prefix="sqlrb_schema_aware_track_a_120_timing",
            timing_dir=TIMING_DIR,
            environment_metadata_path=environment_metadata_path,
        )
        source_median = _median(result.source_runtime_samples_ms)
        candidate_median = _median(result.candidate_runtime_samples_ms)
        timing_success = result.timing_status == "timed" and result.speedup_ratio is not None
        timing_row.update(
            {
                "timing_attempted": "true",
                "timing_success": _bool(timing_success),
                "source_timing_success": _bool(timing_success),
                "candidate_timing_success": _bool(timing_success),
                "source_median_ms": _float_text(source_median),
                "candidate_median_ms": _float_text(candidate_median),
                "speedup_ratio": _float_text(result.speedup_ratio),
                "timing_failure_bucket": "" if timing_success else result.timing_na_reason,
                "source_samples_ms": _samples_text(result.source_runtime_samples_ms),
                "candidate_samples_ms": _samples_text(result.candidate_runtime_samples_ms),
                "runtime_artifact_path": result.timing_artifact_path.as_posix(),
            }
        )
        per_row.append(timing_row)

    _write_csv(AUDIT_DIR / "per_row_timing.csv", per_row, PER_ROW_FIELDS)
    summary = _summary(source_rows=source_rows, timing_rows=per_row)
    _write_json(AUDIT_DIR / "diagnostic_summary.json", summary)
    _write_runtime_manifest(summary, adapter_command)
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0


def _prepare_runtime_dirs() -> None:
    for path in (RESULT_ROOT, LOG_ROOT, REPORT_ROOT, TIMING_DIR):
        path.mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sort_source_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(rows, key=lambda row: (row["case_id"], ENGINE_ORDER.index(row["engine"])))


def _base_timing_row(source_row: dict[str, str]) -> dict[str, str]:
    return {
        "case_id": source_row["case_id"],
        "pool": source_row["pool"],
        "engine": source_row["engine"],
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "exact_gate_source": EXACT_GATE_SOURCE,
        "exact_result_consistent": source_row["exact_result_consistent"],
        "timing_attempted": "false",
        "timing_success": "false",
        "source_timing_success": "false",
        "candidate_timing_success": "false",
        "source_median_ms": "",
        "candidate_median_ms": "",
        "speedup_ratio": "",
        "timing_failure_bucket": "",
        "non_timing_reason": "",
        "source_samples_ms": "",
        "candidate_samples_ms": "",
        "runtime_artifact_path": "",
        "candidate_sql_path": source_row["candidate_sql_path"],
        "local_only": "true",
        "official_metric_input": "false",
        "paper_result": "false",
    }


def _ledger_from_source_row(source_row: dict[str, str]) -> dict[str, object]:
    return {
        "run_id": RUN_ID,
        "case_id": source_row["case_id"],
        "pool": source_row["pool"],
        "engine": source_row["engine"],
        "candidate_generated": "true",
        "candidate_sql_path": source_row["candidate_sql_path"],
        "candidate_preflight_status": CANDIDATE_PREFLIGHT_STATUS_PASSED,
        "source_execution_status": EXECUTION_STATUS_SOURCE_SUCCESS,
        "candidate_execution_status": EXECUTION_STATUS_CANDIDATE_SUCCESS,
        "checker_status": CHECKER_STATUS_SUCCESS,
        "exact_status": EXACT_STATUS_EXACT,
        "failure_bucket": FAILURE_NONE,
        "source_result_path": "",
        "candidate_result_path": "",
        "mismatch_artifact_path": "",
        "notes": "",
    }


def _frontier_reason(source_row: dict[str, str]) -> str:
    if source_row["fail_closed"] == "true":
        return source_row["fail_closed_bucket"] or source_row["failure_bucket"] or "fail_closed"
    if source_row["candidate_execution_failed"] == "true":
        return "candidate_execution_failed"
    if source_row["mismatch"] == "true":
        return source_row["mismatch_class"] or "mismatch"
    if source_row["candidate_generated"] != "true":
        return source_row["failure_bucket"] or "no_candidate"
    return source_row["failure_bucket"] or "not_exact"


def _summary(*, source_rows: list[dict[str, str]], timing_rows: list[dict[str, str]]) -> dict[str, Any]:
    speedups = [_float(row["speedup_ratio"]) for row in timing_rows if row["speedup_ratio"]]
    speedups = [value for value in speedups if value is not None]
    by_engine = _group_summary(source_rows, timing_rows, "engine")
    by_pool = _group_summary(source_rows, timing_rows, "pool")
    timing_failures = Counter(
        row["timing_failure_bucket"]
        for row in timing_rows
        if row["timing_attempted"] == "true" and row["timing_success"] != "true"
    )
    non_timed = Counter(row["non_timing_reason"] for row in timing_rows if row["timing_attempted"] != "true")
    return {
        "schema_version": "sqlglot_schema_aware_track_a_120_exact_timing_summary_v0",
        "task": TASK_ID,
        "run_id": RUN_ID,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "exact_gate_source": EXACT_GATE_SOURCE,
        "selected_rows": 120,
        "generated_candidate_rows": 105,
        "fail_closed_rows": 20,
        "candidate_executable_rows": 91,
        "checker_attempted_rows": 91,
        "exact_rows": 66,
        "non_exact_frontier_rows": 54,
        "timing_attempted_rows": _count_true(timing_rows, "timing_attempted"),
        "timed_exact_rows": _count_true(timing_rows, "timing_success"),
        "timing_failed_rows": sum(
            row["timing_attempted"] == "true" and row["timing_success"] != "true"
            for row in timing_rows
        ),
        "diagnostic_gm_speedup": _geomean(speedups),
        "diagnostic_speedup_p10": _percentile(speedups, 10),
        "diagnostic_speedup_p25": _percentile(speedups, 25),
        "diagnostic_speedup_p50": _percentile(speedups, 50),
        "diagnostic_speedup_p75": _percentile(speedups, 75),
        "diagnostic_speedup_p90": _percentile(speedups, 90),
        "median_speedup_diagnostic": statistics.median(speedups) if speedups else None,
        "by_engine": by_engine,
        "by_pool": by_pool,
        "timing_failure_bucket_counts": dict(sorted(timing_failures.items())),
        "non_timed_frontier_counts": dict(sorted(non_timed.items())),
        "timing_policy": {
            "warmup_count": 1,
            "measured_repetitions": 5,
            "timeout_seconds": 30.0,
            "statistic": "median",
            "exact_gated": True,
        },
        "runtime_output_root": RUNTIME_ROOT.as_posix(),
        "output_shape": {
            "results": RESULT_ROOT.as_posix(),
            "logs": LOG_ROOT.as_posix(),
            "reports": REPORT_ROOT.as_posix(),
        },
        "timing_collected": True,
        "verifier_run": False,
        "official_metric_input": False,
        "paper_result": False,
        "leaderboard_output_created": False,
    }


def _group_summary(
    source_rows: list[dict[str, str]], timing_rows: list[dict[str, str]], key: str
) -> dict[str, dict[str, Any]]:
    source_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    timing_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        source_groups[row[key]].append(row)
    for row in timing_rows:
        timing_groups[row[key]].append(row)
    output: dict[str, dict[str, Any]] = {}
    for name in sorted(source_groups):
        group_rows = timing_groups[name]
        speedups = [_float(row["speedup_ratio"]) for row in group_rows if row["speedup_ratio"]]
        speedups = [value for value in speedups if value is not None]
        output[name] = {
            "selected_rows": len(source_groups[name]),
            "exact_rows": sum(row["exact_result_consistent"] == "true" for row in source_groups[name]),
            "timing_attempted_rows": _count_true(group_rows, "timing_attempted"),
            "timed_exact_rows": _count_true(group_rows, "timing_success"),
            "timing_failed_rows": sum(
                row["timing_attempted"] == "true" and row["timing_success"] != "true"
                for row in group_rows
            ),
            "diagnostic_gm_speedup": _geomean(speedups),
            "diagnostic_speedup_p10": _percentile(speedups, 10),
            "diagnostic_speedup_p25": _percentile(speedups, 25),
            "diagnostic_speedup_p50": _percentile(speedups, 50),
            "diagnostic_speedup_p75": _percentile(speedups, 75),
            "diagnostic_speedup_p90": _percentile(speedups, 90),
        }
    return output


def _write_runtime_manifest(summary: dict[str, Any], adapter_command: str) -> None:
    manifest = {
        "run_id": RUN_ID,
        "task": TASK_ID,
        "adapter_command": adapter_command,
        "exact_gate_source": EXACT_GATE_SOURCE,
        "runtime_output_root": RUNTIME_ROOT.as_posix(),
        "result_root": RESULT_ROOT.as_posix(),
        "log_root": LOG_ROOT.as_posix(),
        "report_root": REPORT_ROOT.as_posix(),
        "summary": summary,
        "local_only": True,
        "official_metric_input": False,
        "paper_result": False,
        "leaderboard_output_created": False,
    }
    _write_json(RESULT_ROOT / "run_manifest.json", manifest)
    (REPORT_ROOT / "boundary.md").write_text(
        "# Boundary\n\n"
        "This is a local exact-gated timing diagnostic only. It is not an official "
        "metric, paper result, retained evidence promotion, verifier run, or leaderboard input.\n",
        encoding="utf-8",
    )


def _count_true(rows: list[dict[str, str]], field: str) -> int:
    return sum(row[field] == "true" for row in rows)


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _samples_text(values: list[float]) -> str:
    return json.dumps([round(value, 6) for value in values], separators=(",", ":"))


def _float(value: str) -> float | None:
    if value == "":
        return None
    return float(value)


def _float_text(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6f}"


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    return float(statistics.median(values))


def _geomean(values: list[float]) -> float | None:
    if not values or any(value <= 0 for value in values):
        return None
    return float(math.exp(sum(math.log(value) for value in values) / len(values)))


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


if __name__ == "__main__":
    raise SystemExit(main())
