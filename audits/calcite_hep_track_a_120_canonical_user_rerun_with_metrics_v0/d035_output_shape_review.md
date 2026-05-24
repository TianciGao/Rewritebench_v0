# D035 Output Shape Review

Runtime root:

```text
/tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/
```

D035 export directories observed:

```text
/tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/results/calcite_hep_track_a_120_canonical_v0/
/tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/logs/calcite_hep_track_a_120_canonical_v0/
/tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/reports/calcite_hep_track_a_120_canonical_v0/
```

Per-engine exports were also written under the same temporary root:

```text
calcite_hep_track_a_120_canonical_v0__postgres
calcite_hep_track_a_120_canonical_v0__mysql
calcite_hep_track_a_120_canonical_v0__spark
```

Canonical aggregate metrics export:

```text
/tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/results/calcite_hep_track_a_120_canonical_v0/metrics/
/tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/reports/calcite_hep_track_a_120_canonical_v0/metrics_summary.md
```

Protected surfaces:
- top-level `reports/`: not used
- top-level `results/`: not used
- repository-level `output/`: not used
- committed `runs/user/`: not staged
- external Calcite artifacts: not staged
