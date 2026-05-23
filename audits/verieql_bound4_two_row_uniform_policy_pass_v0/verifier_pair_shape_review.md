# Verifier Pair Shape Review

Pair shape:

| case_id | pair type | shared pair contract | pair role | source SQL | candidate SQL | schema context |
| --- | --- | --- | --- | --- | --- | --- |
| CONS_0036 | source_candidate | source_vs_candidate | method_candidate_verification | `cases/CONS/CONS_0036/sql/source.sql` | `runs/user/common_core_pg_noop_db_checker/candidate_sql/CONS_0036__postgres.sql` | `schemas/verieql_cons0036_v0/postgres/ddl.sql` |
| CONS_0037 | source_candidate | source_vs_candidate | method_candidate_verification | `cases/CONS/CONS_0037/sql/source.sql` | `runs/user/common_core_pg_noop_db_checker/candidate_sql/CONS_0037__postgres.sql` | `schemas/verieql_cons0037_v0/postgres/ddl.sql` |

Runtime JSONL schema metadata:
- `CONS_0036`: `DEPT.NAME=VARCHAR(32)`
- `CONS_0037`: `EMP.DEPTNO=BIGINT`, `DEPT.DEPTNO=BIGINT`, `DEPT.NAME=VARCHAR(32)`

Command shape:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_bound -f <pairs.jsonl> -s 4 -t 30 -c 1 -o <output.jsonl>
```

