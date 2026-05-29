# Proposed Metrics Output Schema

This schema describes future non-official and official metric outputs. It is not implemented by this task.

## Route-Level Summary

Suggested columns:

- `route_id`
- `method_id`
- `scope_id`
- `metric_contract_version`
- `generation_rate`
- `execution_coverage_rate`
- `result_consistency_rate`
- `semantic_equivalence_rate`
- `gm_speedup_ratio`
- `speedup_p10`
- `speedup_p25`
- `speedup_p50`
- `speedup_p75`
- `speedup_p90`
- `positive_operation_coverage_rate`
- `cross_engine_execution_coverage_rate`
- `cross_engine_result_consistency_rate`
- `cross_engine_gm_speedup_ratio`
- `na_summary`
- `claim_boundary`

## Per-Engine Summary

Group by:

- `route_id`
- `method_id`
- `engine`
- `pool` where relevant

Include numerator/denominator counts for every reported rate.

## Per-Pool Summary

Group by:

- `route_id`
- `method_id`
- `pool`
- `engine` where relevant

Keep PORT/generalization rows separate from same-engine Track A rows.

## Per-Row Timing/Speedup CSV

Suggested columns:

- `route_id`
- `method_id`
- `case_id`
- `pool`
- `engine`
- `denominator_id`
- `source_median_ms`
- `candidate_median_ms`
- `speedup_ratio`
- `timing_status`
- `speedup_na_reason`
- `exact_status`
- `checker_status`
- `timing_artifact_path`
- `claim_boundary`

## N.A. / Unsupported Reporting

Every metric output should include explicit counts for:

- missing candidate
- preflight blocked
- source execution failed
- candidate execution failed
- checker mismatch
- checker failed
- verifier undecidable
- verifier unavailable
- timing unavailable
- timeout
- unsupported/fail-closed

## No-Global-Leaderboard Guard

Outputs may compare route slices for audit/debugging, but must not produce a global winner/ranking table. Any public comparison must be denominator-aware and role-aware.
