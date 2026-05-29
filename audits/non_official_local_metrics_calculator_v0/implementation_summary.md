# Implementation Summary

## Module

`src/sql_rewrite_bench/local_metrics.py` provides:

- `compute_local_metrics(run_dir)`
- `compute_and_write_local_metrics(run_dir)`

The module reads:

- `ledger.csv`
- `config.yaml`
- optional `summary.json`
- optional `timing/timing_summary.json`
- optional `timing/rows/*.json`

## CLI

`scripts/dev/compute_local_user_metrics.py` accepts one or more `--run` paths:

```bash
PYTHONPATH=src python scripts/dev/compute_local_user_metrics.py \
  --run runs/user/<run_name>
```

## Outputs

Outputs are written under `runs/user/{run_name}/metrics/`:

- `local_metrics_summary.json`
- `local_metrics_by_engine.csv`
- `local_metrics_by_pool.csv`
- `local_timing_speedup_rows.csv`
- `local_metrics_boundary.md`

All outputs carry local-only boundary fields:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

## Grouping

The calculator is route-aware, method-aware, engine-aware, denominator-aware, timing-policy-aware, and local-run-aware. It does not merge routes or emit method ranking, winner, best-method, or leaderboard outputs.
