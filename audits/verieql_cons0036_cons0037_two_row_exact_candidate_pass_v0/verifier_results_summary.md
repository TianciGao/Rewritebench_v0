# Verifier Results Summary

Runtime path:
- `/tmp/sqlrb_verieql_cons0036_cons0037_two_row_exact_candidate_pass_v0/`

Per-row verdicts:

| case_id | raw states | normalized verdict | interpretation |
| --- | --- | --- | --- |
| CONS_0036 | `EQU|EQU|EQU|EQU|EQU|EQU|EQU|EQU|EQU|EQU` | equivalent | Clean finite-bound equivalent over a real exact candidate row. |
| CONS_0037 | `EQU|EQU|EQU|EQU|TMO` | timeout | VeriEQL reached the row and schema, but timed out at the bounded path. Partial `EQU` plus `TMO` is not equivalence evidence. |

Counts:
- selected rows: 2
- exact candidate rows: 2
- verifier attempted rows: 2
- equivalent count: 1
- non-equivalent count: 0
- unknown count: 0
- timeout count: 1
- unsupported count: 0
- syntax error count: 0
- not implemented count: 0
- out of memory count: 0
- tool error count: 0
- not attempted count: 0
- decidable count: 1

`CONS_0037` was unblocked by DDL parser hardening in the sense that valid schema metadata reached VeriEQL. It remains non-decidable at `bound_size=10` and `timeout_seconds=30` because of timeout.

