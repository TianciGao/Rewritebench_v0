# Candidate SQL Path Contract

## Valid Future Paths

PG40 PostgreSQL-only:

```text
output/results/direct_llm_repair_1_pg40_v0/candidate_sql/direct_llm_repair_1/direct_llm_repair_1_pg40/postgres/PERF_0006__postgres.sql
```

Track A 120 component paths:

```text
output/results/direct_llm_repair_1_track_a_120_v0/candidate_sql/direct_llm_repair_1/direct_llm_repair_1_track_a_120/postgres/PERF_0006__postgres.sql
output/results/direct_llm_repair_1_track_a_120_v0/candidate_sql/direct_llm_repair_1/direct_llm_repair_1_track_a_120/mysql/PERF_0006__mysql.sql
output/results/direct_llm_repair_1_track_a_120_v0/candidate_sql/direct_llm_repair_1/direct_llm_repair_1_track_a_120/spark/PERF_0006__spark.sql
```

General pattern:

```text
output/results/<run_id>/candidate_sql/<method_id>/<route_id>/<engine>/<CASE_ID>__<engine>.sql
```

## Invalid Future Paths

These are invalid for new user-run candidate SQL output:

```text
cases/PERF/PERF_0006/runs/<run_id>/candidate.sql
reports/<run_id>/candidate_sql/PERF_0006.sql
results/<run_id>/candidate_sql/PERF_0006.sql
output/candidate_sql/PERF_0006.sql
output/results/<run_id>/candidate_sql/PERF_0006.sql
```

Reasons:

- case-local `runs/` is not the future user-run output surface;
- top-level `reports/` and `results/` are official/paper/release-facing surfaces;
- candidate files must be route-bound by method, route, engine, case ID, and run ID;
- filenames must include case ID and engine.

## Route Binding

Candidate SQL is bound by `case_id`, `engine`, `method_id`, `route_id`, `run_id`, `case_set_id`, denominator scope, and candidate SHA-256. This binding is required for future annotation JSONL replay.

PG40 candidate roots cannot fill Track A 120 POCR cells. No official POCR is computed. No paper-facing metric is promoted. No route-level POCR score is emitted.
