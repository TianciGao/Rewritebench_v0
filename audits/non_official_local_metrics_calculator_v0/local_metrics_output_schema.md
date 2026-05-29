# Local Metrics Output Schema

## `local_metrics_summary.json`

Contains:

- `schema_version=local_metrics_summary_v0`
- run identity and route/method identity
- grouping policy
- metric definitions
- overall local diagnostic counts/rates
- by-engine summaries
- by-pool summaries
- per-denominator row summaries
- diagnostic status counts
- deferred metric statuses
- prohibited-output flags
- local-only boundary flags

## `local_metrics_by_engine.csv`

Contains one row per local run / route / method / engine / timing policy group.

Key fields include:

- selected, candidate generated, preflight passed, source executable, candidate executable
- Generation Rate
- Execution Coverage Rate
- exact, mismatch, label-only mismatch, unsupported/fail-closed
- Result Consistency Rate
- timed and speedup denominator counts
- GM Speedup Ratio and P10/P25/P50/P75/P90 percentiles where available
- local-only boundary flags

## `local_metrics_by_pool.csv`

Contains one row per local run / route / method / pool / timing policy group with the same local metric fields as by-engine output.

## `local_timing_speedup_rows.csv`

Contains row-level timing inclusion/exclusion details. Non-exact rows, label-only mismatches, unsupported rows, missing timing rows, and partial timing failures remain visible with explicit exclusion reasons.

## `local_metrics_boundary.md`

States that outputs are local diagnostic only and not official metrics, paper results, retained evidence, reports/results, paper tables, or leaderboard output.
