# Diagnostic Rate Comparison

Rates use selected rows as denominator. They are local diagnostic rates, not
official metrics.

| rate | formula | SQLGlot noop | Calcite HEP fail-closed |
| --- | --- | ---: | ---: |
| local generation rate | generated / selected | 35/40 = 0.875000 | 33/40 = 0.825000 |
| local execution coverage rate | candidate executable / selected | 35/40 = 0.875000 | 28/40 = 0.700000 |
| local result consistency rate | exact / selected | 35/40 = 0.875000 | 22/40 = 0.550000 |

Interpretation:

- SQLGlot noop has higher PostgreSQL candidate generation, execution coverage, and exact/result-consistency coverage in this local diagnostic run.
- SQLGlot noop is a low-transform infrastructure/control route; high coverage is not an optimizer-strength claim.
- Calcite HEP remains a route-development surface with visible frontier buckets.
