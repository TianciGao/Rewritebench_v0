# calcite_hep_pg_frontier_blocker_triage_v0

Task: local-only triage of the non-exact / non-timed Calcite HEP PostgreSQL diagnostic frontier.

Inputs used:

- `audits/calcite_hep_pg_bounded_candidate_generation_v0/`
- `audits/calcite_hep_pg_execution_checker_diagnostic_v0/`
- `audits/calcite_hep_pg_exact_timing_diagnostic_v0/`
- `audits/calcite_hep_pg_local_metrics_projection_v0/`

No new candidate generation, SQL execution, checker run, timing collection, verifier pass, MySQL/Spark run, full-120 run, official metric computation, report/result update, retained-evidence promotion, or leaderboard output was performed.

Frontier counts:

- `no_candidate_sql = 7`
- `mismatch = 3`
- `source_execution_failed = 2`
- `candidate_execution_failed = 8`

Primary blocker counts:

- `calcite_identifier_quoting_blocker = 9`
- `datetime_timestamp_syntax_or_type_blocker = 3`
- `port_source_dialect_not_pg_executable = 2`
- `calcite_generated_candidate_semantic_mismatch = 3`
- `schema_fallback_candidate_failed = 3`

The four schema-fallback rows are `PORT_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024`; all should be excluded from future execution by default until schema-ingestion support is explicitly hardened.
