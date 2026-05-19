# B-line DB/Checker Execution Release Smoke v0

## Purpose and Scope

This verification packet release-smokes the already implemented bounded DB/checker execution MVP from a fresh-checkout and editable-install perspective.

The smoke reran only the authorized bounded path:

- case set: `common_core_v0`
- pool: `PERF`
- case: `PERF_0006`
- engine: `postgres`
- adapter route: SQLGlot no-op
- output root: `runs/user/<run_id>/`
- timing: not collected
- official metrics: not computed
- retained evidence: not updated
- reports/results: not updated
- denominator and case-set files: unchanged
- global leaderboard: not created

## Temporary Checkout Method

The smoke used a temporary local clone outside the release repository:

`/tmp/sqlrb_db_checker_release_smoke/Rewritebench_v0_db_smoke`

The clone was created from:

`/home/tianci_gao/code/Rewritebench_v0`

No temporary checkout files were staged or copied back into the release repo.

## Editable Install Result

A temporary virtual environment was created at:

`/tmp/sqlrb_db_checker_release_smoke/Rewritebench_v0_db_smoke/.venv-db-smoke`

Editable install with SQLGlot extra passed:

`python -m pip install -e ".[sqlglot]"`

## SQLGlot Dependency Result

SQLGlot import passed in the temporary environment.

Observed version:

`30.8.0`

## Postgres Preflight Result

Postgres connectivity passed in the temporary clone using inherited shell environment:

`psql -c "select 1;"`

Secrets policy:

- no DB password was printed
- no full DSN was printed
- no environment variable values were recorded
- only pass/fail connectivity status is recorded

## DB/Checker Smoke Result

The bounded DB/checker smoke passed in the temporary clone:

```bash
python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list tmp_db_checker_smoke_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/db_checker_release_smoke_perf0006 \
  --enable-db-execution \
  --enable-checker
```

The run selected one row, generated one SQLGlot no-op candidate, executed source SQL and candidate SQL locally through Postgres, and ran the local checker.

## Source/Candidate/Checker Artifact Result

Required output files existed:

- `config.yaml`
- `selected_cases.csv`
- `ledger.csv`
- `summary.json`
- `failures.csv`
- `report.md`

Required row artifacts existed:

- `workspaces/PERF_0006/postgres/execution/source_result.jsonl`
- `workspaces/PERF_0006/postgres/execution/candidate_result.jsonl`
- `workspaces/PERF_0006/postgres/checker/checker_result.json`

Ledger statuses:

- `source_execution_status=source_execution_success`
- `candidate_execution_status=candidate_execution_success`
- `checker_status=checker_success`
- `exact_status=exact`
- `failure_bucket=none`

## Ledger Local-only Result

The ledger preserved the required user-run boundaries:

- `local_execution_only=true`
- `official_metric_input=false`
- `retained_evidence_input=false`

The summary preserved:

- `official_metrics_computed=false`
- `paper_tables_rendered=false`
- `retained_evidence_updated=false`
- `no_global_leaderboard=true`

## Output Hygiene Result

All smoke output was written under:

`runs/user/db_checker_release_smoke_perf0006/`

`git status --short runs/user` in the temporary clone produced no staged or tracked changes, confirming the smoke output remained ignored/untracked.

## Protected Boundary Result

`git status --short cases case_sets inventory reports results` in the temporary clone produced no output.

The release repository boundary checks also found no changes under:

- `cases/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- tracked `runs/user`

## Unsupported Features

This task did not implement or run:

- new DB/checker features
- `PERF_0007` expansion
- full Common-core execution
- timing collection
- official metric computation
- paper table rendering
- paper reproduction
- retained-evidence adapter integration
- reports/results migration
- denominator updates
- case-set updates
- MySQL/Spark execution
- Calcite/R-Bot adapters
- global leaderboard output

## Exact Next Safe Action

Authorize a bounded DB/checker hardening task that keeps the same local-only output and official-metric boundaries, or authorize a separate narrowly scoped expansion smoke for `PERF_0007` only.
