# User Entry MVP Task Plan

## Proposed Next Task Title

`b_line_user_entry_mvp_v0`

## MVP Scope

Implement a minimal user runner skeleton only. The MVP should resolve Common-core v0 case selections from `case_sets/` and `inventory/`, invoke a user adapter command in a per-row workspace, capture candidate SQL or adapter failure diagnostics, and write local run outputs under `runs/user/<run_id>/`.

The MVP should not run DB engines, execute checkers, compute metrics, render paper tables, migrate cases, parse retained evidence, or update reports/results.

## Files Allowed To Modify In MVP

Proposed allowed implementation files for a later authorized task:

- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/case_selection.py`
- `src/sql_rewrite_bench/user_run_schema.py`
- `scripts/user/` only if a script wrapper is selected
- `tests/user_entry/`
- `.gitignore` or `runs/.gitignore` only to keep local run outputs untracked
- future docs under `docs/` if documentation is included in the MVP

The MVP must not modify `cases/`, `case_sets/`, `inventory/`, `reports/`, `results/`, paper-result artifacts, denominator files, or raw legacy evidence.

## Scripts And Source Layout Proposal

Use module-first layout:

```text
src/sql_rewrite_bench/
  __init__.py
  user_run.py
  case_selection.py
  user_run_schema.py
tests/user_entry/
```

The future command should be:

```bash
python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --adapter-command "python my_rewriter.py" --out runs/user/<run_id>
```

## Validation Plan

- Unit-test case selection against `case_sets/common_core_v0/cases.csv` and `denominator_same_engine_120.csv`.
- Use a dummy adapter that writes deterministic candidate SQL.
- Verify outputs are written only under the configured `runs/user/<run_id>/` root.
- Verify `ledger.csv`, `summary.json`, `failures.csv`, and `report.md` are produced.
- Verify no files under `cases/`, `case_sets/`, `inventory/`, `reports/`, or `results/` change.
- Run fixture smoke.
- Run `git diff --check`.

## Stop Conditions

Stop if MVP implementation would require DB execution, checker execution, timing collection, retained-evidence parsing, case migration, denominator changes, case-set changes, reports/results writes, paper-result updates, or case-local `runs/` writes.

## Boundaries

- No denominator change.
- No paper result change.
- No retained reports/results update.
- No case-local `runs/` write.
- No global leaderboard.
- No official metrics computation.
