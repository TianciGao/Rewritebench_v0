"""User runner for SQL-RewriteBench local experiment outputs.

By default this invokes a user adapter and captures candidate SQL without DB
execution. A bounded opt-in postgres/checker MVP can run local diagnostics under
``runs/user/<run_id>/``. It does not collect timing, compute official metrics,
write retained evidence, update reports/results, or create a leaderboard.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from .adapter_runner import run_adapter_for_case
from .candidate_preflight import preflight_error_result, run_candidate_preflight
from .case_package_resolver import ResolvedCasePackage, resolve_case_package
from .case_selection import (
    ALLOWED_ENGINES,
    ALLOWED_POOLS,
    SelectedCaseEngineRow,
    repo_root_from_module,
    resolve_common_core_selection,
)
from .local_result_checker import run_local_checker
from .postgres_execution import execute_postgres_case
from .tag_slices import build_tag_slice_rows, write_tag_slices
from .user_ledger import (
    apply_candidate_preflight_result,
    dry_run_ledger_for_row,
    failure_rows_from_ledger,
    ledger_from_adapter_result,
    mark_candidate_preflight_skipped,
    write_failures,
    write_ledger,
)
from .user_quality_report import (
    build_quality_summary,
    write_quality_report,
    write_quality_summary,
)
from .user_run_schema import (
    CANDIDATE_PREFLIGHT_FAILURE_CANDIDATE_MISSING,
    CANDIDATE_PREFLIGHT_FAILURE_NONE,
    CANDIDATE_PREFLIGHT_STATUS_FAILED,
    CHECKER_STATUS_NOT_ENABLED,
    CHECKER_STATUS_SUCCESS,
    EXACT_STATUS_NON_DB,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_EXECUTION_FAILURE,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    FAILURE_ADAPTER_FAILED,
    FAILURE_CANDIDATE_PREFLIGHT_FAILED,
    FAILURE_MISMATCH,
    FAILURE_NO_CANDIDATE_SQL,
    FAILURE_NONE,
    FAILURE_SOURCE_EXECUTION_FAILED,
    SELECTED_CASE_FIELDS,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a user SQL rewrite adapter over selected Common-core rows."
    )
    parser.add_argument("--case-set", required=True, choices=["common_core_v0"])
    parser.add_argument("--pool", default="all", choices=sorted(ALLOWED_POOLS | {"all"}))
    parser.add_argument("--engine", required=True, choices=sorted(ALLOWED_ENGINES | {"all"}))
    parser.add_argument("--case-list", type=Path, default=None)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Select a deterministic tiny Common-core smoke subset: PERF_0006 and CONS_0005.",
    )
    parser.add_argument("--adapter-command", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--adapter-timeout", type=int, default=120)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve selection and write local run files without invoking the adapter.",
    )
    parser.add_argument(
        "--enable-db-execution",
        action="store_true",
        help="Opt in to bounded local postgres execution after candidate capture.",
    )
    parser.add_argument(
        "--enable-checker",
        action="store_true",
        help="Opt in to local checker comparison; requires --enable-db-execution.",
    )
    parser.add_argument("--postgres-dsn-env", default="SQLRB_POSTGRES_DSN")
    parser.add_argument("--execution-timeout-sec", type=int, default=30)
    parser.add_argument("--db-schema-prefix", default="sqlrb_user")
    return parser.parse_args(argv)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def validate_output_root(out_dir: Path, repo_root: Path) -> Path:
    """Return resolved output path if it is a relative path under runs/user."""

    if out_dir.is_absolute():
        raise ValueError("--out must be a relative path under runs/user/")
    if ".." in out_dir.parts:
        raise ValueError("--out must be under runs/user/<run_id>/ and must not contain '..'")
    parts = out_dir.parts
    if len(parts) < 3 or parts[0] != "runs" or parts[1] != "user":
        raise ValueError("--out must be under runs/user/<run_id>/")
    resolved = (repo_root / out_dir).resolve()
    allowed_root = (repo_root / "runs" / "user").resolve()
    if allowed_root not in resolved.parents:
        raise ValueError("--out must resolve under runs/user/<run_id>/")
    if resolved == allowed_root:
        raise ValueError("--out must include a run id below runs/user/")
    return resolved


def _relative_to_repo(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _yaml_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value)
    if text == "" or any(ch in text for ch in [":", "#", "\"", "'", "\\", "\n"]):
        return json.dumps(text)
    return text


def _write_config(path: Path, config: dict[str, object]) -> None:
    lines = [f"{key}: {_yaml_scalar(value)}" for key, value in config.items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _selected_case_rows(
    run_id: str, selected: list[SelectedCaseEngineRow]
) -> list[dict[str, object]]:
    return [
        {
            "run_id": run_id,
            "case_id": row.case_id,
            "pool": row.pool,
            "engine": row.engine,
            "denominator_id": row.denominator_id,
            "planned": row.planned,
            "case_path": row.case_path,
            "source_sql_path": row.source_sql_path,
        }
        for row in selected
    ]


def _apply_candidate_preflight_for_row(
    *,
    ledger: dict[str, object],
    row: SelectedCaseEngineRow,
    resolved_package: ResolvedCasePackage,
    repo_root: Path,
) -> dict[str, object]:
    """Run local text-level preflight for a generated candidate SQL file."""

    if ledger.get("candidate_generated") != "true" or not ledger.get("candidate_sql_path"):
        failure_class = (
            CANDIDATE_PREFLIGHT_FAILURE_CANDIDATE_MISSING
            if ledger.get("failure_bucket") == FAILURE_NO_CANDIDATE_SQL
            else CANDIDATE_PREFLIGHT_FAILURE_NONE
        )
        return mark_candidate_preflight_skipped(ledger, failure_class=failure_class)

    try:
        source_sql_text = resolved_package.source_sql_path.read_text(encoding="utf-8")
        candidate_sql_path = repo_root / str(ledger["candidate_sql_path"])
        candidate_sql_text = candidate_sql_path.read_text(encoding="utf-8")
        result = run_candidate_preflight(
            source_sql_text=source_sql_text,
            candidate_sql_text=candidate_sql_text,
            dialect=row.engine,
        )
    except Exception as exc:
        result = preflight_error_result(str(exc))
    return apply_candidate_preflight_result(ledger, result)


def _apply_db_checker_for_row(
    *,
    ledger: dict[str, object],
    run_id: str,
    row: SelectedCaseEngineRow,
    repo_root: Path,
    out_dir: Path,
    enable_checker: bool,
    postgres_dsn_env: str,
    execution_timeout_sec: int,
    db_schema_prefix: str,
) -> dict[str, object]:
    """Run optional local postgres execution/checker for a generated candidate."""

    ledger["execution_enabled"] = "true"
    ledger["checker_enabled"] = "true" if enable_checker else "false"
    ledger["source_execution_status"] = EXECUTION_STATUS_NOT_ENABLED
    ledger["candidate_execution_status"] = EXECUTION_STATUS_NOT_ENABLED
    if ledger.get("candidate_generated") != "true" or not ledger.get("candidate_sql_path"):
        ledger["notes"] = (
            str(ledger.get("notes", ""))
            + "; db execution skipped because no candidate SQL was generated"
        )
        return ledger

    if ledger.get("candidate_preflight_status") == CANDIDATE_PREFLIGHT_STATUS_FAILED:
        ledger["execution_status"] = EXECUTION_STATUS_NOT_ENABLED
        ledger["checker_status"] = CHECKER_STATUS_NOT_ENABLED
        ledger["exact_status"] = EXACT_STATUS_NON_DB
        ledger["notes"] = (
            str(ledger.get("notes", ""))
            + "; db/checker skipped because candidate preflight failed"
        )
        return ledger

    workspace_dir = out_dir / "workspaces" / row.case_id / row.engine
    candidate_sql_path = repo_root / str(ledger["candidate_sql_path"])
    execution = execute_postgres_case(
        repo_root=repo_root,
        run_id=run_id,
        row=row,
        candidate_sql_path=candidate_sql_path,
        workspace_dir=workspace_dir,
        timeout_sec=execution_timeout_sec,
        schema_prefix=db_schema_prefix,
        dsn_env=postgres_dsn_env,
    )
    ledger.update(
        {
            "execution_status": execution.candidate_execution_status,
            "source_execution_status": execution.source_execution_status,
            "candidate_execution_status": execution.candidate_execution_status,
            "source_result_path": _relative_to_repo(execution.source_result_path, repo_root)
            if execution.source_result_path
            else "",
            "candidate_result_path": _relative_to_repo(execution.candidate_result_path, repo_root)
            if execution.candidate_result_path
            else "",
            "execution_failure_class": execution.execution_failure_class,
            "db_artifact_dir": _relative_to_repo(execution.db_artifact_dir, repo_root),
            "notes": str(ledger.get("notes", "")) + "; " + execution.notes,
        }
    )
    if execution.failure_bucket != FAILURE_NONE:
        ledger["failure_bucket"] = execution.failure_bucket
        if execution.failure_bucket == FAILURE_SOURCE_EXECUTION_FAILED:
            ledger["exact_status"] = EXACT_STATUS_EXECUTION_FAILURE
        return ledger

    if not enable_checker:
        ledger["checker_status"] = CHECKER_STATUS_NOT_ENABLED
        ledger["exact_status"] = EXACT_STATUS_NON_DB
        return ledger

    case_dir = repo_root / row.case_path
    checker_dir = workspace_dir / "checker"
    checker = run_local_checker(
        case_dir=case_dir,
        source_result_path=execution.source_result_path,
        candidate_result_path=execution.candidate_result_path,
        checker_dir=checker_dir,
    )
    ledger.update(
        {
            "checker_config_path": _relative_to_repo(
                case_dir / "checker" / "checker.yaml", repo_root
            ),
            "normalization_config_path": _relative_to_repo(
                case_dir / "checker" / "normalization.yaml", repo_root
            ),
            "compare_config_path": _relative_to_repo(
                case_dir / "checker" / "compare_config.yaml", repo_root
            ),
            "checker_status": checker.checker_status,
            "exact_status": checker.exact_status,
            "checker_failure_class": checker.checker_failure_class,
            "mismatch_artifact_path": _relative_to_repo(checker.mismatch_artifact_path, repo_root)
            if checker.mismatch_artifact_path
            else "",
            "notes": str(ledger.get("notes", "")) + "; " + checker.notes,
        }
    )
    if checker.failure_bucket != FAILURE_NONE:
        ledger["failure_bucket"] = checker.failure_bucket
    elif (
        execution.source_execution_status == EXECUTION_STATUS_SOURCE_SUCCESS
        and execution.candidate_execution_status == EXECUTION_STATUS_CANDIDATE_SUCCESS
        and checker.checker_status == CHECKER_STATUS_SUCCESS
        and checker.exact_status == EXACT_STATUS_EXACT
    ):
        ledger["failure_bucket"] = FAILURE_NONE
    return ledger


def _summary_payload(
    run_id: str,
    ledger_rows: list[dict[str, object]],
    *,
    dry_run: bool,
    db_execution_enabled: bool,
    checker_enabled: bool,
) -> dict[str, object]:
    failure_counts = Counter(row["failure_bucket"] for row in ledger_rows)
    return {
        "run_id": run_id,
        "task_type": "user_entry_db_checker_mvp_local"
        if db_execution_enabled
        else "user_entry_mvp_non_db",
        "dry_run": dry_run,
        "selected_rows": len(ledger_rows),
        "adapter_invoked_rows": sum(row["adapter_invoked"] == "true" for row in ledger_rows),
        "candidate_generated_rows": sum(
            row["candidate_generated"] == "true" for row in ledger_rows
        ),
        "adapter_failed_rows": failure_counts[FAILURE_ADAPTER_FAILED],
        "no_candidate_sql_rows": failure_counts[FAILURE_NO_CANDIDATE_SQL],
        "candidate_preflight_failed_rows": failure_counts[
            FAILURE_CANDIDATE_PREFLIGHT_FAILED
        ],
        "db_execution_enabled": db_execution_enabled,
        "checker_enabled": checker_enabled,
        "source_execution_success_rows": sum(
            row.get("source_execution_status") == EXECUTION_STATUS_SOURCE_SUCCESS
            for row in ledger_rows
        ),
        "candidate_execution_success_rows": sum(
            row.get("candidate_execution_status") == EXECUTION_STATUS_CANDIDATE_SUCCESS
            for row in ledger_rows
        ),
        "checker_success_rows": sum(
            row.get("checker_status") == CHECKER_STATUS_SUCCESS for row in ledger_rows
        ),
        "checker_mismatch_rows": failure_counts[FAILURE_MISMATCH],
        "exact_rows_local": sum(
            row.get("exact_status") == EXACT_STATUS_EXACT for row in ledger_rows
        ),
        "mismatch_rows_local": failure_counts[FAILURE_MISMATCH],
        "local_execution_only": True,
        "official_metrics_computed": False,
        "paper_tables_rendered": False,
        "reports_changed": False,
        "results_changed": False,
        "case_sets_changed": False,
        "denominator_changed": False,
        "paper_results_changed": False,
        "retained_evidence_updated": False,
        "raw_legacy_evidence_changed": False,
        "no_global_leaderboard": True,
    }


def _write_report(
    *,
    path: Path,
    config: dict[str, object],
    selected_rows: list[dict[str, object]],
    ledger_rows: list[dict[str, object]],
    summary: dict[str, object],
) -> None:
    pool_counts = Counter(row["pool"] for row in ledger_rows)
    engine_counts = Counter(row["engine"] for row in ledger_rows)
    failure_counts = Counter(row["failure_bucket"] for row in ledger_rows)
    generated = summary["candidate_generated_rows"]
    selected = summary["selected_rows"]
    lines = [
        f"# SQL-RewriteBench User Run: {config['run_id']}",
        "",
        "This is local user-run output only.",
        "This is not retained paper evidence.",
        "No global leaderboard is created.",
        "Official metrics are not computed in this MVP.",
        "",
        "## Command Summary",
        "",
        "- Command form: `python -m sql_rewrite_bench.user_run ...`",
        f"- Adapter command: `{config['adapter_command']}`",
        f"- Dry-run mode: `{config.get('dry_run', False)}`",
        f"- Output root: `{config['out_dir']}`",
        "",
        "## Run Config",
        "",
    ]
    for key, value in config.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Selected Case / Pool / Engine Summary",
            "",
            f"- Selected case-engine rows: {selected}",
            f"- Unique cases: {len({row['case_id'] for row in selected_rows})}",
            f"- Pools: {', '.join(sorted(pool_counts)) if pool_counts else 'none'}",
            f"- Engines: {', '.join(sorted(engine_counts)) if engine_counts else 'none'}",
            f"- Dry-run mode: {config.get('dry_run', False)}",
            "",
            "## Denominator Funnel",
            "",
            f"- Planned rows: {selected}",
            f"- Selected rows: {selected}",
            f"- Adapter invoked rows: {summary['adapter_invoked_rows']}",
            f"- Candidate generated rows: {generated}",
            f"- Source execution success rows: {summary.get('source_execution_success_rows', 0)}",
            (
                "- Candidate execution success rows: "
                f"{summary.get('candidate_execution_success_rows', 0)}"
            ),
            f"- Local exact rows: {summary.get('exact_rows_local', 0)}",
            "- Timed rows: 0 (not_timed_non_db_mvp)",
            "",
            "## Pool Breakdown",
            "",
        ]
    )
    lines.extend(f"- {pool}: {count}" for pool, count in sorted(pool_counts.items()))
    lines.extend(["", "## Engine Breakdown", ""])
    lines.extend(f"- {engine}: {count}" for engine, count in sorted(engine_counts.items()))
    lines.extend(["", "## Failure Bucket Table", ""])
    lines.extend(f"- {bucket}: {count}" for bucket, count in sorted(failure_counts.items()))
    if summary.get("db_execution_enabled"):
        lines.extend(
            [
                "",
                "## DB/Checker MVP",
                "",
                "- DB execution enabled: `True`",
                f"- Checker enabled: `{summary.get('checker_enabled')}`",
                (
                    "- Source execution success rows: "
                    f"{summary.get('source_execution_success_rows', 0)}"
                ),
                (
                    "- Candidate execution success rows: "
                    f"{summary.get('candidate_execution_success_rows', 0)}"
                ),
                f"- Checker success rows: {summary.get('checker_success_rows', 0)}",
                f"- Checker mismatch rows: {summary.get('checker_mismatch_rows', 0)}",
                f"- Local exact rows: {summary.get('exact_rows_local', 0)}",
                f"- Local mismatch rows: {summary.get('mismatch_rows_local', 0)}",
                "- DB/checker artifacts are local user-run diagnostics only.",
                "- Official metrics are not computed.",
                "- Retained evidence is not updated.",
                "- No global leaderboard is created.",
            ]
        )
    lines.extend(["", "## Artifact Links", ""])
    for row in ledger_rows:
        candidate = row["candidate_sql_path"] or "no candidate SQL"
        lines.append(f"- {row['case_id']} / {row['engine']}: `{candidate}`")
    lines.extend(
        [
            "",
            "## Adapter Invocation Behavior",
            "",
            "- Adapter commands are invoked with `shell=False` via `shlex.split`.",
            "- The subprocess working directory is the repository root.",
            "- Per-row workspace path is provided through `SQLRB_WORKSPACE_DIR`.",
            "- Candidate file path is provided through `SQLRB_CANDIDATE_SQL_PATH`.",
            "- Candidate SQL is captured from workspace `candidate.sql` first, then stdout.",
            "- Candidate SQL is not executed, checked, timed, or scored.",
            "",
            "## Required Warnings",
            "",
            "- This is local user-run output only.",
            "- This is not retained paper evidence.",
            "- No global leaderboard is created.",
            "- Official metrics are not computed in this MVP.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def run_user_benchmark(args: argparse.Namespace, repo_root: Path) -> dict[str, object]:
    enable_db_execution = bool(getattr(args, "enable_db_execution", False))
    enable_checker = bool(getattr(args, "enable_checker", False))
    if enable_checker and not enable_db_execution:
        raise ValueError("--enable-checker requires --enable-db-execution")

    out_dir = validate_output_root(args.out, repo_root)
    run_id = args.run_id or args.out.name
    if not run_id:
        run_id = "user_run_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    selected = resolve_common_core_selection(
        repo_root=repo_root,
        case_set=args.case_set,
        pool=args.pool,
        engine=args.engine,
        case_list=args.case_list,
        smoke=bool(getattr(args, "smoke", False)),
    )
    if not selected:
        raise ValueError("selection produced zero case-engine rows")
    resolved_packages = [resolve_case_package(repo_root=repo_root, row=row) for row in selected]

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "candidate_sql").mkdir(exist_ok=True)
    (out_dir / "workspaces").mkdir(exist_ok=True)

    config = {
        "run_id": run_id,
        "created_at_utc": _utc_now_iso(),
        "case_set": args.case_set,
        "pool": args.pool,
        "engine": args.engine,
        "case_list": args.case_list.as_posix() if args.case_list else "",
        "smoke": bool(getattr(args, "smoke", False)),
        "adapter_command": args.adapter_command,
        "out_dir": _relative_to_repo(out_dir, repo_root),
        "mvp_mode": "postgres_db_checker_mvp_local"
        if enable_db_execution
        else "non_db_adapter_capture_only",
        "dry_run": bool(getattr(args, "dry_run", False)),
        "db_execution_enabled": enable_db_execution,
        "checker_enabled": enable_checker,
        "postgres_dsn_env": getattr(args, "postgres_dsn_env", "SQLRB_POSTGRES_DSN"),
        "execution_timeout_sec": getattr(args, "execution_timeout_sec", 30),
        "db_schema_prefix": getattr(args, "db_schema_prefix", "sqlrb_user"),
        "official_metrics_computed": False,
        "paper_results_updated": False,
        "retained_evidence_updated": False,
        "no_global_leaderboard": True,
    }
    _write_config(out_dir / "config.yaml", config)

    selected_case_rows = _selected_case_rows(run_id, selected)
    _write_csv(out_dir / "selected_cases.csv", selected_case_rows, SELECTED_CASE_FIELDS)

    if getattr(args, "dry_run", False):
        ledger_rows = [
            dry_run_ledger_for_row(run_id=run_id, row=row, repo_root=repo_root, out_dir=out_dir)
            for row in selected
        ]
    else:
        ledger_rows = [
            ledger_from_adapter_result(
                run_id=run_id,
                row=row,
                adapter_result=run_adapter_for_case(
                    run_id=run_id,
                    row=row,
                    resolved_package=resolved,
                    adapter_command=args.adapter_command,
                    repo_root=repo_root,
                    out_dir=out_dir,
                    timeout=args.adapter_timeout,
                ),
                repo_root=repo_root,
            )
            for row, resolved in zip(selected, resolved_packages, strict=True)
        ]
        ledger_rows = [
            _apply_candidate_preflight_for_row(
                ledger=ledger,
                row=row,
                resolved_package=resolved,
                repo_root=repo_root,
            )
            for ledger, row, resolved in zip(
                ledger_rows, selected, resolved_packages, strict=True
            )
        ]
    if enable_db_execution and not getattr(args, "dry_run", False):
        ledger_rows = [
            _apply_db_checker_for_row(
                ledger=ledger,
                run_id=run_id,
                row=row,
                repo_root=repo_root,
                out_dir=out_dir,
                enable_checker=enable_checker,
                postgres_dsn_env=getattr(args, "postgres_dsn_env", "SQLRB_POSTGRES_DSN"),
                execution_timeout_sec=getattr(args, "execution_timeout_sec", 30),
                db_schema_prefix=getattr(args, "db_schema_prefix", "sqlrb_user"),
            )
            for ledger, row in zip(ledger_rows, selected, strict=True)
        ]
    elif enable_db_execution:
        for ledger in ledger_rows:
            ledger["execution_enabled"] = "true"
            ledger["checker_enabled"] = "true" if enable_checker else "false"
            ledger["source_execution_status"] = EXECUTION_STATUS_NOT_ENABLED
            ledger["candidate_execution_status"] = EXECUTION_STATUS_NOT_ENABLED
    write_ledger(out_dir / "ledger.csv", ledger_rows)
    failure_rows = failure_rows_from_ledger(ledger_rows)
    write_failures(out_dir / "failures.csv", failure_rows)

    summary = _summary_payload(
        run_id,
        ledger_rows,
        dry_run=bool(getattr(args, "dry_run", False)),
        db_execution_enabled=enable_db_execution,
        checker_enabled=enable_checker,
    )
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_report(
        path=out_dir / "report.md",
        config=config,
        selected_rows=selected_case_rows,
        ledger_rows=ledger_rows,
        summary=summary,
    )
    quality_summary = build_quality_summary(
        ledger_rows, run_config=config, tag_slices_included=True
    )
    write_quality_summary(quality_summary, out_dir / "quality_summary.json")
    write_quality_report(quality_summary, out_dir / "quality_report.md")
    tag_slice_rows = build_tag_slice_rows(ledger_rows, resolved_packages)
    write_tag_slices(out_dir / "tag_slices.csv", tag_slice_rows)
    return summary


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = repo_root_from_module()
    try:
        summary = run_user_benchmark(args, repo_root)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(
        "user run complete: "
        f"run_id={summary['run_id']} selected_rows={summary['selected_rows']} "
        f"candidate_generated_rows={summary['candidate_generated_rows']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
