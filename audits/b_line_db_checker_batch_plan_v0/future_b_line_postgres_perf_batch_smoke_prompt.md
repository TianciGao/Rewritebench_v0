# Future Prompt Draft: b_line_postgres_perf_batch_smoke_v0

You are working on SQL-RewriteBench clean public release migration / redevelopment.

Task title:
`b_line_postgres_perf_batch_smoke_v0`

This is a bounded B-line DB/checker batch smoke execution task.

This task must execute only the selected rows from:

`audits/b_line_db_checker_batch_plan_v0/postgres_perf_batch_selection.csv`

where:

- `selected_for_first_batch=true`
- `pool=PERF`
- `engine=postgres`
- `expected_adapter_route=sqlglot_noop`

Expected selected case IDs from the planning packet:

- `PERF_0007`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`

Do not include `PERF_0006` as a new batch row. It is the prior canary reference only.

## Scope

Run only:

- case set: `common_core_v0`
- pool: `PERF`
- engine: `postgres`
- candidate route: SQLGlot no-op
- output root: `runs/user/postgres_perf_sqlglot_noop_batch_smoke/`

The command shape should be:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list <batch_case_list_from_selection_csv> \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/postgres_perf_sqlglot_noop_batch_smoke \
  --enable-db-execution \
  --enable-checker
```

## Hard Boundaries

Do not:

- modify the legacy repo
- modify `cases/`
- modify `case_sets/`
- modify `inventory/`
- modify `reports/`
- modify `results/`
- change denominator values or membership
- change paper results
- collect timing
- compute official metrics
- render paper tables
- implement paper reproduction
- implement retained-evidence adapters
- implement MySQL or Spark execution
- implement Calcite or R-Bot adapters
- run LLM calls
- write into case-local `runs/`
- create global leaderboard output
- stage `runs/user/` output
- use `git add .`

All batch artifacts must remain local under:

`runs/user/postgres_perf_sqlglot_noop_batch_smoke/`

## Preflight

Before execution:

1. Verify the release repo is clean except for intended audit files.
2. Verify `psql --version`.
3. Verify `psql -c "select 1;"` using the current shell without logging secrets.
4. Verify SQLGlot is installed or install optional support with `python -m pip install -e ".[sqlglot]"` only if allowed.
5. Build a temporary case-list file from `postgres_perf_batch_selection.csv` selected rows.
6. Confirm all selected cases still have `sql/source.sql`, `schema/postgres/ddl.sql`, `schema/postgres/load.sql`, `checker/checker.yaml`, `checker/normalization.yaml`, and `checker/compare_config.yaml`.

Stop if any preflight fails. Do not fake DB/checker outputs.

## Required Checks After Execution

For every selected row, verify:

- candidate SQL was generated
- `source_result.jsonl` exists
- `candidate_result.jsonl` exists
- `checker_result.json` exists
- ledger has `local_execution_only=true`
- ledger has `official_metric_input=false`
- ledger has `retained_evidence_input=false`
- execution/checker statuses are recorded honestly

Checker mismatch is acceptable only if recorded honestly. Do not hide mismatches.

## Stop Conditions

Stop immediately on any condition listed in:

`audits/b_line_db_checker_batch_plan_v0/postgres_perf_batch_stop_conditions.csv`

Required stop-condition families include:

- protected path changes
- output-root violations
- missing source/candidate/checker artifacts
- DB credential leakage
- global leaderboard output
- official metric computation
- timing output
- retained-evidence update
- reports/results update
- denominator or paper-result change

## Interpretation Policy

Report only local diagnostic counts:

- selected rows
- candidate-generated rows
- source/candidate execution statuses
- checker statuses
- local exact/mismatch statuses
- failure buckets

Do not report official Generation Rate, official Execution Coverage Rate, official Result Consistency Rate, speedup, paper results, leaderboard rank, or method winner.

## Required Audit Outputs

Create a new audit directory for the execution task. Record command summaries, validation results, a smoke manifest, and summary JSON. Do not include secrets, DB passwords, full DSNs, raw long stdout/stderr dumps, or environment secrets.
