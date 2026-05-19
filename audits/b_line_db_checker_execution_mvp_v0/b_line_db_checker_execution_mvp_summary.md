# B-line DB/Checker Execution MVP v0

## Purpose and Scope

This packet records the bounded `b_line_db_checker_execution_mvp_v0` implementation. The implemented scope is intentionally narrow:

- case set: `common_core_v0`
- engine execution MVP: postgres only
- smoke pool: PERF only
- smoke case: `PERF_0006`
- candidate route: SQLGlot no-op
- output root: `runs/user/<run_id>/` only
- timing: not collected
- official metrics: not computed
- retained evidence: not updated
- reports/results: not updated
- denominator and case-set files: unchanged
- leaderboard: not created

## Implementation Summary

The user runner now has explicit opt-in DB/checker flags:

- `--enable-db-execution`
- `--enable-checker`
- `--postgres-dsn-env`
- `--execution-timeout-sec`
- `--db-schema-prefix`

DB execution never runs unless `--enable-db-execution` is present. Checker execution never runs unless both `--enable-db-execution` and `--enable-checker` are present. Existing non-DB adapter-capture behavior remains the default.

Files added:

- `src/sql_rewrite_bench/postgres_execution.py`
- `src/sql_rewrite_bench/local_result_checker.py`
- `tests/user_entry/test_db_checker_execution_mvp.py`

Files modified:

- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/user_run_schema.py`

## Environment Preflight Result

- `psql` availability: available
- Observed version: `psql (PostgreSQL) 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)`
- Postgres connection check: `psql -c "select 1;"` passed
- Connection source: libpq environment variables were present
- Credential policy: no DB passwords or full DSNs were printed or stored

## DB Config Source Used

The live smoke used libpq environment variables from the shell. Audit files record only set/unset state, not values.

Redacted source summary:

- `SQLRB_POSTGRES_DSN`: unset
- `PGHOST`: set
- `PGPORT`: set
- `PGDATABASE`: set
- `PGUSER`: set
- `PGPASSWORD`: set

## Local Postgres Smoke Result

The bounded live smoke passed for `PERF_0006`:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list /tmp/sqlrb_db_checker_perf0006_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/db_checker_postgres_perf0006_smoke \
  --enable-db-execution \
  --enable-checker
```

The command completed with one selected row and one generated candidate. Because Python subprocess access to `psql` was sandbox-constrained, the successful live smoke was run with approved escalation so the runner subprocess could use the shell's Postgres environment.

Captured local artifacts:

- `runs/user/db_checker_postgres_perf0006_smoke/workspaces/PERF_0006/postgres/execution/source_result.jsonl`
- `runs/user/db_checker_postgres_perf0006_smoke/workspaces/PERF_0006/postgres/execution/candidate_result.jsonl`
- `runs/user/db_checker_postgres_perf0006_smoke/workspaces/PERF_0006/postgres/checker/checker_result.json`
- `runs/user/db_checker_postgres_perf0006_smoke/workspaces/PERF_0006/postgres/checker/normalized_source_result.jsonl`
- `runs/user/db_checker_postgres_perf0006_smoke/workspaces/PERF_0006/postgres/checker/normalized_candidate_result.jsonl`

Ledger status:

- `source_execution_status=source_execution_success`
- `candidate_execution_status=candidate_execution_success`
- `checker_status=checker_success`
- `exact_status=exact`
- `failure_bucket=none`
- `local_execution_only=true`
- `official_metric_input=false`
- `retained_evidence_input=false`

## Checker Behavior Result

The local checker consumed the local source and candidate JSONL result artifacts plus the case-local checker, normalization, and compare config files. It performed conservative local normalization and exact JSONL comparison. For the SQLGlot no-op smoke, the checker returned `checker_success` and `exact`.

This checker is a local MVP diagnostic only. It is not an official semantic-equivalence verifier, does not compute official metrics, and does not create retained paper evidence.

## Ledger Extension Summary

The user-run `ledger.csv` now preserves the existing row grain and adds these local DB/checker fields:

- `execution_enabled`
- `checker_enabled`
- `source_execution_status`
- `candidate_execution_status`
- `source_result_path`
- `candidate_result_path`
- `checker_config_path`
- `normalization_config_path`
- `compare_config_path`
- `execution_failure_class`
- `checker_failure_class`
- `mismatch_artifact_path`
- `db_artifact_dir`
- `local_execution_only`
- `official_metric_input`
- `retained_evidence_input`

For non-DB runs, the new fields are populated with non-DB defaults and official metric / retained evidence flags remain false.

## Output Hygiene Summary

All DB/checker smoke output was written under:

`runs/user/db_checker_postgres_perf0006_smoke/`

The smoke output is ignored and was not staged. No case-local `runs/` directory was written.

## Protected Boundary Summary

The task did not modify:

- `cases/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- denominator files
- paper result files
- retained evidence
- raw legacy evidence
- the legacy repository

The task did not compute official metrics, collect timing, render paper tables, implement paper reproduction, implement retained-evidence adapters, implement MySQL/Spark execution, implement Calcite/R-Bot routes, or create leaderboard output.

## Unsupported Features

The following remain unsupported and require separate authorization:

- MySQL execution
- Spark execution
- timing collection
- official metric computation
- paper table rendering
- paper reproduction CLI
- retained-evidence adapter integration
- broad Common-core execution
- SQLGlot paper evaluation
- Calcite and R-Bot adapters
- global leaderboard output

## Exact Next Safe Action

Authorize a DB/checker MVP hardening or release-smoke task that reruns the postgres-only local execution/checker path in a fresh environment, then optionally expands only to `PERF_0007` under the same local-only, no-timing, no-official-metrics, no-retained-evidence, no-reports/results, no-denominator-change, and no-leaderboard boundaries.
