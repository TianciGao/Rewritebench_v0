# SQLGlot Optimize Schema-Aware MySQL ARRAY_ANY Fail-Closed v0

Task: `sqlglot_optimize_schema_aware_mysql_array_any_fail_closed_v0`

Branch: `feature/case-package-v2-external-schema`

This packet records a narrow route-hardening change for:

- route_id: `sqlglot_optimize_schema_aware`
- adapter option: `--route optimize_schema_aware`
- target engine: MySQL only

The adapter now detects known MySQL-unsupported SQLGlot optimize output containing `ARRAY_ANY` or lambda-style syntax and fails closed before DB execution. The unsupported SQL is retained in the local workspace as `unsupported_candidate.sql`, but it is not written to `SQLRB_CANDIDATE_SQL_PATH`, so the user-entry runner records no executable candidate.

## Result

Bounded smoke rows:

- `CONS_0005` / MySQL: before `candidate_execution_failed`; after fail-closed before DB execution with adapter status bucket `mysql_unsupported_array_any`.
- `CONS_0005` / PostgreSQL control: exact.
- `CONS_0005` / Spark control: remains mismatch, preserving the separate semantic-risk blocker.
- `PERF_0006` / MySQL control: exact.

No full Track A 120 run, all Common-core run, timing, verifier pass, official metric, Semantic Equivalence Rate, formal Regression@20, report/result update, retained-evidence promotion, leaderboard output, denominator change, case membership change, paper result change, physical migration, or committed runtime artifact occurred.
