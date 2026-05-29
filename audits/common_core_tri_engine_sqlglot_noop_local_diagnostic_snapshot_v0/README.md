# Common-core Tri-engine SQLGlot Noop Local Diagnostic Snapshot

Verdict: `completed_with_failures`

This packet records a full-chain Common-core v0 local diagnostic snapshot for the existing SQLGlot user-entry adapter route:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route noop
```

The run covered the planned local diagnostic surface of 40 Common-core v0 case rows for each of PostgreSQL, MySQL, and Spark, for 120 selected/planned rows total. Case selection came from `case_sets/common_core_v0` through the user-entry runner, not by scanning `cases/`.

## Engine Summaries

PostgreSQL:

- selected rows: 40
- adapter invoked rows: 40
- candidate generated/preflight-passed rows: 35/35
- source/candidate executable rows: 35/35
- checker attempted/exact/mismatch rows: 35/35/0
- failure buckets: `adapter_failed=5`, `none=35`
- affected adapter-failed rows: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`

MySQL:

- selected rows: 40
- adapter invoked rows: 40
- candidate generated/preflight-passed rows: 40/40
- source/candidate executable rows: 40/39
- checker attempted/exact/mismatch rows: 39/31/8
- failure buckets: `candidate_execution_failed=1`, `mismatch=8`, `none=31`
- candidate execution failure: `PORT_0008`
- mismatch rows: `PERF_0062`, `PORT_0003`, `PORT_0004`, `PORT_0005`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`

Spark:

- selected rows: 40
- adapter invoked rows: 40
- candidate generated/preflight-passed rows: 40/40
- source/candidate executable rows: 35/27
- checker attempted/exact/mismatch rows: 27/25/2
- failure buckets: `candidate_execution_failed=8`, `mismatch=2`, `none=25`, `unsupported_engine=5`
- candidate execution failures: `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, `PERF_0082`, `PORT_0003`, `PORT_0013`
- mismatch rows: `PORT_0004`, `PORT_0005`
- explicit unsupported/fail-closed Spark PORT rows: `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, `PORT_0025`

## Overall Funnel

- selected rows: 120
- adapter invoked rows: 120
- candidate generated rows: 115
- candidate preflight passed rows: 115
- source executable rows: 110
- candidate executable rows: 101
- checker attempted rows: 101
- exact rows: 91
- mismatch rows: 10
- source-like/no-op rows: 6
- unsupported/fail-closed rows: 5

Overall failure buckets: `adapter_failed=5`, `candidate_execution_failed=9`, `mismatch=10`, `none=91`, `unsupported_engine=5`.

## Interpretation Boundary

This is a local diagnostic snapshot of SQLGlot noop route behavior through the current user-entry runner. It is not official SQLGlot baseline evidence and is not a paper result. It does not compute official metrics, timing, speedup, retained-evidence promotion, reports/results updates, or leaderboard output.

SQLGlot noop and SQLGlot optimize remain separate routes. The optimize route was not run in this task.

PORT controlled target-reference diagnostics remain separate from these SQLGlot noop user-adapter rows. The PORT failures and mismatches here are real SQLGlot noop adapter diagnostic behavior, not controlled target-reference results.

## Local Run Paths

- PostgreSQL: `runs/user/common_core_sqlglot_noop_postgres_snapshot`
- MySQL: `runs/user/common_core_sqlglot_noop_mysql_snapshot`
- Spark: `runs/user/common_core_sqlglot_noop_spark_snapshot`

These local run outputs are not committed.

## Next Safe Action

Triage the fail-visible SQLGlot noop failures before any broader real-adapter interpretation. Keep same-engine rows, real PORT adapter rows, controlled PORT target-reference rows, and unsupported/fail-closed role rows separate.
