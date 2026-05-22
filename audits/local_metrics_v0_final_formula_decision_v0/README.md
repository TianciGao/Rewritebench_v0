# local_metrics_v0_final_formula_decision_v0

Verdict: `completed`

This decision/audit packet records the final team decision for non-official local metrics calculator v0 formulas and boundaries before implementation.

No metrics calculator was implemented. No metrics were computed. No Common-core run, reports/results update, retained-evidence promotion, paper table rendering, or leaderboard output was performed.

## Decision Number

Decision recorded: `D033`.

## Summary

The v0 local metrics calculator may later summarize local diagnostic runs only. Its initial formula scope is:

- Generation Rate: `candidate_generated / selected`
- Execution Coverage Rate: `candidate_executable / selected`
- Result Consistency Rate: `exact / selected`
- GM Speedup Ratio and Speedup Ratio Percentiles over strict exact + timed rows only

`preflight_passed` and `source_executable` remain diagnostics, not numerator conditions for the above formulas.

Semantic Equivalence Rate is `N.A.` unless formal verifier evidence exists. Cross-Engine GM Speedup Ratio is `N.A.` unless target-engine paired timing exists. POCR remains deferred pending the collaborator external skill script and stable `skill/` schema.

## Boundary

The future calculator remains non-official and local-only. It must not update reports/results, promote retained evidence, render paper tables, create leaderboard output, change denominators, change case membership, create skill folders, or infer operation atoms.
