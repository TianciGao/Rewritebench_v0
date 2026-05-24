# Source Run Layout

The user facade created per-engine source runs:

- `runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__postgres/`
- `runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__mysql/`
- `runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__spark/`

Each per-engine source run contains:

- `ledger.csv`
- `config.yaml`
- `summary.json`
- `timing/rows/*.json`

The canonical aggregate metrics command created:

- `runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0/`
- `runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0/metrics/`

The aggregate source run is internal staging only. It was not staged or committed.
