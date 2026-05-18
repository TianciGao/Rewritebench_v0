#!/usr/bin/env python3
"""Run the lightweight B-line user-entry CI smoke.

This script verifies the existing non-DB user-entry public surface from the
current checkout. It intentionally does not execute SQL, run checkers, collect
timing, compute official metrics, parse retained evidence, or mutate reports
or results.
"""

from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from importlib.util import find_spec
from pathlib import Path


EXPECTED_RUN_FILES = [
    "config.yaml",
    "selected_cases.csv",
    "ledger.csv",
    "summary.json",
    "failures.csv",
    "report.md",
]
PROTECTED_PATHS = ["cases", "case_sets", "inventory", "reports", "results"]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def smoke_env(root: Path) -> dict[str, str]:
    env = dict(os.environ)
    src = str(root / "src")
    current = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = src if not current else src + os.pathsep + current
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_command(
    label: str,
    command: list[str],
    *,
    root: Path,
    env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    print(f"[run] {label}")
    completed = subprocess.run(
        command,
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        print(f"[fail] {label}: exit {completed.returncode}", file=sys.stderr)
        if completed.stdout:
            print("--- stdout ---", file=sys.stderr)
            print(completed.stdout[-4000:], file=sys.stderr)
        if completed.stderr:
            print("--- stderr ---", file=sys.stderr)
            print(completed.stderr[-4000:], file=sys.stderr)
        raise SystemExit(completed.returncode)
    print(f"[pass] {label}")
    return completed


def choose_test_command() -> tuple[str, list[str]]:
    if find_spec("pytest") is not None:
        return "user-entry tests via pytest", [sys.executable, "-m", "pytest", "tests/user_entry", "-q"]
    return (
        "user-entry tests via unittest",
        [sys.executable, "-m", "unittest", "discover", "-s", "tests/user_entry", "-q"],
    )


def write_perf_case_list(root: Path) -> Path:
    cases_path = root / "case_sets" / "common_core_v0" / "cases.csv"
    selected: list[str] = []
    with cases_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("pool") == "PERF" and row.get("common_core_v0_member") == "true":
                selected.append(row["case_id"])
            if len(selected) == 2:
                break
    if len(selected) < 1:
        raise SystemExit("no Common-core PERF cases found for user-entry smoke")
    temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False)
    with temp:
        temp.write("\n".join(selected) + "\n")
    print(f"[info] selected smoke cases: {', '.join(selected)}")
    return Path(temp.name)


def reset_smoke_output(root: Path, relative_out: str) -> None:
    out_dir = (root / relative_out).resolve()
    allowed_root = (root / "runs" / "user").resolve()
    if allowed_root not in out_dir.parents:
        raise SystemExit(f"refusing to remove non-user smoke output: {out_dir}")
    shutil.rmtree(out_dir, ignore_errors=True)


def run_user_smoke(
    label: str,
    *,
    root: Path,
    env: dict[str, str],
    case_list_path: Path,
    relative_out: str,
    dry_run: bool,
) -> dict[str, object]:
    reset_smoke_output(root, relative_out)
    command = [
        sys.executable,
        "-m",
        "sql_rewrite_bench.user_run",
        "--case-set",
        "common_core_v0",
        "--pool",
        "PERF",
        "--engine",
        "postgres",
        "--case-list",
        str(case_list_path),
        "--adapter-command",
        f"{sys.executable} tests/user_entry/fixtures/dummy_adapter.py",
        "--out",
        relative_out,
    ]
    if dry_run:
        command.append("--dry-run")
    run_command(label, command, root=root, env=env)
    out_dir = root / relative_out
    verify_output_files(out_dir)
    summary = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
    verify_summary(label, out_dir, summary, dry_run=dry_run)
    return summary


def verify_output_files(out_dir: Path) -> None:
    missing = [name for name in EXPECTED_RUN_FILES if not (out_dir / name).exists()]
    if missing:
        raise SystemExit(f"missing smoke output files in {out_dir}: {', '.join(missing)}")


def verify_summary(label: str, out_dir: Path, summary: dict[str, object], *, dry_run: bool) -> None:
    selected_rows = int(summary.get("selected_rows", 0))
    adapter_invoked_rows = int(summary.get("adapter_invoked_rows", 0))
    candidate_generated_rows = int(summary.get("candidate_generated_rows", 0))
    if selected_rows < 1:
        raise SystemExit(f"{label}: expected at least one selected row")
    if dry_run and (adapter_invoked_rows != 0 or candidate_generated_rows != 0):
        raise SystemExit(f"{label}: dry-run should not invoke adapter or generate candidates")
    if not dry_run and (
        adapter_invoked_rows != selected_rows or candidate_generated_rows != selected_rows
    ):
        raise SystemExit(f"{label}: dummy adapter should generate one candidate per selected row")

    with (out_dir / "ledger.csv").open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != selected_rows:
        raise SystemExit(f"{label}: ledger row count does not match selected_rows")
    if dry_run:
        if {row["extraction_status"] for row in rows} != {"skipped_dry_run"}:
            raise SystemExit(f"{label}: unexpected dry-run extraction status")
    else:
        if {row["extraction_status"] for row in rows} != {"captured_from_candidate_file"}:
            raise SystemExit(f"{label}: unexpected adapter extraction status")
        if not all(row["candidate_sql_path"].startswith("runs/user/") for row in rows):
            raise SystemExit(f"{label}: candidate SQL paths must stay under runs/user/")


def verify_git_clean_for_paths(root: Path, env: dict[str, str], paths: list[str], label: str) -> None:
    completed = run_command(
        label,
        ["git", "status", "--short", *paths],
        root=root,
        env=env,
    )
    if completed.stdout.strip():
        raise SystemExit(f"{label}: unexpected git status output:\n{completed.stdout}")


def main() -> int:
    root = repo_root()
    env = smoke_env(root)

    run_command(
        "module help",
        [sys.executable, "-m", "sql_rewrite_bench.user_run", "--help"],
        root=root,
        env=env,
    )
    run_command(
        "wrapper help",
        [sys.executable, "scripts/user/run_user_benchmark.py", "--help"],
        root=root,
        env=env,
    )

    test_label, test_command = choose_test_command()
    run_command(test_label, test_command, root=root, env=env)

    case_list_path = write_perf_case_list(root)
    try:
        dry_summary = run_user_smoke(
            "dry-run smoke",
            root=root,
            env=env,
            case_list_path=case_list_path,
            relative_out="runs/user/ci_smoke_dry_run",
            dry_run=True,
        )
        adapter_summary = run_user_smoke(
            "dummy adapter smoke",
            root=root,
            env=env,
            case_list_path=case_list_path,
            relative_out="runs/user/ci_smoke_adapter",
            dry_run=False,
        )
    finally:
        case_list_path.unlink(missing_ok=True)

    verify_git_clean_for_paths(root, env, PROTECTED_PATHS, "protected paths unchanged")
    verify_git_clean_for_paths(root, env, ["runs/user"], "runs/user smoke outputs unstaged")

    print("user-entry ci smoke passed")
    print(f"dry-run selected_rows={dry_summary['selected_rows']}")
    print(
        "adapter selected_rows="
        f"{adapter_summary['selected_rows']} "
        f"candidate_generated_rows={adapter_summary['candidate_generated_rows']}"
    )
    print("non-db boundary preserved: no SQL execution, no checker execution, no metrics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
