"""Non-official local metrics for user-entry diagnostic runs.

This module reads ``runs/user/<run_name>`` artifacts and writes local-only
diagnostic summaries under ``runs/user/<run_name>/metrics``. It does not
compute official metrics, update reports/results, promote retained evidence,
render paper tables, or create leaderboard output.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .local_timing import route_identity
from .user_run_schema import (
    CANDIDATE_PREFLIGHT_STATUS_PASSED,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_MISMATCH,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    FAILURE_NONE,
    FAILURE_UNSUPPORTED_ENGINE,
    LEDGER_FIELDS,
    SELECTED_CASE_FIELDS,
    TIMING_STATUS_PARTIAL_FAILURE,
    TIMING_STATUS_TIMED,
)

BOUNDARY_FLAGS = {
    "local_diagnostic_only": True,
    "official_metric_input": False,
    "paper_result_input": False,
    "retained_evidence_promoted": False,
    "leaderboard_input": False,
}

NA_METRIC = {
    "value": None,
    "status": "not_applicable",
}

PERCENTILES = (10, 25, 50, 75, 90)

AGGREGATE_RUN_ALLOWED_NAMES = {
    "config.yaml",
    "ledger.csv",
    "selected_cases.csv",
    "summary.json",
    "metrics",
}

ENGINE_FIELDS = [
    "local_run_id",
    "route_id",
    "method_id",
    "engine",
    "timing_policy_id",
    "denominator_ids",
    "selected",
    "candidate_generated",
    "generation_rate",
    "preflight_passed",
    "source_executable",
    "candidate_executable",
    "execution_coverage_rate",
    "exact",
    "result_consistency_rate",
    "mismatch",
    "label_only_mismatch",
    "unsupported_fail_closed",
    "timing_eligible",
    "timed",
    "timing_partial_failure",
    "speedup_denominator",
    "gm_speedup_ratio",
    "speedup_p10",
    "speedup_p25",
    "speedup_p50",
    "speedup_p75",
    "speedup_p90",
    "performance_na_reason",
    "semantic_equivalence_rate_status",
    "cross_engine_gm_speedup_status",
    "pocr_status",
    "local_diagnostic_only",
    "official_metric_input",
    "paper_result_input",
    "retained_evidence_promoted",
    "leaderboard_input",
]

POOL_FIELDS = [
    "local_run_id",
    "route_id",
    "method_id",
    "pool",
    "engine_ids",
    "timing_policy_id",
    "denominator_ids",
    "selected",
    "candidate_generated",
    "generation_rate",
    "preflight_passed",
    "source_executable",
    "candidate_executable",
    "execution_coverage_rate",
    "exact",
    "result_consistency_rate",
    "mismatch",
    "label_only_mismatch",
    "unsupported_fail_closed",
    "timing_eligible",
    "timed",
    "timing_partial_failure",
    "speedup_denominator",
    "gm_speedup_ratio",
    "speedup_p10",
    "speedup_p25",
    "speedup_p50",
    "speedup_p75",
    "speedup_p90",
    "performance_na_reason",
    "semantic_equivalence_rate_status",
    "cross_engine_gm_speedup_status",
    "pocr_status",
    "local_diagnostic_only",
    "official_metric_input",
    "paper_result_input",
    "retained_evidence_promoted",
    "leaderboard_input",
]

SPEEDUP_ROW_FIELDS = [
    "local_run_id",
    "route_id",
    "method_id",
    "engine",
    "pool",
    "case_id",
    "denominator_id",
    "timing_policy_id",
    "exact_status",
    "failure_bucket",
    "label_only_mismatch",
    "timing_eligible",
    "timing_status",
    "source_median_ms",
    "candidate_median_ms",
    "speedup_ratio",
    "included_in_performance",
    "exclusion_reason",
    "timing_artifact_path",
    "local_diagnostic_only",
    "official_metric_input",
    "paper_result_input",
    "retained_evidence_promoted",
    "leaderboard_input",
]


@dataclass(frozen=True)
class LocalMetricsOutputs:
    metrics_dir: Path
    summary_path: Path
    by_engine_path: Path
    by_pool_path: Path
    speedup_rows_path: Path
    boundary_path: Path


def compute_and_write_local_metrics(run_dir: Path) -> LocalMetricsOutputs:
    """Compute local diagnostic metrics for one user-run directory."""

    metrics = compute_local_metrics(run_dir)
    return _write_metrics_outputs(run_dir, metrics)


def compute_and_write_aggregate_local_metrics(
    run_dirs: list[Path],
    aggregate_run_dir: Path,
    *,
    aggregate_run_id: str,
) -> LocalMetricsOutputs:
    """Compute canonical local metrics for a multi-run local diagnostic aggregate."""

    source_run_dirs = [Path(run_dir) for run_dir in run_dirs]
    _validate_aggregate_run_dir_safe(aggregate_run_dir, source_run_dirs)
    metrics = compute_aggregate_local_metrics(
        source_run_dirs,
        aggregate_run_id=aggregate_run_id,
        aggregate_run_dir=aggregate_run_dir,
    )
    _write_aggregate_source_run(
        aggregate_run_dir=aggregate_run_dir,
        metrics=metrics,
        source_run_dirs=source_run_dirs,
        aggregate_run_id=aggregate_run_id,
    )
    return _write_metrics_outputs(aggregate_run_dir, metrics)


def _write_metrics_outputs(run_dir: Path, metrics: dict[str, Any]) -> LocalMetricsOutputs:
    """Write already-computed local metrics artifacts under a run directory."""

    metrics_dir = run_dir / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    summary_path = metrics_dir / "local_metrics_summary.json"
    by_engine_path = metrics_dir / "local_metrics_by_engine.csv"
    by_pool_path = metrics_dir / "local_metrics_by_pool.csv"
    speedup_rows_path = metrics_dir / "local_timing_speedup_rows.csv"
    boundary_path = metrics_dir / "local_metrics_boundary.md"

    summary_path.write_text(
        json.dumps(metrics["summary"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_csv(by_engine_path, metrics["by_engine"], ENGINE_FIELDS)
    _write_csv(by_pool_path, metrics["by_pool"], POOL_FIELDS)
    _write_csv(speedup_rows_path, metrics["speedup_rows"], SPEEDUP_ROW_FIELDS)
    boundary_path.write_text(_boundary_markdown(metrics["summary"]), encoding="utf-8")
    return LocalMetricsOutputs(
        metrics_dir=metrics_dir,
        summary_path=summary_path,
        by_engine_path=by_engine_path,
        by_pool_path=by_pool_path,
        speedup_rows_path=speedup_rows_path,
        boundary_path=boundary_path,
    )


def compute_local_metrics(run_dir: Path) -> dict[str, Any]:
    """Return local diagnostic metrics payloads for one user-run directory."""

    run_path = Path(run_dir)
    enriched_rows, run_id = _load_enriched_rows(run_path)
    return _metrics_from_enriched_rows(
        enriched_rows,
        run_path=run_path,
        run_id=run_id,
        aggregate=False,
        source_run_ids=[run_id],
        source_run_paths=[run_path.as_posix()],
    )


def compute_aggregate_local_metrics(
    run_dirs: list[Path],
    *,
    aggregate_run_id: str,
    aggregate_run_dir: Path | None = None,
) -> dict[str, Any]:
    """Return local diagnostic metrics for a canonical multi-run aggregate.

    The aggregate path is intended for D035 Track A-style runs where the user
    facade creates one source run per engine, for example
    ``<run_id>__postgres``, ``<run_id>__mysql``, and ``<run_id>__spark``.
    """

    source_run_dirs = [Path(run_dir) for run_dir in run_dirs]
    if not source_run_dirs:
        raise ValueError("at least one source run directory is required")
    if (
        not aggregate_run_id
        or aggregate_run_id in {".", ".."}
        or "/" in aggregate_run_id
        or "\\" in aggregate_run_id
        or ".." in Path(aggregate_run_id).parts
    ):
        raise ValueError("aggregate_run_id must be a single non-empty path component")

    enriched_rows: list[dict[str, Any]] = []
    source_run_ids: list[str] = []
    source_run_paths: list[str] = []
    for source_run_dir in source_run_dirs:
        source_enriched, source_run_id = _load_enriched_rows(
            source_run_dir,
            local_run_id_override=aggregate_run_id,
        )
        source_run_ids.append(source_run_id)
        source_run_paths.append(source_run_dir.as_posix())
        for row in source_enriched:
            row["source_run_id"] = source_run_id
            row["source_run_path"] = source_run_dir.as_posix()
        enriched_rows.extend(source_enriched)

    return _metrics_from_enriched_rows(
        enriched_rows,
        run_path=aggregate_run_dir or Path(aggregate_run_id),
        run_id=aggregate_run_id,
        aggregate=True,
        source_run_ids=source_run_ids,
        source_run_paths=source_run_paths,
    )


def _load_enriched_rows(
    run_dir: Path,
    *,
    local_run_id_override: str | None = None,
) -> tuple[list[dict[str, Any]], str]:
    ledger_path = run_dir / "ledger.csv"
    if not ledger_path.exists():
        raise ValueError(f"ledger.csv is required for local metrics: {ledger_path}")
    ledger_rows = _read_csv(ledger_path)
    config = _read_config(run_dir / "config.yaml")
    summary = _read_json_if_exists(run_dir / "summary.json")
    source_run_id = _text(config.get("run_id") or summary.get("run_id") or run_dir.name)
    local_run_id = local_run_id_override or source_run_id
    timing_rows = _load_timing_rows(run_dir)
    default_route_id, default_method_id = route_identity(_text(config.get("adapter_command")))
    enriched_rows = []
    for row in ledger_rows:
        row_for_metrics = dict(row)
        if local_run_id_override:
            row_for_metrics["run_id"] = local_run_id
        enriched_rows.append(
            _enrich_row(
                row_for_metrics,
                timing_rows=timing_rows,
                run_id=local_run_id,
                default_route_id=default_route_id,
                default_method_id=default_method_id,
            )
        )
    return enriched_rows, source_run_id


def _metrics_from_enriched_rows(
    enriched_rows: list[dict[str, Any]],
    *,
    run_path: Path,
    run_id: str,
    aggregate: bool,
    source_run_ids: list[str],
    source_run_paths: list[str],
) -> dict[str, Any]:
    route_groups = _group_rows(enriched_rows, ("local_run_id", "route_id", "method_id"))
    overall = (
        _summarize_group(enriched_rows)
        if len(route_groups) <= 1
        else {
            "status": "not_available",
            "reason": "multiple_routes_present_route_mixing_disallowed",
            "route_group_count": len(route_groups),
            **BOUNDARY_FLAGS,
        }
    )
    by_engine = [
        _summary_to_engine_row(key, _summarize_group(rows))
        for key, rows in sorted(_group_rows(enriched_rows, ("local_run_id", "route_id", "method_id", "engine", "timing_policy_id")).items())
    ]
    by_pool = [
        _summary_to_pool_row(key, _summarize_group(rows))
        for key, rows in sorted(_group_rows(enriched_rows, ("local_run_id", "route_id", "method_id", "pool", "timing_policy_id")).items())
    ]
    per_denominator_rows = [
        _per_denominator_row(row)
        for row in sorted(
            enriched_rows,
            key=lambda item: (
                item["local_run_id"],
                item["route_id"],
                item["method_id"],
                item["engine"],
                item["denominator_id"],
                item["timing_policy_id"],
            ),
        )
    ]
    speedup_rows = [_speedup_row(row) for row in per_denominator_rows]

    summary_payload = {
        "schema_version": "local_metrics_summary_v0",
        "created_at_utc": _utc_now_iso(),
        "run_path": run_path.as_posix(),
        "local_run_id": run_id,
        "route_ids": sorted({row["route_id"] for row in enriched_rows}),
        "method_ids": sorted({row["method_id"] for row in enriched_rows}),
        "grouping_policy": {
            "route_aware": True,
            "method_aware": True,
            "engine_aware": True,
            "denominator_aware": True,
            "timing_policy_aware": True,
            "multi_engine_aggregate_supported": True,
            "route_mixing_allowed": False,
            "leaderboard_output": False,
            "method_ordering_output": False,
        },
        "aggregation_policy": {
            "multi_run_aggregate": aggregate,
            "source_run_count": len(source_run_ids),
            "source_run_ids": source_run_ids,
            "source_run_paths": source_run_paths,
            "denominator_combination": "sum_selected_rows_across_source_runs",
            "timing_combination": "concatenate_strict_exact_timed_rows_across_source_runs",
            "official_metric_input": False,
        },
        "metric_definitions": _metric_definitions(),
        "overall": overall,
        "by_engine": by_engine,
        "by_pool": by_pool,
        "per_denominator_rows": per_denominator_rows,
        "diagnostic_status_counts": _diagnostic_status_counts(enriched_rows),
        "deferred_metrics": {
            "regression_at_20": {
                "status": "not_implemented",
                "reason": "removed_from_formal_local_metrics_v0_scope_by_D033",
            },
            "semantic_equivalence_rate": {
                **NA_METRIC,
                "reason": "formal_verifier_evidence_missing",
            },
            "cross_engine_gm_speedup_ratio": {
                **NA_METRIC,
                "reason": "target_engine_paired_timing_missing",
            },
            "positive_operation_coverage_rate": {
                **NA_METRIC,
                "reason": "external_skill_adapter_pending",
                "skill_adapter_pending": True,
            },
        },
        "prohibited_outputs": {
            "method_selection_output_emitted": False,
            "method_ordering_output_emitted": False,
            "leaderboard_output_created": False,
            "paper_table_rendered": False,
            "reports_results_updated": False,
            "retained_evidence_promoted": False,
        },
        **BOUNDARY_FLAGS,
    }
    return {
        "summary": summary_payload,
        "by_engine": by_engine,
        "by_pool": by_pool,
        "speedup_rows": speedup_rows,
        "aggregate_source_rows": enriched_rows,
    }


def _write_aggregate_source_run(
    *,
    aggregate_run_dir: Path,
    metrics: dict[str, Any],
    source_run_dirs: list[Path],
    aggregate_run_id: str,
) -> None:
    """Create a minimal source-run directory for exporting aggregate metrics."""

    aggregate_run_dir.mkdir(parents=True, exist_ok=True)
    enriched_rows = metrics.get("aggregate_source_rows", [])
    ledger_rows = [_aggregate_ledger_row(row, aggregate_run_id) for row in enriched_rows]
    selected_case_rows = [_selected_case_row(row, aggregate_run_id) for row in ledger_rows if _is_true(row.get("selected"))]
    source_configs = [_read_config(run_dir / "config.yaml") for run_dir in source_run_dirs]
    adapter_commands = sorted({_text(config.get("adapter_command")) for config in source_configs if _text(config.get("adapter_command"))})
    case_sets = sorted({_text(config.get("case_set")) for config in source_configs if _text(config.get("case_set"))})
    pools = sorted({_text(config.get("pool")) for config in source_configs if _text(config.get("pool"))})
    engines = sorted({_text(row.get("engine")) for row in ledger_rows if _text(row.get("engine"))})
    source_run_ids = metrics["summary"]["aggregation_policy"]["source_run_ids"]
    overall = metrics["summary"].get("overall", {})
    counts = overall.get("counts", {}) if isinstance(overall, dict) else {}
    config = {
        "run_id": aggregate_run_id,
        "created_at_utc": _utc_now_iso(),
        "case_set": case_sets[0] if len(case_sets) == 1 else ",".join(case_sets),
        "pool": pools[0] if len(pools) == 1 else ",".join(pools) or "all",
        "engine": ",".join(engines),
        "adapter_command": adapter_commands[0] if len(adapter_commands) == 1 else "",
        "out_dir": aggregate_run_dir.as_posix(),
        "local_metrics_aggregate": True,
        "source_run_ids": ";".join(source_run_ids),
        "db_execution_enabled": True,
        "checker_enabled": True,
        "timing_enabled": bool(counts.get("timed", 0)),
        "official_metrics_computed": False,
        "paper_results_updated": False,
        "retained_evidence_updated": False,
        "no_global_leaderboard": True,
    }
    _write_config(aggregate_run_dir / "config.yaml", config)
    _write_csv(aggregate_run_dir / "ledger.csv", ledger_rows, LEDGER_FIELDS)
    _write_csv(aggregate_run_dir / "selected_cases.csv", selected_case_rows, SELECTED_CASE_FIELDS)
    (aggregate_run_dir / "summary.json").write_text(
        json.dumps(
            {
                "schema_version": "aggregate_user_run_summary_v0",
                "run_id": aggregate_run_id,
                "source_run_ids": source_run_ids,
                "source_run_paths": metrics["summary"]["aggregation_policy"]["source_run_paths"],
                "selected_rows": counts.get("selected", 0),
                "candidate_generated_rows": counts.get("candidate_generated", 0),
                "candidate_preflight_passed_rows": counts.get("preflight_passed", 0),
                "source_executable_rows": counts.get("source_executable", 0),
                "candidate_executable_rows": counts.get("candidate_executable", 0),
                "exact_rows": counts.get("exact", 0),
                "mismatch_rows": counts.get("mismatch", 0),
                "timed_rows": counts.get("timed", 0),
                "local_diagnostic_only": True,
                "official_metric_input": False,
                "paper_result_input": False,
                "retained_evidence_promoted": False,
                "leaderboard_input": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _aggregate_ledger_row(row: dict[str, Any], aggregate_run_id: str) -> dict[str, str]:
    ledger_row = {field: _text(row.get(field)) for field in LEDGER_FIELDS}
    ledger_row["run_id"] = aggregate_run_id
    return ledger_row


def _selected_case_row(row: dict[str, str], aggregate_run_id: str) -> dict[str, str]:
    return {
        "run_id": aggregate_run_id,
        "case_id": _text(row.get("case_id")),
        "pool": _text(row.get("pool")),
        "engine": _text(row.get("engine")),
        "denominator_id": _text(row.get("denominator_id")),
        "planned": _text(row.get("planned")),
        "case_path": _text(row.get("case_path")),
        "source_sql_path": _text(row.get("source_sql_path")),
    }


def _write_config(path: Path, config: dict[str, object]) -> None:
    lines = []
    for key, value in config.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif value is None:
            rendered = ""
        else:
            rendered = str(value)
        lines.append(f"{key}: {rendered}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _validate_aggregate_run_dir_safe(aggregate_run_dir: Path, source_run_dirs: list[Path]) -> None:
    aggregate_resolved = aggregate_run_dir.resolve()
    source_resolved = {run_dir.resolve() for run_dir in source_run_dirs}
    if aggregate_resolved in source_resolved:
        raise ValueError("aggregate_run_dir must be distinct from source run directories")
    if not aggregate_run_dir.exists():
        return
    unexpected = sorted(
        child.name
        for child in aggregate_run_dir.iterdir()
        if child.name not in AGGREGATE_RUN_ALLOWED_NAMES
    )
    if unexpected:
        raise ValueError(
            "aggregate_run_dir contains non-aggregate artifacts that could be exported as stale output: "
            + ", ".join(unexpected)
        )


def _enrich_row(
    row: dict[str, str],
    *,
    timing_rows: dict[str, dict[str, Any]],
    run_id: str,
    default_route_id: str,
    default_method_id: str,
) -> dict[str, Any]:
    timing = _timing_for_row(row, timing_rows)
    route_id = _text(timing.get("route_id") if timing else "") or default_route_id
    method_id = _text(timing.get("method_id") if timing else "") or default_method_id
    timing_policy_id = _text(timing.get("timing_policy_id") if timing else "") or "not_timed"
    speedup_ratio = _float_or_none(timing.get("speedup_ratio") if timing else row.get("speedup_ratio"))
    source_median = _float_or_none(timing.get("source_median_ms") if timing else None)
    candidate_median = _float_or_none(timing.get("candidate_median_ms") if timing else None)
    label_only = _is_true(timing.get("label_only_mismatch") if timing else None) or "label_only_mismatch=true" in _text(row.get("notes"))
    timing_status = _text(timing.get("timing_status") if timing else row.get("timing_status")) or "not_requested"
    timing_eligible = _is_true(timing.get("timing_eligible") if timing else row.get("timing_eligible"))
    exact_status = _text(row.get("exact_status"))
    failure_bucket = _text(row.get("failure_bucket"))
    performance_exclusion = _performance_exclusion_reason(
        exact_status=exact_status,
        failure_bucket=failure_bucket,
        label_only=label_only,
        timing_eligible=timing_eligible,
        timing_status=timing_status,
        speedup_ratio=speedup_ratio,
        source_median=source_median,
        candidate_median=candidate_median,
    )
    return {
        **row,
        "local_run_id": run_id,
        "route_id": route_id,
        "method_id": method_id,
        "timing_policy_id": timing_policy_id,
        "timing_artifact_path": _text(row.get("timing_artifact_path") or (timing or {}).get("_artifact_path")),
        "selected_bool": _is_true(row.get("selected")),
        "candidate_generated_bool": _is_true(row.get("candidate_generated")),
        "preflight_passed_bool": _is_true(row.get("candidate_preflight_passed")) or _text(row.get("candidate_preflight_status")) == CANDIDATE_PREFLIGHT_STATUS_PASSED,
        "source_executable_bool": _text(row.get("source_execution_status")) == EXECUTION_STATUS_SOURCE_SUCCESS,
        "candidate_executable_bool": _text(row.get("candidate_execution_status")) == EXECUTION_STATUS_CANDIDATE_SUCCESS,
        "exact_bool": exact_status == EXACT_STATUS_EXACT,
        "mismatch_bool": exact_status == EXACT_STATUS_MISMATCH or failure_bucket == "mismatch",
        "label_only_mismatch_bool": label_only,
        "unsupported_fail_closed_bool": failure_bucket == FAILURE_UNSUPPORTED_ENGINE,
        "timing_eligible_bool": timing_eligible,
        "timed_bool": timing_status == TIMING_STATUS_TIMED,
        "timing_partial_failure_bool": timing_status == TIMING_STATUS_PARTIAL_FAILURE,
        "source_median_ms": source_median,
        "candidate_median_ms": candidate_median,
        "speedup_ratio_float": speedup_ratio,
        "included_in_performance": performance_exclusion == "",
        "performance_exclusion_reason": performance_exclusion,
    }


def _performance_exclusion_reason(
    *,
    exact_status: str,
    failure_bucket: str,
    label_only: bool,
    timing_eligible: bool,
    timing_status: str,
    speedup_ratio: float | None,
    source_median: float | None,
    candidate_median: float | None,
) -> str:
    if exact_status != EXACT_STATUS_EXACT:
        return "not_exact"
    if failure_bucket != FAILURE_NONE:
        return "failure_bucket"
    if label_only:
        return "label_only_mismatch"
    if not timing_eligible:
        return "timing_not_eligible"
    if timing_status != TIMING_STATUS_TIMED:
        if timing_status == TIMING_STATUS_PARTIAL_FAILURE:
            return "timing_partial_failure"
        return "not_timed"
    if speedup_ratio is None or speedup_ratio <= 0:
        return "invalid_speedup_ratio"
    if source_median is None or candidate_median is None or source_median <= 0 or candidate_median <= 0:
        return "invalid_median"
    return ""


def _summarize_group(rows: list[dict[str, Any]]) -> dict[str, Any]:
    selected = sum(row["selected_bool"] for row in rows)
    generated = sum(row["candidate_generated_bool"] for row in rows)
    preflight = sum(row["preflight_passed_bool"] for row in rows)
    source_executable = sum(row["source_executable_bool"] for row in rows)
    candidate_executable = sum(row["candidate_executable_bool"] for row in rows)
    exact = sum(row["exact_bool"] for row in rows)
    mismatch = sum(row["mismatch_bool"] for row in rows)
    label_only = sum(row["label_only_mismatch_bool"] for row in rows)
    unsupported = sum(row["unsupported_fail_closed_bool"] for row in rows)
    timing_eligible = sum(row["timing_eligible_bool"] for row in rows)
    timed = sum(row["timed_bool"] for row in rows)
    partial = sum(row["timing_partial_failure_bool"] for row in rows)
    speedups = [
        float(row["speedup_ratio_float"])
        for row in rows
        if row["included_in_performance"]
    ]
    return {
        "denominator_ids": sorted({_text(row.get("denominator_id")) for row in rows}),
        "engine_ids": sorted({_text(row.get("engine")) for row in rows}),
        "counts": {
            "selected": selected,
            "candidate_generated": generated,
            "preflight_passed": preflight,
            "source_executable": source_executable,
            "candidate_executable": candidate_executable,
            "exact": exact,
            "mismatch": mismatch,
            "label_only_mismatch": label_only,
            "unsupported_fail_closed": unsupported,
            "timing_eligible": timing_eligible,
            "timed": timed,
            "timing_partial_failure": partial,
            "speedup_denominator": len(speedups),
        },
        "rates": {
            "generation_rate": _rate(generated, selected),
            "execution_coverage_rate": _rate(candidate_executable, selected),
            "result_consistency_rate": _rate(exact, selected),
        },
        "performance": _performance_summary(speedups, exact_rows=exact),
        "diagnostics": {
            "preflight_passed_is_metric_numerator": False,
            "source_executable_is_metric_numerator": False,
            "label_only_mismatch_treated_as_exact": False,
            "unsupported_fail_closed_rows_visible": True,
            "semantic_equivalence_rate": {
                **NA_METRIC,
                "reason": "formal_verifier_evidence_missing",
            },
            "cross_engine_gm_speedup_ratio": {
                **NA_METRIC,
                "reason": "target_engine_paired_timing_missing",
            },
            "positive_operation_coverage_rate": {
                **NA_METRIC,
                "reason": "external_skill_adapter_pending",
                "skill_adapter_pending": True,
            },
        },
        **BOUNDARY_FLAGS,
    }


def _performance_summary(speedups: list[float], *, exact_rows: int) -> dict[str, Any]:
    if not speedups:
        reason = "no_exact_timed_rows" if exact_rows else "no_exact_rows"
        return {
            "gm_speedup_ratio": None,
            "speedup_percentiles": {f"p{p}": None for p in PERCENTILES},
            "speedup_denominator": 0,
            "performance_na_reason": reason,
        }
    return {
        "gm_speedup_ratio": _geomean(speedups),
        "speedup_percentiles": {
            f"p{p}": _percentile(speedups, p) for p in PERCENTILES
        },
        "speedup_denominator": len(speedups),
        "performance_na_reason": "",
    }


def _summary_to_engine_row(key: tuple[str, ...], summary: dict[str, Any]) -> dict[str, Any]:
    local_run_id, route_id, method_id, engine, timing_policy_id = key
    row = _flat_summary_row(summary)
    row.update(
        {
            "local_run_id": local_run_id,
            "route_id": route_id,
            "method_id": method_id,
            "engine": engine,
            "timing_policy_id": timing_policy_id,
            "denominator_ids": ";".join(summary["denominator_ids"]),
        }
    )
    return row


def _summary_to_pool_row(key: tuple[str, ...], summary: dict[str, Any]) -> dict[str, Any]:
    local_run_id, route_id, method_id, pool, timing_policy_id = key
    row = _flat_summary_row(summary)
    row.update(
        {
            "local_run_id": local_run_id,
            "route_id": route_id,
            "method_id": method_id,
            "pool": pool,
            "engine_ids": ";".join(summary["engine_ids"]),
            "timing_policy_id": timing_policy_id,
            "denominator_ids": ";".join(summary["denominator_ids"]),
        }
    )
    return row


def _flat_summary_row(summary: dict[str, Any]) -> dict[str, Any]:
    counts = summary["counts"]
    rates = summary["rates"]
    performance = summary["performance"]
    percentiles = performance["speedup_percentiles"]
    return {
        "selected": counts["selected"],
        "candidate_generated": counts["candidate_generated"],
        "generation_rate": _format_optional(rates["generation_rate"]),
        "preflight_passed": counts["preflight_passed"],
        "source_executable": counts["source_executable"],
        "candidate_executable": counts["candidate_executable"],
        "execution_coverage_rate": _format_optional(rates["execution_coverage_rate"]),
        "exact": counts["exact"],
        "result_consistency_rate": _format_optional(rates["result_consistency_rate"]),
        "mismatch": counts["mismatch"],
        "label_only_mismatch": counts["label_only_mismatch"],
        "unsupported_fail_closed": counts["unsupported_fail_closed"],
        "timing_eligible": counts["timing_eligible"],
        "timed": counts["timed"],
        "timing_partial_failure": counts["timing_partial_failure"],
        "speedup_denominator": counts["speedup_denominator"],
        "gm_speedup_ratio": _format_optional(performance["gm_speedup_ratio"]),
        "speedup_p10": _format_optional(percentiles["p10"]),
        "speedup_p25": _format_optional(percentiles["p25"]),
        "speedup_p50": _format_optional(percentiles["p50"]),
        "speedup_p75": _format_optional(percentiles["p75"]),
        "speedup_p90": _format_optional(percentiles["p90"]),
        "performance_na_reason": performance["performance_na_reason"],
        "semantic_equivalence_rate_status": "not_applicable",
        "cross_engine_gm_speedup_status": "not_applicable",
        "pocr_status": "deferred",
        **_csv_boundary_flags(),
    }


def _per_denominator_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "local_run_id": row["local_run_id"],
        "route_id": row["route_id"],
        "method_id": row["method_id"],
        "engine": row.get("engine", ""),
        "pool": row.get("pool", ""),
        "case_id": row.get("case_id", ""),
        "denominator_id": row.get("denominator_id", ""),
        "timing_policy_id": row["timing_policy_id"],
        "selected": row["selected_bool"],
        "candidate_generated": row["candidate_generated_bool"],
        "preflight_passed": row["preflight_passed_bool"],
        "source_executable": row["source_executable_bool"],
        "candidate_executable": row["candidate_executable_bool"],
        "exact": row["exact_bool"],
        "mismatch": row["mismatch_bool"],
        "label_only_mismatch": row["label_only_mismatch_bool"],
        "unsupported_fail_closed": row["unsupported_fail_closed_bool"],
        "timing_eligible": row["timing_eligible_bool"],
        "timed": row["timed_bool"],
        "timing_partial_failure": row["timing_partial_failure_bool"],
        "source_median_ms": row["source_median_ms"],
        "candidate_median_ms": row["candidate_median_ms"],
        "speedup_ratio": row["speedup_ratio_float"],
        "included_in_performance": row["included_in_performance"],
        "performance_exclusion_reason": row["performance_exclusion_reason"],
        "timing_artifact_path": row["timing_artifact_path"],
        "exact_status": row.get("exact_status", ""),
        "failure_bucket": row.get("failure_bucket", ""),
        "timing_status": row.get("timing_status", ""),
    }


def _speedup_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "local_run_id": row["local_run_id"],
        "route_id": row["route_id"],
        "method_id": row["method_id"],
        "engine": row["engine"],
        "pool": row["pool"],
        "case_id": row["case_id"],
        "denominator_id": row["denominator_id"],
        "timing_policy_id": row["timing_policy_id"],
        "exact_status": row["exact_status"],
        "failure_bucket": row["failure_bucket"],
        "label_only_mismatch": _csv_bool(row["label_only_mismatch"]),
        "timing_eligible": _csv_bool(row["timing_eligible"]),
        "timing_status": row["timing_status"],
        "source_median_ms": _format_optional(row["source_median_ms"]),
        "candidate_median_ms": _format_optional(row["candidate_median_ms"]),
        "speedup_ratio": _format_optional(row["speedup_ratio"]),
        "included_in_performance": _csv_bool(row["included_in_performance"]),
        "exclusion_reason": row["performance_exclusion_reason"],
        "timing_artifact_path": row["timing_artifact_path"],
        **_csv_boundary_flags(),
    }


def _load_timing_rows(run_dir: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    timing_dir = run_dir / "timing" / "rows"
    if not timing_dir.exists():
        return rows
    for path in sorted(timing_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_artifact_path"] = path.as_posix()
        rows[_timing_key(data)] = data
    return rows


def _timing_for_row(row: dict[str, str], timing_rows: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    key = ":".join(
        [
            _text(row.get("case_id")),
            _text(row.get("engine")),
            _text(row.get("denominator_id")),
        ]
    )
    return timing_rows.get(key)


def _timing_key(timing: dict[str, Any]) -> str:
    return ":".join(
        [
            _text(timing.get("case_id")),
            _text(timing.get("engine")),
            _text(timing.get("denominator_id")),
        ]
    )


def _diagnostic_status_counts(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    fields = [
        "candidate_preflight_status",
        "source_execution_status",
        "candidate_execution_status",
        "checker_status",
        "exact_status",
        "failure_bucket",
        "timing_status",
    ]
    return {
        field: dict(sorted(Counter(_text(row.get(field)) for row in rows).items()))
        for field in fields
    }


def _group_rows(rows: list[dict[str, Any]], fields: tuple[str, ...]) -> dict[tuple[str, ...], list[dict[str, Any]]]:
    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(_text(row.get(field)) for field in fields)].append(row)
    return grouped


def _metric_definitions() -> dict[str, Any]:
    return {
        "generation_rate": {
            "formula": "candidate_generated / selected",
            "preflight_passed_in_numerator": False,
        },
        "execution_coverage_rate": {
            "formula": "candidate_executable / selected",
            "source_executable_in_numerator": False,
        },
        "result_consistency_rate": {
            "formula": "exact / selected",
            "label_only_mismatch_counts_as_exact": False,
        },
        "gm_speedup_ratio": {
            "formula": "geometric_mean(speedup_ratio) over strict exact + timed rows",
            "official_metric": False,
        },
        "speedup_ratio_percentiles": {
            "formula": "linear interpolation percentiles over strict exact + timed rows",
            "percentiles": list(PERCENTILES),
            "official_metric": False,
        },
    }


def _boundary_markdown(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Local Metrics Boundary",
            "",
            "This output is local diagnostic metrics only.",
            "",
            f"- Run id: `{summary.get('local_run_id', '')}`",
            "- Official metric input: `false`",
            "- Paper result input: `false`",
            "- Retained evidence promoted: `false`",
            "- Leaderboard input: `false`",
            "- Reports/results updated: `false`",
            "- Paper tables rendered: `false`",
            "",
            "These summaries must not be treated as official metrics or paper evidence.",
            "",
        ]
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _read_config(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    config: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        config[key.strip()] = value.strip().strip('"')
    return config


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _rate(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return numerator / denominator


def _geomean(values: list[float]) -> float:
    return math.exp(sum(math.log(value) for value in values) / len(values))


def _percentile(values: list[float], percentile: int) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (percentile / 100) * (len(ordered) - 1)
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[int(rank)]
    fraction = rank - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def _float_or_none(value: object) -> float | None:
    if value in {None, ""}:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _is_true(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return _text(value).strip().lower() in {"true", "1", "yes"}


def _text(value: object) -> str:
    return "" if value is None else str(value)


def _format_optional(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return repr(value)
    return str(value)


def _csv_bool(value: object) -> str:
    return "true" if bool(value) else "false"


def _csv_boundary_flags() -> dict[str, str]:
    return {
        "local_diagnostic_only": "true",
        "official_metric_input": "false",
        "paper_result_input": "false",
        "retained_evidence_promoted": "false",
        "leaderboard_input": "false",
    }


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
