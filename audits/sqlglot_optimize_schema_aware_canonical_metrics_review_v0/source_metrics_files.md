# Source Metrics Files

Canonical source directory:

`runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0/metrics/`

Required canonical files:

- `local_metrics_summary.json`
- `local_metrics_by_engine.csv`
- `local_metrics_by_pool.csv`
- `local_timing_speedup_rows.csv`
- `local_metrics_boundary.md`

These files were created by:

```bash
python -m cli.main user compute-local-metrics \
  --run-id-prefix sqlglot_optimize_schema_aware_track_a_120_canonical_v0 \
  --engines postgres,mysql,spark \
  --aggregate-run-id sqlglot_optimize_schema_aware_track_a_120_canonical_v0 \
  --source-run-root runs/user \
  --output-root /tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_canonical_user_rerun_v0/output
```

Related committed source audit:

`audits/sqlglot_optimize_schema_aware_track_a_120_canonical_user_rerun_v0/`

That prior audit contains copied canonical snapshots:

- `canonical_metrics_snapshot.json`
- `canonical_engine_metrics_snapshot.csv`
