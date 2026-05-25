# Canonical Metrics Outputs

No canonical `local_metrics.py` outputs were recovered.

Expected source-run metrics paths after a successful single-run recovery would be:

- `runs/user/rbot_gpt54_pg40_bounded_diagnostic_v0/metrics/local_metrics_summary.json`
- `runs/user/rbot_gpt54_pg40_bounded_diagnostic_v0/metrics/local_metrics_by_engine.csv`
- `runs/user/rbot_gpt54_pg40_bounded_diagnostic_v0/metrics/local_metrics_by_pool.csv`
- `runs/user/rbot_gpt54_pg40_bounded_diagnostic_v0/metrics/local_timing_speedup_rows.csv`
- `runs/user/rbot_gpt54_pg40_bounded_diagnostic_v0/metrics/local_metrics_boundary.md`

Expected exported metrics paths after a successful single-run recovery would be under:

```text
/tmp/sqlrb_rbot_gpt54_pg40_bounded_local_diagnostic_v0/output/results/rbot_gpt54_pg40_bounded_diagnostic_v0/metrics/
```

Actual result: not produced, because the source run directory was missing and the metrics command was not executed.
