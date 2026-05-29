"""Adapter invocation and candidate capture for local user-entry runs."""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .case_package_resolver import ResolvedCasePackage
from .case_selection import SelectedCaseEngineRow
from .user_run_schema import (
    EXTRACTION_ADAPTER_FAILED,
    EXTRACTION_CAPTURED_FROM_CANDIDATE_FILE,
    EXTRACTION_CAPTURED_FROM_STDOUT,
    EXTRACTION_NO_CANDIDATE_SQL,
    FAILURE_ADAPTER_FAILED,
    FAILURE_ADAPTER_TIMEOUT,
    FAILURE_INTERNAL_RUNNER_ERROR,
    FAILURE_NO_CANDIDATE_SQL,
    FAILURE_NONE,
)


@dataclass(frozen=True)
class AdapterInvocationResult:
    """Result of invoking a user adapter for one selected row."""

    adapter_invoked: bool
    adapter_exit_code: int | None
    adapter_status: str
    candidate_generated: bool
    candidate_capture_mode: str
    candidate_sql_path: Path | None
    workspace_dir: Path
    adapter_stdout_path: Path
    adapter_stderr_path: Path
    artifact_path: str
    extraction_status: str
    failure_bucket_hint: str
    notes: str


def relative_to_repo(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def build_adapter_env(
    *,
    base_env: dict[str, str],
    run_id: str,
    row: SelectedCaseEngineRow,
    resolved_package: ResolvedCasePackage,
    workspace_dir: Path,
    candidate_path: Path,
) -> dict[str, str]:
    """Build the public adapter environment contract."""

    env = dict(base_env)
    env.update(
        {
            "SQLRB_RUN_ID": run_id,
            "SQLRB_CASE_ID": row.case_id,
            "SQLRB_POOL": row.pool,
            "SQLRB_ENGINE": row.engine,
            "SQLRB_SOURCE_SQL_PATH": str(resolved_package.source_sql_path.resolve()),
            "SQLRB_CASE_DIR": str(resolved_package.case_dir.resolve()),
            "SQLRB_WORKSPACE_DIR": str(workspace_dir.resolve()),
            "SQLRB_CANDIDATE_SQL_PATH": str(candidate_path.resolve()),
        }
    )
    return env


def run_adapter_for_case(
    *,
    run_id: str,
    row: SelectedCaseEngineRow,
    resolved_package: ResolvedCasePackage,
    adapter_command: str,
    repo_root: Path,
    out_dir: Path,
    timeout: int,
) -> AdapterInvocationResult:
    """Invoke an adapter and capture candidate SQL without judging correctness."""

    workspace_dir = out_dir / "workspaces" / row.case_id / row.engine
    workspace_dir.mkdir(parents=True, exist_ok=True)
    candidate_from_workspace = workspace_dir / "candidate.sql"
    stdout_path = workspace_dir / "adapter_stdout.txt"
    stderr_path = workspace_dir / "adapter_stderr.txt"
    artifact_path = relative_to_repo(workspace_dir, repo_root)
    env = build_adapter_env(
        base_env=os.environ,
        run_id=run_id,
        row=row,
        resolved_package=resolved_package,
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

        if completed.returncode != 0:
            return AdapterInvocationResult(
                adapter_invoked=True,
                adapter_exit_code=completed.returncode,
                adapter_status="adapter_failed",
                candidate_generated=False,
                candidate_capture_mode="none",
                candidate_sql_path=None,
                workspace_dir=workspace_dir,
                adapter_stdout_path=stdout_path,
                adapter_stderr_path=stderr_path,
                artifact_path=artifact_path,
                extraction_status=EXTRACTION_ADAPTER_FAILED,
                failure_bucket_hint=FAILURE_ADAPTER_FAILED,
                notes="adapter command exited non-zero; SQL was not evaluated",
            )

        candidate_dir = out_dir / "candidate_sql"
        candidate_dir.mkdir(parents=True, exist_ok=True)
        canonical_candidate = candidate_dir / f"{row.case_id}__{row.engine}.sql"
        if candidate_from_workspace.exists() and candidate_from_workspace.read_text(
            encoding="utf-8"
        ).strip():
            shutil.copyfile(candidate_from_workspace, canonical_candidate)
            return AdapterInvocationResult(
                adapter_invoked=True,
                adapter_exit_code=completed.returncode,
                adapter_status="success",
                candidate_generated=True,
                candidate_capture_mode="candidate_file",
                candidate_sql_path=canonical_candidate,
                workspace_dir=workspace_dir,
                adapter_stdout_path=stdout_path,
                adapter_stderr_path=stderr_path,
                artifact_path=artifact_path,
                extraction_status=EXTRACTION_CAPTURED_FROM_CANDIDATE_FILE,
                failure_bucket_hint=FAILURE_NONE,
                notes="candidate captured from workspace candidate.sql",
            )
        if (completed.stdout or "").strip():
            canonical_candidate.write_text(completed.stdout, encoding="utf-8")
            return AdapterInvocationResult(
                adapter_invoked=True,
                adapter_exit_code=completed.returncode,
                adapter_status="success",
                candidate_generated=True,
                candidate_capture_mode="stdout",
                candidate_sql_path=canonical_candidate,
                workspace_dir=workspace_dir,
                adapter_stdout_path=stdout_path,
                adapter_stderr_path=stderr_path,
                artifact_path=artifact_path,
                extraction_status=EXTRACTION_CAPTURED_FROM_STDOUT,
                failure_bucket_hint=FAILURE_NONE,
                notes="candidate captured from adapter stdout",
            )
        return AdapterInvocationResult(
            adapter_invoked=True,
            adapter_exit_code=completed.returncode,
            adapter_status="no_candidate_sql",
            candidate_generated=False,
            candidate_capture_mode="none",
            candidate_sql_path=None,
            workspace_dir=workspace_dir,
            adapter_stdout_path=stdout_path,
            adapter_stderr_path=stderr_path,
            artifact_path=artifact_path,
            extraction_status=EXTRACTION_NO_CANDIDATE_SQL,
            failure_bucket_hint=FAILURE_NO_CANDIDATE_SQL,
            notes="adapter succeeded but emitted no candidate SQL",
        )
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text(str(exc.stdout or ""), encoding="utf-8")
        stderr_path.write_text(str(exc.stderr or ""), encoding="utf-8")
        return AdapterInvocationResult(
            adapter_invoked=True,
            adapter_exit_code=None,
            adapter_status="adapter_timeout",
            candidate_generated=False,
            candidate_capture_mode="none",
            candidate_sql_path=None,
            workspace_dir=workspace_dir,
            adapter_stdout_path=stdout_path,
            adapter_stderr_path=stderr_path,
            artifact_path=artifact_path,
            extraction_status=EXTRACTION_ADAPTER_FAILED,
            failure_bucket_hint=FAILURE_ADAPTER_TIMEOUT,
            notes=f"adapter timed out after {timeout} seconds",
        )
    except Exception as exc:  # fail closed and record a local diagnostic row
        stderr_path.write_text(str(exc), encoding="utf-8")
        return AdapterInvocationResult(
            adapter_invoked=True,
            adapter_exit_code=None,
            adapter_status="internal_runner_error",
            candidate_generated=False,
            candidate_capture_mode="none",
            candidate_sql_path=None,
            workspace_dir=workspace_dir,
            adapter_stdout_path=stdout_path,
            adapter_stderr_path=stderr_path,
            artifact_path=artifact_path,
            extraction_status=EXTRACTION_ADAPTER_FAILED,
            failure_bucket_hint=FAILURE_INTERNAL_RUNNER_ERROR,
            notes=f"internal runner error: {exc}",
        )
