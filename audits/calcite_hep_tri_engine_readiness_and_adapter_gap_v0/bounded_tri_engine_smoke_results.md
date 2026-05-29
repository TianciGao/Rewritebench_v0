# Bounded Tri-Engine Smoke Results

Two bounded user-facade smokes were run:

1. Pre-guard smoke to identify whether MySQL/Spark failures were adapter/runtime
   target-dialect gaps.
2. Post-guard smoke after the narrow fail-closed guard was added.

The post-guard run is the result of record for this packet:

`calcite_hep_tri_engine_readiness_after_guard_v0`

Post-guard summary:

| engine | selected | generated candidates | fail-closed / no executable candidate | source executable | candidate executable | checker attempted | exact | mismatch |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| postgres | 6 | 5 | 1 | 5 | 5 | 5 | 4 | 1 |
| mysql | 6 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| spark | 6 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |

PostgreSQL details:

- `PERF_0006`, `CONS_0005`, `CONS_0037`, and `PORT_0024` were exact.
- `CONS_0036` executed source and candidate, then remained a label-only
  checker mismatch.
- `PORT_0004` remained `calcite_no_candidate_sql`.

MySQL details:

- `PORT_0004` remained `calcite_no_candidate_sql`.
- The other five rows failed closed before DB execution with
  `mysql_postgres_dialect_quoted_identifier`.
- No MySQL candidate reached DB execution after the guard.

Spark details:

- `PORT_0004` remained `calcite_no_candidate_sql`.
- The other five rows failed closed before DB execution with
  `spark_postgres_dialect_quoted_identifier`.
- `PORT_0024` also remains a Spark source-role / target-reference policy row;
  the generated candidate was blocked before DB execution.

Pre-guard discovery:

- PostgreSQL generated 5 candidates and behaved the same as above.
- MySQL generated 5 candidates, but all 5 failed candidate execution because
  the runtime emitted PostgreSQL double-quoted identifiers.
- Spark generated 5 candidates; target execution failed or was unsupported
  because the runtime emitted PostgreSQL-dialect SQL for Spark.

The guard converts those MySQL/Spark DB execution failures into explicit
fail-closed adapter outcomes.
