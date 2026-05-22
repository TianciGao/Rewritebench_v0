# Timing Artifact Examples

Example row fields produced by the bounded timing smoke:

```json
{
  "schema_version": "timing_artifact_schema_v0",
  "route_id": "sqlglot_noop",
  "method_id": "sqlglot",
  "case_id": "PERF_0006",
  "engine": "postgres",
  "timing_policy_id": "local_exact_gated_default_v0",
  "exact_status": "exact",
  "failure_bucket": "none",
  "timing_eligible": true,
  "timing_status": "timed",
  "source_runtime_samples_ms": ["five inline numeric samples"],
  "candidate_runtime_samples_ms": ["five inline numeric samples"],
  "source_median_ms": "numeric",
  "candidate_median_ms": "numeric",
  "speedup_ratio": "numeric local diagnostic value",
  "source_sql_hash": "sha256",
  "candidate_sql_hash": "sha256",
  "claim_boundary": "local_diagnostic_only",
  "official_metric_input": false,
  "paper_result_input": false,
  "retained_evidence_promoted": false,
  "leaderboard_input": false
}
```

The actual timing artifacts are local run outputs under `runs/user/` and are not committed.

## N.A. Row Shape

Non-exact or unsupported rows would retain a timing row with:

```json
{
  "timing_eligible": false,
  "timing_status": "not_eligible",
  "timing_na_reason": "checker_mismatch",
  "speedup_ratio": null
}
```

Label-only mismatches remain `not_eligible` under the current strict-label checker policy.
