# LONGTAIL_0024

## Case Summary

LONGTAIL_0024 is a LONGTAIL structural robustness case. Manual Stack-substrate query with PostHistory revision aggregation, temporal min/max fields, post join, and sorted output. It is packaged for correctness-gated rewrite evaluation, hard-negative checking, and plan observability.

Canonical package status: canonical public-release case package.

This case contributes structural robustness evidence only. It must not be described as workload-frequency or production-frequency evidence, and this migration creates no new benchmark result.

## Case Design

- Source query: `sql/source.sql`.
- Positive rewrite: `sql/positives/pos_01.sql`. The positive rewrite preserves one aggregate row per post by moving revision statistics into an inline derived table.
- Hard negative: `sql/negatives/neg_01.sql`. The hard negative groups PostHistory revision aggregation by editor as well as post, fragmenting per-post revision history.

The maintainer-approved expected rejection reason for `neg_01` is `posthistory_revision_aggregation_fragmented_by_editor`. The hard negative is a checker control, not a method-generated failure.

## LONGTAIL Structure Boundary

The case remains part of the frozen Common-core LONGTAIL six-case set. Its interpretation is structural robustness for per-post temporal revision aggregation; workload_frequency_claim_created is false and production_frequency_claim_created is false.

## Public Release Boundary

No database run was performed during migration. No evidence was regenerated. The denominator is unchanged, paper results are unchanged, Common-core membership is unchanged, case_sets are unchanged, reports are unchanged, results are unchanged, and raw legacy evidence is unchanged. No global leaderboard is established by this package.

## Evidence Map

- Retention policy and legacy artifact map: `evidence/runs_retention.yaml`.
- Expected hard-negative rejection: `checker/expected_rejections.yaml`.
- Retained source and positive outputs: `evidence/retained_controls/`.
- Retained hard-negative outputs: `evidence/hard_negative/`.
- Retained plan evidence: `evidence/retained_plans/`, with Spark plan text published only as sanitized copies.

Raw legacy runs are mapped and retained in the legacy source repository. They were not deleted, rewritten, or copied wholesale into this public package.

## Validation Script Caveat

The copied validation scripts are retained legacy validation assets. They are not final public user runners and were not executed during migration. Future public runners should write outputs outside case-local `runs/` by default.
