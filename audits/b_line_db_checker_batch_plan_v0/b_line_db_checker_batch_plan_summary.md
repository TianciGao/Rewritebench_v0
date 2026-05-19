# B-line DB/Checker Batch Plan v0

## Purpose and Scope

This audit packet plans the first bounded batch expansion after the successful postgres-only DB/checker MVP and fresh-checkout release smoke. It is design and selection only. It does not run DB execution, run checkers, collect timing, compute official metrics, render paper tables, implement paper reproduction, update retained evidence, update reports/results, update `case_sets/`, update denominators, update paper results, migrate cases, create a global leaderboard, or modify raw legacy evidence.

The planned expansion remains local-user-output only: future artifacts must stay under `runs/user/<run_id>/` and must not become retained paper evidence.

## Current Canary and Release-smoke Status

The current bounded DB/checker MVP has been implemented and release-smoked for one row:

- case set: `common_core_v0`
- pool: `PERF`
- case: `PERF_0006`
- engine: `postgres`
- candidate route: `sqlglot_noop`
- output scope: `runs/user/<run_id>/`
- local source execution: passed
- local candidate execution: passed
- local checker result: `checker_success`
- local exact status: `exact`
- ledger boundaries: `local_execution_only=true`, `official_metric_input=false`, `retained_evidence_input=false`

`PERF_0006` is therefore treated as the prior canary and is not selected as a new batch row.

## Why Batch Plan Comes Before Batch Execution

The next step should not jump from one canary row to all 120 Common-core same-engine denominator rows. Batch planning first keeps scope explicit, checks static package readiness before any DB interaction, and defines stop conditions before local execution can create artifacts. This also preserves the distinction between local diagnostics and official benchmark evidence.

## Common-core PERF Postgres Candidate Universe

The candidate universe is derived from `case_sets/common_core_v0/cases.csv` and `case_sets/common_core_v0/denominator_same_engine_120.csv`, not from directory guessing.

Filters applied:

- `pool=PERF`
- `common_core_v0_member=true`
- postgres denominator row exists
- postgres-only row selection

The resulting universe contains 16 Common-core PERF postgres cases:

`PERF_0006`, `PERF_0007`, `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, `PERF_0033`, `PERF_0034`, `PERF_0035`, `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, and `PERF_0082`.

Static asset review checked only file presence for:

- `manifest.yaml`
- `sql/source.sql`
- `schema/postgres/ddl.sql`
- `schema/postgres/load.sql`
- `checker/checker.yaml`
- `checker/normalization.yaml`
- `checker/compare_config.yaml`
- `metadata/denominator_eligibility.yaml`

All 16 candidates have the required static assets present.

## Candidate Readiness Summary

`common_core_perf_postgres_candidate_readiness.csv` records readiness for all 16 cases.

- `PERF_0006`: `already_canary_verified`
- Remaining 15 cases: `ready_for_batch_smoke` by static file-presence review
- Cases deferred from the first batch are deferred only for scope control, not because of missing static assets

This is not a claim that future execution/checker results will pass. It is only a static readiness classification for a future authorized batch smoke.

## Recommended First Batch

Recommended first batch size: 4 cases.

Selected case IDs:

- `PERF_0007`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`

Selection rationale:

- All selected rows have complete postgres schema/load/checker assets.
- `PERF_0007` is the nearest follow-on candidate after the verified canary.
- The batch stays within the requested 3-5 case target.
- The batch remains PERF-only, postgres-only, Common-core-only, and SQLGlot no-op only.
- The batch avoids expanding directly to all 15 remaining PERF cases or all 120 Common-core same-engine rows.

## Excluded or Deferred Cases

`PERF_0006` is excluded because it is already the verified canary and release-smoke row.

`PERF_0019`, `PERF_0024`, `PERF_0033`, `PERF_0034`, `PERF_0035`, `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, and `PERF_0082` are statically ready but deferred to keep the first expansion bounded. They can be considered after the selected first batch passes without protected-surface changes or local-output violations.

## Future Command Shape

The future execution task should create a case-list file from selected rows in `postgres_perf_batch_selection.csv` where `selected_for_first_batch=true`, then run:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list <batch_case_list> \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/postgres_perf_sqlglot_noop_batch_smoke \
  --enable-db-execution \
  --enable-checker
```

The future task must not collect timing, compute official metrics, update retained evidence, update reports/results, update denominators, update paper results, or create a leaderboard.

## Stop Conditions

The future execution task must stop on:

- Postgres connection failure or missing connection configuration.
- Any output path outside `runs/user/<run_id>/`.
- Any change under `cases/`, `case_sets/`, `inventory/`, `reports/`, or `results/`.
- Any denominator or paper-result change.
- Any retained-evidence update.
- Any official metric computation or timing output.
- Any global leaderboard or method-rank output.
- Any selected row missing source, candidate, or checker artifacts after execution.
- Any DB credential leakage in logs, audit files, reports, or command summaries.
- Repeated schema setup failure.
- Missing checker, normalization, or compare config for a selected row.

Full details are in `postgres_perf_batch_stop_conditions.csv`.

## Local-diagnostic-only Interpretation Policy

Future batch output may report local diagnostic counts:

- selected rows
- candidate-generated rows
- source and candidate execution statuses
- checker statuses
- local exact or mismatch statuses
- failure buckets

Future batch output must not report:

- official Generation Rate
- official Execution Coverage Rate
- official Result Consistency Rate
- speedup
- paper results
- leaderboard rank
- method winner

`local_execution_only=true`, `official_metric_input=false`, and `retained_evidence_input=false` must remain explicit in the future batch ledger.

## No-global-leaderboard Boundary

The recommended batch is a local smoke expansion, not a method comparison benchmark. It must not rank SQLGlot against any method, publish a winner, or create global leaderboard output.

## Exact Next Safe Action

Authorize `b_line_postgres_perf_batch_smoke_v0` to execute only the rows selected in `postgres_perf_batch_selection.csv` under the same local-only boundaries: postgres only, Common-core PERF only, SQLGlot no-op only, output under `runs/user/` only, no timing, no official metrics, no reports/results updates, no retained-evidence updates, no denominator changes, no paper-result changes, and no leaderboard.
