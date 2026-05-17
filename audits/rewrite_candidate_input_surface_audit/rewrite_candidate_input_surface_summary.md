# Rewrite Candidate Input-surface Audit

Date: 2026-05-17

## Purpose And Scope

This audit reviews which existing release-repo files, audit outputs, summaries, and scaffolds can safely serve as future input surfaces for filling `rewrite_candidate_cell` rows after the already-created `rewrite_candidate_adapter_v0` Track-A scaffold.

This is an input-surface audit and planning artifact only. It did not implement a candidate status adapter, parse production retained evidence, parse legacy reports/results/runs, fill candidate statuses, compute metrics, create `results/retained`, create `reports/evaluation`, update denominator values, change paper results, or modify raw legacy evidence.

## Scaffold Status

`rewrite_candidate_adapter_v0` scaffold is complete and validated.

- Scaffold script exists: `scripts/dev/build_rewrite_candidate_scaffold_ledger.py`.
- Scaffold ledger exists: `audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv`.
- Scaffold summary exists: `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_summary.json`.
- Ledger validation summary exists: `audits/rewrite_candidate_adapter_v0/ledger_validation/ledger_validation_summary.json`.
- Developer documentation exists: `docs/dev/REWRITE_CANDIDATE_ADAPTER_V0.md`.
- Rows emitted: 600 planned `rewrite_candidate_cell` rows.
- Method routes emitted: 5.
- Saved ledger validation: passed with 600 rows checked, 0 errors, and 0 warnings.
- `metrics_computed=false` and `production_retained_evidence_parsed=false` in the scaffold and validation summaries.

## Explicit Non-actions

- Candidate statuses filled: no.
- Generation Rate computed: no.
- Execution Coverage Rate computed: no.
- Result Consistency Rate computed: no.
- Timing metrics computed: no.
- Production retained evidence parsed: no.
- Legacy repo read: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.

## Methods Reviewed

The audit covers exactly the five main Track-A same-engine method routes included in the v0 scaffold:

- `direct_llm_original`
- `direct_llm_repair_1`
- `sqlglot_optimize`
- `sqlglot_noop`
- `calcite_hep_fail_closed`

Excluded routes such as R-Bot, LLM-R2, LearnedRewrite, SQLGlot Transpile, LLM Translate, SQLSolver, VeriEQL, and user-submitted methods remain outside this audit because they require separate prior-system, portability, verifier-support, or public-runner adapters.

## Safe Release-repo Inputs

The following release-repo inputs are safe for planning, scaffold identity, denominator joins, route/method scope, and validation boundaries:

- `case_sets/common_core_v0/cases.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`
- `inventory/case_registry.csv`
- `repository_spec/metrics_contract_v1.md`
- `repository_spec/evidence_ledger_column_schema_v1_draft.md`
- `repository_spec/evidence_ledger_validation_rules_v1_draft.md`
- `repository_spec/evidence_record_type_policy_v1_draft.md`
- `repository_spec/adapter_row_grain_policy_v1_draft.md`
- `repository_spec/production_ledger_validation_policy_v1_draft.md`
- `audits/rewrite_candidate_adapter_v0/*`
- `audits/control_layer_adapter_closeout/*`
- `audits/retained_evidence_ledger_mapping/*`
- `audits/reports_results_retained_evidence_map/*` as metadata only

These inputs can support future adapter planning, method-scope selection, denominator alignment, candidate row-grain checks, retained artifact trace planning, and safety flag checks. They cannot by themselves authorize or prove generated, ready, executed, exact, timed, latency, speedup, or metric eligibility facts.

## Unauthorized Legacy/raw Inputs

The following input surfaces remain unauthorized for this task and cannot be used by a release-summary-only adapter as metric facts:

- Legacy `reports/`, `results/`, `runs/`, or raw retained evidence paths.
- Method raw outputs.
- Timing files and timing logs.
- Release `reports/results` as production evidence.
- `retained_evidence_candidate_map.csv` as production evidence input.
- Legacy paths referenced inside release-repo audit maps.

The existing reports/results and retained-evidence mapping audits may be inspected only as release-repo metadata. They are not production evidence ledgers and should not be treated as candidate outcome rows.

## Per-field Input-surface Summary

- `generated`, `ready`, `candidate_sql_path`, and `parse_status` require a later candidate-status adapter with explicit input authorization. Current release summaries can identify likely artifact groups, but they do not safely fill these fields at row grain.
- `executed`, `exact`, `result_status`, and `checker_status` require production retained-evidence parsing and row-grain validation before use. Summary result cards must not be converted into candidate facts without adapter validation.
- `failure_stage` and `failure_type` require retained-evidence parsers or manually reviewed row-grain mappings. They must remain `N.A.` or `evidence_not_adapted_yet` now.
- `timed`, `latency_ms`, `speedup_ratio`, and `timing_eligible` require a separate timing adapter and timing policy. Missing timing must not be treated as zero.
- `plan_available` and `plan_artifact_path` require a later plan-observability adapter and public-hygiene review.
- `evidence_source` can remain `release_denominator_scaffold` for the scaffold rows. Real retained evidence sources require a later adapter.
- `retained_artifact_path` must remain blank or `evidence_not_adapted_yet` for candidate rows until a retained-evidence adapter maps public-safe artifacts at row grain.
- `metric_input_authorized` must remain `false`.

## Route-specific Risks

- `direct_llm_original`: likely has retained generation/result-card references, but release audit maps do not prove per-case per-engine row outcomes without parsing approved evidence.
- `direct_llm_repair_1`: repair flow may mix original generation, repair attempts, and execution/timing artifacts; status and timing boundaries need stricter source separation.
- `sqlglot_optimize`: deterministic method output may be recoverable later, but result status and timing still require production retained-evidence and timing adapters.
- `sqlglot_noop`: no-op rows risk being confused with source controls. They must remain rewrite candidate rows with distinct method identity and cannot inherit source-control outcomes.
- `calcite_hep_fail_closed`: fail-closed semantics require careful distinction between unsupported/no-candidate/fail-closed and generated-but-failed candidate states.

## Recommended Next Bounded Adapter

The safest next bounded adapter is a separately authorized `candidate_status_adapter_v0` limited to non-timing candidate status fields and release-summary-only input surfaces. It should fill no timing fields, compute no metrics, leave `metric_input_authorized=false`, and fail closed if release summaries cannot prove row-grain mappings without reading legacy/raw artifacts.

If that scope is not explicitly authorized, the next safe action is to prepare a more detailed approval packet for `candidate_status_adapter_v0` rather than implementing it.

## Next Safe Action

Request explicit maintainer authorization for a bounded `candidate_status_adapter_v0` that may only fill non-timing, non-metric candidate status fields from approved release-repo summaries when row grain is unambiguous. Do not parse legacy raw evidence, read legacy reports/results/runs, compute metrics, authorize metric input, render paper tables, update reports/results, change denominators, or modify raw legacy evidence.
