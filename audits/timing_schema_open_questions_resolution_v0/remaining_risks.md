# Remaining Risks

## Local Timing Comparability

Local timing diagnostics can validate plumbing and artifact shape, but they should not be interpreted as hardware-comparable or production-stable performance evidence. Cache, session, and schema setup policies are recorded as metadata, not fully controlled guarantees.

## Execution Order Bias

The default requires recording `execution_order_policy`, but this task does not decide whether Phase 2 should use source-then-candidate, candidate-then-source, or alternating order. That choice should be explicit in the Phase 2 policy artifact.

## Source Timing Repetition Cost

No cross-route source timing reuse is allowed in v0. This is simpler and safer, but it may increase local runtime. A future `source_timing_reuse_id` policy can be considered separately.

## Partial Sample Interpretation

Partial timing samples remain visible but do not produce speedup. This avoids misleading performance values, but future implementation must make partial failures easy to diagnose.

## Target-Engine Role Availability

Cross-engine timing depends on manifest-declared target-engine source/reference roles. Rows without safe target-engine roles remain unsupported/fail-closed for timing.

## Official Promotion

Local timing artifacts are not official evidence. A future promotion gate must be strict enough to validate environment metadata, timing policy, exact gate, route identity, denominator identity, artifacts, and hashes.

## POCR Deferral

POCR remains deferred. Metrics implementation must not accidentally create operation-atom or skill-folder scaffolding while adding timing support.
