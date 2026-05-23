# Calcite HEP PostgreSQL Post-Quoting Chain Rerun

Task: `calcite_hep_pg_post_quoting_chain_rerun_v0`

Branch: `feature/case-package-v2-external-schema`

This audit reran the bounded local-only PostgreSQL Calcite HEP diagnostic chain after `calcite_hep_pg_identifier_quoting_fix_v0`.

Scope:

- Common-core v0 PostgreSQL slice only.
- `method_id=calcite_hep_fail_closed`
- `route_id=calcite_hep_fail_closed`
- Runtime root: `/tmp/sqlrb_calcite_hep_pg_post_quoting_chain_rerun_v0/`

Post-fix denominator chain:

| field | count |
| --- | ---: |
| selected_rows | 40 |
| generated_candidate_rows | 33 |
| no_candidate_rows | 7 |
| schema_fallback_rows | 4 |
| schema_fallback_excluded_rows | 4 |
| execution_attempted_rows | 29 |
| source_executable_rows | 28 |
| candidate_executable_rows | 28 |
| checker_attempted_rows | 28 |
| exact_rows | 22 |
| mismatch_rows | 6 |
| source_execution_failed_rows | 1 |
| candidate_execution_failed_rows | 0 |
| timed_exact_rows | 22 |
| timing_failed_rows | 0 |

Local diagnostic speedup summary over exact timed rows:

- GM speedup: `1.009852`
- P10/P25/P50/P75/P90: `0.981979 / 0.989623 / 0.995700 / 1.005620 / 1.008519`

This is not official metrics, official Semantic Equivalence Rate, formal Regression@20, paper evidence, retained evidence, or leaderboard output.
