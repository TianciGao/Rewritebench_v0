# Paper Table Plan

This packet proposes five paper-facing table families. These are table plans and local diagnostic evidence summaries only; they do not render paper tables or promote results.

## 1. Unified Route Evidence Ledger

Purpose: one compact denominator-aware ledger of completed Track A 120 canonical local diagnostics, PostgreSQL-only PG40 prior-method bounded evidence, and verifier/support rows.

Suggested placement: appendix first; selected Track A rows may inform main-text narrative after paper-scope review.

Source files: `unified_route_evidence_ledger.csv`, route `local_metrics_summary_review.md` files, and `evidence_location_index.csv`.

Claim boundary: local diagnostic evidence only. Track A 120 and PG40 rows must remain separated.

What not to claim: no official metrics, no global leaderboard, no direct Track A vs PG40 ranking.

## 2. Failure Frontier Summary

Purpose: summarize exact, mismatch, execution-failed, fail-closed/no-candidate, unsupported, source-like/no-op, and timing-ineligible boundaries.

Suggested placement: appendix; small excerpts may support main-text error analysis.

Source files: `failure_frontier_summary.csv`, route `frontier_review.md`, PG40 `bounded_diagnostic_summary.json`, and route boundary packets.

Claim boundary: frontier taxonomy is diagnostic/support only.

What not to claim: failure buckets are not SER, not POCR, and not hard-negative checker controls.

## 3. Failure Bucket x Taxonomy Tag Summary

Purpose: provide a compact view of retained taxonomy tags associated with failure frontiers.

Suggested placement: appendix.

Source files: `tag_failure_summary.csv`, `audits/track_a_120_tag_failure_slices_v0/`, and `audits/prior_methods_pg40_tag_failure_slices_v0/`.

Claim boundary: tag slices are diagnostic only.

What not to claim: no operation-atom coverage, no POCR, no method ranking.

## 4. Correctness-Gated Timing Slice Summary

Purpose: summarize GM speedup and percentiles over exact + timed rows only.

Suggested placement: appendix or main text if the paper explicitly labels local diagnostic timing.

Source files: `timing_slice_summary.csv` and route `local_metrics_summary_review.md` files.

Claim boundary: timing applies only to strict exact/result-consistent timed rows.

What not to claim: missing timing is not zero; speedup is not global route quality; do not rank PG40 against Track A 120.

## 5. Evidence Location / Artifact Index

Purpose: provide a paper-writing artifact map for reviewers and maintainers.

Suggested placement: appendix or reproducibility supplement.

Source files: `evidence_location_index.csv`.

Claim boundary: index only; no new evidence or metrics.

What not to claim: the index does not promote retained evidence or official paper results.
