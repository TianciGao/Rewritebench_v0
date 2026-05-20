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
import os
import shlex
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from .case_selection import (
    ALLOWED_ENGINES,
    ALLOWED_POOLS,
    SelectedCaseEngineRow,
    repo_root_from_module,
    resolve_common_core_selection,
)
from .local_result_checker import run_local_checker
from .postgres_execution import execute_postgres_case
from .user_run_schema import (
    CHECKER_STATUS_NON_DB,
    CHECKER_STATUS_NOT_ENABLED,
    CHECKER_STATUS_SUCCESS,
    EXACT_STATUS_NON_DB,
    EXACT_STATUS_EXACT,
    EXACT_STATUS_EXECUTION_FAILURE,
    EXECUTION_STATUS_NON_DB,
    EXECUTION_STATUS_NOT_ENABLED,
    EXECUTION_STATUS_SOURCE_SUCCESS,
    EXECUTION_STATUS_CANDIDATE_SUCCESS,
    EXTRACTION_ADAPTER_FAILED,
    EXTRACTION_CAPTURED_FROM_CANDIDATE_FILE,
    EXTRACTION_CAPTURED_FROM_STDOUT,
    EXTRACTION_NO_CANDIDATE_SQL,
    EXTRACTION_SKIPPED_DRY_RUN,
    FAILURE_ADAPTER_FAILED,
    FAILURE_ADAPTER_TIMEOUT,
    FAILURE_FIELDS,
    FAILURE_INTERNAL_RUNNER_ERROR,
    FAILURE_MISMATCH,
    FAILURE_NO_CANDIDATE_SQL,
    FAILURE_NONE,
    FAILURE_SOURCE_EXECUTION_FAILED,
    LEDGER_FIELDS,
    SELECTED_CASE_FIELDS,
    TIMED_STATUS_NON_DB,
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


def _build_env(
    *,
    base_env: dict[str, str],
    run_id: str,
    row: SelectedCaseEngineRow,
    repo_root: Path,
    workspace_dir: Path,
    candidate_path: Path,
) -> dict[str, str]:
    env = dict(base_env)
    env.update(
        {
            "SQLRB_RUN_ID": run_id,
            "SQLRB_CASE_ID": row.case_id,
            "SQLRB_POOL": row.pool,
            "SQLRB_ENGINE": row.engine,
            "SQLRB_SOURCE_SQL_PATH": str((repo_root / row.source_sql_path).resolve()),
            "SQLRB_CASE_DIR": str((repo_root / row.case_path).resolve()),
            "SQLRB_WORKSPACE_DIR": str(workspace_dir.resolve()),
            "SQLRB_CANDIDATE_SQL_PATH": str(candidate_path.resolve()),
        }
    )
    return env


def _ledger_base(run_id: str, row: SelectedCaseEngineRow, artifact_path: str) -> dict[str, object]:
    return {
        "run_id": run_id,
        "case_id": row.case_id,
        "pool": row.pool,
        "engine": row.engine,
        "denominator_id": row.denominator_id,
        "planned": "true",
        "selected": "true",
        "adapter_invoked": "true",
        "adapter_exit_code": "",
        "candidate_generated": "false",
        "candidate_sql_path": "",
        "extraction_status": EXTRACTION_NO_CANDIDATE_SQL,
        "execution_status": EXECUTION_STATUS_NON_DB,
        "checker_status": CHECKER_STATUS_NON_DB,
        "exact_status": EXACT_STATUS_NON_DB,
        "timed_status": TIMED_STATUS_NON_DB,
        "failure_bucket": FAILURE_NO_CANDIDATE_SQL,
        "artifact_path": artifact_path,
        "notes": "non_db_mvp_adapter_capture_only",
        "execution_enabled": "false",
        "checker_enabled": "false",
        "source_execution_status": EXECUTION_STATUS_NON_DB,
        "candidate_execution_status": EXECUTION_STATUS_NON_DB,
        "source_result_path": "",
        "candidate_result_path": "",
        "checker_config_path": "",
        "normalization_config_path": "",
        "compare_config_path": "",
        "execution_failure_class": "",
        "checker_failure_class": "",
        "mismatch_artifact_path": "",
        "db_artifact_dir": "",
        "local_execution_only": "true",
        "official_metric_input": "false",
        "retained_evidence_input": "false",
    }


def _dry_run_ledger_for_row(
    *, run_id: str, row: SelectedCaseEngineRow, repo_root: Path, out_dir: Path
) -> dict[str, object]:
    workspace_dir = out_dir / "workspaces" / row.case_id / row.engine
    workspace_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = _relative_to_repo(workspace_dir, repo_root)
    ledger = _ledger_base(run_id, row, artifact_path)
    ledger.update(
        {
            "adapter_invoked": "false",
            "adapter_exit_code": "",
            "candidate_generated": "false",
            "candidate_sql_path": "",
            "extraction_status": EXTRACTION_SKIPPED_DRY_RUN,
            "failure_bucket": FAILURE_NONE,
            "notes": "dry_run_selection_only_no_adapter_invoked",
        }
    )
    return ledger


def _run_adapter_for_row(
    *,
    run_id: str,
    row: SelectedCaseEngineRow,
    adapter_command: str,
    repo_root: Path,
    out_dir: Path,
    timeout: int,
) -> dict[str, object]:
    workspace_dir = out_dir / "workspaces" / row.case_id / row.engine
    workspace_dir.mkdir(parents=True, exist_ok=True)
    candidate_from_workspace = workspace_dir / "candidate.sql"
    stdout_path = workspace_dir / "adapter_stdout.txt"
    stderr_path = workspace_dir / "adapter_stderr.txt"
    artifact_path = _relative_to_repo(workspace_dir, repo_root)
    ledger = _ledger_base(run_id, row, artifact_path)
    env = _build_env(
        base_env=os.environ,
        run_id=run_id,
        row=row,
        repo_root=repo_root,
        workspace_dir=workspace_dir,
        candidate_path=candidate_from_workspace,
    )

    try:
        command = shlex.split(adapter_command)
        if not command:
            raise ValueError("adapter command is empty")
        completed = subprocess.run(
            command,
            cwd=repo_root,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        stdout_path.write_text(completed.stdout or "", encoding="utf-8")
        stderr_path.write_text(completed.stderr or "", encoding="utf-8")
        ledger["adapter_exit_code"] = str(completed.returncode)

        if completed.returncode != 0:
            ledger.update(
                {
                    "extraction_status": EXTRACTION_ADAPTER_FAILED,
                    "failure_bucket": FAILURE_ADAPTER_FAILED,
                    "notes": "adapter command exited non-zero; SQL was not evaluated",
                }
            )
            return ledger

        candidate_dir = out_dir / "candidate_sql"
        candidate_dir.mkdir(parents=True, exist_ok=True)
        canonical_candidate = candidate_dir / f"{row.case_id}__{row.engine}.sql"
        if candidate_from_workspace.exists() and candidate_from_workspace.read_text(
            encoding="utf-8"
        ).strip():
            shutil.copyfile(candidate_from_workspace, canonical_candidate)
            ledger.update(
                {
                    "candidate_generated": "true",
                    "candidate_sql_path": _relative_to_repo(canonical_candidate, repo_root),
                    "extraction_status": EXTRACTION_CAPTURED_FROM_CANDIDATE_FILE,
                    "failure_bucket": FAILURE_NONE,
                    "notes": "candidate captured from workspace candidate.sql",
                }
            )
        elif (completed.stdout or "").strip():
            canonical_candidate.write_text(completed.stdout, encoding="utf-8")
            ledger.update(
                {
                    "candidate_generated": "true",
                    "candidate_sql_path": _relative_to_repo(canonical_candidate, repo_root),
                    "extraction_status": EXTRACTION_CAPTURED_FROM_STDOUT,
                    "failure_bucket": FAILURE_NONE,
                    "notes": "candidate captured from adapter stdout",
                }
            )
        else:
            ledger.update(
                {
                    "extraction_status": EXTRACTION_NO_CANDIDATE_SQL,
                    "failure_bucket": FAILURE_NO_CANDIDATE_SQL,
                    "notes": "adapter succeeded but emitted no candidate SQL",
                }
            )
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text(exc.stdout or "", encoding="utf-8")
        stderr_path.write_text(exc.stderr or "", encoding="utf-8")
        ledger.update(
            {
                "adapter_exit_code": "",
                "extraction_status": EXTRACTION_ADAPTER_FAILED,
                "failure_bucket": FAILURE_ADAPTER_TIMEOUT,
                "notes": f"adapter timed out after {timeout} seconds",
            }
        )
    except Exception as exc:  # fail closed and record a local diagnostic row
        stderr_path.write_text(str(exc), encoding="utf-8")
        ledger.update(
            {
                "adapter_exit_code": "",
                "extraction_status": EXTRACTION_ADAPTER_FAILED,
                "failure_bucket": FAILURE_INTERNAL_RUNNER_ERROR,
                "notes": f"internal runner error: {exc}",
            }
        )
    return ledger


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
        ledger["notes"] = str(ledger.get("notes", "")) + "; db execution skipped because no candidate SQL was generated"
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
            "checker_config_path": _relative_to_repo(case_dir / "checker" / "checker.yaml", repo_root),
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
        "exact_rows_local": sum(row.get("exact_status") == EXACT_STATUS_EXACT for row in ledger_rows),
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
            f"- Candidate execution success rows: {summary.get('candidate_execution_success_rows', 0)}",
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
                f"- Source execution success rows: {summary.get('source_execution_success_rows', 0)}",
                f"- Candidate execution success rows: {summary.get('candidate_execution_success_rows', 0)}",
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
            _dry_run_ledger_for_row(run_id=run_id, row=row, repo_root=repo_root, out_dir=out_dir)
            for row in selected
        ]
    else:
        ledger_rows = [
            _run_adapter_for_row(
                run_id=run_id,
                row=row,
                adapter_command=args.adapter_command,
                repo_root=repo_root,
                out_dir=out_dir,
                timeout=args.adapter_timeout,
            )
            for row in selected
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
    _write_csv(out_dir / "ledger.csv", ledger_rows, LEDGER_FIELDS)

    failure_rows = [
        {
            "run_id": row["run_id"],
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "denominator_id": row["denominator_id"],
            "failure_bucket": row["failure_bucket"],
            "artifact_path": row["artifact_path"],
            "notes": row["notes"],
        }
        for row in ledger_rows
        if row["failure_bucket"] != FAILURE_NONE
    ]
    _write_csv(out_dir / "failures.csv", failure_rows, FAILURE_FIELDS)

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
