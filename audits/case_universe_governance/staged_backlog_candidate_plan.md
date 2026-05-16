# Staged And Backlog Candidate Plan

Date: 2026-05-17

This is a planning note only. It does not create official `case_sets/staged_v0` or `case_sets/backlog_v0` membership files.

## Candidate Classes

`staged_v0` candidates should be non-Common-core cases that are registered, have source/positive/negative/schema assets, have manageable retained-evidence mapping needs, and can follow an existing Common-core canonical pattern.

`backlog_v0` candidates should be registered cases that are not immediate staged candidates but should remain governed for future review.

`manual_review_required` cases require human review before batching because of missing skeleton assets, incomplete engine closure, or explicit registry/readiness issues.

`orphan_or_unregistered` directories require registry reconciliation before any public planning decision.

`extended_v0` is not released yet and should not be created until staged/backlog governance is approved.

## Suggested Process

1. Review `case_universe_index.csv` and `non_common_core_readiness_matrix.csv`.
2. Resolve the 7 unregistered directories.
3. Approve staged/backlog criteria.
4. Create official staged/backlog membership only in a later explicit task.
5. Plan low-risk non-Common-core migration batches after public v0 scope remains protected.

## Guardrails

- Do not change Common-core v0 membership.
- Do not change Track A denominator values.
- Do not copy raw runs/logs wholesale.
- Do not create workload-frequency or leaderboard claims.
- Do not migrate cases in the membership planning task.
