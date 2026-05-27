"""Default-off CLI wrapper for diagnostic POCR aggregation."""

from __future__ import annotations

import argparse
from pathlib import Path

from sql_rewrite_bench.pocr.pocr_aggregator import (
    aggregate_pocr_rows,
    read_stage_b_row_metrics,
    write_pocr_aggregate_outputs,
)
from sql_rewrite_bench.user_output import build_output_paths


def add_pocr_aggregate_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    *,
    epilog: str,
) -> None:
    parser = subparsers.add_parser(
        "pocr-aggregate",
        help="Aggregate diagnostic POCR row metrics into a route summary.",
        description=(
            "Aggregate existing pocr_stage_b_row_metrics.csv files into promotion-diagnostic "
            "POCR@planned / POCR@candidate summaries. This command is default-off and does not "
            "call APIs, replay annotation, run DB/checker/timing, compute official POCR, promote "
            "paper metrics, update top-level reports/results, or create leaderboard output."
        ),
        epilog=epilog,
    )
    parser.add_argument(
        "--enable-pocr-diagnostic",
        action="store_true",
        help="Opt in to diagnostic POCR aggregation. Without this flag no POCR aggregation runs.",
    )
    parser.add_argument(
        "--row-metrics",
        type=Path,
        nargs="+",
        action="append",
        help="One or more pocr_stage_b_row_metrics.csv paths. The flag may be repeated.",
    )
    parser.add_argument("--run-id", help="Aggregate output run id.")
    parser.add_argument("--output-root", type=Path, help="D035 output root, usually output.")
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Write only pocr_route_summary.csv and skip the optional Markdown report.",
    )


def run_pocr_aggregate_command(args: argparse.Namespace, *, repo_root: Path) -> int:
    """Run the default-off diagnostic POCR aggregate facade."""

    if not args.enable_pocr_diagnostic:
        raise ValueError("pocr-aggregate requires --enable-pocr-diagnostic")
    _require_enabled_args(args)
    row_metrics = _flatten_row_metrics(args.row_metrics)
    output_root = _resolve_output_root(args.output_root, repo_root)
    build_output_paths(output_root, args.run_id, repo_root=repo_root)
    rows = read_stage_b_row_metrics(row_metrics)
    summaries = aggregate_pocr_rows(rows)
    output_paths = write_pocr_aggregate_outputs(
        output_root=output_root,
        run_id=args.run_id,
        summaries=summaries,
        write_report=not args.no_report,
    )
    print(
        "sqlrb user pocr-aggregate complete: "
        f"run_id={args.run_id} row_metrics_files={len(row_metrics)} "
        f"route_summaries={len(summaries)} results={output_paths.route_summary_csv}"
    )
    if output_paths.route_summary_report_md is not None:
        print(f"report={output_paths.route_summary_report_md}")
    print(
        "boundary: Positive Operation Coverage promotion-diagnostic aggregation only; "
        "official_pocr_computed=false; route_level_official_pocr_score_emitted=false; "
        "paper_metric_promoted=false; leaderboard_output=false"
    )
    return 0


def _require_enabled_args(args: argparse.Namespace) -> None:
    required = [
        ("--row-metrics", args.row_metrics),
        ("--run-id", args.run_id),
        ("--output-root", args.output_root),
    ]
    missing = [flag for flag, value in required if value is None or value == ""]
    if missing:
        raise ValueError("--enable-pocr-diagnostic requires " + ", ".join(missing))


def _flatten_row_metrics(row_metrics: list[list[Path]] | None) -> tuple[Path, ...]:
    if not row_metrics:
        return ()
    return tuple(path for group in row_metrics for path in group)


def _resolve_output_root(output_root: Path, repo_root: Path) -> Path:
    return output_root if output_root.is_absolute() else repo_root / output_root
