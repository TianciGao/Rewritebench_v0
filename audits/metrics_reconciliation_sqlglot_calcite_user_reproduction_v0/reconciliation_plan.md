# Reconciliation Plan

Inputs inspected read-only:

- New D035-style local outputs under `output/results/*_track_a_120_user_reproduction_v0/`.
- New audit packet `audits/nightly_user_reproduction_sqlglot_calcite_track_a_120_metrics_v0/`.
- Prior canonical packets for SQLGlot no-op, SQLGlot optimize schema-aware, and Calcite HEP fail-closed.
- Prior current `runs/user/<canonical_run_id>/metrics/` CSV/JSON files for row-level timing and failure bucket reconciliation.
- Paper-facing table packet and candidate-capture packet as context only.

Method:

1. Copy no metrics into source artifacts and rerun nothing.
2. Parse existing JSON/CSV files.
3. Compare counts, rates, GM speedup, percentiles, row-level exact/timed status, and failure buckets.
4. For GM review, recompute geometric means from existing per-row `speedup_ratio` arrays for audit verification only and label the result diagnostic.
5. Preserve the boundary that the new outputs are local diagnostic reproduction evidence only.
