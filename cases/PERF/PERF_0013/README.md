# PERF_0013 Canonical Case Package

## Case Summary

PERF_0013 is a PERF / performance-sensitive analytical rewrite case derived from TPC-H Query 5. It tests predicate_pushdown, join_reorder, join_filter_isolation using static case files and retained evidence. The package is organized for correctness-gated rewrite evaluation and plan observability; this migration does not create a new speedup, timing, ranking, leaderboard, or paper-result claim.

## Case Design

`sql/source.sql` is the original analytical query. `sql/positives/pos_01.sql` makes joins explicit while preserving region and order-date filters. `sql/negatives/neg_01.sql` retains the positive rewrite shape but changes the region predicate. The hard-negative reason is static-inferred from the SQL and retained result evidence: `region_predicate_changed`. The checker should accept source/positive equivalence and reject the hard negative.

## Performance Boundary

PERF_0013 is performance-sensitive by design. No timing run was executed during migration. No speedup, latency, timing, ranking, leaderboard, or paper-result claim is created by this migration. Any performance interpretation must come only from retained denominator-aware paper evidence.

## Public Release Boundary

No DB rerun was performed during migration. No evidence was regenerated. Denominator unchanged. Paper results unchanged. Common-core membership unchanged. No global leaderboard is introduced.

## Evidence Map

The evidence map is `evidence/runs_retention.yaml`. The expected hard-negative rejection is `checker/expected_rejections.yaml`. Raw legacy runs are mapped and retained in the legacy repo; they are not deleted and were not copied wholesale into this canonical package.

## Validation Script Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner outputs must not write to case-local `runs/` by default.
