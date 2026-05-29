# Validation Notes

Generation checks completed:

- Source audit artifact existence checks: passed.
- Same-8 after-guards summary loaded from existing JSON: passed.
- Same-8 row reconciliation basis: selected=8, identity_passed=2, no_verifier_support=3, unclassified identity blockers=3, actual equivalent=2, ready_for_sqlglot_noop_pg_35=false.
- Residual blockers represented: CONS_0005, LONGTAIL_0012, PERF_0007.
- No-verifier-support rows represented: LONGTAIL_0011, PORT_0003, PORT_0005.
- No SQLSolver, VeriEQL, adapter, DB/checker/timing, LLM, local_metrics, official metric, paper rendering, Repair-1, or larger verifier pass was run.

Post-generation validation:

- CSV parse checks for all generated CSVs: passed.
- Markdown non-empty checks: passed.
- Source audit artifact existence checks: passed.
- Same-8 count reconciliation checks: passed.
- Residual/no-verifier-support row coverage checks: passed.
- No-prohibited-command check: passed by command log review.
- `git diff --check`: passed.
- Changed-file secret scan: passed; value-oriented diff scan found no secret values.
- Protected-path review: passed.
