# Route Assembly Policy

## Route identity

`direct_llm_repair_1` is a separate route from `direct_llm_original`.

It must report:

- `route_id=direct_llm_repair_1`
- `method_id=direct_llm_repair_1`
- `original_route_id=direct_llm_original`
- `original_method_id=direct_llm_original`

Its metrics must not be merged into, backfilled into, or described as Direct LLM original metrics.

## Planned denominator

The route uses the same Track A same-engine denominator as Direct LLM original:

- Common-core v0
- 40 cases
- engines: `postgres`, `mysql`, `spark`
- planned rows: 120

Unsupported rows remain in the selected/planned denominator.

## Final candidate selection

For each planned row, the final Repair-1 route candidate is assembled from the original Direct LLM canonical output and, where eligible, one Repair-1 attempt.

Original exact rows:

- Do not call Repair-1.
- Use the original Direct LLM candidate SQL as the final candidate for the Repair-1 route.
- Record `final_candidate_source=original`.
- Re-run the final candidate through the Repair-1 route's own DB/checker/timing path during the future 120 diagnostic; do not import Direct LLM original exactness as a Repair-1 metric.

Original mismatch rows:

- Attempt exactly one Repair-1 call using `checker_mismatch_feedback`.
- If a repaired candidate is generated and extracts to exactly one SQL statement, use it as the final candidate.
- Record `final_candidate_source=repaired`.
- If the repaired candidate is missing, prose-only, ambiguous, or multiple statements, fail closed with no final candidate.
- If the repaired candidate executes but remains result-inconsistent, final bucket is `mismatch`.
- If the repaired candidate is exact and timed, it is eligible for exact-gated speedup.

Original candidate-execution-failed rows:

- Attempt exactly one Repair-1 call using `candidate_execution_error_feedback`.
- If a repaired candidate is generated and extracts to exactly one SQL statement, use it as the final candidate.
- Record `final_candidate_source=repaired`.
- If execution still fails, final bucket is `candidate_execution_failed`.
- If execution succeeds but checker result differs, final bucket is `mismatch`.
- If exact and timed, it is eligible for exact-gated speedup.

Original unsupported-engine rows:

- Do not attempt Repair-1.
- Preserve `unsupported_engine` as a boundary bucket.
- Record `final_candidate_source=none`.
- Keep the row visible in the selected/planned denominator.

Original no-candidate or extraction-failure rows, if such rows appear in a future source run:

- Fail closed unless both explicit original-candidate context and explicit execution/checker feedback exist.
- If no original candidate is available, Repair-1 cannot construct a supported repair prompt.
- If feedback is missing or unsupported, no Repair-1 call is allowed.

Provider or preflight failures:

- Do not silently fall back to original non-exact candidates.
- Record the fail-closed bucket and keep the row in the denominator.

## Final status semantics

`final_candidate_generated` means a final SQL candidate exists for the Repair-1 route, regardless of whether it came from the original exact candidate or a repaired candidate.

`repair_attempted` must remain separate from `final_candidate_generated`:

- original exact rows: `repair_attempted=false`, `final_candidate_generated=true`
- repaired rows with extracted SQL: `repair_attempted=true`, `final_candidate_generated=true`
- unsupported rows: `repair_attempted=false`, `final_candidate_generated=false`
- failed repair extraction/provider/preflight rows: `repair_attempted` depends on failure point, `final_candidate_generated=false`

Failure buckets describe final route behavior, not original Direct LLM behavior, while original buckets must remain recorded as provenance.
