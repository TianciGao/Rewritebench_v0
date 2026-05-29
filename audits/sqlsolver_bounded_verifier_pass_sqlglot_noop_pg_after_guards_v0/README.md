# SQLSolver Bounded Verifier Pass After Guards

This packet reruns the same 8 selected SQLGlot no-op PostgreSQL benchmark pairs from `audits/sqlsolver_bounded_verifier_pass_sqlglot_noop_pg_v0/selected_pairs.csv` after SQLSolver canonicalization and support-scope guards.

## Scope

- Route: `sqlglot_noop`
- Run id: `sqlglot_noop_track_a_120_canonical_v0`
- Engine: `postgres`
- Selected pairs: `8`
- SQLSolver mode: external JAR, redacted in command logs
- Official SER: `false`
- SER status: `coverage_limited`

## Summary

- Identity guard passed pairs: `2`
- Identity guard no-verifier-support pairs: `3`
- Unclassified identity UNKNOWN pairs: `3`
- Actual source-candidate checks attempted: `2`
- Actual equivalent: `2`
- Actual non-equivalent: `0`
- Actual no-verifier-support: `3`
- Ready for SQLGlot no-op PostgreSQL 35 exact subset: `false`

## Pair Outcomes

- `CONS_0005`: source identity `unknown`, candidate identity `unknown`, actual `identity_guard_failed`
- `CONS_0007`: source identity `equivalent`, candidate identity `equivalent`, actual `equivalent`
- `LONGTAIL_0011`: source identity `no_verifier_support`, candidate identity `no_verifier_support`, actual `no_verifier_support`
- `LONGTAIL_0012`: source identity `unknown`, candidate identity `unknown`, actual `identity_guard_failed`
- `PERF_0006`: source identity `equivalent`, candidate identity `equivalent`, actual `equivalent`
- `PERF_0007`: source identity `equivalent`, candidate identity `unknown`, actual `identity_guard_failed`
- `PORT_0003`: source identity `no_verifier_support`, candidate identity `no_verifier_support`, actual `no_verifier_support`
- `PORT_0005`: source identity `no_verifier_support`, candidate identity `no_verifier_support`, actual `no_verifier_support`

## Boundary

This is bounded verifier-support evidence only. It does not compute or promote official Semantic Equivalence Rate, update paper results, update retained evidence, recompute local metrics, or authorize Repair-1.
