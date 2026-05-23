# Selection Review

Source run:
- `runs/user/common_core_pg_noop_db_checker`

Source ledger:
- `runs/user/common_core_pg_noop_db_checker/ledger.csv`

Selected rows:

| case_id | pool | engine | route_id | method_id | reason |
| --- | --- | --- | --- | --- | --- |
| CONS_0036 | CONS | postgres | sqlglot_noop | sqlglot_noop | Current positive control and previously proven clean finite-bound equivalent row. |
| CONS_0037 | CONS | postgres | sqlglot_noop | sqlglot_noop | First expansion candidate after DDL parameterized type parser hardening. |

No new Common-core run was created. No timing was collected. No SQLSolver run was performed.

Runtime output root:
- `/tmp/sqlrb_verieql_cons0036_cons0037_two_row_exact_candidate_pass_v0/`

No runtime output under repository-level `output/` or `runs/user/` was committed.

