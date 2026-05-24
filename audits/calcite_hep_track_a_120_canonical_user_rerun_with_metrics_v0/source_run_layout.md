# Source Run Layout

Canonical source run:

```text
runs/user/calcite_hep_track_a_120_canonical_v0/
  config.yaml
  ledger.csv
  metrics/
    local_metrics_boundary.md
    local_metrics_by_engine.csv
    local_metrics_by_pool.csv
    local_metrics_summary.json
    local_timing_speedup_rows.csv
```

Source runs aggregated:

```text
runs/user/calcite_hep_track_a_120_canonical_v0__postgres/
  config.yaml
  ledger.csv
  timing/rows/*.json

runs/user/calcite_hep_track_a_120_canonical_v0__mysql/
  config.yaml
  ledger.csv
  timing/rows/*.json

runs/user/calcite_hep_track_a_120_canonical_v0__spark/
  config.yaml
  ledger.csv
  timing/rows/*.json
```

User-facing D035 export root:

```text
/tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/
  results/calcite_hep_track_a_120_canonical_v0/
  logs/calcite_hep_track_a_120_canonical_v0/
  reports/calcite_hep_track_a_120_canonical_v0/
```

The per-engine runs were also exported under the same temporary output root with `__postgres`, `__mysql`, and `__spark` suffixes. No repository-level `output/`, top-level `reports/`, or top-level `results/` output was used.
