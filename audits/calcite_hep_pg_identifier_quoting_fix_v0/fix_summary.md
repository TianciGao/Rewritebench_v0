# Fix Summary

Changed file: `baselines/calcite_hep_fail_closed/adapter.py`.

Implemented a PostgreSQL-only candidate postprocess:

- Resolve the per-engine PostgreSQL DDL already used for the external Calcite invocation.
- Parse `CREATE TABLE` definitions conservatively for unquoted table and column identifiers.
- Build the set of identifiers PostgreSQL folds to lowercase.
- In generated candidate SQL, replace only simple quoted identifiers whose lowercase form is in that DDL identifier set.
- Leave aliases and computed names unchanged when they are not DDL identifiers.
- Record postprocess metadata in `calcite_hep_status.json` under `candidate_postprocess`.

Policy name: `postgres_only_unquoted_ddl_identifier_fold_v0`.

Example after fix:

```sql
SELECT emp.deptno, COUNT(DISTINCT dept.name)
FROM emp
LEFT JOIN dept ON emp.deptno = dept.deptno
GROUP BY emp.deptno
```

The fix does not rewrite case files, does not change Calcite runtime artifacts, does not modify `src/sql_rewrite_bench/`, and preserves fail-closed behavior for missing runtime, missing schema DDL, runtime errors, timeout, or empty candidate output.
