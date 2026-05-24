# Calcite HEP Fail-Closed Tag Failure Review

Route identity: `calcite_hep_fail_closed`

Run id: `calcite_hep_track_a_120_canonical_v0`

## Source Artifact Paths

- Aggregate audit packet: `audits/calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0`
- Source run paths: `runs/user/calcite_hep_track_a_120_canonical_v0__mysql/failures.csv; runs/user/calcite_hep_track_a_120_canonical_v0__mysql/ledger.csv; runs/user/calcite_hep_track_a_120_canonical_v0__mysql/tag_slices.csv; runs/user/calcite_hep_track_a_120_canonical_v0__postgres/failures.csv; runs/user/calcite_hep_track_a_120_canonical_v0__postgres/ledger.csv; runs/user/calcite_hep_track_a_120_canonical_v0__postgres/tag_slices.csv; runs/user/calcite_hep_track_a_120_canonical_v0__spark/failures.csv; runs/user/calcite_hep_track_a_120_canonical_v0__spark/ledger.csv; runs/user/calcite_hep_track_a_120_canonical_v0__spark/tag_slices.csv`
- Inventory packet: `audits/track_a_120_existing_baseline_evidence_inventory_v0/`

## Dominant Failure Buckets

none=81, no_candidate_sql=21, mismatch=14, candidate_execution_failed=3, unsupported_engine=1

## Dominant Tag Axes Involved

- `portability_risk`: identifier_quoting=15, type_semantics_gap=11, date_time_semantics=9, literal_predicate_boundary=8, type_coercion=8, limit_fetch_gap=6, null_semantics_gap=6, date_filter_semantics=6
- `sql_feature`: expression_complexity=11, window_function=7, cte=6, date_time_function=6, outer_join=6, join=5, aggregation=5, aggregate=4
- `rewrite_opportunity`: dialect_adaptation=26, expression_simplification=7, order_limit_simplification=6, function_normalization=6, aggregation_rewrite=4, cte_strategy=3, predicate_pushdown=1
- `plan_operator`: No rows in this slice.
- `workload_realism`: No rows in this slice.

## Engine Boundary Notes

- `postgres` failure buckets: none=25, mismatch=7, no_candidate_sql=7, candidate_execution_failed=1
- `mysql` failure buckets: none=26, mismatch=7, no_candidate_sql=7
- `spark` failure buckets: none=30, no_candidate_sql=7, candidate_execution_failed=2, unsupported_engine=1

## Pool Boundary Notes

- `PERF` failure buckets: none=43, mismatch=4, candidate_execution_failed=1
- `CONS` failure buckets: none=25, mismatch=2
- `PORT` failure buckets: no_candidate_sql=21, candidate_execution_failed=2, mismatch=2, none=1, unsupported_engine=1
- `LONGTAIL` failure buckets: none=12, mismatch=6

## Diagnostic Boundary

These findings are diagnostic/support only. They must not be claimed as primary metrics, official metrics, SER, POCR, paper evidence, retained evidence, or leaderboard input. Local checker exactness remains Result Consistency evidence only and is not formal verifier evidence.

## What Must Not Be Claimed

- Do not claim tag slices are POCR or operation-atom coverage.
- Do not claim tag slices are SER or formal semantic equivalence evidence.
- Do not claim unsupported verifier absence as method failure.
- Do not claim route comparisons as a global method ranking.
