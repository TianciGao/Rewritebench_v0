"""Thin public CLI facade for local user evaluation commands.

The facade delegates to ``sql_rewrite_bench`` internals. It does not implement
rewrite logic, verifier integration, official metrics, reports/results updates,
retained-evidence promotion, or leaderboard output.
"""

from __future__ import annotations

import argparse
import json
import sys
from argparse import Namespace
from pathlib import Path

from sql_rewrite_bench import user_run
from sql_rewrite_bench.case_selection import ALLOWED_ENGINES, ALLOWED_POOLS, repo_root_from_module
from sql_rewrite_bench.local_metrics import compute_and_write_local_metrics
from sql_rewrite_bench.user_output import build_output_paths, export_run_to_output
from sql_rewrite_bench.user_output_schema import output_schema_text

LOCAL_BOUNDARY_TEXT = """# Local Diagnostic Boundary

SQL-RewriteBench user outputs are local diagnostic artifacts only.

- Not official metrics.
- Not paper results.
- Not retained evidence.
- Not leaderboard input.

- official_metric_input: false
- paper_result_input: false
- retained_evidence_promoted: false
- leaderboard_input: false

Semantic Equivalence Rate is N.A. until formal VeriEQL or SQLSolver evidence
exists. POCR remains deferred pending external skill-adapter integration.

Promotion to top-level reports/, results/, or retained evidence requires a
separate authorized task.
"""

LOCAL_ONLY_EPILOG = (
    "Boundary: local diagnostic output only; no official metrics, paper results, "
    "retained-evidence promotion, or leaderboard output."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sqlrb",
        description=(
            "SQL-RewriteBench public facade. Commands in this facade write local "
            "diagnostic outputs only; they do not compute official metrics or "
            "paper results, promote retained evidence, or create leaderboard output."
        ),
    )
    subparsers = parser.add_subparsers(dest="command_group", required=True)
    user_parser = subparsers.add_parser(
        "user",
        help="Local user-evaluation workbench commands.",
        description=(
            "User-facing local diagnostic commands. Outputs are local-only and "
            "not official metrics, paper results, retained evidence, or leaderboard input."
        ),
    )
    user_subparsers = user_parser.add_subparsers(dest="user_command", required=True)
    _add_evaluate_parser(user_subparsers)
    _add_list_cases_parser(user_subparsers)
    _add_explain_selection_parser(user_subparsers)
    _add_show_output_schema_parser(user_subparsers)
    _add_show_boundary_parser(user_subparsers)
    _add_compute_local_metrics_parser(user_subparsers)
    _add_summarize_parser(user_subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command_group == "user":
            return _handle_user_command(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    parser.error("unknown command")
    return 2


def _add_evaluate_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "evaluate",
        help="Run a local diagnostic user evaluation and export user-facing output.",
        description=(
            "Run a local diagnostic user evaluation. This delegates to the internal "
            "user-run pipeline and then exports artifacts to output/results|logs|reports. "
            "No official metrics, paper results, retained evidence, or leaderboard output is created."
        ),
        epilog=LOCAL_ONLY_EPILOG,
    )
    _add_selection_args(parser)
    parser.add_argument("--engines", required=True, help="Comma-separated engine list, e.g. postgres or postgres,mysql,spark.")
    parser.add_argument("--adapter-command", required=True)
    parser.add_argument("--output-root", type=Path, default=Path("output"))
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--adapter-timeout", type=int, default=120)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--enable-db-execution", action="store_true")
    parser.add_argument("--enable-checker", action="store_true")
    parser.add_argument("--postgres-dsn-env", default="SQLRB_POSTGRES_DSN")
    parser.add_argument("--execution-timeout-sec", type=int, default=30)
    parser.add_argument("--db-schema-prefix", default="sqlrb_user")
    parser.add_argument("--collect-timing", action="store_true")
    parser.add_argument("--timing-warmup", type=int, default=1)
    parser.add_argument("--timing-repetitions", type=int, default=5)
    parser.add_argument("--timing-timeout", type=float, default=30.0)
    parser.add_argument(
        "--verifier",
        action="append",
        choices=["verieql", "sqlsolver"],
        default=[],
        help=(
            "Reserved for future verifier support; not implemented in Phase 2B. "
            "Semantic Equivalence Rate remains N.A. without verifier evidence."
        ),
    )


def _add_list_cases_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "list-cases",
        help="List metadata-selected cases.",
        description="List local diagnostic case selections without running adapters or computing metrics.",
        epilog=LOCAL_ONLY_EPILOG,
    )
    _add_selection_args(parser)
    parser.add_argument("--engines", default="all")


def _add_explain_selection_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "explain-selection",
        help="Explain the selected local diagnostic rows.",
        description="Explain local diagnostic row selection without running adapters or computing metrics.",
        epilog=LOCAL_ONLY_EPILOG,
    )
    _add_selection_args(parser)
    parser.add_argument("--engines", default="all")


def _add_show_output_schema_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    subparsers.add_parser(
        "show-output-schema",
        help="Show local output schema and D035 output-root shape.",
        description="Show the D035 local output contract for user-run diagnostic artifacts.",
        epilog=LOCAL_ONLY_EPILOG,
    )


def _add_show_boundary_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "show-boundary",
        help="Show the local-only output boundary.",
        description="Show the local-only, non-official output boundary for a run or generic user output.",
        epilog=LOCAL_ONLY_EPILOG,
    )
    parser.add_argument("--output-root", type=Path, default=Path("output"))
    parser.add_argument("--run-id")


def _add_compute_local_metrics_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "compute-local-metrics",
        help="Delegate to the non-official local metrics calculator for an existing source run.",
        description=(
            "Compute non-official local diagnostic metrics for an existing local source run. "
            "This does not compute official metrics or write top-level reports/results."
        ),
        epilog=LOCAL_ONLY_EPILOG,
    )
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-root", type=Path, default=Path("output"))
    parser.add_argument("--source-run-root", type=Path, default=Path("runs/user"))


def _add_summarize_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "summarize",
        help="Print an existing local output summary.",
        description="Print local diagnostic output summaries without recomputing metrics or touching official surfaces.",
        epilog=LOCAL_ONLY_EPILOG,
    )
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-root", type=Path, default=Path("output"))


def _add_selection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--case-set", choices=["common_core_v0"], required=True)
    parser.add_argument("--pool", default="all", choices=sorted(ALLOWED_POOLS | {"all"}))
    parser.add_argument("--case-list", type=Path)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Use the deterministic tiny smoke subset: PERF_0006 and CONS_0005.",
    )


def _handle_user_command(args: argparse.Namespace) -> int:
    command = args.user_command
    if command == "evaluate":
        return _evaluate(args)
    if command == "list-cases":
        return _delegate_selection_command(args, "--list-cases")
    if command == "explain-selection":
        return _delegate_selection_command(args, "--explain-selection")
    if command == "show-output-schema":
        return _show_output_schema()
    if command == "show-boundary":
        return _show_boundary(args)
    if command == "compute-local-metrics":
        return _compute_local_metrics(args)
    if command == "summarize":
        return _summarize(args)
    raise ValueError(f"unknown user command: {command}")


def _evaluate(args: argparse.Namespace) -> int:
    if args.verifier:
        raise ValueError(
            "verifier integration is not implemented in Phase 2B; "
            "Semantic Equivalence Rate remains N.A. without verifier evidence"
        )
    repo_root = repo_root_from_module()
    engines = _parse_engines(args.engines)
    output_root = _resolve_output_root(args.output_root, repo_root)
    for engine in engines:
        run_id = args.run_id if len(engines) == 1 else f"{args.run_id}__{engine}"
        build_output_paths(output_root, run_id, repo_root=repo_root)
    results = []
    for engine in engines:
        run_id = args.run_id if len(engines) == 1 else f"{args.run_id}__{engine}"
        source_out = Path("runs") / "user" / run_id
        run_args = Namespace(
            case_set=args.case_set,
            pool=args.pool,
            engine=engine,
            case_list=args.case_list,
            smoke=args.smoke,
            adapter_command=args.adapter_command,
            out=source_out,
            run_id=run_id,
            adapter_timeout=args.adapter_timeout,
            dry_run=args.dry_run,
            enable_db_execution=args.enable_db_execution,
            enable_checker=args.enable_checker,
            postgres_dsn_env=args.postgres_dsn_env,
            execution_timeout_sec=args.execution_timeout_sec,
            db_schema_prefix=args.db_schema_prefix,
            collect_timing=args.collect_timing,
            timing_warmup=args.timing_warmup,
            timing_repetitions=args.timing_repetitions,
            timing_timeout=args.timing_timeout,
        )
        summary = user_run.run_user_benchmark(run_args, repo_root)
        exported = export_run_to_output(
            repo_root / source_out,
            output_root,
            run_id=run_id,
            repo_root=repo_root,
        )
        results.append((summary, exported))
    for summary, exported in results:
        print(
            "sqlrb user evaluate complete: "
            f"run_id={exported.run_id} selected_rows={summary['selected_rows']} "
            f"candidate_generated_rows={summary['candidate_generated_rows']} "
            f"results={exported.paths.result_root} reports={exported.paths.report_root}"
        )
    print("boundary: local diagnostic only; official_metric_input=false; leaderboard_input=false")
    return 0


def _delegate_selection_command(args: argparse.Namespace, command_flag: str) -> int:
    engine = _single_engine_or_all(args.engines)
    argv = [
        "--case-set",
        args.case_set,
        "--pool",
        args.pool,
        "--engine",
        engine,
        command_flag,
    ]
    if args.case_list:
        argv.extend(["--case-list", args.case_list.as_posix()])
    if args.smoke:
        argv.append("--smoke")
    return user_run.main(argv)


def _show_output_schema() -> int:
    print("SQL-RewriteBench user output contract v0")
    print()
    print("User-facing local outputs are exported to:")
    print("- output/results/<run_id>/")
    print("- output/logs/<run_id>/")
    print("- output/reports/<run_id>/")
    print()
    print("These outputs are local diagnostic artifacts only, not official metrics, paper results, retained evidence, or leaderboard input.")
    print()
    print(output_schema_text(), end="")
    return 0


def _show_boundary(args: argparse.Namespace) -> int:
    repo_root = repo_root_from_module()
    if args.run_id:
        paths = build_output_paths(_resolve_output_root(args.output_root, repo_root), args.run_id, repo_root=repo_root)
        boundary_path = paths.report_root / "boundary.md"
        if boundary_path.exists():
            print(boundary_path.read_text(encoding="utf-8"), end="")
            return 0
    print(LOCAL_BOUNDARY_TEXT, end="")
    return 0


def _compute_local_metrics(args: argparse.Namespace) -> int:
    repo_root = repo_root_from_module()
    source_run_dir = _resolve_source_run_root(args.source_run_root, repo_root) / args.run_id
    output_root = _resolve_output_root(args.output_root, repo_root)
    build_output_paths(output_root, args.run_id, repo_root=repo_root)
    outputs = compute_and_write_local_metrics(source_run_dir)
    exported = export_run_to_output(
        source_run_dir,
        output_root,
        run_id=args.run_id,
        repo_root=repo_root,
    )
    print(f"local metrics written: {outputs.metrics_dir}")
    print(f"user-facing metrics output: {exported.paths.result_root / 'metrics'}")
    print(f"user-facing metrics report: {exported.paths.report_root / 'metrics_summary.md'}")
    print("deferred metrics: Semantic Equivalence Rate=N.A. without verifier evidence; POCR=deferred")
    print(
        "boundary: local diagnostic metrics only; official_metric_input=false; "
        "paper_result_input=false; retained_evidence_promoted=false; leaderboard_input=false"
    )
    return 0


def _summarize(args: argparse.Namespace) -> int:
    repo_root = repo_root_from_module()
    paths = build_output_paths(_resolve_output_root(args.output_root, repo_root), args.run_id, repo_root=repo_root)
    summary_path = paths.report_root / "summary.md"
    manifest_path = paths.result_root / "run_manifest.json"
    if not summary_path.exists() and not manifest_path.exists():
        raise ValueError(f"no exported output found for run id: {args.run_id}")

    print("# SQL-RewriteBench Local Output Summary")
    print()
    print("This is local diagnostic output only.")
    print()
    print("## Output Roots")
    print()
    print(f"- results: `{paths.result_root}`")
    print(f"- logs: `{paths.log_root}`")
    print(f"- reports: `{paths.report_root}`")
    print()

    if summary_path.exists():
        _print_report_file("Run Summary", summary_path)
    else:
        _print_manifest_summary(manifest_path)

    _print_report_file(
        "Failure Buckets",
        paths.report_root / "failure_buckets.md",
        missing_message="Failure buckets: N.A.; not available in this exported output.",
    )
    _print_report_file(
        "Tag Slices",
        paths.report_root / "tag_slices.md",
        missing_message="Tag slices: N.A.; not available in this exported output.",
    )
    _print_report_file(
        "Local Metrics",
        paths.report_root / "metrics_summary.md",
        missing_message=(
            "Local metrics: N.A.; metrics were not computed for this exported output.\n\n"
            "- Semantic Equivalence Rate: `N.A.` without verifier evidence\n"
            "- POCR: deferred pending external skill adapter"
        ),
    )
    _print_report_file(
        "Verifier",
        paths.report_root / "verifier_summary.md",
        missing_message=(
            "Verifier: N.A.; VeriEQL and SQLSolver evidence is not available.\n\n"
            "- Semantic Equivalence Rate: `N.A.`"
        ),
    )
    _print_report_file("Boundary", paths.report_root / "boundary.md", missing_message=LOCAL_BOUNDARY_TEXT.rstrip())
    return 0


def _print_manifest_summary(manifest_path: Path) -> None:
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        print("## Run Manifest")
        print()
        for key in [
            "run_id",
            "case_set",
            "selected_case_count",
            "selected_engines",
            "route_id",
            "method_id",
            "local_diagnostic_only",
            "official_metric_input",
            "paper_result_input",
            "retained_evidence_promoted",
            "leaderboard_input",
        ]:
            print(f"- {key}: `{manifest.get(key)}`")
        print()


def _print_report_file(title: str, path: Path, *, missing_message: str | None = None) -> None:
    print(f"## {title}")
    print()
    if path.exists():
        text = path.read_text(encoding="utf-8").strip()
        print(text if text else f"{title}: N.A.; file is empty.")
    else:
        print(missing_message or f"{title}: N.A.; file not available.")
    print()


def _parse_engines(raw_engines: str) -> list[str]:
    engines = [part.strip() for part in raw_engines.split(",") if part.strip()]
    if not engines:
        raise ValueError("--engines must contain at least one engine")
    invalid = [engine for engine in engines if engine not in ALLOWED_ENGINES]
    if invalid:
        raise ValueError(f"unsupported engine(s): {', '.join(invalid)}")
    return engines


def _single_engine_or_all(raw_engines: str) -> str:
    if raw_engines.strip() == "all":
        return "all"
    engines = _parse_engines(raw_engines)
    return engines[0] if len(engines) == 1 else "all"


def _resolve_output_root(output_root: Path, repo_root: Path) -> Path:
    return output_root if output_root.is_absolute() else repo_root / output_root


def _resolve_source_run_root(source_run_root: Path, repo_root: Path) -> Path:
    return source_run_root if source_run_root.is_absolute() else repo_root / source_run_root


if __name__ == "__main__":
    raise SystemExit(main())
