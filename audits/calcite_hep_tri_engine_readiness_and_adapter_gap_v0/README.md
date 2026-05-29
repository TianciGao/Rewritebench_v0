# Calcite HEP Tri-Engine Readiness And Adapter Gap

Task: `calcite_hep_tri_engine_readiness_and_adapter_gap_v0`

Branch: `feature/case-package-v2-external-schema`

Verdict: Calcite HEP is invokable through the D035 user facade for PostgreSQL,
MySQL, and Spark, and it resolves per-engine DDL. It is not ready for a
canonical Track A 120 user-facade metrics run yet.

The bounded smoke used six representative cases over three engines:

- `PERF_0006`
- `CONS_0005`
- `CONS_0036`
- `CONS_0037`
- `PORT_0004`
- `PORT_0024`

PostgreSQL remains the only target with executable Calcite candidates in this
smoke. MySQL and Spark now fail closed before DB execution when the external
runtime emits PostgreSQL-dialect SQL such as double-quoted identifiers.

No full Track A 120 run was performed. No timing, verifier pass,
`compute-local-metrics`, official metric, paper result, retained evidence
promotion, leaderboard output, denominator change, or case membership change
was performed.
