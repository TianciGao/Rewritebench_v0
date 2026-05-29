# Canonical Metrics Outputs

Produced by `src/sql_rewrite_bench/local_metrics.py` through:

```bash
python -m cli.main user compute-local-metrics
```

Required outputs:

```text
runs/user/direct_llm_original_track_a_120_canonical_v0/metrics/local_metrics_summary.json
runs/user/direct_llm_original_track_a_120_canonical_v0/metrics/local_metrics_by_engine.csv
runs/user/direct_llm_original_track_a_120_canonical_v0/metrics/local_metrics_by_pool.csv
runs/user/direct_llm_original_track_a_120_canonical_v0/metrics/local_timing_speedup_rows.csv
runs/user/direct_llm_original_track_a_120_canonical_v0/metrics/local_metrics_boundary.md
```

Parse validation:

```text
local_metrics_summary.json=parse_ok
local_metrics_by_engine.csv_rows=3
local_metrics_by_pool.csv_rows=4
local_timing_speedup_rows.csv_rows=120
```

Copied audit snapshots:

- `canonical_metrics_snapshot.json`
- `canonical_engine_metrics_snapshot.csv`
