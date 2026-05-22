# Bounded Metrics Smoke Summary

Command:

```bash
PYTHONPATH=src python scripts/dev/compute_local_user_metrics.py \
  --run runs/user/timing_sqlglot_noop_postgres_smoke \
  --run runs/user/timing_sqlglot_noop_mysql_smoke \
  --run runs/user/timing_sqlglot_noop_spark_smoke
```

## PostgreSQL

- Run path: `runs/user/timing_sqlglot_noop_postgres_smoke/`
- selected: 2
- candidate_generated: 2
- candidate_executable: 2
- exact: 2
- timed: 2
- speedup_denominator: 2
- local GM Speedup Ratio: 0.9958493720356396
- output path: `runs/user/timing_sqlglot_noop_postgres_smoke/metrics/`

## MySQL

- Run path: `runs/user/timing_sqlglot_noop_mysql_smoke/`
- selected: 2
- candidate_generated: 2
- candidate_executable: 2
- exact: 2
- timed: 2
- speedup_denominator: 2
- local GM Speedup Ratio: 1.0001388459335048
- output path: `runs/user/timing_sqlglot_noop_mysql_smoke/metrics/`

## Spark

- Run path: `runs/user/timing_sqlglot_noop_spark_smoke/`
- selected: 2
- candidate_generated: 2
- candidate_executable: 2
- exact: 2
- timed: 2
- speedup_denominator: 2
- local GM Speedup Ratio: 1.0296001429221677
- output path: `runs/user/timing_sqlglot_noop_spark_smoke/metrics/`

These are local diagnostic metrics only. They are not official metrics, paper results, retained evidence, reports/results updates, or leaderboard output.
