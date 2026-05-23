# Selection Review

Source run:
- `runs/user/common_core_pg_noop_db_checker`

Selected rows:

| case_id | pool | engine | route_id | method_id | reason |
| --- | --- | --- | --- | --- | --- |
| CONS_0036 | CONS | postgres | sqlglot_noop | sqlglot_noop | Positive-control exact row that previously produced clean bounded equivalence. |
| CONS_0037 | CONS | postgres | sqlglot_noop | sqlglot_noop | First expansion candidate; prior bound probe showed clean all-`EQU` through `bound_size=4`. |

No new Common-core run was created. No SQLSolver run was performed. No timing was collected.

Runtime output root:
- `/tmp/sqlrb_verieql_bound4_two_row_uniform_policy_pass_v0/`

