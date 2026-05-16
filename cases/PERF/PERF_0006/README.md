# PERF_0006 Canonical Case Package

## Case Summary

PERF_0006 is a PERF case package derived from TPC-H Query 1. It is a performance-sensitive analytical rewrite case that tests predicate placement and filter isolation before aggregation. The package is organized for correctness-gated rewrite evaluation and plan observability; this migration does not create a new speedup claim.

## Case Design

`sql/source.sql` is the original analytical aggregation query. `sql/positives/pos_01.sql` isolates the cutoff filter in a derived relation before aggregation. `sql/negatives/neg_01.sql` changes the cutoff predicate from `<=` to `<`. The hard negative is intentional because it excludes the cutoff-date witness row. The checker should accept source/positive equivalence and reject the hard negative.

## Performance Boundary

PERF_0006 is performance-sensitive by design. No timing run was executed during migration. No speedup, latency, timing, ranking, leaderboard, or paper-result claim is created by this migration. Any performance interpretation must come only from retained denominator-aware paper evidence.

## Public Release Boundary

No DB rerun was performed during migration. No evidence was regenerated. Denominator unchanged. Paper results unchanged. Common-core membership unchanged. No global leaderboard is introduced.

## Evidence Map

The evidence map is `evidence/runs_retention.yaml`. The expected hard-negative rejection is `checker/expected_rejections.yaml`. Raw legacy runs are mapped and retained in the legacy repo; they are not deleted and were not copied wholesale into this canonical package.

## Validation Script Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runners must not write to case-local runs/ by default.
