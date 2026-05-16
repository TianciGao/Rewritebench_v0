# PERF_0017 Canonical Case Package

## Case Summary

PERF_0017 is a PERF / performance-sensitive analytical rewrite case derived from TPC-H-Q10 (Returned Item Reporting Query). It tests predicate_pushdown, join_reorder using static case files and retained evidence. The package is organized for correctness-gated rewrite evaluation and plan observability; this migration does not create a new speedup, timing, ranking, leaderboard, or paper-result claim.

## Case Design

`sql/source.sql` is the original analytical query. `sql/positives/pos_01.sql` makes joins explicit while preserving the date window and returned-item filter before aggregation. `sql/negatives/neg_01.sql` changes the return-flag predicate from 'R' to 'A'. The hard-negative reason is static-inferred from the SQL and retained result evidence: `return_flag_predicate_changed`. The hard negative changes the returned-item filter from `l_returnflag = 'R'` to `l_returnflag = 'A'`, changing the aggregation input and retained output row. The checker should accept source/positive equivalence and reject the hard negative.

## Performance Boundary

PERF_0017 is performance-sensitive by design. No timing run was executed during migration. No speedup, latency, timing, ranking, leaderboard, or paper-result claim is created by this migration. Any performance interpretation must come only from retained denominator-aware paper evidence.

## Public Release Boundary

No DB rerun was performed during migration. No evidence was regenerated. Denominator unchanged. Paper results unchanged. Common-core membership unchanged. No global leaderboard is introduced.

## Evidence Map

The evidence map is `evidence/runs_retention.yaml`. The expected hard-negative rejection is `checker/expected_rejections.yaml`. Raw legacy runs are mapped and retained in the legacy repo; they are not deleted and were not copied wholesale into this canonical package.

## Validation Script Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner outputs must not write to case-local `runs/` by default.
