# Row-Level Stage B Schema

Canonical artifact filename:

```text
pocr_stage_b_row_metrics.csv
```

Required row granularity:

```text
one row per route x case_id x engine planned/candidate-bound row
```

This row must exist for planned rows even when no candidate exists or annotation fails closed. A missing row is itself an artifact error.

Required core fields:

- `run_id`
- `case_set_id`
- `denominator_scope`
- `case_id`
- `pool`
- `engine`
- `method_id`
- `route_id`
- `candidate_id`
- `candidate_rel_path`
- `candidate_sha256`
- `skills_md_sha256`
- `planned_pocr_eligible`
- `candidate_bound`
- `annotation_attempted`
- `annotation_status`
- `replay_row_present`
- `route_mismatch`
- `candidate_mismatch`
- `expected_operation_atoms`
- `stage_b_supported_operation_atoms`
- `presence_only_operation_atoms`
- `insufficient_transformation_evidence_atoms`
- `rejected_noop_equivalent_atoms`
- `semantic_guard_atoms`
- `oc_i`
- `oc_i_fail_closed`
- `pocr_planned_denominator_member`
- `pocr_candidate_denominator_member`
- `pocr_curated_denominator_member`
- `curated_manifest_id`
- `fail_closed_status`
- `not_applicable_reason`
- `source_artifact_path`
- `diagnostic_only`
- `official_pocr_computed`
- `route_level_pocr_aggregated`
- `paper_metric_promoted`
- `notes`

`oc_i` is the row ratio only when the row has expected operation atoms and Stage B row evidence is valid. `oc_i_fail_closed` is the denominator-safe value used by the aggregator after fail-closed policy is applied.

Macro-average over per-row OC_i is required. Aggregators use `oc_i_fail_closed` for denominator views, not aggregate atom totals.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
