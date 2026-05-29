# Next Steps

Recommended next task:

Run exact-gated timing over the 81 exact/result-consistent rows from this
diagnostic.

After timing:

- Run canonical `compute-local-metrics` through `src/sql_rewrite_bench/local_metrics.py`.
- Produce any route-card review only from canonical metrics outputs.

Separate triage tasks:

- PORT no-candidate rows.
- `PORT_0013` candidate execution failures.
- Spark `PERF_0062` candidate execution failure.
- PostgreSQL/MySQL checker mismatches.
- Spark `PORT_0024` target-reference/source-role policy.
- High parse-only candidate share on Spark.
