# SQLGlot Optimize Schema-Aware Post ARRAY_ANY Tri-Engine Rerun v0

Task: `sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0`

Branch: `feature/case-package-v2-external-schema`

This packet records a bounded local-only tri-engine execution/checker rerun for:

- route_id: `sqlglot_optimize_schema_aware`
- method_id: `sqlglot`
- adapter option: `--route optimize_schema_aware`
- cases: `CONS_0005`, `PERF_0006`, `CONS_0036`
- engines: PostgreSQL, MySQL, Spark

The rerun happened after the MySQL `ARRAY_ANY` fail-closed guard. Runtime artifacts were written only under `/tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/`.

## Result

- planned rows: 9
- generated executable candidates: 8
- explicit fail-closed rows: 1
- source executable rows: 9
- candidate executable rows: 8
- checker attempted rows: 8
- exact/result-consistent rows: 6
- mismatches: 2
- source execution failures: 0
- candidate execution failures: 0

`CONS_0005` / MySQL no longer appears as `candidate_execution_failed`. It is now fail-closed before candidate DB execution with bucket `mysql_unsupported_array_any`.

No full Track A 120 run, all-Common-core run, timing, verifier pass, official metrics, Semantic Equivalence Rate, formal Regression@20, paper report/result update, retained-evidence promotion, leaderboard output, denominator change, case membership change, or committed runtime artifact occurred.
