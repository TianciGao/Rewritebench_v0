# B-line SQLGlot Adapter MVP v0

## Purpose And Scope

This task adds optional SQLGlot no-op and optimize routes as non-DB user-entry adapters. The adapters plug into the existing B-line user runner through `--adapter-command` and generate candidate SQL only.

This task does not execute SQL, run database engines, run checkers, collect timing, compute official metrics, compute speedup, render paper tables, implement paper reproduction, implement retained-evidence adapters, parse candidate status retained evidence, migrate cases, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, create a global leaderboard, or modify raw legacy evidence.

## Files Created Or Modified

Created:

- `baselines/sqlglot/README.md`
- `baselines/sqlglot/sqlglot_user_adapter.py`
- `tests/user_entry/test_sqlglot_adapter.py`
- `audits/b_line_sqlglot_adapter_mvp_v0/b_line_sqlglot_adapter_mvp_summary.md`
- `audits/b_line_sqlglot_adapter_mvp_v0/b_line_sqlglot_adapter_mvp_validation_results.csv`
- `audits/b_line_sqlglot_adapter_mvp_v0/b_line_sqlglot_adapter_mvp_summary.json`
- `audits/b_line_sqlglot_adapter_mvp_v0/sqlglot_adapter_command_log.md`
- `audits/b_line_sqlglot_adapter_mvp_v0/sqlglot_adapter_smoke_manifest.csv`

Modified:

- `docs/USER_BENCHMARK_GUIDE.md`
- `pyproject.toml`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Adapter Routes Added

- `sqlglot_noop`: `python baselines/sqlglot/sqlglot_user_adapter.py --route noop`
- `sqlglot_optimize`: `python baselines/sqlglot/sqlglot_user_adapter.py --route optimize`

Both routes read `SQLRB_SOURCE_SQL_PATH`, infer dialect from `SQLRB_ENGINE`, and write candidate SQL to `SQLRB_CANDIDATE_SQL_PATH`.

Supported engine-to-dialect mapping:

- `postgres` -> `postgres`
- `mysql` -> `mysql`
- `spark` -> `spark`

The adapter validates required user-run environment variables, source path existence, engine support, route selection, SQLGlot availability, parse success, and non-empty candidate emission. It exits nonzero on failure and does not silently fall back to raw source SQL.

## Dependency Status

SQLGlot dependency available in this environment: no.

The adapter dependency guard was validated. With required environment variables and a source SQL file present, the adapter exits nonzero with:

```text
SQLGlot is not installed. Install optional SQLGlot support before using this adapter.
```

`pyproject.toml` now exposes SQLGlot as an optional extra only:

```toml
[project.optional-dependencies]
sqlglot = ["sqlglot"]
```

SQLGlot was not added as a required dependency and was not installed during this task.

## Dry-run And User-run Compatibility

The SQLGlot adapter command is compatible with the existing user-entry runner. Dry-run mode resolves selection and writes local output files without invoking the adapter, so it passes even when SQLGlot is not installed.

Validated dry-run command shape:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list <small temp case list> \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/sqlglot_noop_dry_run_smoke \
  --dry-run
```

## Real SQLGlot Smoke Result

Real `sqlglot_noop` smoke: skipped because SQLGlot is not installed.

Real `sqlglot_optimize` smoke: skipped because SQLGlot is not installed.

Candidate SQL capture through the real SQLGlot adapter was not exercised in this environment. The user-run tests include conditional real no-op/optimize smoke tests that will run automatically when SQLGlot is available.

## Boundaries

- Non-DB MVP only: yes.
- DB execution implemented: no.
- Checker execution implemented: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Raw legacy evidence changed: no.
- Global leaderboard created: no.

## Validation Summary

- Adapter help passed.
- Unit tests passed: 19 tests run, 2 real-SQLGlot tests skipped because SQLGlot is unavailable.
- Missing dependency guard passed.
- Route validation passed.
- SQLGlot dry-run user-run compatibility passed.
- User-entry CI smoke passed.
- Synthetic ledger fixture smoke passed.
- Summary JSON invariant check passed.
- Boundary checks passed.
- `git diff --check` passed.

## Exact Next Safe Action

Optionally authorize a follow-up SQLGlot-enabled environment smoke that installs `.[sqlglot]` and runs the real no-op/optimize adapter routes, still without DB execution, checker execution, official metrics, paper rendering, retained-evidence updates, reports/results updates, denominator changes, paper-result changes, or leaderboard output.
