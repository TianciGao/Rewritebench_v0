# Summary JSON Shape Review

Reviewed files:

- `runs/user/timing_sqlglot_noop_postgres_smoke/metrics/local_metrics_summary.json`
- `runs/user/timing_sqlglot_noop_mysql_smoke/metrics/local_metrics_summary.json`
- `runs/user/timing_sqlglot_noop_spark_smoke/metrics/local_metrics_summary.json`

## Required Sections

All three summary JSON files contain:

- `local_run_id`
- `route_ids`
- `method_ids`
- `grouping_policy`
- `metric_definitions`
- `overall`
- `by_engine`
- `by_pool`
- `per_denominator_rows`
- `diagnostic_status_counts`
- `deferred_metrics`
- `prohibited_outputs`
- local-only boundary flags

## Reviewed Counts

| Run | selected | candidate_generated | preflight_passed | source_executable | candidate_executable | exact | mismatch | timing_eligible | timed | speedup_denominator |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PostgreSQL smoke | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 2 | 2 | 2 |
| MySQL smoke | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 2 | 2 | 2 |
| Spark smoke | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 2 | 2 | 2 |

## Deferred Metrics

All three summaries report:

- `regression_at_20.status=not_implemented`
- `semantic_equivalence_rate.status=not_applicable`
- `cross_engine_gm_speedup_ratio.status=not_applicable`
- `positive_operation_coverage_rate.status=not_applicable`
- `positive_operation_coverage_rate.skill_adapter_pending=true`

## Verdict

Summary JSON shape is suitable for broader local diagnostic projection, with one non-blocking wording note: explicit false `leaderboard` boundary/prohibited-output fields create literal token occurrences but do not create leaderboard output.
