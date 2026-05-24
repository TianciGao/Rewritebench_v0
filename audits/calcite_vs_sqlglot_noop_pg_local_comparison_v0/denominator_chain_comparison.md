# Denominator Chain Comparison

| field | SQLGlot noop | Calcite HEP fail-closed |
| --- | ---: | ---: |
| selected rows | 40 | 40 |
| generated candidate rows | 35 | 33 |
| no-candidate rows | 5 | 7 |
| execution attempted rows | 35 | 29 |
| source executable rows | 35 | 28 |
| candidate executable rows | 35 | 28 |
| checker attempted rows | 35 | 28 |
| exact/result-consistent rows | 35 | 22 |
| timed exact rows | 35 | 22 |
| timing failed rows | 0 | 0 |

Calcite-specific denominator notes:

- 4 schema-fallback candidates were excluded by policy.
- 1 row failed source execution in the PostgreSQL-only route-card context.
- 6 checker mismatches remain visible.

Denominator warning:

- SQLGlot noop has 35 timed exact rows.
- Calcite HEP has 22 timed exact rows.
- Speedup diagnostics are computed over different exact-timed denominators and must not be used as a global rank.
