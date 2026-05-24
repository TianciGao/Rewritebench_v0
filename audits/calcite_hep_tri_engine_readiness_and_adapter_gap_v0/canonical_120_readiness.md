# Canonical Track A 120 Readiness

Verdict: not ready.

Readiness positives:

- The route can be invoked through `python -m cli.main user evaluate`.
- The adapter resolves per-engine DDL for PostgreSQL, MySQL, and Spark.
- PostgreSQL candidate generation/execution/checker behavior remains available.
- MySQL/Spark PostgreSQL-dialect output no longer reaches DB execution.
- Runtime output can be kept under a temp D035-shaped output root.

Blocking gaps before canonical Track A 120:

- External Calcite runtime has no committed user-facing `--engine` dialect mode.
- MySQL and Spark generated SQL is currently treated as unsupported when it
  contains PostgreSQL dialect forms.
- DATETIME/TIMESTAMP and PORT source-role blockers remain separate.
- Schema-fallback policy remains separate.
- Existing Calcite mismatches remain unresolved.

Required next step:

Authorize a narrow Calcite runtime/adapter engine-mode task that proves target
dialect emission for MySQL and Spark on a bounded matrix. Only after that should
a canonical 40 cases x 3 engines user-facade run be attempted.

Still not authorized:

- full Track A 120
- `compute-local-metrics`
- timing
- SQLSolver / VeriEQL
- official metrics
- paper reports/results
- retained evidence promotion
- leaderboard output
