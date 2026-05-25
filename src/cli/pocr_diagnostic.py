"""Default-off CLI wrapper for diagnostic POCR user-output files."""

from __future__ import annotations

import argparse
from pathlib import Path

from sql_rewrite_bench.case_selection import ALLOWED_ENGINES, read_case_list
from sql_rewrite_bench.pocr.user_facade import run_pocr_diagnostic_user_facade
from sql_rewrite_bench.user_output import build_output_paths


def add_pocr_diagnostic_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    *,
    epilog: str,
) -> None:
    parser = subparsers.add_parser(
        "pocr-diagnostic",
        help="Write optional diagnostic POCR user-output files.",
        description=(
            "Write Positive Operation Coverage diagnostic support files under a D035 "
            "output root. This command is default-off and does not call APIs, run DB/checker/timing, "
            "run baselines, compute official POCR, aggregate route-level POCR, promote paper metrics, "
            "or create leaderboard output."
        ),
        epilog=epilog,
    )
    parser.add_argument(
        "--enable-pocr-diagnostic",
        action="store_true",
        help="Opt in to diagnostic POCR output. Without this flag no POCR code runs.",
    )
    parser.add_argument("--candidate-root", type=Path)
    parser.add_argument("--method-id")
    parser.add_argument("--route-id")
    parser.add_argument("--engine", choices=sorted(ALLOWED_ENGINES))
    parser.add_argument("--run-id")
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--annotation-jsonl", type=Path)
    parser.add_argument(
        "--case-list",
        type=Path,
        help="Optional newline/comma-separated Common-core case-id filter for diagnostic output.",
    )


def run_pocr_diagnostic_command(args: argparse.Namespace, *, repo_root: Path) -> int:
    """Run the default-off diagnostic POCR facade from the public CLI."""

    if not args.enable_pocr_diagnostic:
        print("POCR diagnostic disabled: --enable-pocr-diagnostic was not supplied; no POCR code ran.")
        print(
            "boundary: pocr diagnostic support only; official_pocr_computed=false; "
            "route_level_pocr_aggregated=false; paper_metric_promoted=false"
        )
        return 0

    _require_enabled_args(args)
    output_root = _resolve_output_root(args.output_root, repo_root)
    build_output_paths(output_root, args.run_id, repo_root=repo_root)
    case_ids = tuple(sorted(read_case_list(args.case_list))) if args.case_list else None
    result = run_pocr_diagnostic_user_facade(
        repo_root=repo_root,
        run_id=args.run_id,
        candidate_root=args.candidate_root,
        method_id=args.method_id,
        route_id=args.route_id,
        engine=args.engine,
        annotation_jsonl=args.annotation_jsonl,
        live_enabled=False,
        output_root=output_root,
        case_ids=case_ids,
    )
    output_paths = result.output_paths
    if output_paths is None:
        raise RuntimeError("internal error: POCR diagnostic output paths were not written")
    print(
        "sqlrb user pocr-diagnostic complete: "
        f"run_id={args.run_id} rows={len(result.rows)} "
        f"results={output_root / 'results' / args.run_id / 'pocr'} "
        f"reports={output_root / 'reports' / args.run_id}"
    )
    print(
        "boundary: Positive Operation Coverage diagnostic support only; "
        "official_pocr_computed=false; route_level_pocr_aggregated=false; "
        "paper_metric_promoted=false; leaderboard_input=false"
    )
    return 0


def _require_enabled_args(args: argparse.Namespace) -> None:
    required = [
        ("--candidate-root", args.candidate_root),
        ("--method-id", args.method_id),
        ("--route-id", args.route_id),
        ("--engine", args.engine),
        ("--run-id", args.run_id),
        ("--output-root", args.output_root),
    ]
    missing = [flag for flag, value in required if value in {None, ""}]
    if missing:
        raise ValueError("--enable-pocr-diagnostic requires " + ", ".join(missing))


def _resolve_output_root(output_root: Path, repo_root: Path) -> Path:
    return output_root if output_root.is_absolute() else repo_root / output_root
