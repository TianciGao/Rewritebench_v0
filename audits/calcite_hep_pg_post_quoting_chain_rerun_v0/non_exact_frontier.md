# Non-Exact Frontier

The post-fix non-exact / non-timed frontier has 18 rows:

| bucket | rows |
| --- | ---: |
| no_candidate_sql | 7 |
| schema_fallback_excluded | 4 |
| source_execution_failed | 1 |
| checker_mismatch | 6 |

No-candidate rows:

- `PORT_0003`
- `PORT_0004`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`
- `PORT_0022`
- `PORT_0025`

Schema-fallback excluded rows:

- `PORT_0013`
- `LONGTAIL_0022`
- `LONGTAIL_0023`
- `LONGTAIL_0024`

Source execution failed:

- `PORT_0024`

Checker mismatches:

- `PERF_0035`
- `PERF_0062`
- `CONS_0036`
- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`

`CONS_0036` is label-only with value-exact result under strict checker labels. The LONGTAIL mismatch rows are value mismatches and require semantic review.
