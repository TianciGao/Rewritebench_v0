# Approved Timing Defaults

These defaults are approved for the next exact-gated local timing diagnostic implementation task, if separately authorized.

## Boundary Defaults

```yaml
claim_boundary: local_diagnostic_only
local_diagnostic_only: true
official_metric_input: false
paper_result_input: false
retained_evidence_promoted: false
leaderboard_input: false
```

## Timing Policy Defaults

```yaml
timing_policy_id: local_exact_gated_default_v0
exact_gated: true
warmup_count: 1
measured_repetitions: 5
timeout_seconds: 30
statistic: median
sample_storage: inline_json_arrays
speedup_formula: source_median_ms / candidate_median_ms
source_timing_reuse: none_cross_route_v0
```

## Required Policy Metadata

Phase 2 must record these fields explicitly:

- `execution_order_policy`
- `cache_policy`
- `connection_session_policy`
- `schema_setup_policy`
- `transaction_policy` where applicable
- `retry_policy`
- `partial_sample_policy`
- `environment_metadata_path`

## Required Timing Row Fields

The timing row schema should include:

- `source_runtime_samples_ms`
- `candidate_runtime_samples_ms`
- `source_median_ms`
- `candidate_median_ms`
- `speedup_ratio`
- `timing_eligible`
- `timing_status`
- `timing_na_reason`
- `source_sql_hash`
- `candidate_sql_hash`
- optional `schema_hash_ref`
- optional `data_hash_ref`

## Timing Eligibility Defaults

Timing eligibility requires:

- candidate generated;
- preflight passed;
- source/reference execution succeeded;
- candidate execution succeeded;
- checker attempted;
- strict `exact_status=exact`;
- `failure_bucket=none`;
- `label_only_mismatch=false`;
- supported engine and role;
- timing policy allows the row's timing scope.

## Target-Engine Defaults

For cross-engine timing:

- source/reference timing must be measured in the target engine;
- candidate timing must be measured in the same target engine;
- both measurements must occur in the same local run and timing policy context;
- manifest-declared roles are required;
- Track A same-engine timing must not be reused as target-engine timing.

## Not Approved In V0

- Cross-route source timing reuse.
- External sample-array files.
- Partial-sample speedup.
- Timing label-only mismatches.
- Official metric computation.
- Reports/results updates.
- Retained-evidence promotion.
- POCR or skill-folder work.
