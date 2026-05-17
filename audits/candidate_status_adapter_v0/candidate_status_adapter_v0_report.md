# candidate_status_adapter_v0 Report

## Purpose And Scope

`candidate_status_adapter_v0` is a release-summary-only, non-timing overlay for the 600 Track-A same-engine `rewrite_candidate_cell` scaffold rows.
It attempts to use release-repo audit metadata only, and fills candidate status fields only when exact row-grain release evidence exists.

## Inputs Read

- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv`
- `audits/retained_summary_adapter_v0/retained_summary_ledger_v0.csv`
- `audits/reports_results_retained_evidence_map/reports_results_retained_evidence_summary.md`
- `audits/reports_results_retained_evidence_map/reports_results_artifact_inventory.csv`
- `audits/reports_results_retained_evidence_map/retained_evidence_candidate_map.csv`
- `audits/retained_evidence_ledger_mapping/retained_evidence_to_ledger_field_map.csv`
- `audits/retained_evidence_ledger_mapping/common_core_ledger_source_inventory.csv`
- `audits/retained_evidence_ledger_mapping/metrics_dependency_matrix.csv`
- `audits/metrics_contract_formalization/finalized_metric_table.csv`
- `audits/common_core40_final_closeout/common_core40_final_case_status_matrix.csv`
- `audits/common_core40_registry_alignment/common_core40_registry_alignment_summary.md`

No legacy paths referenced inside release audit CSVs were opened.

## Rows Emitted

- Rows emitted: 600
- Record types emitted: rewrite_candidate_cell
- Methods emitted: direct_llm_original, direct_llm_repair_1, sqlglot_optimize, sqlglot_noop, calcite_hep_fail_closed

## Row-grain Policy

The overlay preserves one row per `case_id x engine x rewrite_method` from the scaffold.
Route-level or group-level summary references were not distributed across row statuses.

## Fields Filled

- Overlay provenance fields: `adapter_name`, `adapter_scope`, `source_scaffold_record_id`, `status_fill_level`, `status_fill_confidence`, and `notes`.
- `evidence_source` records release-summary metadata overlay when route-level metadata was found.
- No row-level candidate outcome fields were filled because exact row-grain release evidence was not found.

## Fields Remaining Unresolved

- `generated`, `ready`, `executed`, `exact`, and `timed` remain `N.A.`.
- `result_status` remains `evidence_not_adapted_yet`.
- `failure_stage`, `failure_type`, `parse_status`, and `checker_status` remain `requires_production_retained_evidence`.
- `retained_artifact_path` remains blank.
- `metric_input_authorized=false` for every row.

## Explicit Non-goals

- No production retained evidence was parsed.
- No legacy reports/results/runs were parsed.
- No timing adapter was implemented.
- No portability or verifier support adapter was implemented.
- No metrics were computed.
- No paper table was rendered.
- No reports/results, denominator, paper-result, case membership, or raw legacy evidence changes were made.

## Why This Is Not Metrics Computation

The adapter emits row-level unresolved status markers only. It does not aggregate rows, count generated or executed candidates, compute correctness denominators, compute speedups, or authorize metric input.

## Why This Is Not Production Retained-evidence Parsing

The adapter reads release-repo audit metadata and the existing scaffold only. It does not open legacy artifact paths or parse raw retained candidate evidence referenced by audit CSVs.

## Why Timing Fields Remain N.A.

Timing fields require a separate timing adapter and timing eligibility policy. `latency_ms` and `speedup_ratio` remain blank for every row.

## Validation Result

- scaffold row count = 600: PASS (actual=600)
- emitted row count = 600: PASS (actual=600)
- all rows record_type=rewrite_candidate_cell: PASS (record_types=['rewrite_candidate_cell'])
- all rows metric_input_authorized=false: PASS (values=['false'])
- all rows metrics_computed=false: PASS (values=['false'])
- all rows production_retained_evidence_parsed=false: PASS (values=['false'])
- no legacy repo path read: PASS (input use log legacy_paths_opened=false for every inspected metadata file)
- no reports/results changed: PASS (adapter writes only under audits/candidate_status_adapter_v0)
- denominator unchanged: PASS (adapter reads scaffold only and does not write case_sets)
- paper results unchanged: PASS (no paper tables or result summaries written)
- no timing fields filled: PASS (timed_non_na=0;numeric_timing_values=0)
- no speedup fields filled: PASS (speedup_or_latency_values=0)
- no metric computed: PASS (summary records all metric computation flags as false)
- route-level summary counts not distributed into row statuses: PASS (route_level_summary_only_rows=600)
- unresolved rows explicitly marked: PASS (unresolved_rows=600)

## Next Safe Action

Review the unresolved overlay and authorize a stricter production retained-evidence adapter only if exact row-grain retained candidate evidence parsing is in scope. Do not compute metrics or fill timing fields yet.
