# Exact Gating And Denominator Policy

Timing eligibility is exact-gated. Performance rows for `M_r` or `M_tgt_r` must be a subset of result-consistent rows with complete retained paired timing.

## Eligibility Predicate

A row is `timing_eligible=true` only when all of the following are true:

- the row is selected or planned within an authorized local timing diagnostic surface;
- candidate SQL is generated;
- candidate preflight passes;
- source/reference execution succeeds;
- candidate execution succeeds;
- checker is attempted and succeeds;
- strict `exact_status=exact`;
- `failure_bucket=none`;
- `label_only_mismatch=false`;
- the engine/role is supported and not fail-closed;
- the local timing policy allows timing for the row's `timing_scope`.

Any failed condition keeps the row visible with `timing_eligible=false` and a specific `timing_na_reason`.

## Denominator Chain Preservation

Future timing summaries must preserve the chain:

```text
planned/selected -> generated -> preflight_passed -> source_executable -> candidate_executable -> checker_attempted -> exact -> timing_eligible -> timed
```

Timing summaries must not silently replace the planned or selected denominator with only timed rows.

## Latest-Paper Denominator Links

The timing schema should support later joins to:

- `N_S`: planned source-case denominator for the route/surface;
- `G_r`: generated candidates;
- `E_r`: executable candidates, pending human confirmation of exact numerator semantics;
- `X_r`: result-consistent rows;
- `M_r`: exact and fully timed rows for same-engine performance;
- `N_PORT`: planned PORT target-engine denominator;
- `E_tgt_r`: executable target-engine candidates;
- `X_tgt_r`: result-consistent target-engine rows;
- `M_tgt_r`: exact and fully timed target-engine rows.

POCR denominator `C_r` is intentionally deferred until external operation-atom schema review.

## Cross-Engine Target Timing

For Cross-Engine GM Speedup Ratio, timing must be collected in the target engine context. Source/reference timing and target-candidate timing must be paired in the same target engine/environment/run context, or the row must be `timing_status=not_eligible` or `skipped_policy` with a clear reason.

## No Denominator Change

This design does not change any benchmark denominator, Common-core membership, PORT membership, paper result, reports/results table, or retained evidence surface.
