# Non-Exact Frontier

The non-exact frontier contains 54 rows:

- 25 mismatches;
- 9 candidate execution failures;
- 20 fail-closed/no executable candidate rows.

## Frontier Bucket Counts

| bucket | rows |
|---|---:|
| `candidate_execution_failed` | 9 |
| `mismatch` | 25 |
| `mysql_unsupported_array_any` | 1 |
| `sqlglot_optimize_failed` | 5 |
| `sqlglot_parse_failed` | 5 |
| `sqlglot_schema_parse_failed` | 4 |
| `unsupported_engine` | 5 |

## Mismatch Rows

- semantic mismatch: `CONS_0005/spark`, `CONS_0037/mysql`, `PERF_0062/postgres`, `PERF_0062/mysql`, `PORT_0003/mysql`, `PORT_0004/spark`, `PORT_0005/mysql`, `PORT_0005/spark`, `PORT_0012/mysql`
- label-only mismatch under current strict-label policy: `CONS_0011/spark`, `CONS_0036/spark`, `CONS_0037/postgres`, `CONS_0037/spark`, `LONGTAIL_0011/spark`, `LONGTAIL_0012/spark`, `LONGTAIL_0013/spark`, `LONGTAIL_0022/spark`, `LONGTAIL_0023/spark`, `LONGTAIL_0024/spark`, `PERF_0062/spark`, `PORT_0004/mysql`, `PORT_0012/postgres`, `PORT_0013/mysql`, `PORT_0022/mysql`, `PORT_0024/mysql`

## Candidate Execution Failures

- `CONS_0007/postgres`
- `CONS_0007/mysql`
- `CONS_0007/spark`
- `CONS_0024/postgres`
- `CONS_0024/mysql`
- `CONS_0024/spark`
- `PORT_0003/spark`
- `PORT_0008/mysql`
- `PORT_0013/spark`

## Fail-Closed / No Executable Candidate Rows

- `CONS_0005/mysql`: `mysql_unsupported_array_any`
- `CONS_0009/postgres`, `CONS_0009/mysql`, `CONS_0009/spark`, `CONS_0010/mysql`, `CONS_0011/mysql`: `sqlglot_optimize_failed`
- `PERF_0008/mysql`, `PERF_0013/mysql`, `PERF_0017/mysql`, `PERF_0019/mysql`: `sqlglot_schema_parse_failed`
- `PORT_0004/postgres`, `PORT_0013/postgres`, `PORT_0022/postgres`, `PORT_0024/postgres`, `PORT_0025/postgres`: `sqlglot_parse_failed`
- `PORT_0008/spark`, `PORT_0012/spark`, `PORT_0022/spark`, `PORT_0024/spark`, `PORT_0025/spark`: `unsupported_engine`
