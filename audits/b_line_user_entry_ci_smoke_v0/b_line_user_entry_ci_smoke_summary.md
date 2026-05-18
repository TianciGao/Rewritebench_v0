# B-line User Entry CI Smoke v0

## Purpose And Scope

This task wires the already implemented, hardened, documented, and release-smoked non-DB B-line user-entry MVP into a lightweight CI/dev-smoke path.

The task does not implement new user-run features, execute SQL, run database engines, run checkers, collect timing, compute official metrics, render paper tables, implement SQLGlot/Calcite/R-Bot adapters, implement paper reproduction, implement retained-evidence adapters, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

## Files Created

- `.github/workflows/user_entry_smoke.yml`
- `scripts/dev/run_user_entry_ci_smoke.py`
- `audits/b_line_user_entry_ci_smoke_v0/b_line_user_entry_ci_smoke_summary.md`
- `audits/b_line_user_entry_ci_smoke_v0/b_line_user_entry_ci_smoke_validation_results.csv`
- `audits/b_line_user_entry_ci_smoke_v0/b_line_user_entry_ci_smoke_summary.json`
- `audits/b_line_user_entry_ci_smoke_v0/ci_smoke_command_log.md`

## Dev-smoke Behavior

`scripts/dev/run_user_entry_ci_smoke.py` runs from the current checkout and verifies:

- module help for `python -m sql_rewrite_bench.user_run --help`
- wrapper help for `python scripts/user/run_user_benchmark.py --help`
- user-entry tests via `pytest` when available, otherwise standard-library `unittest`
- a two-case Common-core PERF dry-run smoke under `runs/user/ci_smoke_dry_run`
- a two-case Common-core PERF dummy-adapter smoke under `runs/user/ci_smoke_adapter`
- expected output files for both smoke runs
- selected rows, dry-run adapter counts, dummy-adapter candidate counts, and extraction statuses
- protected paths `cases/`, `case_sets/`, `inventory/`, `reports/`, and `results/` remain clean
- smoke output under `runs/user/` remains ignored/unstaged

The script sets `PYTHONPATH=src` for subprocesses so it can be used before or after editable install. It does not invoke DB engines, checkers, timing workloads, metric computation, paper rendering, or retained-evidence parsing.

## CI Workflow Behavior

`.github/workflows/user_entry_smoke.yml` runs on `push`, `pull_request`, and `workflow_dispatch`.

The workflow:

- checks out the repository
- uses Python 3.11
- installs the package with `python -m pip install -e .`
- runs `python scripts/dev/run_user_entry_ci_smoke.py`
- runs `python scripts/dev/smoke_ledger_fixtures.py`
- runs `git diff --check`
- verifies protected paths and `runs/user` smoke outputs have no tracked/untracked status output

It intentionally installs no DB engines, SQLGlot, Calcite, Java, Spark, LLM, timing, or checker dependencies.

## Validation Summary

Local validation passed:

- `PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`
- `python scripts/dev/smoke_ledger_fixtures.py`
- workflow YAML parse with PyYAML
- summary JSON invariant check
- protected-path boundary checks
- `git diff --check`

The local dev-smoke selected `PERF_0006` and `PERF_0007`, wrote dry-run and dummy-adapter outputs only under ignored `runs/user/` directories, and left protected paths unchanged.

## Protected Boundary Summary

- `cases/` changed: no
- `case_sets/` changed: no
- `inventory/` changed: no
- `reports/` changed: no
- `results/` changed: no
- denominator changed: no
- paper results changed: no
- raw legacy evidence changed: no
- official metrics computed: no
- paper tables rendered: no

## Unsupported Features

- DB execution remains unsupported.
- Checker execution remains unsupported.
- Timing collection remains unsupported.
- Official benchmark metrics remain unsupported for user-entry smoke.
- Paper reproduction remains unsupported.
- Retained-evidence adapter implementation remains unsupported.
- SQLGlot, Calcite, and R-Bot adapters are not implemented.
- User outputs remain local experiment outputs and do not create retained paper evidence or a leaderboard.

## Exact Next Safe Action

Use the new user-entry smoke workflow as a push/PR guard. Separately authorize either a B-line publication-surface closeout or a DB/checker execution design packet; keep case packages, `case_sets/`, inventory, denominators, reports/results, paper results, retained evidence, and raw legacy evidence unchanged unless separately authorized.
