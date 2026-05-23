# Selection Review

Input source:
- Existing run directory: `runs/user/common_core_pg_noop_db_checker`.
- Ledger: `runs/user/common_core_pg_noop_db_checker/ledger.csv`.
- Route/method: SQLGlot noop.
- Engine: PostgreSQL.

Selection policy:
- Select 2 to 5 existing local diagnostic rows.
- Require result-consistency gate before verifier execution.
- Do not create a new Common-core run.
- Do not enable timing.
- Do not use method-generated rows outside the tiny selected set.

Selected rows:

| case_id | pool | engine | route_id | method_id | candidate path | reason selected |
| --- | --- | --- | --- | --- | --- | --- |
| CONS_0036 | CONS | postgres | sqlglot_noop | sqlglot_noop | `runs/user/common_core_pg_noop_db_checker/candidate_sql/CONS_0036__postgres.sql` | Simple exact row from a VeriEQL-family schema; likely best first real candidate. |
| PERF_0077 | PERF | postgres | sqlglot_noop | sqlglot_noop | `runs/user/common_core_pg_noop_db_checker/candidate_sql/PERF_0077__postgres.sql` | Exact JOB/IMDB row with joins and `LIKE`, useful for exposing feature gaps. |
| PERF_0082 | PERF | postgres | sqlglot_noop | sqlglot_noop | `runs/user/common_core_pg_noop_db_checker/candidate_sql/PERF_0082__postgres.sql` | Exact JOB/IMDB row with joins and `LIKE`, useful as a second real feature-gap probe. |

No new local diagnostic run was created. Runtime verifier outputs were written under `/tmp/sqlrb_verieql_exact_candidate_tiny_local_pass_v0/` only.

