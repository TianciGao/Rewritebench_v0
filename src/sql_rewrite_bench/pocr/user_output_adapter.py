"""D035-style user-output writer for diagnostic POCR support files."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from sql_rewrite_bench.pocr.diagnostic_output_schema import (
    POCRDiagnosticPoolSummary,
    POCRDiagnosticRow,
    render_diagnostic_markdown_report,
    summarize_by_pool,
    write_diagnostic_rows_csv,
    write_diagnostic_summary_csv,
)


@dataclass(frozen=True)
class POCRDiagnosticOutputPaths:
    diagnostic_rows_csv: Path
    diagnostic_summary_by_pool_csv: Path
    diagnostic_log: Path
    diagnostic_report_md: Path


def write_pocr_diagnostic_user_outputs(
    *,
    output_root: Path,
    run_id: str,
    rows: tuple[POCRDiagnosticRow, ...],
    summaries: tuple[POCRDiagnosticPoolSummary, ...] | None = None,
) -> POCRDiagnosticOutputPaths:
    """Write diagnostic POCR files under a caller-provided D035 output root."""

    if not run_id.strip():
        raise ValueError("run_id is required")
    summaries = summaries if summaries is not None else summarize_by_pool(rows)
    results_dir = output_root / "results" / run_id / "pocr"
    logs_dir = output_root / "logs" / run_id / "pocr"
    reports_dir = output_root / "reports" / run_id
    paths = POCRDiagnosticOutputPaths(
        diagnostic_rows_csv=results_dir / "diagnostic_rows.csv",
        diagnostic_summary_by_pool_csv=results_dir / "diagnostic_summary_by_pool.csv",
        diagnostic_log=logs_dir / "pocr_diagnostic.log",
        diagnostic_report_md=reports_dir / "pocr_diagnostic.md",
    )
    write_diagnostic_rows_csv(paths.diagnostic_rows_csv, rows)
    write_diagnostic_summary_csv(paths.diagnostic_summary_by_pool_csv, summaries)
    paths.diagnostic_log.parent.mkdir(parents=True, exist_ok=True)
    paths.diagnostic_log.write_text(_log_text(run_id=run_id, rows=rows), encoding="utf-8")
    paths.diagnostic_report_md.parent.mkdir(parents=True, exist_ok=True)
    paths.diagnostic_report_md.write_text(
        render_diagnostic_markdown_report(run_id=run_id, rows=rows, summaries=summaries),
        encoding="utf-8",
    )
    return paths


def _log_text(*, run_id: str, rows: tuple[POCRDiagnosticRow, ...]) -> str:
    return (
        f"timestamp_utc={datetime.now(UTC).isoformat()}\n"
        f"run_id={run_id}\n"
        f"rows={len(rows)}\n"
        "diagnostic_only=true\n"
        "official_pocr_computed=false\n"
        "route_level_pocr_aggregated=false\n"
        "paper_metric_promoted=false\n"
        "boundary=Positive Operation Coverage diagnostic support only; no official POCR score emitted.\n"
    )
