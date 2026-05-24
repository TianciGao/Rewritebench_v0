# Calcite HEP Target Dialect Runtime Mode

Task: `calcite_hep_target_dialect_runtime_mode_v0`

Branch: `feature/case-package-v2-external-schema`

Verdict: target-dialect runtime mode is staged and wired through the adapter.

The external runtime now accepts `--engine postgres|mysql|spark` and uses the
matching Calcite `SqlDialect` for RelToSql and parse-only emission. The release
repo adapter now passes the user-run target engine to the runtime. The existing
MySQL/Spark fail-closed guard remains in place, so PostgreSQL-dialect output
for non-PostgreSQL targets still does not reach DB execution.

Bounded validation used the same six-case matrix as the prior readiness smoke:

- `PERF_0006`
- `CONS_0005`
- `CONS_0036`
- `CONS_0037`
- `PORT_0004`
- `PORT_0024`

PostgreSQL behavior stayed stable. MySQL generated and executed five target
dialect candidates. Spark generated five target dialect candidates; four
executed and checked exact, while the PORT source-role row remained unsupported
by local diagnostic policy.

No full Track A 120 run, `compute-local-metrics`, timing, verifier pass,
official metric, paper result, retained evidence promotion, leaderboard output,
denominator change, or case membership change was performed.
