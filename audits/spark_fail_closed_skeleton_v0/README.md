# Spark Fail-Closed Skeleton v0

Verdict: `completed`.

This packet records the implementation of a narrow Spark fail-closed skeleton and local environment detector for user-entry local diagnostics. Spark is now explicit and inspectable in the engine execution path, but live Spark SQL execution remains unimplemented.

## Summary

- `src/sql_rewrite_bench/spark_execution.py` now detects lightweight Spark environment signals without importing or starting Spark.
- Spark-selected DB execution rows fail closed with structured local diagnostic status and `unsupported_engine` failure bucket.
- Spark execution writes only a small `spark_environment_status.json` metadata artifact under the per-row execution directory.
- Spark execution does not create source/candidate result JSONL artifacts, start a Spark session, load schemas, execute SQL, compute timing, compute official metrics, update reports/results, or create leaderboard data.
- `scripts/dev/check_local_engine_env.py` reports Spark readiness signals and clearly states that Spark is fail-closed/not live implemented.
- PostgreSQL and MySQL behavior was preserved by unit tests and two-case live local diagnostic smokes.

## Local Smoke Snapshot

- Spark smoke: `runs/user/spark_fail_closed_smoke/`, selected rows 2, candidate generated rows 2, failure buckets `unsupported_engine=2`, checker attempted rows 0.
- PostgreSQL smoke: `runs/user/spark_skeleton_pg_smoke/`, selected rows 2, exact rows 2.
- MySQL smoke: `runs/user/spark_skeleton_mysql_smoke/`, selected rows 2, exact rows 2.

The local run outputs above are ignored local diagnostics and are not committed.

## Boundary

- Spark live SQL execution implemented: no.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Paper tables rendered: no.
- Reports/results updated: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.

## Next Safe Action

If Spark work continues, the next narrow task should add a Spark schema/load resolver or mocked execution contract tests only. Live Spark SQL execution, timing, official metrics, paper rendering, reports/results updates, retained-evidence promotion, and leaderboard output remain separate authorization boundaries.
