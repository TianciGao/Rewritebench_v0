# SQLGlot No-Op Tag Failure Review

Route identity: `sqlglot_noop`

Run id: `sqlglot_noop_track_a_120_canonical_v0`

## Source Artifact Paths

- Aggregate audit packet: `audits/sqlglot_noop_track_a_120_canonical_user_rerun_v0`
- Source run paths: `runs/user/sqlglot_noop_track_a_120_canonical_v0__mysql/failures.csv; runs/user/sqlglot_noop_track_a_120_canonical_v0__mysql/ledger.csv; runs/user/sqlglot_noop_track_a_120_canonical_v0__mysql/tag_slices.csv; runs/user/sqlglot_noop_track_a_120_canonical_v0__postgres/failures.csv; runs/user/sqlglot_noop_track_a_120_canonical_v0__postgres/ledger.csv; runs/user/sqlglot_noop_track_a_120_canonical_v0__postgres/tag_slices.csv; runs/user/sqlglot_noop_track_a_120_canonical_v0__spark/failures.csv; runs/user/sqlglot_noop_track_a_120_canonical_v0__spark/ledger.csv; runs/user/sqlglot_noop_track_a_120_canonical_v0__spark/tag_slices.csv`
- Inventory packet: `audits/track_a_120_existing_baseline_evidence_inventory_v0/`

## Dominant Failure Buckets

none=97, mismatch=10, adapter_failed=5, unsupported_engine=5, candidate_execution_failed=3

## Dominant Tag Axes Involved

- `portability_risk`: identifier_quoting=12, literal_predicate_boundary=9, type_semantics_gap=8, type_coercion=8, date_time_semantics=7, date_filter_semantics=6, datetime_semantics_gap=5, limit_fetch_gap=4
- `sql_feature`: expression_complexity=7, date_time_function=4, aggregate=1, disjunction=1, join=1, range_predicate=1
- `rewrite_opportunity`: dialect_adaptation=22, expression_simplification=5, order_limit_simplification=4, function_normalization=4
- `plan_operator`: No rows in this slice.
- `workload_realism`: No rows in this slice.

## Engine Boundary Notes

- `postgres` failure buckets: none=35, adapter_failed=5
- `mysql` failure buckets: none=31, mismatch=8, candidate_execution_failed=1
- `spark` failure buckets: none=31, unsupported_engine=5, candidate_execution_failed=2, mismatch=2

## Pool Boundary Notes

- `PERF` failure buckets: none=47, mismatch=1
- `CONS` failure buckets: none=27
- `PORT` failure buckets: mismatch=9, none=5, adapter_failed=5, unsupported_engine=5, candidate_execution_failed=3
- `LONGTAIL` failure buckets: none=18

## Diagnostic Boundary

These findings are diagnostic/support only. They must not be claimed as primary metrics, official metrics, SER, POCR, paper evidence, retained evidence, or leaderboard input. Local checker exactness remains Result Consistency evidence only and is not formal verifier evidence.

## What Must Not Be Claimed

- Do not claim tag slices are POCR or operation-atom coverage.
- Do not claim tag slices are SER or formal semantic equivalence evidence.
- Do not claim unsupported verifier absence as method failure.
- Do not claim route comparisons as a global method ranking.
