# CSV Shape Review

Reviewed CSV outputs:

- `local_metrics_by_engine.csv`
- `local_metrics_by_pool.csv`
- `local_timing_speedup_rows.csv`

## By-Engine And By-Pool CSVs

The by-engine and by-pool CSVs for PostgreSQL, MySQL, and Spark expose the required fields:

- selected
- candidate_generated
- generation_rate
- preflight_passed
- source_executable
- candidate_executable
- execution_coverage_rate
- exact
- result_consistency_rate
- mismatch
- label_only_mismatch
- unsupported_fail_closed
- timing_eligible
- timed
- speedup_denominator
- gm_speedup_ratio
- speedup_p10
- speedup_p25
- speedup_p50
- speedup_p75
- speedup_p90
- semantic_equivalence_rate_status
- cross_engine_gm_speedup_status
- pocr_status
- local-only boundary flags

`preflight_passed` and `source_executable` are present as diagnostics only. They are not encoded as rate numerator definitions.

## Row Counts

| Run | by_engine rows | by_pool rows | speedup row rows |
|---|---:|---:|---:|
| PostgreSQL smoke | 1 | 2 | 2 |
| MySQL smoke | 1 | 2 | 2 |
| Spark smoke | 1 | 2 | 2 |

## Per-Row Timing CSV

`local_timing_speedup_rows.csv` includes only per-row timing diagnostics:

- `case_id`
- `denominator_id`
- `route_id`
- `method_id`
- `engine`
- `timing_policy_id`
- `exact_status`
- `failure_bucket`
- `timing_eligible`
- `timing_status`
- `source_median_ms`
- `candidate_median_ms`
- `speedup_ratio`
- `included_in_performance`
- `exclusion_reason`
- boundary flags

There is no winner, rank, best-method, or method-selection field.

## Verdict

CSV shape is suitable for route-aware, denominator-aware local diagnostic projection. The outputs remain local-only and diagnostic.
