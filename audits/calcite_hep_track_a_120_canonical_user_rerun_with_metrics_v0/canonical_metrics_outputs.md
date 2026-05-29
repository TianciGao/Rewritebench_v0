# Canonical Metrics Outputs

Metrics were produced by:

```bash
python -m cli.main user compute-local-metrics \
  --run-id-prefix calcite_hep_track_a_120_canonical_v0 \
  --engines postgres,mysql,spark \
  --aggregate-run-id calcite_hep_track_a_120_canonical_v0 \
  --source-run-root runs/user \
  --output-root /tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output
```

Source metrics directory:

```text
runs/user/calcite_hep_track_a_120_canonical_v0/metrics/
```

Files:

```text
local_metrics_summary.json
local_metrics_by_engine.csv
local_metrics_by_pool.csv
local_timing_speedup_rows.csv
local_metrics_boundary.md
```

User-facing metrics export:

```text
/tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/results/calcite_hep_track_a_120_canonical_v0/metrics/
```

User-facing metrics report:

```text
/tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/reports/calcite_hep_track_a_120_canonical_v0/metrics_summary.md
```

Copied audit snapshots:

```text
audits/calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/canonical_metrics_snapshot.json
audits/calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/canonical_engine_metrics_snapshot.csv
```

These snapshots are direct copies from canonical metrics outputs. This packet does not compute route metrics independently.
