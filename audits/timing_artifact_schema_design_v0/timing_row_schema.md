# Timing Row Schema

This schema is a design proposal for future local timing diagnostics. It is not implemented by this task.

## Artifact Grain

One timing row represents one route/method/case/engine/candidate timing eligibility record. Exact rows may also include source/candidate timing samples. Non-exact, unsupported, or failed rows remain present with `timing_eligible=false`.

Suggested local path:

```text
runs/user/{run_name}/timing/rows/{case_id}__{engine}__{route_id}__{candidate_id}.json
```

## Required Identity Fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `schema_version` | string | yes | Suggested value: `timing_artifact_schema_v0`. |
| `route_id` | string | yes | User-entry route, for example `sqlglot_noop`. |
| `method_id` | string | yes | Method family, independent from route variant. |
| `case_id` | string | yes | Case identifier. |
| `pool` | string | yes | `PERF`, `CONS`, `PORT`, or `LONGTAIL`. |
| `engine` | string | yes | Engine where timing is measured. |
| `denominator_id` | string | yes | Denominator surface, for example `common_core_v0:spark`. |
| `candidate_id` | string | yes | Candidate artifact identity within the local run. |
| `local_run_id` | string | yes | Stable local run identifier. |
| `timing_scope` | string | yes | `same_engine`, `cross_engine_target`, or `controlled_reference`. |
| `timing_policy_id` | string | yes | References the timing policy artifact. |

## Diagnostic And Execution Fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `diagnostic_mode` | string | yes | Resolved mode from runner/manifest, not inferred from filenames. |
| `role_class` | string | yes | Same-engine, target-candidate, source-reference, unsupported, or equivalent resolved class. |
| `candidate_generated` | boolean | yes | Raw adapter candidate artifact was generated. |
| `candidate_preflight_status` | string | yes | Preserve preflight separate from generation. |
| `source_execution_status` | string | yes | Source/reference execution status. |
| `candidate_execution_status` | string | yes | Candidate execution status. |
| `checker_status` | string | yes | Checker attempted/succeeded/mismatch/failure status. |
| `exact_status` | string | yes | Current strict exact/mismatch status. |
| `failure_bucket` | string | yes | Existing local diagnostic failure bucket. |
| `value_exact` | boolean/null | yes | From label diagnostics when available. |
| `label_exact` | boolean/null | yes | From label diagnostics when available. |
| `label_only_mismatch` | boolean | yes | Strict mismatch remains timing-ineligible unless separately authorized. |

## Timing Fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `timing_eligible` | boolean | yes | True only after exact-gating passes. |
| `timing_status` | string | yes | See `timing_status_and_na_policy.md`. |
| `timing_na_reason` | string/null | yes | Required when timing is ineligible, skipped, failed, partial, or timed out. |
| `source_runtime_samples_ms` | array[number] | yes | Empty for ineligible or untimed rows. |
| `candidate_runtime_samples_ms` | array[number] | yes | Empty for ineligible or untimed rows. |
| `source_median_ms` | number/null | yes | Median from retained source samples. |
| `candidate_median_ms` | number/null | yes | Median from retained candidate samples. |
| `speedup_ratio` | number/null | yes | `source_median_ms / candidate_median_ms` only when eligible and fully timed. |
| `speedup_na_reason` | string/null | yes | Required when `speedup_ratio` is null. |
| `warmup_count` | integer | yes | From referenced timing policy. |
| `measured_repetitions` | integer | yes | Successful measured repetitions per side. |
| `requested_repetitions` | integer | yes | Requested measured repetitions per side. |
| `timeout_seconds` | number | yes | Per-query or per-pair timeout from policy. |
| `timeout_status` | string | yes | `none`, `source_timeout`, `candidate_timeout`, `both_timeout`, or `partial_timeout`. |
| `cache_policy` | string | yes | From policy, for example `session_reuse_recorded`. |
| `connection_session_policy` | string | yes | Connection/session handling for source/candidate pair. |

## Environment And Artifact Fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `engine_version` | string/null | yes | Resolved engine version if available. |
| `environment_metadata_path` | string | yes | Relative path to environment metadata artifact. |
| `source_sql_artifact_path` | string/null | yes | Local run artifact path. |
| `candidate_sql_artifact_path` | string/null | yes | Local run artifact path. |
| `source_result_artifact_path` | string/null | yes | Existing local diagnostic result artifact. |
| `candidate_result_artifact_path` | string/null | yes | Existing local diagnostic result artifact. |
| `checker_artifact_path` | string/null | yes | Checker details or mismatch artifact. |
| `timing_log_artifact_path` | string/null | yes | Optional detailed timing trace path. |
| `source_sql_sha256` | string/null | yes | Recommended for future reproducibility. |
| `candidate_sql_sha256` | string/null | yes | Recommended for future reproducibility. |
| `created_at_utc` | string | yes | ISO-8601 timestamp. |

## Claim Boundary Fields

| Field | Type | Required | Required Value For This Phase |
| --- | --- | --- | --- |
| `claim_boundary` | string | yes | `local_diagnostic_only`. |
| `local_diagnostic_only` | boolean | yes | `true`. |
| `official_metric_input` | boolean | yes | `false`. |
| `paper_result_input` | boolean | yes | `false`. |
| `retained_evidence_promoted` | boolean | yes | `false`. |
| `leaderboard_input` | boolean | yes | `false`. |

## Example Skeleton

```json
{
  "schema_version": "timing_artifact_schema_v0",
  "route_id": "sqlglot_noop",
  "method_id": "sqlglot",
  "case_id": "PERF_0006",
  "pool": "PERF",
  "engine": "postgres",
  "denominator_id": "common_core_v0:postgres",
  "candidate_id": "candidate_0001",
  "local_run_id": "runs/user/example",
  "timing_scope": "same_engine",
  "timing_policy_id": "local_exact_gated_default_v0",
  "exact_status": "exact",
  "failure_bucket": "none",
  "timing_eligible": true,
  "timing_status": "timed",
  "source_runtime_samples_ms": [12.4, 12.1, 12.3, 12.2, 12.5],
  "candidate_runtime_samples_ms": [10.1, 10.0, 10.4, 10.2, 10.1],
  "source_median_ms": 12.3,
  "candidate_median_ms": 10.1,
  "speedup_ratio": 1.2178217821782178,
  "claim_boundary": "local_diagnostic_only",
  "official_metric_input": false,
  "paper_result_input": false,
  "retained_evidence_promoted": false,
  "leaderboard_input": false
}
```
