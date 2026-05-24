# Exact Gate Source Review

Exact gate source:

- `audits/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/per_row_execution_checker_status.csv`

Gate counts from the source audit:

| Field | Count |
| --- | ---: |
| selected/planned rows | 120 |
| generated candidate rows | 105 |
| fail-closed rows | 20 |
| source executable rows | 108 |
| candidate executable rows | 91 |
| checker attempted rows | 91 |
| exact/result-consistent rows | 66 |
| mismatch rows | 25 |
| source execution failures | 0 |
| candidate execution failures | 9 |

Per-engine exact gate:

| Engine | Exact Rows | Selected Rows |
| --- | ---: | ---: |
| PostgreSQL | 29 | 40 |
| MySQL | 20 | 40 |
| Spark | 17 | 40 |

The timing helper consumed candidate SQL paths from the gate audit and skipped every row not marked exact. Rows with fail-closed status, mismatches, candidate execution failures, no candidate, unsupported engine, or strict-label mismatch were not timed.
