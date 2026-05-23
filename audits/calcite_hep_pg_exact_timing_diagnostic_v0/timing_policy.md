# Timing Policy

The pass reused the existing local timing defaults from `src/sql_rewrite_bench/local_timing.py` and user-entry defaults:

- Timing policy id: `local_exact_gated_default_v0`
- Warmup count: 1
- Measured repetitions: 5
- Timeout seconds: 30.0
- Statistic: median
- Execution order: source then candidate
- Schema setup: fresh PostgreSQL schema per timing row
- Cache policy: recorded, not controlled
- Retry policy: no retries
- Partial sample policy: visible partial failure, no speedup

The helper measured elapsed process time around the existing PostgreSQL `psql` execution path. This keeps the diagnostic aligned with the local workbench timing implementation, but it also means small-row measurements include client/process overhead and local system noise.

Win/tie/loss was not computed because the existing timing policy does not define a durable threshold for those labels.
