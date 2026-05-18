# B-line SQLGlot Enabled Smoke Summary

## Purpose and Scope

This audit verifies the optional SQLGlot dependency path for the B-line non-DB user-entry runner. It installs the release package with the `sqlglot` optional extra in an isolated temporary clone, runs SQLGlot no-op and optimize adapter routes through the existing user-entry runner, and verifies local candidate SQL capture under `runs/user/<run_id>/`.

This task did not implement features, execute SQL, run database engines, run checkers, collect timing, compute official metrics, render paper tables, implement paper reproduction, implement retained-evidence adapters, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, create a leaderboard, or modify raw legacy evidence.

## Temporary Checkout Method

- Source checkout: `/home/tianci_gao/code/Rewritebench_v0`
- Temporary clone root: `/tmp/sqlrb_sqlglot_enabled_smoke/Rewritebench_v0_sqlglot_smoke`
- Environment: `.venv-sqlglot-smoke` inside the temporary clone
- Install command: `python -m pip install -e ".[sqlglot]"`
- Smoke case list: `PERF_0006`, `PERF_0007`
- Engine: `postgres`
- User-run output roots: `runs/user/sqlglot_enabled_noop_dry_run`, `runs/user/sqlglot_enabled_noop_smoke`, and `runs/user/sqlglot_enabled_optimize_smoke` in the temporary clone only

## Optional Dependency Install Result

Editable install with the SQLGlot optional extra passed in the temporary virtual environment.

- SQLGlot dependency available: yes
- SQLGlot version observed: `30.8.0`
- Package installed editable: yes

## SQLGlot Import Result

`import sqlglot` passed in the temporary virtual environment.

## Adapter Help Result

`python baselines/sqlglot/sqlglot_user_adapter.py --help` passed in the temporary clone.

## Dry-Run Result

The SQLGlot no-op adapter command was used in user-entry dry-run mode:

- Selected rows: 2
- Adapter invocations: 0
- Candidate SQL rows generated: 0
- Dry-run ledger status: `skipped_dry_run`
- Non-DB execution/checker/timing status boundaries preserved

## Real No-Op Adapter Smoke Result

The SQLGlot no-op route passed through the user-entry runner.

- Selected rows: 2
- Adapter invocations: 2
- Candidate SQL rows generated: 2
- Candidate files created under `runs/user/sqlglot_enabled_noop_smoke/candidate_sql/`
- Ledger rows used `captured_from_candidate_file`
- Execution status remained `not_run_non_db_mvp`
- Checker status remained `not_run_non_db_mvp`
- Exact status remained `not_evaluated_non_db_mvp`
- Timed status remained `not_timed_non_db_mvp`

## Real Optimize Adapter Smoke Result

The SQLGlot optimize route passed through the user-entry runner.

- Selected rows: 2
- Adapter invocations: 2
- Candidate SQL rows generated: 2
- Candidate files created under `runs/user/sqlglot_enabled_optimize_smoke/candidate_sql/`
- Ledger rows used `captured_from_candidate_file`
- Execution status remained `not_run_non_db_mvp`
- Checker status remained `not_run_non_db_mvp`
- Exact status remained `not_evaluated_non_db_mvp`
- Timed status remained `not_timed_non_db_mvp`

## Candidate SQL Capture Result

Candidate SQL capture passed for both real SQLGlot routes:

- No-op route: 2 candidate SQL files
- Optimize route: 2 candidate SQL files
- Both real smoke summaries reported `candidate_generated_rows > 0`
- Both real smoke ledgers reported `candidate_generated=true` for successful rows

## Output Hygiene Result

All smoke outputs were created under `runs/user/` in the temporary clone. `git status --short runs/user` in the temporary clone produced no tracked or staged output.

## Protected Boundary Result

Protected path checks in the temporary clone reported no changes under:

- `cases/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`

Release-repo validation also preserved these protected paths.

## Unsupported Features

The SQLGlot enabled smoke remains candidate-generation-only. The following remain intentionally unsupported:

- DB execution
- Checker execution
- Timing collection
- Official metric computation
- Paper table rendering
- Paper reproduction CLI
- Retained-evidence adapter implementation
- Reports/results updates
- Denominator changes
- Paper-result changes
- Global leaderboard output

## Validation Summary

Validation passed:

- Temporary clone created.
- Temporary virtual environment created.
- Editable install with `.[sqlglot]` passed.
- SQLGlot import passed.
- Adapter help passed.
- SQLGlot no-op dry-run smoke passed.
- Real SQLGlot no-op smoke passed.
- Real SQLGlot optimize smoke passed.
- Candidate SQL files were generated for real smoke routes.
- Ledger `candidate_generated=true` rows were present.
- Non-DB statuses were preserved.
- Temporary clone smoke outputs stayed under ignored `runs/user/`.
- Protected paths stayed unchanged.
- Release-repo user-entry CI smoke passed.
- Release-repo fixture smoke passed.
- Summary JSON parsed and boundary invariants passed.
- `git diff --check` passed.

## Exact Next Safe Action

Use the SQLGlot-enabled smoke result as validation that optional candidate-generation adapters can plug into the non-DB user-entry runner. Any DB execution, checker execution, official metrics, timing, retained-evidence integration, paper reproduction, or leaderboard design should be separately authorized before implementation.
