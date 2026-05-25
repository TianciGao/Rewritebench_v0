# Calcite Runtime Review

Java availability: `openjdk version "17.0.18" 2026-01-20`

Calcite environment flags observed without printing values:

- `SQLRB_CALCITE_HEP_CMD` set: false
- `SQLRB_CALCITE_HEP_JAR` set: false
- `SQLRB_CALCITE_HEP_ROOT` set: false

The Calcite HEP fail-closed route proceeded through the user pipeline but produced zero candidates because the Calcite runtime environment was unavailable. The output manifests keep all 120 planned rows visible as preflight-blocked candidate rows, while the user ledger records `no_candidate_sql` failure buckets.
