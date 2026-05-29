# Future Metrics Join Plan

The timing artifact schema is designed to feed a later non-official local metrics calculator without changing current benchmark results.

## Join Keys

Future joins should use:

- `route_id`
- `method_id`
- `case_id`
- `pool`
- `engine`
- `denominator_id`
- `candidate_id`
- `local_run_id`
- `timing_policy_id`

Summaries must never merge `sqlglot_noop`, `sqlglot_optimize`, controlled target-reference adapters, and future real user-adapter routes into one score.

## Coverage And Correctness Inputs

The metrics input surface should join candidate generation, preflight, execution, checker, and label-only diagnostics:

- `candidate_generated`
- `candidate_preflight_status`
- `source_execution_status`
- `candidate_execution_status`
- `checker_status`
- `exact_status`
- `failure_bucket`
- `value_exact`
- `label_exact`
- `label_only_mismatch`

## Performance Inputs

Performance joins use timing fields only for exact and fully timed rows:

- `timing_eligible`
- `timing_status`
- `source_runtime_samples_ms`
- `candidate_runtime_samples_ms`
- `source_median_ms`
- `candidate_median_ms`
- `speedup_ratio`
- `timing_na_reason`

`M_r` and `M_tgt_r` are subsets of exact rows with complete paired timing, not replacements for `N_S` or `N_PORT`.

## Output Shapes

Future non-official local metrics outputs can include:

- route-level coverage/correctness/performance/generalization summary;
- per-engine summary;
- per-pool summary;
- per-row timing/speedup CSV;
- N.A. and unsupported reporting;
- timing policy and environment metadata references.

## No Global Leaderboard Guard

All summaries must retain claim-boundary fields:

- `local_diagnostic_only`
- `official_metric_input`
- `paper_result_input`
- `retained_evidence_input`
- `leaderboard_input`

No global leaderboard-ready aggregate is authorized by this design.

## POCR Boundary

Positive Operation Coverage Rate remains deferred. Timing artifacts should not include operation atoms, skill definitions, or inferred POCR fields until the external skill-adapter schema is stable and separately authorized.
