# B-line User Entry Packaging / Documentation v0

## Purpose And Scope

This task stabilizes the already implemented and hardened non-DB B-line user-entry MVP for easier public-facing use. It adds stable user documentation, run-artifact policy documentation, minimal packaging metadata, README discoverability, and validation coverage for help commands and documented CLI options.

This task does not migrate cases, execute SQL, run DB engines, run checkers, collect timing, compute official metrics, render paper tables, implement SQLGlot/Calcite/R-Bot baselines, implement paper reproduction, implement retained-evidence adapters, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

## Files Promoted From Preview To Public Docs

- `audits/b_line_user_entry_hardening_v0/user_guide_preview.md` was promoted into `docs/USER_BENCHMARK_GUIDE.md`.
- `docs/USER_BENCHMARK_GUIDE.md` documents installation/import modes, module and wrapper commands, dry-run use, dummy adapter use, adapter environment variables, output files, output-root rules, and MVP limitations.
- `docs/RUN_ARTIFACT_POLICY.md` documents the boundary between case-local legacy retained evidence, local `runs/user/<run_id>/` outputs, curated retained results, curated reports, and the no-global-leaderboard rule.
- `README.md` received a short pointer to the user guide and states that the current user-entry MVP is non-DB adapter capture only.

## Packaging Changes

Created `pyproject.toml` with minimal editable-install metadata:

- project name: `sql-rewrite-bench`
- Python requirement: `>=3.10`
- package discovery under `src`
- runtime dependencies: none

No DB engine, SQLGlot, Calcite, Java, LLM, timing, or checker dependency was introduced.

## Wrapper And Help Behavior

`scripts/user/run_user_benchmark.py` remains a thin wrapper around `sql_rewrite_bench.user_run`. Validation confirmed:

- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help` works.
- `PYTHONPATH=src python scripts/user/run_user_benchmark.py --help` works.
- Both surfaces expose the same core options, including `--case-set`, `--pool`, `--engine`, `--case-list`, `--adapter-command`, `--out`, `--adapter-timeout`, and `--dry-run`.

## Validation Summary

- `python -m pytest tests/user_entry -q`: unavailable in this environment because `pytest` is not installed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/user_entry -q`: passed, 12 tests.
- Module help check: passed.
- Wrapper help check: passed.
- Dry-run smoke: passed with 2 selected rows, 0 adapter invocations, 0 generated candidates, and `skipped_dry_run` extraction status.
- Dummy adapter smoke: passed with 2 selected rows and 2 captured candidates.
- `pyproject.toml` parse/check: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Boundary checks: no tracked changes under `cases/`, `case_sets/`, `inventory/`, `reports/`, or `results/`.

## Remaining Unsupported Features

- DB execution is not implemented.
- Checker execution is not implemented.
- Timing collection is not implemented.
- Official benchmark metrics are not computed.
- Paper table rendering is not implemented.
- SQLGlot, Calcite, and R-Bot baselines are not implemented.
- Paper reproduction CLI is not implemented.
- Retained-evidence adapter implementation is not included.
- User outputs are not retained paper evidence and do not create a leaderboard.

## Exact Next Safe Action

Authorize a B-line user-entry release-smoke task to verify editable install behavior and local output hygiene in a fresh checkout, or separately authorize a future DB/checker execution design packet. Keep case packages, `case_sets/`, inventory, denominators, reports/results, paper results, retained evidence, and raw legacy evidence unchanged until a separate task explicitly authorizes those surfaces.
