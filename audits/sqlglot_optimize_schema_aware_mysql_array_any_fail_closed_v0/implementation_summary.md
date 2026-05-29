# Implementation Summary

Files changed:

- `baselines/sqlglot/sqlglot_user_adapter.py`
- `baselines/sqlglot/README.md`
- `tests/user_entry/test_sqlglot_adapter.py`

Implementation details:

- Added route-scoped detection function `unsupported_mysql_schema_aware_output_bucket`.
- Added explicit buckets:
  - `mysql_unsupported_array_any`
  - `sqlglot_unsupported_mysql_lambda`
- Added MySQL-only post-generation fail-closed handling before writing to `SQLRB_CANDIDATE_SQL_PATH`.
- Retained unsupported generated SQL as `unsupported_candidate.sql` in the adapter workspace for local traceability.
- Preserved the context-free `sqlglot_optimize` route and the separate `sqlglot_optimize_schema_aware` route id.
- Updated SQLGlot adapter README to document the new fail-closed buckets.

Focused tests added:

- MySQL `ARRAY_ANY` detection is scoped to `optimize_schema_aware` + MySQL.
- PostgreSQL and Spark are not blocked by the MySQL guard.
- Context-free `optimize` is not blocked by the MySQL guard.
- Lambda-only MySQL pattern has an explicit bucket.
- SQLGlot-installed integration test confirms `CONS_0005` / MySQL emits no executable candidate and records `mysql_unsupported_array_any`.

No shared runner or `src/sql_rewrite_bench/` code was modified.
