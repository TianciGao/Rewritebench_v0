# Fail-Closed Policy

Policy scope:

- route: `optimize_schema_aware`
- route_id: `sqlglot_optimize_schema_aware`
- dialect: `mysql`

Detection is intentionally narrow:

- `ARRAY_ANY(` in generated MySQL schema-aware optimize SQL maps to `mysql_unsupported_array_any`.
- SQLGlot-style lambda variable syntax such as `` `_x` -> `` maps to `sqlglot_unsupported_mysql_lambda`.

The guard does not run for:

- PostgreSQL.
- Spark.
- context-free `sqlglot_optimize`.
- `sqlglot_noop`.

## Runtime behavior

When the guard fires:

1. The adapter keeps the original SQLGlot output in the local workspace as `unsupported_candidate.sql`.
2. The adapter writes `sqlglot_status.json` with:
   - `candidate_generated = false`
   - `failure_bucket = mysql_unsupported_array_any` or `sqlglot_unsupported_mysql_lambda`
   - `preflight_status` set to the same bucket
   - `unsupported_reason` describing the MySQL route limitation
3. The adapter returns success with no executable candidate file.
4. The user-entry runner sees no `SQLRB_CANDIDATE_SQL_PATH` candidate and skips preflight/DB execution.

This preserves denominator visibility without allowing known-unsupported MySQL SQL to become a `candidate_execution_failed` row.

The guard does not rewrite SQL and does not change case SQL, checker policy, Spark behavior, or source execution.
