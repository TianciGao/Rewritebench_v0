# CONS_0037 Readiness Check

Purpose:
- Confirm the first planned expansion candidate, `CONS_0037`, no longer emits truncated parameterized type metadata.
- This was a wrapper-level schema extraction smoke only.
- VeriEQL was not invoked.

Runtime path:
- `/tmp/sqlrb_verieql_ddl_parameterized_type_parser_hardening_v0/cons0037_pairs.jsonl`

Input row:
- Source run: `runs/user/common_core_pg_noop_db_checker`
- Case: `CONS_0037`
- Engine: PostgreSQL
- Route/method: SQLGlot noop
- Pair type: `source_vs_candidate`
- Schema context: `schemas/verieql_cons0037_v0/postgres/ddl.sql`

Generated schema metadata:

```json
{
  "DEPT": {
    "DEPTNO": "BIGINT",
    "NAME": "VARCHAR(32)"
  },
  "EMP": {
    "DEPTNO": "BIGINT"
  }
}
```

Readiness result:
- DDL parser blocker for `CONS_0037` is cleared.
- `CONS_0037` remains a suitable first expansion candidate for a separately authorized two-row exact-candidate VeriEQL pass.
- That future pass may still expose VeriEQL feature limits for `LEFT JOIN` or `COUNT(DISTINCT)`.

