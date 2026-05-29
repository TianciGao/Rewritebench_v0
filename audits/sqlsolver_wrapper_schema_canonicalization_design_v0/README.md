# SQLSolver Wrapper/Schema Canonicalization Design

Task: `sqlsolver_wrapper_schema_canonicalization_design_v0`

This design packet exists because the bounded SQLSolver pass produced useful but coverage-limited verifier-support evidence: 3 actual source-candidate checks were equivalent after passing identity guards, while 5 selected pairs had identity-guard `UNKNOWN` outcomes.

## What Failed

The identity-guard unknown rows were:

- `LONGTAIL_0011`
- `PERF_0006`
- `PERF_0007`
- `PORT_0003`
- `PORT_0005`

Gap categories from the triage packet:

- `schema_canonicalization_gap`: 1
- `unsupported_postgres_dialect`: 2
- `unsupported_sql_feature`: 1
- `wrapper_input_format_gap`: 1

## Why Upstream SQLSolver Requirements Matter

SQLSolver expects line-paired query files with one SQL statement per physical line, parses SQL through Calcite, and reports `UNKNOWN` for cases it cannot decide, including unsupported features and syntax errors. Those constraints map directly to the current failures: comment/line shaping, PostgreSQL date/interval syntax, draft DDL syntax, quoted identifiers/null ordering, and DENSE_RANK/CTE support.

## Proposed Canonicalization Families

- `feature_support_scope` for `LONGTAIL_0011`
- `sql_line_shaping_and_comment_policy` for `PERF_0006`
- `date_interval_normalization_policy` for `PERF_0007`
- `schema_ddl_canonicalization_policy` for `PORT_0003`
- `identifier_ordering_canonicalization_policy` for `PORT_0005`

## Canary Plan

- `leading_line_comments_date_literal_identity_canary`: wrapper_input_format_gap
- `date_interval_arithmetic_identity_canary`: unsupported_postgres_dialect
- `double_precision_inline_ddl_comment_identity_canary`: schema_canonicalization_gap
- `quoted_identifier_null_ordering_identity_canary`: unsupported_postgres_dialect
- `dense_rank_cte_identity_canary`: unsupported_sql_feature

These canaries are design targets only. They were not run in this task.

## Current Boundary

- Code changed: no
- SQLSolver run: no
- VeriEQL run: no
- Larger verifier pass authorized: no
- Official SER produced: no
- Repair-1 run: no

## Next Safe Action

Authorize a narrow implementation task for SQLSolver wrapper/schema canonicalization with fixture tests and non-benchmark identity canaries. Do not broaden SQLSolver coverage and do not start Repair-1 until the same 8-pair bounded verifier pass is stable after canonicalization.
