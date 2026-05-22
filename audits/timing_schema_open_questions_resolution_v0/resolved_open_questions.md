# Resolved Open Questions

This file resolves the open questions raised by `timing_artifact_schema_design_v0`.

## 1. Local Timing Before Official Promotion

Resolution: allowed for local diagnostics only.

Local timing diagnostics may run before official retained-evidence promotion only when every timing artifact records:

- `claim_boundary=local_diagnostic_only`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

Local timing artifacts remain under `runs/user/` and must not update reports/results or paper tables.

## 2. Timing Sample Storage

Resolution: inline sample arrays in timing row JSON for v0.

Required v0 fields:

- `source_runtime_samples_ms`
- `candidate_runtime_samples_ms`

Future large-scale runs may split samples into referenced files, but v0 should keep the artifact simple and self-contained.

## 3. SQL Hashes

Resolution: required.

Timing artifacts must store:

- `source_sql_hash`
- `candidate_sql_hash`

Optional fields may include schema/data hash pointers if available. Hashing is for traceability and provenance; it is not a semantic comparison rule.

## 4. Source Timing Reuse

Resolution: no cross-route source timing reuse in v0.

Source and candidate timing must be paired within the same route, run, timing policy, engine, environment, and context. A future optimization may introduce `source_timing_reuse_id`, but only after a separate policy task.

## 5. Default Local Timing Policy

Resolution:

- `warmup_count=1`
- `measured_repetitions=5`
- `timeout_seconds=30`
- `statistic=median`
- source/candidate measured in the same engine/environment/run context
- `execution_order_policy` recorded explicitly
- cache/session/schema setup policy recorded explicitly

This follows the current paper experimental setup direction while remaining local-only until promotion.

## 6. Cache And Session Policy

Resolution: record policy as metadata.

The v0 local diagnostic must not claim hardware-comparable or production-stable performance. It must record:

- whether connection/session is reused;
- whether schema is rebuilt per row or per run;
- cache policy and reset assumptions.

The artifact should not pretend cache control is complete.

## 7. Partial Timing Failure

Resolution:

- `timing_status=partial_failure`
- `timing_eligible` may remain true only as pre-timing eligibility
- timed denominator membership requires complete valid source and candidate sample arrays
- `speedup_ratio=null` unless both medians are positive and `timing_status=timed`
- partial failures stay visible with `timing_na_reason`

## 8. Label-Only Mismatch

Resolution: timing-ineligible under current strict policy.

Under the current strict-label checker policy, label-only mismatch remains `exact_status=mismatch`. Therefore label-only mismatch rows are timing-ineligible. Any exactness-changing label policy requires separate authorization.

## 9. Target-Engine Timing

Resolution: target-engine paired timing required.

Cross-Engine GM Speedup Ratio requires target-engine paired source/reference timing and candidate timing in the same target-engine run context. Track A same-engine source timing must not be reused as Track C target-engine timing. For PORT/cross-engine rows, the target-engine source/reference SQL role must be manifest-declared.

## 10. Promotion Gate

Resolution: separate promotion task required.

Local timing artifacts under `runs/user/` are not official metrics. Promotion to retained evidence requires a separate retained-evidence/official timing promotion task that validates:

- route identity;
- denominator identity;
- environment metadata;
- timing policy;
- exact gate;
- artifact paths;
- source/candidate SQL hashes;
- claim-boundary fields.

## 11. Route-Mixing Prevention

Resolution: route-aware grouping required.

Future summaries must group by:

- `route_id`
- `method_id`
- `engine`
- `denominator_id`
- `timing_policy_id`
- `local_run_id`
- `candidate_id`

Combined route aggregates are disallowed unless explicitly marked as diagnostic and non-leaderboard. No global leaderboard output is allowed.

## 12. POCR

Resolution: deferred.

Phase 2 must not implement POCR, create skill folders, infer operation atoms, or add operation-atom artifacts. POCR remains pending external skill-adapter schema review.
