# LONGTAIL_0013

## Case Summary

LONGTAIL_0013 is a LONGTAIL structural robustness case. SQLStorm Stack Overflow query with CTEs, window ranking, outer joins, user statistics, and ordered aggregate output. It is packaged for correctness-gated rewrite evaluation, hard-negative checking, and plan observability.

Canonical package status: canonical public-release case package.

This case contributes structural robustness evidence only. It must not be described as workload-frequency or production-frequency evidence, and this migration creates no new benchmark result.

## Case Design

- Source query: `sql/source.sql`.
- Positive rewrite: `sql/positives/pos_01.sql`. The positive rewrite isolates the best-question attachment in a derived table while preserving users through a left join.
- Hard negative: `sql/negatives/neg_01.sql`. The hard negative changes the best-question attachment from a left join into an inner join, dropping users without a qualifying ranked question row.

The maintainer-approved expected rejection reason for `neg_01` is `best_question_attachment_left_join_changed_to_inner_join`. The hard negative is a checker control, not a method-generated failure.

## LONGTAIL Structure Boundary

The case remains part of the frozen Common-core LONGTAIL six-case set. Its interpretation is structural robustness for best-question window attachment with null-preserving outer joins; workload_frequency_claim_created is false and production_frequency_claim_created is false.

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
