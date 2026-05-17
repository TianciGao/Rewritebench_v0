# rewrite_candidate_adapter_v0 Report

## Purpose And Scope

This bounded scaffold emits draft `rewrite_candidate_cell` rows for the
main Track-A same-engine rewrite method scope. It materializes row grain
only: `case_id x engine x rewrite_method x denominator_id`.

## Inputs Read

- Case set: `case_sets/common_core_v0/cases.csv`
- Same-engine denominator: `case_sets/common_core_v0/denominator_same_engine_120.csv`
- Case registry: `inventory/case_registry.csv`

No legacy reports/results/runs, raw method outputs, timing files, or
retained-evidence candidate maps were read.

## Method Scope

- `direct_llm_original`: Direct LLM original (llm_direct)
- `direct_llm_repair_1`: Direct LLM + Repair-1 (llm_feedback_repair)
- `sqlglot_optimize`: SQLGlot optimize (sqlglot_optimize)
- `sqlglot_noop`: SQLGlot no-op (sqlglot_noop)
- `calcite_hep_fail_closed`: Calcite HEP fail-closed (calcite_hep)

Excluded route families include R-Bot, LLM-R2, LearnedRewrite,
SQLGlot Transpile, LLM Translate, SQLSolver, VeriEQL, and future
user-submitted methods. These are prior, portability, verifier, or
future public-runner routes requiring separate adapters.

## Rows Emitted

- Same-engine denominator rows: 120.
- Method routes: 5.
- Scaffold rows emitted: 600.

- `calcite_hep_fail_closed`: 120 rows.
- `direct_llm_original`: 120 rows.
- `direct_llm_repair_1`: 120 rows.
- `sqlglot_noop`: 120 rows.
- `sqlglot_optimize`: 120 rows.

## Explicit Non-goals

- No production retained evidence was parsed.
- No method candidate evidence was parsed.
- No timing files were parsed.
- No metrics were computed.
- No reports/results were copied or changed.
- No denominator, paper result, case membership, or raw legacy evidence was changed.

## Why This Is Not Metrics Computation

All candidate outcome fields remain `N.A.` and `result_status` is
`evidence_not_adapted_yet`. The scaffold does not count generated,
executed, result-consistent, exact, timed, or speedup rows and cannot
be used to compute Generation Rate, Execution Coverage Rate, Result
Consistency Rate, or timing metrics.

## Validation Result

`scripts/dev/validate_ledger_csv.py` passed on the scaffold output:
600 rows checked, 0 errors, 0 warnings, `validation_passed=true`.

## Next Safe Action

Review scaffold row grain and method scope. Do not parse retained
candidate evidence, compute metrics, or emit metric-eligible rows
without separate authorization.
