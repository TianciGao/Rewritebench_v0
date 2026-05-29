# Execution Checker Summary

## Aggregate

| field | value |
|---|---:|
| planned rows | 9 |
| generated executable candidates | 8 |
| preflight passed rows | 8 |
| fail-closed rows | 1 |
| source executable rows | 9 |
| candidate executable rows | 8 |
| checker attempted rows | 8 |
| exact/result-consistent rows | 6 |
| mismatch rows | 2 |
| source execution failures | 0 |
| candidate execution failures | 0 |

## By Engine

| engine | planned | generated | fail-closed | source executable | candidate executable | checker attempted | exact | mismatch | candidate execution failed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PostgreSQL | 3 | 3 | 0 | 3 | 3 | 3 | 3 | 0 | 0 |
| MySQL | 3 | 2 | 1 | 3 | 2 | 2 | 2 | 0 | 0 |
| Spark | 3 | 3 | 0 | 3 | 3 | 3 | 1 | 2 | 0 |

## By Case

| case_id | planned | generated | fail-closed | source executable | candidate executable | checker attempted | exact | mismatch |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `CONS_0005` | 3 | 2 | 1 | 3 | 2 | 2 | 1 | 1 |
| `PERF_0006` | 3 | 3 | 0 | 3 | 3 | 3 | 3 | 0 |
| `CONS_0036` | 3 | 3 | 0 | 3 | 3 | 3 | 2 | 1 |

## Notes

- The prior invalid `table1.table2.i` qualification remains absent from the schema-aware route output in this rerun.
- `CONS_0005` / MySQL is explicit fail-closed with `mysql_unsupported_array_any`.
- `CONS_0005` / Spark remains a semantic mismatch candidate.
- `CONS_0036` / Spark remains a label-only mismatch candidate.
- No timing was collected.
- No verifier was run.
