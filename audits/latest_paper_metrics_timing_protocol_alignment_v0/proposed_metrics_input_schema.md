# Proposed Metrics Input Schema

This schema describes future metric input rows. It is not implemented by this task.

## Row Identity

- `route_id`
- `method_id`
- `case_id`
- `pool`
- `engine`
- `denominator_id`
- `diagnostic_mode`
- `role_class`
- `record_type`

## Funnel Status

- `planned`
- `selected`
- `candidate_generated`
- `candidate_generation_status`
- `candidate_preflight_status`
- `source_execution_status`
- `candidate_execution_status`
- `checker_status`
- `consistency_status`
- `exact_status`
- `failure_bucket`
- `unsupported_status`
- `source_like_status`

## Verifier / Semantic Equivalence

- `verifier_status`
- `verifier_decidable`
- `semantic_equivalence_status`
- `semantic_equivalence_na_reason`

## Timing

- `timed_status`
- `timing_eligible`
- `source_runtime_samples`
- `candidate_runtime_samples`
- `source_median_ms`
- `candidate_median_ms`
- `speedup_ratio`
- `speedup_na_reason`
- `timing_artifact_path`

## Checker Diagnostics

- `value_exact`
- `label_exact`
- `label_only_mismatch`
- `label_policy`
- `label_mismatch_class`
- `value_mismatch_reason`

## POCR / Skill Adapter

Deferred fields:

- `operation_atom_schema_version`
- `operation_atom_artifact_path`
- `expected_operation_atom_count`
- `covered_operation_atom_count`
- `pocr_row_value`
- `pocr_validation_stage`
- `pocr_na_reason`

These must remain absent or null until external skill-adapter integration is authorized.

## Boundary Fields

- `claim_boundary`
- `local_diagnostic_only`
- `official_metric_input`
- `paper_result_input`
- `retained_evidence_input`
- `leaderboard_input`
