# status_inference_policy_v0 Dry-run v2 Plan

## Purpose

A possible future `normalized_status_only_metrics_dryrun_v2` could test status-only dry-run behavior using separately authorized inferred fields.

## Boundaries

- Audit-only.
- No official metrics.
- No paper table.
- No timing, latency, speedup, or performance metrics.
- No reports/results updates.
- No denominator changes.
- No parser ledger or normalization overlay mutation.

## Inputs

- Existing parser-v1 ledger.
- Existing metric-input authorization overlay.
- Existing normalized status overlay.
- A future approved inference overlay that records `inferred_generated`, `inferred_executed`, inference rule IDs, and source fields.
- Track A same-engine denominator scaffold.

## Observed And Inferred Separation

Dry-run v2 must report observed and inferred numerator counts separately. It must not overwrite observed normalized fields. It must include caveats wherever a metric uses inferred support.

## Denominator Handling

The planned denominator remains visible. Unauthorized overlap rows and unresolved rows remain in accounting and cannot be removed. Method-specific denominators must not be mixed into a global leaderboard.

## Validation Gates

- Inference overlay row count and source fields validated.
- All inferred rows have rule IDs and future authorization references.
- All unknowns remain unknown.
- Timing fields remain absent.
- Every output row is marked `audit_only=true`, `official_metric=false`, and `paper_result=false`.

## Authorization Needed Before Implementation

A maintainer must separately approve which inference rules and source-specific semantics are allowed, and whether inferred fields may be used only in dry-run or also in a later metric-input authorization review.
