# Canary Pair Definition

Pair identity:

- `pair_id`: `PERF_0062_source_vs_positive_pos_01`
- `run_id`: `verieql_perf0062_one_pair_canary_v0`
- `tool`: `verieql`
- `case_id`: `PERF_0062`
- `pool`: `PERF`
- `engine`: `postgres`
- `route_id`: `verieql_local_canary`
- `method_id`: `verieql`
- `pair_type`: `source_vs_positive`
- `denominator_id`: `local_verieql_perf0062_one_pair_canary_v0`

Manifest-resolved source and positive paths:

- Source SQL: `cases/PERF/PERF_0062/sql/source.sql`
- Positive SQL: `cases/PERF/PERF_0062/sql/pos_01.sql`
- Schema context: `schemas/tpcds_perf0062_v0/postgres/ddl.sql`
- Checker context: `cases/PERF/PERF_0062/checker/checker.yaml`

Why selected:

- `verieql_feature_support_next_canary_selection_v0` selected `PERF_0062` as the lowest-risk Common-core `source_vs_positive` pair after `CONS_0007` returned unsupported due `EXISTS`.
- The pair avoids `EXISTS`, nested `SELECT`, window functions, date/time/interval syntax, outer joins, and set operations.
- Known remaining risks were aggregate handling and literal `IN (...)` lists.

Expected high-level intent:

- Source and positive are intended to be equivalent.
- The task did not force or assume a verifier verdict.

Boundary flags:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`
