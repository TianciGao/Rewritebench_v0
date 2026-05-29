# Proposed Timing Artifact Schema

This schema is a design proposal only.

## Artifact File

Suggested local artifact:

```text
runs/user/{run_name}/timing/{case_id}__{engine}__{route_id}.json
```

Official retained timing, if later authorized, should use a separate retained-evidence path and promotion gate.

## Required Fields

```yaml
schema_version: timing_artifact_v0
claim_boundary: local_diagnostic_only
route_id: string
method_id: string
case_id: string
pool: string
engine: string
denominator_id: string
diagnostic_mode: same_engine | cross_engine_target | controlled_reference
source_sql_path: string
candidate_sql_path: string
source_execution_status: string
candidate_execution_status: string
checker_status: string
exact_status: string
result_consistent: boolean
timing_status: timed | not_timed | timeout | failed | not_eligible
timing_eligible: boolean
warmup_count: integer
repetition_count: integer
source_runtime_samples_ms: list[number]
candidate_runtime_samples_ms: list[number]
source_median_ms: number | null
candidate_median_ms: number | null
speedup_ratio: number | null
speedup_na_reason: string | null
timeout_seconds: number | null
environment:
  host_fingerprint: string | null
  os: string | null
  python_version: string | null
  engine_version: string | null
  connection_mode: string | null
  schema_setup_mode: string | null
  cache_reset_policy: string | null
created_at_utc: string
official_metric_input: false
paper_result_input: false
retained_evidence_promoted: false
leaderboard_input: false
```

## Eligibility Rules

- `speedup_ratio` is present only when `result_consistent=true`, `timing_status=timed`, and both medians are positive.
- Timeouts and failures set `speedup_ratio=null` and a specific `speedup_na_reason`.
- Local diagnostic timing artifacts are not official metric inputs unless separately promoted by a retained-evidence policy task.
