# sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0

This audit records a bounded tri-engine execution/checker diagnostic for the new schema-aware SQLGlot optimize route.

Route:
- `route_id = sqlglot_optimize_schema_aware`
- `method_id = sqlglot`
- adapter option: `--route optimize_schema_aware`

Scope:
- cases: `CONS_0005`, `PERF_0006`, `CONS_0036`
- engines: PostgreSQL, MySQL, Spark
- planned rows: 9

Summary:
- generated candidates: 9/9
- preflight passed: 9/9
- source executable: 9/9
- candidate executable: 8/9
- checker attempted: 8/9
- exact/result-consistent: 6/9
- mismatches: 2/9
- source execution failures: 0/9
- candidate execution failures: 1/9

The prior invalid `CONS_0005` three-part qualification did not appear in any generated candidate. PostgreSQL `CONS_0005` was exact. MySQL `CONS_0005` failed candidate execution because the schema-aware optimize output contained unsupported `ARRAY_ANY` syntax for MySQL. Spark `CONS_0005` executed but mismatched row count. Spark `CONS_0036` executed and was a strict-label mismatch with value equality.

Boundary:
- No full Track A 120 run.
- No timing.
- No verifier pass.
- No official metrics, Semantic Equivalence Rate, formal Regression@20, reports/results update, retained-evidence promotion, leaderboard output, denominator change, case membership change, or paper-result change.
