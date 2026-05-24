# Execution Checker Summary

Overall:
- planned rows: 9
- generated candidate rows: 9
- preflight passed rows: 9
- source executable rows: 9
- candidate executable rows: 8
- checker attempted rows: 8
- exact rows: 6
- mismatch rows: 2
- source execution failed rows: 0
- candidate execution failed rows: 1

By engine:

| engine | planned | generated | source executable | candidate executable | checker attempted | exact | mismatch | candidate failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| PostgreSQL | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 |
| MySQL | 3 | 3 | 3 | 2 | 2 | 2 | 0 | 1 |
| Spark | 3 | 3 | 3 | 3 | 3 | 1 | 2 | 0 |

By case:

| case_id | planned | generated | source executable | candidate executable | checker attempted | exact | mismatch | candidate failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `CONS_0005` | 3 | 3 | 3 | 2 | 2 | 1 | 1 | 1 |
| `PERF_0006` | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 |
| `CONS_0036` | 3 | 3 | 3 | 3 | 3 | 2 | 1 | 0 |

Failure buckets:
- `none`: 6
- `mismatch`: 2
- `candidate_execution_failed`: 1

No source execution failures occurred.
