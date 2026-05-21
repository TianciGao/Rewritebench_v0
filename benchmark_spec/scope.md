# Benchmark Scope

SQL-RewriteBench evaluates emitted statement-level SQL. It is not an optimizer-internal AST benchmark, rule-trace benchmark, or parser-only transformation benchmark.

The case package is the benchmark unit.

Public v0 scope:

- Common-core v0 = 40 cases.
- Pool split = 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL.
- Track A same-engine denominator = 120 planned rows across PostgreSQL, MySQL, and Spark SQL.
- Common-core v0 is controlled coverage, not a production workload frequency sample.

Public v0 boundaries:

- No global leaderboard.
- No denominator change is authorized by this spec skeleton.
- No official metrics are computed by this document.
- No paper tables are rendered by this document.
- User-entry local diagnostics are local outputs only and do not define official benchmark results.
