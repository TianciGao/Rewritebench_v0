# Bound/Timeout Matrix

Source row:
- Source run: `runs/user/common_core_pg_noop_db_checker`
- Case: `CONS_0037`
- Engine: PostgreSQL
- Route/method: SQLGlot noop
- Pair: source-vs-candidate

Verifier settings:
- Tool: VeriEQL
- Mode: finite-bound
- Cores: 1
- Schema canonicalization: enabled
- Source SQL: `cases/CONS/CONS_0037/sql/source.sql`
- Candidate SQL: `runs/user/common_core_pg_noop_db_checker/candidate_sql/CONS_0037__postgres.sql`
- Schema context: `schemas/verieql_cons0037_v0/postgres/ddl.sql`

Matrix result:

| bound_size | timeout_seconds | raw states | normalized verdict | interpretation |
| ---: | ---: | --- | --- | --- |
| 1 | 30 | `EQU` | equivalent | Clean bounded equivalent at bound 1. |
| 2 | 30 | `EQU|EQU` | equivalent | Clean bounded equivalent through bound 2. |
| 3 | 30 | `EQU|EQU|EQU` | equivalent | Clean bounded equivalent through bound 3. |
| 4 | 30 | `EQU|EQU|EQU|EQU` | equivalent | Clean bounded equivalent through bound 4. |
| 5 | 30 | N.A.; wrapper-level timeout before output JSONL row was populated | timeout | Non-decidable at bound 5 / 30 seconds. |
| 10 | 30 | N.A.; wrapper-level timeout before output JSONL row was populated | timeout | Non-decidable at bound 10 / 30 seconds. |
| 5 | 120 | N.A.; wrapper-level timeout before output JSONL row was populated | timeout | Increasing timeout to 120 seconds did not make bound 5 decidable. |
| 10 | 120 | N.A.; wrapper-level timeout before output JSONL row was populated | timeout | Increasing timeout to 120 seconds did not make bound 10 decidable. |

Note:
- The previous two-row pass observed `CONS_0037` at `bound_size=10`, `timeout_seconds=30` as `EQU|EQU|EQU|EQU|TMO`.
- In this single-row matrix, the wrapper's outer bounded subprocess timeout expired before the timeout settings wrote output JSONL rows for bounds 5 and 10.
- Both observations have the same strict normalized verdict: `timeout`.

