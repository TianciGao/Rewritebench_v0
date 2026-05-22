# exact_gated_local_timing_diagnostic_v0

Verdict: `completed`

This task implements an opt-in exact-gated local timing diagnostic layer for user-entry runs. The new timing path is disabled by default and writes local-only timing artifacts under `runs/user/{run_name}/timing/` only when `--collect-timing` is supplied with `--enable-db-execution` and `--enable-checker`.

The implementation records per-row local diagnostic timing samples and a nullable per-row `speedup_ratio` only for exact, fully timed rows. It does not compute official metrics, route-level paper metrics, reports/results tables, retained-evidence outputs, paper tables, POCR, skill artifacts, or leaderboard outputs.

## Preflight Summary

- Branch: `feature/case-package-v2-external-schema`.
- Required prior commit present: `b3ad644 docs(audit): resolve timing schema open questions`.
- Required prior audit present: `audits/timing_schema_open_questions_resolution_v0/`.
- D032 present in `project_control/DECISION_LOG.md`.
- Metadata correction required: the older run-log entry for `timing_schema_open_questions_resolution_v0` still records commit/push as pending; this task records that final commit `b3ad644` was pushed to `origin/feature/case-package-v2-external-schema`.

## Implementation Summary

- Added `src/sql_rewrite_bench/local_timing.py`.
- Added CLI flags:
  - `--collect-timing`
  - `--timing-warmup`
  - `--timing-repetitions`
  - `--timing-timeout`
- Default timing policy:
  - `warmup_count=1`
  - `measured_repetitions=5`
  - `timeout_seconds=30`
  - `statistic=median`
- Added local timing fields to `ledger.csv` for visibility:
  - `timing_eligible`
  - `timing_status`
  - `timing_na_reason`
  - `timing_artifact_path`
  - `speedup_ratio`

## Bounded Timing Smoke

SQLGlot noop timing smoke was run for `PERF_0006` and `CONS_0005` only, with DB execution and checker enabled:

- PostgreSQL: selected 2, exact 2, timing eligible 2, timed 2.
- MySQL: selected 2, exact 2, timing eligible 2, timed 2.
- Spark: selected 2, exact 2, timing eligible 2, timed 2.

All smoke outputs remain under `runs/user/` and were not staged or committed.

## Boundary

Local diagnostic only. No official metrics, route-level metrics, reports/results updates, retained-evidence promotion, paper table rendering, POCR, skill folders, operation atoms, denominator changes, case membership changes, or leaderboard output were created.

## Next Safe Action

Review the local timing artifacts and implementation. If accepted, authorize a separate non-official local metrics calculator task for Coverage/Correctness/Performance/Generalization, still without reports/results updates or retained-evidence promotion.
