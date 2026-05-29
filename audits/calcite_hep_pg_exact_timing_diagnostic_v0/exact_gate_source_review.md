# Exact Gate Source Review

The exact gate source was:

- `audits/calcite_hep_pg_execution_checker_diagnostic_v0/per_row_execution_checker_status.csv`

The timing helper verified that the CSV contains 40 selected PostgreSQL rows and 20 exact rows. All 20 exact-row candidate SQL files recorded in the prior audit were still present under the previous `/tmp` candidate-generation runtime snapshot.

Timing-attempted exact rows:

- `PERF_0006`
- `PERF_0007`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0034`
- `PERF_0052`
- `PERF_0054`
- `PERF_0056`
- `PERF_0077`
- `PERF_0082`
- `CONS_0005`
- `CONS_0007`
- `CONS_0009`
- `CONS_0010`
- `CONS_0012`
- `CONS_0024`

Rows not marked exact in the prior execution/checker audit were not timed and remain visible in `per_row_timing.csv` with `timing_attempted=false`.
