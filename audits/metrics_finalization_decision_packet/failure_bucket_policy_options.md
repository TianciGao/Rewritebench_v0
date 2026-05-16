# Failure Bucket Policy Options

This file proposes a failure taxonomy for review. It does not implement or finalize the taxonomy.

## Candidate Failure Buckets

`generation_failed`: no candidate was produced by the method.

`extraction_failed`: output existed but no usable SQL candidate could be extracted.

`parse_failed`: candidate SQL failed parser or dialect parser acceptance.

`preflight_blocked`: deterministic preflight blocked execution before DB run.

`execution_failed`: DB execution failed after reaching execution stage.

`checker_failed`: checker infrastructure failed or could not complete.

`semantic_mismatch`: candidate executed but did not match expected semantics.

`hard_negative_false_accept`: checker accepted a hard negative that should be rejected.

`unsupported`: route, engine, syntax, or feature is outside supported scope.

`timeout`: execution or validation exceeded allowed time.

`timing_missing`: execution/correctness evidence exists but usable timing evidence is absent.

`source_like_noop`: candidate is source-like or a no-op where a substantive rewrite or adaptation was expected.

`no_candidate`: no candidate artifact exists for the row.

`unknown_manual_review`: static adapter cannot classify without human review.

## Record Type Usage

`rewrite_candidate_cell`:

- generation, extraction, parse, preflight, execution, checker, semantic, unsupported, timeout, timing, source-like, no-candidate, unknown.

`control_cell`:

- checker, semantic mismatch for controls, hard-negative false accept, unsupported, unknown.

`portability_candidate_cell`:

- parse, preflight, execution, semantic mismatch, unsupported, timeout, no-candidate, unknown.

`plan_observability_artifact`:

- plan collection, missing artifact, public hygiene blocked, unknown.

`verifier_support_pair`:

- verifier unsupported, checker/support failed, unknown.

`retained_summary_artifact`:

- unknown/manual review, public hygiene blocked, duplicate/superseded.

`user_run_candidate_cell`:

- same buckets as rewrite candidates plus user submission format failures.

## Policy Questions

- Should `checker_failed` mean checker infrastructure failure only, or also checker rejection?
- Should `semantic_mismatch` be used for hard negatives, or should hard negatives use only expected-rejection statuses?
- Should `source_like_noop` be a failure bucket, a diagnostic flag, or both?
- Should `unsupported` be excluded from execution coverage or counted as non-executed?

## Recommendation

Use these buckets as diagnostic fields first. Do not let failure buckets alter planned denominators. Future reports should show row counts by route, record type, method role, and engine.
