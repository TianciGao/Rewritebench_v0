# B-line User Entry Hardening v0

## Purpose And Scope

This task hardens the existing non-DB B-line user-entry MVP so an external user can try the runner more safely. The work remains limited to local adapter capture under `runs/user/<run_id>/`.

This task does not migrate cases, execute SQL, run DB engines, run checkers, collect timing, compute official metrics, render paper tables, implement a paper reproduction CLI, implement retained-evidence adapters, update `case_sets/`, update inventory, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

## What Was Hardened

- Added `--dry-run` to resolve Common-core v0 selections and write local run files without invoking the adapter.
- Added `scripts/user/run_user_benchmark.py` as a thin wrapper around `sql_rewrite_bench.user_run`.
- Strengthened output-root error messaging so invalid paths explicitly point users to `runs/user/<run_id>/`.
- Expanded tests for candidate capture from workspace `candidate.sql`, candidate capture from stdout, adapter nonzero exit, empty adapter output, adapter timeout, dry-run behavior, and invalid output roots.
- Improved `report.md` content with command summary, dry-run flag, selected-row count, pool/engine breakdowns, adapter/candidate counts, failure buckets, artifact links, and explicit local-output/no-paper/no-metrics/no-leaderboard warnings.
- Added a user-guide preview for the MVP runner without promoting final public documentation.

## Dry-run Behavior

Dry-run mode uses the same metadata-driven Common-core v0 selection as the normal runner. It writes `config.yaml`, `selected_cases.csv`, `ledger.csv`, `summary.json`, `failures.csv`, and `report.md` under the requested `runs/user/<run_id>/` root.

In dry-run rows:

- `adapter_invoked=false`
- `candidate_generated=false`
- `extraction_status=skipped_dry_run`
- `execution_status=not_run_non_db_mvp`
- `checker_status=not_run_non_db_mvp`
- `exact_status=not_evaluated_non_db_mvp`
- `timed_status=not_timed_non_db_mvp`
- `failure_bucket=none`

No adapter command is invoked in dry-run mode and no candidate SQL is created from adapter output.

## Output-root Hygiene Behavior

The runner continues to reject output paths outside `runs/user/<run_id>/`, including case-local `runs/`, `results/retained/`, `reports/evaluation/`, absolute paths such as `/tmp/demo`, and parent-relative paths such as `../demo`.

Local smoke outputs remain ignored by `runs/.gitignore` and are not staged.

## Adapter Failure Handling

Adapter failures remain local diagnostic rows only. Nonzero exit maps to `extraction_status=adapter_failed` and `failure_bucket=adapter_failed`. Empty successful output maps to `extraction_status=no_candidate_sql` and `failure_bucket=no_candidate_sql`. Timeout support already existed and is now covered by a test, mapping to `failure_bucket=adapter_timeout`.

Candidate SQL is still never executed, checked, timed, scored, or treated as retained paper evidence.

## Report And User-guide Changes

`report.md` now makes the runner mode and boundaries clearer:

- command form and adapter command
- dry-run flag
- output root
- selected row and unique-case counts
- pool and engine breakdowns
- adapter invocation and candidate generation counts
- failure bucket table
- artifact links
- local-output-only warning
- not-retained-paper-evidence warning
- official-metrics-not-computed warning
- no-global-leaderboard warning

`audits/b_line_user_entry_hardening_v0/user_guide_preview.md` documents minimal use, dry-run, dummy adapter behavior, adapter environment variables, output files, and current limitations.

## Validation Summary

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/user_entry -q`: passed, 10 tests.
- Dry-run smoke: passed; 2 selected rows, 0 adapter invocations, 0 candidates, `skipped_dry_run` ledger rows.
- Dummy adapter smoke: passed; 2 selected rows and 2 candidate SQL files under ignored `runs/user/smoke_user_entry_hardening_adapter/`.
- Thin wrapper help command: passed.
- `python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Boundary checks: no tracked changes under `cases/`, `case_sets/`, `inventory/`, `reports/`, or `results/`.

## Remaining Unsupported Features

- DB execution is not implemented.
- Checker execution is not implemented.
- Timing collection is not implemented.
- Official benchmark metrics are not computed.
- Paper table rendering is not implemented.
- Paper reproduction CLI is not implemented.
- Retained-evidence adapter implementation is not included.
- User outputs are not retained paper evidence and do not create a leaderboard.

## Exact Next Safe Action

Authorize a documentation and packaging stabilization task for the B-line user-entry MVP, or separately authorize a future DB/checker execution design packet. Keep case packages, `case_sets/`, inventory, denominators, reports/results, paper results, retained evidence, and raw legacy evidence unchanged until a separate task explicitly authorizes those surfaces.
