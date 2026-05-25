# PG40 vs Track A 120 Storage Examples

## PG40

PG40 is PostgreSQL-only and uses 40 Common-core cases.

Example:

```text
output/results/rbot_gpt54_pg40_diagnostic_v0/candidate_sql/rbot_gpt54_adapted/rbot_gpt54_pg40_diagnostic/postgres/PERF_0006__postgres.sql
```

The root manifest should record:

- `engine_scope=postgres`
- `denominator_scope=PG40`
- `case_set_id=common_core_v0`
- `expected_count=40`

## Track A 120

Track A 120 uses 40 Common-core cases x 3 engines.

Example:

```text
output/results/direct_llm_repair_1_track_a_120_v0/candidate_sql/direct_llm_repair_1/direct_llm_repair_1_track_a_120/postgres/PERF_0006__postgres.sql
output/results/direct_llm_repair_1_track_a_120_v0/candidate_sql/direct_llm_repair_1/direct_llm_repair_1_track_a_120/mysql/PERF_0006__mysql.sql
output/results/direct_llm_repair_1_track_a_120_v0/candidate_sql/direct_llm_repair_1/direct_llm_repair_1_track_a_120/spark/PERF_0006__spark.sql
```

The root manifest should record:

- `engine_scope=mysql;postgres;spark`
- `denominator_scope=TrackA120`
- `case_set_id=common_core_v0`
- `expected_count=120`

## Boundary

PG40 candidate roots cannot fill Track A 120 POCR cells. Track A 120 needs all 120 planned route-bound candidate rows, or an explicit fail-closed/no-candidate policy that keeps missing candidates denominator-visible.

No official POCR is computed. No paper-facing metric is promoted. No route-level POCR score is emitted.
