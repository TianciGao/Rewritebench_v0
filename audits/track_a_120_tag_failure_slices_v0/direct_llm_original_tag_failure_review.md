# Direct LLM Original Tag Failure Review

Route identity: `direct_llm_original`

Run id: `direct_llm_original_track_a_120_canonical_v0`

## Source Artifact Paths

- Aggregate audit packet: `audits/direct_llm_original_track_a_120_canonical_user_rerun_v0`
- Source run paths: `runs/user/direct_llm_original_track_a_120_canonical_v0__mysql/failures.csv; runs/user/direct_llm_original_track_a_120_canonical_v0__mysql/ledger.csv; runs/user/direct_llm_original_track_a_120_canonical_v0__mysql/tag_slices.csv; runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/failures.csv; runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/ledger.csv; runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/tag_slices.csv; runs/user/direct_llm_original_track_a_120_canonical_v0__spark/failures.csv; runs/user/direct_llm_original_track_a_120_canonical_v0__spark/ledger.csv; runs/user/direct_llm_original_track_a_120_canonical_v0__spark/tag_slices.csv`
- Inventory packet: `audits/track_a_120_existing_baseline_evidence_inventory_v0/`

## Dominant Failure Buckets

none=102, mismatch=10, unsupported_engine=5, candidate_execution_failed=3

## Dominant Tag Axes Involved

- `portability_risk`: literal_predicate_boundary=5, type_coercion=5, identifier_quoting=4, type_semantics_gap=4, date_time_semantics=4, null_semantics_gap=3, date_filter_semantics=3, datetime_semantics_gap=3
- `sql_feature`: correlated_subquery=5, expression_complexity=4, outer_join=3, date_time_function=3, aggregate=1, disjunction=1, join=1, range_predicate=1
- `rewrite_opportunity`: dialect_adaptation=10, subquery_decorrelation=3, expression_simplification=3, function_normalization=3, aggregation_rewrite=1
- `plan_operator`: No rows in this slice.
- `workload_realism`: No rows in this slice.

## Engine Boundary Notes

- `postgres` failure buckets: none=39, mismatch=1
- `mysql` failure buckets: none=32, mismatch=8
- `spark` failure buckets: none=31, unsupported_engine=5, candidate_execution_failed=3, mismatch=1

## Pool Boundary Notes

- `PERF` failure buckets: none=47, mismatch=1
- `CONS` failure buckets: none=21, mismatch=4, candidate_execution_failed=2
- `PORT` failure buckets: none=17, mismatch=5, unsupported_engine=5
- `LONGTAIL` failure buckets: none=17, candidate_execution_failed=1

## Diagnostic Boundary

These findings are diagnostic/support only. They must not be claimed as primary metrics, official metrics, SER, POCR, paper evidence, retained evidence, or leaderboard input. Local checker exactness remains Result Consistency evidence only and is not formal verifier evidence.

## What Must Not Be Claimed

- Do not claim tag slices are POCR or operation-atom coverage.
- Do not claim tag slices are SER or formal semantic equivalence evidence.
- Do not claim unsupported verifier absence as method failure.
- Do not claim route comparisons as a global method ranking.
