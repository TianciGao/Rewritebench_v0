# B-line User Entry MVP v0

## Purpose And Scope

This task implements a minimal non-DB user runner skeleton for SQL-RewriteBench. The runner lets an external user invoke an adapter command once per selected Common-core v0 case-engine row and captures candidate SQL as local user output under `runs/user/<run_id>/`.

This task does not migrate cases, update `case_sets/`, update inventory, change denominators, change paper results, write reports/results, implement retained-evidence adapters, implement paper reproduction, execute SQL, run checkers, collect timing, compute official metrics, render paper tables, or modify raw legacy evidence.

## Implementation Summary

Implemented module-first user-entry MVP files:

- `src/sql_rewrite_bench/__init__.py`
- `src/sql_rewrite_bench/case_selection.py`
- `src/sql_rewrite_bench/user_run_schema.py`
- `src/sql_rewrite_bench/user_run.py`

Implemented standard-library tests and dummy adapters:

- `tests/user_entry/test_case_selection.py`
- `tests/user_entry/test_user_run_outputs.py`
- `tests/user_entry/fixtures/dummy_adapter.py`
- `tests/user_entry/fixtures/empty_adapter.py`

Added `runs/.gitignore` so local run output under `runs/user/` is not committed by default.

## Command Examples

Run with `PYTHONPATH=src` until packaging is separately added:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list /path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/demo_run
```

Smoke command used in validation:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list <small temp case list> \
  --adapter-command "python tests/user_entry/fixtures/dummy_adapter.py" \
  --out runs/user/smoke_user_entry_mvp
```

## Output-root Policy

The runner refuses `--out` paths outside `runs/user/<run_id>/`. Invalid examples include `cases/.../runs/...`, `results/retained/...`, `reports/evaluation/...`, absolute paths such as `/tmp/demo`, and paths with `..`.

User outputs are local runtime artifacts and must not enter case packages, case-local `runs/`, retained paper evidence, reports/results, or leaderboard outputs.

## Adapter Invocation Behavior

For each selected case-engine row, the runner creates:

```text
runs/user/<run_id>/workspaces/<case_id>/<engine>/
```

The adapter is invoked with `shell=False` using `shlex.split`, with the subprocess working directory set to the repository root. Per-row context is passed through environment variables:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

The runner captures stdout and stderr into the per-row workspace. If workspace `candidate.sql` exists and is non-empty, it is copied into `candidate_sql/<case_id>__<engine>.sql`; otherwise non-empty stdout is captured as candidate SQL. Candidate SQL is not executed, checked, timed, scored, or treated as retained paper evidence.

## Output Files

Each run writes:

- `config.yaml`
- `selected_cases.csv`
- `candidate_sql/`
- `workspaces/`
- `ledger.csv`
- `summary.json`
- `failures.csv`
- `report.md`

The ledger row grain is one selected case-engine row. MVP statuses use `not_run_non_db_mvp`, `not_evaluated_non_db_mvp`, and `not_timed_non_db_mvp` for execution/checker/exact/timing fields.

## Validation Summary

- `PYTHONPATH=src python -m unittest discover -s tests/user_entry -q`: passed, 6 tests.
- Dummy adapter smoke: passed, 2 selected rows and 2 captured candidates under `runs/user/smoke_user_entry_mvp/`.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Summary JSON invariant check: passed.
- Boundary checks: passed; no files under `cases/`, `case_sets/`, `inventory/`, `reports/`, or `results/` changed.
- `git diff --check`: passed.

## Boundaries

- Public runner skeleton implemented: yes.
- Non-DB MVP only: yes.
- DB execution implemented: no.
- Checker execution implemented: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Paper reproduction CLI implemented: no.
- Retained-evidence adapter implemented: no.
- Case migration performed: no.

## Exact Next Safe Action

Authorize a B-line user-entry hardening task to add packaging/CLI documentation, stable tests, output hygiene checks, and optional dry-run mode while still keeping DB execution, checker execution, timing, official metrics, paper reproduction, retained evidence, reports/results, denominators, case sets, and raw legacy evidence unchanged.
