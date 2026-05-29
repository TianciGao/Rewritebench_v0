# CONS_0005 MySQL Fail-Closed Review

Before the MySQL `ARRAY_ANY` guard, `CONS_0005` / MySQL generated a candidate containing MySQL-unsupported `ARRAY_ANY` / lambda-style syntax and reached DB execution, where it was recorded as `candidate_execution_failed`.

After the guard:

- candidate DB execution was not reached;
- no executable candidate path was exposed;
- unsupported generated SQL was retained only in the local runtime workspace;
- `unsupported_candidate_sql_sha256` was recorded in the audit ledger;
- source execution still succeeded;
- the row is recorded as fail-closed with bucket `mysql_unsupported_array_any`.

This is the intended behavior for a known unsupported SQLGlot MySQL dialect-emission shape. It avoids recording a predictable unsupported candidate as a DB execution failure while preserving traceability for later dialect-specific work.

Control outcomes:

- `CONS_0005` / PostgreSQL remained exact/result-consistent.
- `CONS_0005` / Spark remained a separate mismatch and was not changed by this MySQL-only guard.
- `PERF_0006` / MySQL remained exact/result-consistent.
