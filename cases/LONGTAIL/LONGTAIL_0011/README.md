# LONGTAIL_0011 Canonical Case Package

## Case Summary

LONGTAIL_0011 is a LONGTAIL case package for realistic-structure SQL. It tests structurally complex SQL rather than workload frequency. The source query includes a CTE pipeline, window ranking, joins, aggregate/order logic, and tie-sensitive ranking behavior. The package is organized for correctness, hard-negative checking, and plan/failure observability. This migration does not create workload-frequency, production-frequency, timing, speedup, ranking, leaderboard, or paper-result claims.

## Case Design

`sql/source.sql` is the original long-tail query. `sql/positives/pos_01.sql` is the trusted positive rewrite/adaptation. `sql/negatives/neg_01.sql` is an intentional hard negative.

`neg_01.sql` replaces `DENSE_RANK()` with `ROW_NUMBER()`. This breaks tie-sensitive ranking semantics because tied rows no longer share the same rank. `DENSE_RANK()` preserves tied rows at the same rank, while `ROW_NUMBER()` assigns a unique order and can collapse tied worst-score rows. Therefore `neg_01` should be rejected by the checker.

## Long-Tail Boundary

LONGTAIL_0011 is a controlled structural robustness case. It should not be interpreted as production workload frequency evidence, and it does not claim that this structure is common in real workloads.

## Public Release Boundary

No DB rerun was performed during migration. No evidence was regenerated. Denominator unchanged. Paper results unchanged. Common-core membership unchanged. No global leaderboard is introduced.

## Evidence Map

The evidence map is `evidence/runs_retention.yaml`. The expected hard-negative rejection is recorded in `checker/expected_rejections.yaml`. Raw legacy runs are mapped and retained in the legacy repo; they are not deleted and were not copied wholesale into this canonical package.

## Validation Script Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runners must not write to case-local runs/ by default.
