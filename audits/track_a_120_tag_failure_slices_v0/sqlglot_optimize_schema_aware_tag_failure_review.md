# SQLGlot Optimize Schema-Aware Tag Failure Review

Route identity: `sqlglot_optimize_schema_aware`

Run id: `sqlglot_optimize_schema_aware_track_a_120_canonical_v0`

## Source Artifact Paths

- Aggregate audit packet: `audits/sqlglot_optimize_schema_aware_track_a_120_canonical_user_rerun_v0`
- Source run paths: `runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__mysql/failures.csv; runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__mysql/ledger.csv; runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__mysql/tag_slices.csv; runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__postgres/failures.csv; runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__postgres/ledger.csv; runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__postgres/tag_slices.csv; runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__spark/failures.csv; runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__spark/ledger.csv; runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__spark/tag_slices.csv`
- Inventory packet: `audits/track_a_120_existing_baseline_evidence_inventory_v0/`

## Dominant Failure Buckets

none=66, mismatch=25, adapter_failed=14, candidate_execution_failed=9, unsupported_engine=5, no_candidate_sql=1

## Dominant Tag Axes Involved

- `portability_risk`: identifier_quoting=13, literal_predicate_boundary=9, type_semantics_gap=9, type_coercion=8, date_time_semantics=7, date_filter_semantics=6, datetime_semantics_gap=6, null_semantics_gap=6
- `sql_feature`: correlated_subquery=14, outer_join=13, date_time_function=8, expression_complexity=8, join=6, subquery_in_from=6, cte=5, sort=5
- `rewrite_opportunity`: dialect_adaptation=23, expression_simplification=7, subquery_decorrelation=5, function_normalization=5, predicate_pushdown=5, aggregation_rewrite=4, order_limit_simplification=4, materialization_strategy=2
- `plan_operator`: No rows in this slice.
- `workload_realism`: No rows in this slice.

## Engine Boundary Notes

- `postgres` failure buckets: none=29, adapter_failed=6, mismatch=3, candidate_execution_failed=2
- `mysql` failure buckets: none=20, mismatch=9, adapter_failed=7, candidate_execution_failed=3, no_candidate_sql=1
- `spark` failure buckets: none=17, mismatch=13, unsupported_engine=5, candidate_execution_failed=4, adapter_failed=1

## Pool Boundary Notes

- `PERF` failure buckets: none=41, adapter_failed=4, mismatch=3
- `CONS` failure buckets: none=9, candidate_execution_failed=6, mismatch=6, adapter_failed=5, no_candidate_sql=1
- `PORT` failure buckets: mismatch=10, adapter_failed=5, unsupported_engine=5, none=4, candidate_execution_failed=3
- `LONGTAIL` failure buckets: none=12, mismatch=6

## Diagnostic Boundary

These findings are diagnostic/support only. They must not be claimed as primary metrics, official metrics, SER, POCR, paper evidence, retained evidence, or leaderboard input. Local checker exactness remains Result Consistency evidence only and is not formal verifier evidence.

## What Must Not Be Claimed

- Do not claim tag slices are POCR or operation-atom coverage.
- Do not claim tag slices are SER or formal semantic equivalence evidence.
- Do not claim unsupported verifier absence as method failure.
- Do not claim route comparisons as a global method ranking.
