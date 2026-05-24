# sqlglot_optimize_schema_aware_route_design_fix_v0

This audit records a narrow SQLGlot optimize route design fix for the Track A same-engine local diagnostic surface.

Decision:
- New route id: `sqlglot_optimize_schema_aware`
- Existing context-free route preserved: `sqlglot_optimize`
- User-entry method id remains `sqlglot`, matching existing route identity grouping.

Implementation:
- `baselines/sqlglot/sqlglot_user_adapter.py` now accepts `--route optimize_schema_aware`.
- The route resolves per-engine DDL from the selected case manifest/schema profile.
- It builds a table/column schema mapping from `CREATE TABLE` DDL and calls `sqlglot.optimizer.optimize(expression, schema=..., dialect=...)`.
- Missing or unparsable schema context fails closed with explicit status metadata.

Bounded validation:
- Cases: `CONS_0005`, `PERF_0006`, `CONS_0036`
- Engines: PostgreSQL, MySQL, Spark
- Rows attempted: 9
- Candidate generated rows: 9
- Candidate preflight passed rows: 9
- Rows with the prior invalid `table1.table2.i` qualification: 0

Boundary:
- No full Track A 120 run.
- No DB execution/checker pass in this task.
- No timing, verifier pass, official metrics, Semantic Equivalence Rate, reports/results update, retained-evidence promotion, leaderboard output, denominator change, case membership change, or paper-result change.
