# rewrite_candidate_adapter_v0

Developer-facing note. This is a Track-A scaffold generator, not public runner documentation and not a production metrics ledger.

## Command

```bash
python scripts/dev/build_rewrite_candidate_scaffold_ledger.py \
  --case-set case_sets/common_core_v0/cases.csv \
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --out-dir audits/rewrite_candidate_adapter_v0
```

## Scope

The adapter reads only release-repo Common-core scaffolds and `inventory/case_registry.csv`. It emits one `rewrite_candidate_cell` row for each planned `case_id x engine x rewrite_method` combination in Track A.

The scaffold is `120 same-engine denominator rows x 5 method routes = 600 rows`.

## Included Method Routes

- `direct_llm_original`: Direct LLM original.
- `direct_llm_repair_1`: Direct LLM + Repair-1.
- `sqlglot_optimize`: SQLGlot optimize.
- `sqlglot_noop`: SQLGlot no-op.
- `calcite_hep_fail_closed`: Calcite HEP fail-closed.

## Excluded Method Routes

R-Bot, LLM-R2, LearnedRewrite, SQLGlot Transpile, LLM Translate, SQLSolver, VeriEQL, and user-submitted methods are excluded. They require separate bounded adapters because they are prior-system, portability, verifier-support, or future public-runner routes.

## Outputs

- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_method_scope.csv`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_summary.json`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_report.md`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_checks.csv`
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_limitations.md`
- `audits/rewrite_candidate_adapter_v0/ledger_validation/*`

## Non-goals

- No legacy repo reads.
- No legacy reports/results/runs parsing.
- No retained candidate evidence parsing.
- No method raw output parsing.
- No timing adapter work.
- No portability or verifier support adapter work.
- No metrics computation.
- No Generation Rate, Execution Coverage Rate, Result Consistency Rate, GM_Speedup, or Speedup Ratio Percentiles computation.
- No reports/results migration.
- No production ledger under `results/retained`.
- No paper table rendering.

## Validation Command

```bash
python scripts/dev/validate_ledger_csv.py \
  --ledger audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv \
  --case-set case_sets/common_core_v0/cases.csv \
  --same-engine-denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --controls case_sets/common_core_v0/controls_360.csv \
  --out-dir audits/rewrite_candidate_adapter_v0/ledger_validation
```

## Relation To Future Metrics

These rows define planned candidate row grain only. Candidate outcome fields remain `N.A.`, `result_status=evidence_not_adapted_yet`, `metric_input_authorized=false`, and `metrics_computed=false`.

Future metrics require separately authorized retained-evidence parsing, production ledger validation, and metrics computation. This scaffold is not paper evidence by itself.
