# LONGTAIL_0011 Migration Notes

Date: 2026-05-16

This is a copy-first canonical-layout full case migration pilot for `LONGTAIL_0011` only. Legacy source files remain unchanged.

## Public Boundary

No DB engines were run during migration. No validation scripts were executed. No evidence was regenerated. Denominator unchanged. Paper results unchanged. Common-core membership unchanged. No global leaderboard is introduced.

## Long-Tail Boundary

LONGTAIL_0011 is packaged as a controlled structural robustness case. It records CTE pipeline, window ranking, joins, aggregate/order logic, and tie-sensitive ranking behavior. It does not create workload-frequency or production-frequency evidence.

## Hard Negative Approval

The maintainer-approved hard-negative reason is `tie_sensitive_ranking_semantics_not_preserved`. `sql/negatives/neg_01.sql` replaces `DENSE_RANK()` with `ROW_NUMBER()`. `DENSE_RANK()` preserves tied rows at the same rank, while `ROW_NUMBER()` assigns a unique order and can collapse tied worst-score rows. Therefore `neg_01` is an intentional hard negative and should be rejected by the checker.

## Spark Plan Handling

Raw Spark plan text from legacy runs contains local temporary path traces. Raw Spark plan text was not copied into public retained evidence. Sanitized public copies are stored under `evidence/retained_plans/spark/`, and original raw paths are mapped in `evidence/runs_retention.yaml` as do-not-delete originals.

## Validation Script Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runners must not write to case-local runs/ by default.
