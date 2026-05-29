# Verifier Pair Shape Review

Verifier settings:
- verifier tool: `verieql`
- verifier mode: `finite_bound`
- bound size: 10
- timeout seconds: 30
- cores: 1
- schema canonicalization: enabled
- result checker exactness used as verifier evidence: false

Command shape:

```text
/home/tianci_gao/.venvs/sqlrb-verieql/bin/python -m parallel.cli_within_bound -f <pairs.jsonl> -s 10 -t 30 -c 1 -o <output.jsonl>
```

Pair rows:

| case_id | pair type requested | pair type in shared contract | pair role | source SQL | candidate SQL | schema context |
| --- | --- | --- | --- | --- | --- | --- |
| CONS_0036 | source_candidate | source_vs_candidate | method_candidate_verification | `cases/CONS/CONS_0036/sql/source.sql` | `runs/user/common_core_pg_noop_db_checker/candidate_sql/CONS_0036__postgres.sql` | `schemas/verieql_cons0036_v0/postgres/ddl.sql` |
| CONS_0037 | source_candidate | source_vs_candidate | method_candidate_verification | `cases/CONS/CONS_0037/sql/source.sql` | `runs/user/common_core_pg_noop_db_checker/candidate_sql/CONS_0037__postgres.sql` | `schemas/verieql_cons0037_v0/postgres/ddl.sql` |

Schema metadata observed in the runtime JSONL:
- `CONS_0036`: `DEPT.NAME=VARCHAR(32)`
- `CONS_0037`: `EMP.DEPTNO=BIGINT`, `DEPT.DEPTNO=BIGINT`, `DEPT.NAME=VARCHAR(32)`

This confirms the DDL parser hardening emitted non-empty, parameterized schema metadata for both rows.

