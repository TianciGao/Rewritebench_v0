# SQLSolver Bounded Verifier Pass: SQLGlot No-op PostgreSQL

Task: `sqlsolver_bounded_verifier_pass_sqlglot_noop_pg_v0`

This packet records a bounded SQLSolver-first verifier-support pass over a deterministic subset of existing Track A 120 exact/result-consistent SQLGlot no-op PostgreSQL pairs.

## Scope

- Route: `sqlglot_noop`
- Run id: `sqlglot_noop_track_a_120_canonical_v0`
- Engine: `postgres`
- Tool: `SQLSolver` only
- Selected pairs: `8`
- Identity guard passed pairs: `3`
- Actual source-candidate attempts: `3`
- Actual equivalent verdicts: `3`
- Actual non-equivalent verdicts: `0`
- Identity guard failed pairs: `5`
- SER status: `coverage_limited`
- Official SER: `false`

## Selected Pairs

- 1. `CONS` `CONS_0005`: `sqlglot_noop__postgres__CONS_0005`
- 2. `CONS` `CONS_0007`: `sqlglot_noop__postgres__CONS_0007`
- 3. `LONGTAIL` `LONGTAIL_0011`: `sqlglot_noop__postgres__LONGTAIL_0011`
- 4. `LONGTAIL` `LONGTAIL_0012`: `sqlglot_noop__postgres__LONGTAIL_0012`
- 5. `PERF` `PERF_0006`: `sqlglot_noop__postgres__PERF_0006`
- 6. `PERF` `PERF_0007`: `sqlglot_noop__postgres__PERF_0007`
- 7. `PORT` `PORT_0003`: `sqlglot_noop__postgres__PORT_0003`
- 8. `PORT` `PORT_0005`: `sqlglot_noop__postgres__PORT_0005`

## Verdict Summary

The bounded decidable source-candidate subset was equivalent for `3` of `3` decidable actual checks, so `bounded_SER_if_decidable` is `1.0`. This is local diagnostic support only and is not official SER.

Identity guards blocked `5` pairs before actual source-candidate checking. These are verifier/modeling limitations, not SQLGlot no-op method failures.

## Outputs

- `selected_pairs.csv`
- `sqlsolver_verdicts.jsonl`
- `identity_guard_results.csv`
- `bounded_semantic_equivalence_summary.json`
- `runtime_artifacts/`
- `sqlsolver_bounded_pass_report.md`
- `verifier_boundary.md`
- `command_log.txt`
- `validation_notes.md`

## Boundary

No VeriEQL run occurred. No adapter, DB execution, checker execution, timing collection, LLM call, `local_metrics.py`, official metrics, paper rendering, retained evidence promotion, or Repair-1 command occurred.
