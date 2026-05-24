# SQLGlot Optimize Schema-Aware Bounded Tri-Engine Blocker Triage v0

Task: `sqlglot_optimize_schema_aware_bounded_tri_engine_blocker_triage_v0`

Branch: `feature/case-package-v2-external-schema`

This packet triages the three remaining non-exact rows from the bounded tri-engine execution/checker diagnostic for:

- route_id: `sqlglot_optimize_schema_aware`
- method_id: `sqlglot`
- adapter option: `--route optimize_schema_aware`

Input audit:

- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/`

No new candidate generation, SQL execution, checker run, timing, verifier run, official metric, Semantic Equivalence Rate, paper report/result update, retained-evidence promotion, leaderboard output, denominator change, case membership change, or physical layout migration was performed.

## Rows inspected

1. `CONS_0005` / MySQL / candidate execution failed.
2. `CONS_0005` / Spark / checker mismatch.
3. `CONS_0036` / Spark / strict-label checker mismatch.

## Triage result

- MySQL `CONS_0005`: primary `mysql_array_any_dialect_emission_blocker`; SQLGlot emitted MySQL-unsupported `ARRAY_ANY(..., _x -> ...)` syntax. This is a dialect-emission/optimizer-output blocker, not the prior schema qualification failure.
- Spark `CONS_0005`: primary `spark_semantic_mismatch_candidate`; source row count was 0 and candidate row count was 1. This is not label-only and is not safe to normalize.
- Spark `CONS_0036`: primary `spark_label_only_mismatch_candidate`; values matched, but strict result labels differed (`C`/`NAME` versus `c`/`name`).

The prior invalid `table1.table2.i` qualification is still resolved across all three engines.

## Readiness impact

The route is safe for exact-gated timing over the six currently exact rows if a narrow timing smoke is useful, but it is not ready for a larger 40 x 3 Track A local diagnostic trial. The next higher-value step is a dedicated fix/design task for MySQL `ARRAY_ANY` fail-closed or dialect emission, plus Spark `CONS_0005` semantic triage before broader Spark coverage.

