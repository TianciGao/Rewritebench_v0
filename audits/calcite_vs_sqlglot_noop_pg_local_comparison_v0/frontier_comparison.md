# Frontier Comparison

## SQLGlot Noop

Frontier: 5 no-candidate PORT rows.

- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

Source audit interpretation:

- The five rows are cross-dialect PORT cases whose source SQL is MySQL-like while SQLGlot noop was invoked with PostgreSQL dialect settings.
- Treat as a PORT source-role / dialect-syntax issue, not a PostgreSQL execution/checker failure for generated candidates.

## Calcite HEP Fail-Closed

Frontier: 18 rows.

| bucket | count | rows |
| --- | ---: | --- |
| no_candidate_sql | 7 | `PORT_0003`, `PORT_0004`, `PORT_0005`, `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0025` |
| schema_fallback_excluded | 4 | `PORT_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, `LONGTAIL_0024` |
| source_execution_failed | 1 | `PORT_0024` |
| checker_mismatch | 6 | `PERF_0035`, `PERF_0062`, `CONS_0036`, `LONGTAIL_0011`, `LONGTAIL_0012`, `LONGTAIL_0013` |

Source audit interpretation:

- Schema-fallback candidates were excluded by policy.
- `CONS_0036` is label-only with value-exact result under strict checker labels.
- The LONGTAIL mismatch rows are value mismatches and require semantic review.

Comparison:

- SQLGlot noop frontier is smaller and concentrated in no-candidate PORT rows.
- Calcite HEP frontier is broader and includes route-development blockers across generation, schema-fallback policy, source-role execution, and checker mismatch categories.
