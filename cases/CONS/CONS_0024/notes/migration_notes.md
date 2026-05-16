# Migration Notes

Date: 2026-05-16
Batch id: `cons_hard_negative_approved_batch_002`

This case was migrated copy-first from the legacy repository into the canonical public-release layout. The legacy repository and raw legacy evidence were not modified.

Maintainer-approved hard-negative reason: rewrite_neg_01 changes a LEFT JOIN that preserves left-side employee rows into an INNER JOIN constrained by aggregate EXISTS/HAVING logic. This filters out employee rows that should have been preserved. Therefore neg_01 is an intentional hard negative and should be rejected by the checker.

Spark plan text was not copied raw into public retained evidence. Sanitized public copies under `evidence/retained_plans/spark/` redact local temporary paths while preserving plan structure. Original raw Spark plans remain mapped as do-not-delete legacy artifacts in `evidence/runs_retention.yaml`.

Validation scripts in `validation/` are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner output must not write to case-local `runs/` by default.

Denominator unchanged, paper results unchanged, Common-core membership unchanged, raw legacy evidence unchanged, and no global leaderboard is introduced.
