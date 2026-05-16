# PERF_0024 Canonical Case Package

## Case Summary

PERF_0024 is a PERF / performance-sensitive analytical rewrite case derived from TPC-H-Q20 (Potential Part Promotion Query). It tests subquery_decorrelation, predicate_pushdown using static case files and retained evidence. The package is organized for correctness-gated rewrite evaluation and plan observability; this migration does not create a new speedup, timing, ranking, leaderboard, or paper-result claim.

## Case Design

`sql/source.sql` is the original analytical query. `sql/positives/pos_01.sql` uses explicit joins and EXISTS while preserving supplier, part, nation, and quantity filters. `sql/negatives/neg_01.sql` changes the part-name prefix from 'pale%' to 'blue%'. The hard-negative reason is static-inferred from the SQL and retained result evidence: `part_name_prefix_predicate_changed`. The hard negative changes the part-name prefix from `pale%` to `blue%`, changing the nested part/supplier filter and eliminating the retained supplier row. The checker should accept source/positive equivalence and reject the hard negative.

## Performance Boundary

PERF_0024 is performance-sensitive by design. No timing run was executed during migration. No speedup, latency, timing, ranking, leaderboard, or paper-result claim is created by this migration. Any performance interpretation must come only from retained denominator-aware paper evidence.

## Public Release Boundary

No DB rerun was performed during migration. No evidence was regenerated. Denominator unchanged. Paper results unchanged. Common-core membership unchanged. No global leaderboard is introduced.

## Evidence Map

The evidence map is `evidence/runs_retention.yaml`. The expected hard-negative rejection is `checker/expected_rejections.yaml`. Raw legacy runs are mapped and retained in the legacy repo; they are not deleted and were not copied wholesale into this canonical package.

## Validation Script Caveat

The scripts in `validation/` are retained legacy validation assets. They were not executed during migration and are not final public user runners. Future public runner outputs must not write to case-local `runs/` by default.
