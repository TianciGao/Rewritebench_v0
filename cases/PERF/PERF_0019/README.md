# PERF_0019 Canonical Case Package

## Case Summary

PERF_0019 is a PERF / performance-sensitive analytical rewrite case derived from TPC-H-Q13 (Customer Distribution Query). It tests materialization_strategy, predicate_pushdown using static case files and retained evidence. The package is organized for correctness-gated rewrite evaluation and plan observability; this migration does not create a new speedup, timing, ranking, leaderboard, or paper-result claim.

## Case Design

`sql/source.sql` is the original analytical query. `sql/positives/pos_01.sql` makes the derived-table aliases explicit while preserving left-join predicate placement. `sql/negatives/neg_01.sql` changes the excluded order-comment phrase from '%express%deposits%' to '%special%deposits%'. The hard-negative reason is static-inferred from the SQL and retained result evidence: `excluded_comment_phrase_changed`. The hard negative changes the excluded order-comment phrase, altering the left-join count distribution on the retained witness. The checker should accept source/positive equivalence and reject the hard negative.

## Performance Boundary

PERF_0019 is performance-sensitive by design. No timing run was executed during migration. No speedup, latency, timing, ranking, leaderboard, or paper-result claim is created by this migration. Any performance interpretation must come only from retained denominator-aware paper evidence.

## Public Release Boundary

No DB rerun was performed during migration. No evidence was regenerated. Denominator unchanged. Paper results unchanged. Common-core membership unchanged. No global leaderboard is introduced.

## Evidence Map

The evidence map is `evidence/runs_retention.yaml`. The expected hard-negative rejection is `checker/expected_rejections.yaml`. Raw legacy runs are mapped and retained in the legacy repo; they are not deleted and were not copied wholesale into this canonical package.

## Validation Script Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner outputs must not write to case-local `runs/` by default.
