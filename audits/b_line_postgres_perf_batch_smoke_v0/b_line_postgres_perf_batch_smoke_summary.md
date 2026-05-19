# B-line Postgres PERF Batch Smoke v0

## Purpose and Scope

This audit records the first bounded local DB/checker batch smoke after the `PERF_0006` canary and release smoke. It executed exactly four Common-core PERF postgres rows:

- `PERF_0007`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`

The smoke used SQLGlot no-op only as an adapter command through the existing method-agnostic user runner. It did not add SQLGlot-specific logic to the core runner or DB/checker modules.

This task did not compute official metrics, collect timing, render paper tables, implement paper reproduction, implement retained-evidence adapters, update reports/results, update retained evidence, update denominators, update `case_sets/`, migrate cases, create a global leaderboard, modify the legacy repo, or modify raw legacy evidence.

## Environment Preflight

- Release repo: clean and aligned with `origin/main` before intended task writes.
- `psql --version`: passed.
- `psql -c "select 1;"`: passed.
- SQLGlot import: passed in the current Python environment.
- DB credentials, full DSNs, `PGPASSWORD`, and environment values were not recorded.
- Target output directory `runs/user/postgres_perf_sqlglot_noop_batch_smoke` was absent before the run.

## Batch Command

The audit case list was created at:

`audits/b_line_postgres_perf_batch_smoke_v0/postgres_perf_batch_cases.txt`

Command run:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list audits/b_line_postgres_perf_batch_smoke_v0/postgres_perf_batch_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/postgres_perf_sqlglot_noop_batch_smoke \
  --enable-db-execution \
  --enable-checker
```

## Batch Result

The runner completed successfully:

- selected rows: 4
- candidate-generated rows: 4
- source execution success rows: 4
- candidate execution success rows: 4
- checker success rows: 4
- checker mismatch rows: 0
- local exact rows: 4
- local mismatch rows: 0

All four rows recorded:

- `source_execution_status=source_execution_success`
- `candidate_execution_status=candidate_execution_success`
- `checker_status=checker_success`
- `exact_status=exact`
- `failure_bucket=none`
- `local_execution_only=true`
- `official_metric_input=false`
- `retained_evidence_input=false`

## Artifact Result

For each selected row, the local run output contains:

- candidate SQL under `candidate_sql/`
- source execution result under `workspaces/<case_id>/postgres/execution/source_result.jsonl`
- candidate execution result under `workspaces/<case_id>/postgres/execution/candidate_result.jsonl`
- checker result under `workspaces/<case_id>/postgres/checker/checker_result.json`

No mismatch artifact was created because all four local checker comparisons were exact.

## Output Hygiene

All run output stayed under:

`runs/user/postgres_perf_sqlglot_noop_batch_smoke/`

`git status --short runs/user` produced no staged or tracked output. The smoke output remains local and ignored.

## Protected Boundary Summary

Protected path checks produced no output for:

- `cases/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`

No denominator files or paper result files changed. No case-local `runs/` directory was written.

## Interpretation

These results are local diagnostics only. They are not official Generation Rate, Execution Coverage Rate, Result Consistency Rate, speedup, paper results, retained evidence, or leaderboard output.

## Validation Summary

Validation passed:

- user-entry CI smoke passed
- fixture smoke passed
- summary JSON invariant checks passed
- results CSV checks passed
- protected-path checks passed
- smoke output not staged
- `git diff --check` passed

## Exact Next Safe Action

Review the four-row local batch smoke. If acceptable, authorize a separate bounded follow-up for either another small PERF postgres batch or DB/checker hardening, still with local `runs/user/` output only and no timing, official metrics, retained evidence, reports/results updates, denominator changes, paper-result changes, or leaderboard output.
