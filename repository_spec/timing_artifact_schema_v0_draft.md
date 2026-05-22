# Timing Artifact Schema v0 Draft

Status: draft design only.

This draft specifies the intended artifact shape for a future exact-gated local timing diagnostic layer. It is not an implementation and does not authorize timing execution, speedup computation, official metrics, retained-evidence promotion, reports/results updates, paper rendering, POCR, skill folders, or leaderboard output.

## Claim Boundary

Timing artifacts produced under this draft are local diagnostics unless a separate retained-evidence promotion task authorizes otherwise.

Required boundary fields:

```yaml
claim_boundary: local_diagnostic_only
local_diagnostic_only: true
official_metric_input: false
paper_result_input: false
retained_evidence_promoted: false
leaderboard_input: false
```

## Timing Row Artifact

Recommended path:

```text
runs/user/{run_name}/timing/rows/{case_id}__{engine}__{route_id}__{candidate_id}.json
```

Required field groups:

- identity: `schema_version`, `route_id`, `method_id`, `case_id`, `pool`, `engine`, `denominator_id`, `candidate_id`, `local_run_id`, `timing_scope`, `timing_policy_id`;
- diagnostic status: generation, preflight, source execution, candidate execution, checker, exactness, failure bucket, label-only diagnostics;
- eligibility: `timing_eligible`, `timing_status`, `timing_na_reason`;
- samples: `source_runtime_samples_ms`, `candidate_runtime_samples_ms`, `source_median_ms`, `candidate_median_ms`, `speedup_ratio`;
- policy echo: warmups, repetitions, timeout, timeout status, cache policy, connection/session policy;
- provenance: environment metadata pointer, engine version, source/candidate SQL artifact paths and hashes, result/checker artifact paths, timestamp;
- claim boundary fields.

## Exact Gate

Timing eligibility requires strict exactness:

- candidate generated;
- preflight passed;
- source/reference execution succeeded;
- candidate execution succeeded;
- checker attempted and succeeded;
- `exact_status=exact`;
- no failure bucket;
- not a label-only mismatch under current strict policy;
- supported engine/role.

Rows that do not satisfy the gate remain present with `timing_eligible=false`.

## Timing Policy Artifact

Recommended path:

```text
runs/user/{run_name}/timing/timing_policy.json
```

Required fields include `timing_policy_id`, `exact_gated`, `warmup_count`, `measured_repetitions`, `timeout_seconds`, `pairing_policy`, `execution_order_policy`, `cache_policy`, `connection_session_policy`, `schema_setup_policy`, `retry_policy`, `partial_sample_policy`, `statistic`, and boundary fields.

## Environment Metadata Artifact

Recommended path:

```text
runs/user/{run_name}/timing/environment_metadata.json
```

Required fields include host/runtime metadata, engine version, engine connection mode with secrets redacted, schema setup mode, cache/session policy, relevant package versions, and boundary fields.

## Status And N.A. Policy

Supported timing statuses:

- `not_requested`
- `not_eligible`
- `timed`
- `timeout`
- `partial_failure`
- `failed_internal`
- `skipped_policy`

Speedup is `null` unless timing is complete, exact-gated, and both medians are positive.

## Future Metrics Join

Future local metrics calculators should join timing rows by `route_id`, `method_id`, `case_id`, `pool`, `engine`, `denominator_id`, `candidate_id`, `local_run_id`, and `timing_policy_id`. Route mixing is disallowed. POCR remains deferred until external operation-atom schema review.
