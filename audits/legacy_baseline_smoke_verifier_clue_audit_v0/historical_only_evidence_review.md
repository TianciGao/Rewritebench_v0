# Historical-Only Evidence Review

## Baseline Smoke Folder

The two SQLSolver/VeriEQL files in `reports/baseline_smoke/` are static readiness outputs. They are not real verifier execution outputs and must not be promoted.

## Adjacent Legacy Evidence Found

Read-only inspection found adjacent legacy artifacts outside `reports/baseline_smoke/`, including:

- `docs/_scratch/SQLSOLVER_SUPPORT_SMOKE_CONS_0007_0035_v1.md`
- `docs/_scratch/SQLSOLVER_SUPPORT_SMOKE_ROLLUP_v1.md`
- `docs/_scratch/SQLSOLVER_ADAPTER_PREFLIGHT_CONS_0007_0035_v1.md`
- `docs/_scratch/SQLSOLVER_RUNNER_DRY_RUN_WITH_JAR_CONS_0007_0035_v1.md`
- `docs/_scratch/VERIEQL_SUPPORT_BOOTSTRAP_PROBE_v0.md`
- `docs/_scratch/VERIEQL_SUPPORT_WRAPPER_SCAFFOLD_v0.md`
- `docs/_scratch/VERIEQL_SUPPORT_CANARY_v0.md`
- `docs/_scratch/VERIEQL_SUPPORT_VERDICT_INTERPRETATION_v0.md`
- `docs/_scratch/PRIOR_SUPPORT_EVIDENCE_SUMMARY_SQLSOLVER_VERIEQL_v1.md`
- `reports/formal_expansion/verieql_support/*.jsonl`

These are useful historical support clues. They are not release-repo official verifier evidence.

## Historical SQLSolver Evidence

Legacy scratch notes summarize a bounded SQLSolver smoke on `CONS_0007` and `CONS_0035`:

- `CONS_0007` positive: `EQ`
- `CONS_0007` negative: `NEQ`
- `CONS_0035` positive: `NEQ` unexpected
- `CONS_0035` negative: `NEQ`

This remains historical support evidence only.

## Historical VeriEQL Evidence

Legacy JSONL output outside `baseline_smoke` shows:

- `CONS_0007`: `Not supported feature: EXISTS`
- `CONS_0035`: empty-constraint source-positive and source-negative both `non_equivalent`
- `CONS_0035`: constrained source-positive timed out; constrained source-negative remained non-equivalent

This is useful for adapter planning and constraint-policy warnings only.

## Promotion Boundary

None of these legacy artifacts may become official Semantic Equivalence Rate, retained evidence, reports/results output, paper evidence, or leaderboard input without a separate retained-evidence mapping and official promotion task.
