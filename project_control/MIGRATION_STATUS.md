# SQL-RewriteBench Migration Status Snapshot

Date: 2026-05-18

## Repository Roles

- Legacy/source repository: `sql-rewrite-bench-artifact-clean`.
- Public release repository: `Rewritebench_v0`.
- Chronological execution history lives in `project_control/MIGRATION_RUN_LOG.md`.
- This file is the concise current-state snapshot.

## Current Status Summary

Common-core 40 canonical case-package migration is complete: 40/40 fixed Common-core cases now have canonical public-release case packages.

This status is verified by the final closeout audit under `audits/common_core40_final_closeout/` and fresh validator v0.3 outputs over the fixed Common-core 40 case list.

No case migration was performed by the final closeout task. It only verified release-repo package state and wrote closeout audit outputs.

Common-core v0 release membership and inventory scaffolds are now aligned under `case_sets/common_core_v0/` and `inventory/`.

Reports/results retained-evidence mapping is complete under `audits/reports_results_retained_evidence_map/`. This is a reference map only; no release `reports/` or `results/` directories were updated.

Common-core retained evidence to draft ledger mapping audit is complete under `audits/retained_evidence_ledger_mapping/`. This audit maps retained evidence candidate groups to ledger field coverage and future adapter needs only; it does not implement adapters, compute metrics, copy reports/results, or authorize the reproduction interface.

Evidence ledger semantics and adapter row-grain policy drafts are complete under `repository_spec/` and `audits/ledger_semantics_row_grain_policy/`. This policy layer defines typed ledger record types, field semantics, row-grain rules, and denominator boundaries only; it does not authorize adapters, metrics, runner implementation, reproduction CLI implementation, or paper rendering.

Metrics finalization decision packet completed under `audits/metrics_finalization_decision_packet/`. This packet organizes maintainer/team decisions for metric naming, denominator use, performance regression reporting, observability, parseability/extractability/runnable SQL status, failure buckets, and future user-output format. It does not finalize or implement metrics, authorize retained-evidence adapters, authorize the reproduction interface, authorize public runner implementation, render paper tables, or change paper results.

Metrics contract resolution draft completed under `repository_spec/metrics_contract_v1_draft.md` and `audits/metrics_contract_resolution/`. The aligned draft reflects the maintainer-provided updated paper scope: Generation Rate, Execution Coverage Rate, Result Consistency Rate, Semantic Equivalence Rate, GM_Speedup, Speedup Ratio Percentiles, Attribution Coverage, Cross-Engine Execution, Cross-Engine Consistency, and Speedup Retention. It remains draft-only and does not authorize metrics implementation, adapters, reproduction interfaces, public runners, paper table rendering, reports/results migration, denominator changes, or paper result changes.

Metrics Contract v1 formalized under `repository_spec/metrics_contract_v1.md`, with supporting audit outputs under `audits/metrics_contract_formalization/` and an attribution policy draft under `repository_spec/explainability_attribution_policy_v1_draft.md`. The formal contract locks the approved paper-scope metric names, denominator boundaries, N.A. conditions, diagnostic/support boundaries, and no-global-leaderboard rule. Metrics implementation, retained-evidence adapter implementation, reproduction interface implementation, public runner implementation, paper table rendering, reports/results migration, denominator changes, paper-result changes, and case membership changes remain unauthorized.

Retained-evidence adapter design and validation plan completed under `repository_spec/retained_evidence_adapter_design_v1_draft.md` and `audits/retained_evidence_adapter_design/`. The design defines adapter families, input source groups, output ledger record types, denominator joins, unsupported/N.A. handling, metric dependencies, validation gates, and a phased implementation plan. It does not implement adapters, compute metrics, create scripts or source package code, copy reports/results, render paper tables, update denominator values, change paper results, or modify raw legacy evidence.

Ledger schema model and non-mutating validation fixtures completed under `repository_spec/evidence_ledger_column_schema_v1_draft.md`, `repository_spec/evidence_ledger_validation_rules_v1_draft.md`, `repository_spec/evidence_ledger_fixture_policy_v1_draft.md`, and `audits/ledger_schema_validation_fixtures/`. The fixture set is synthetic only and covers all seven ledger record types plus intentionally invalid rows. It does not parse production retained evidence, implement adapters, compute metrics, create scripts/source code, copy reports/results, render paper tables, update denominator values, change paper results, or modify raw legacy evidence.

Whole-case universe governance audit completed under `audits/case_universe_governance/`. The audit detected 197 legacy case-like directories, reconciled them against 190 legacy registry rows, identified seven detected-but-unregistered directories, and classified the 157 non-Common-core directories for future staged/backlog/manual-review planning. It did not migrate cases, create staged/backlog membership files, update `case_sets/`, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

Overnight governance and redevelopment investigation completed under `audits/overnight_investigation_bundle/`. The bundle refined planning labels for all 157 non-Common-core cases, inspected the seven unregistered legacy directories, inventoried 123 legacy script/tool files as redevelopment references, audited 24 public release skeleton components, and drafted future prompts for safe next tasks. It did not migrate cases, create official staged/backlog membership files, update `case_sets/`, update reports/results, implement scripts, compute metrics, change denominators, change paper results, or modify raw legacy evidence.

Staged/backlog membership preview completed under `audits/staged_backlog_membership_preview/`. The preview covers all 157 non-Common-core cases with 61 proposed staged rows, 76 proposed backlog rows, 13 manual-review rows, and 7 orphan/unregistered review rows. It did not create official `case_sets/staged_v0/` or `case_sets/backlog_v0/`, migrate cases, update `case_sets/`, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

Clean public release export strategy adopted in `project_control/DECISION_LOG.md` as D017 and specified in `repository_spec/public_release_surface_policy_v1.md`. `Rewritebench_v0` is now explicitly treated as a release construction repository; the final public v0 surface should be produced later through a clean export branch or clean public release repository. No deletion, history rewrite, release branch creation, case migration, reports/results update, case-set update, denominator change, paper-result change, or raw legacy evidence change was performed by the policy task.

Current phase: Workbench redevelopment phase.

The next phase is redevelopment-led public workbench construction around canonical Common-core 40 packages, an evidence ledger schema, metrics contract, runner/output policy, retained evidence adapter, user-facing candidate runner, reproduction/report renderer, and public documentation. Legacy scripts, reports, and results are reference inputs, retained evidence sources, or adapter targets, not the architecture to copy wholesale.

Important blocker: Metrics Contract v1 is formalized, but implementation remains unauthorized. Before implementing retained-evidence adapters, a unified reproduction CLI, public runner outputs, paper table rendering, or metrics computation, the maintainer/team must authorize the corresponding implementation phase and validation gates.

Production ledger validation-gate planning is complete under `repository_spec/production_ledger_validation_policy_v1_draft.md` and `audits/production_ledger_validation_gates/`. The plan defines schema, record-type, denominator, status/N.A., metric-readiness, public-hygiene, mutation-boundary, no-global-leaderboard, provenance, and CI-smoke gates for future production ledgers. It does not implement a production ledger validator, parse production retained evidence, implement adapters, compute metrics, render paper tables, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

`retained_summary_adapter_v0` is complete as a narrow low-risk adapter skeleton under `scripts/dev/build_retained_summary_ledger.py` and `audits/retained_summary_adapter_v0/`. Scope is `release_repo_summary_only`; it emits only `retained_summary_artifact` rows from release-repo summaries, Common-core scaffolds, inventory, and repository specs. It emitted 31 rows, with `metric_input_authorized=false`, `metrics_computed=false`, `production_retained_evidence_parsed=false`, and `legacy_repo_read=false` for every row. This is not a general retained-evidence adapter, not a production ledger, and not a metrics input.

Production ledger validator skeleton and `control_cell_adapter_v0` are complete under `scripts/dev/validate_ledger_csv.py`, `scripts/dev/build_control_cell_ledger.py`, `audits/production_ledger_validator_skeleton/`, and `audits/control_cell_adapter_v0/`. This bounded implementation validates ledger-style CSV files without computing metrics and emits only `control_cell` rows from release-repo canonical Common-core case-package metadata and `controls_360.csv`. It emitted 360 rows, exactly matching the planned control scaffold, with 120 source, 120 positive, and 120 hard-negative rows. Production retained evidence parsing, legacy repo reads, general adapter implementation, metrics computation, reproduction interface implementation, public runner implementation, paper table rendering, reports/results migration, denominator changes, paper-result changes, and raw legacy evidence changes remain unauthorized.

`hard_negative_control_detail_adapter_v0` is complete under `scripts/dev/build_hard_negative_control_detail_ledger.py` and `audits/hard_negative_control_detail_adapter_v0/`. This bounded adapter emits only `control_cell` rows for `control_route=hard_negative` from release-repo canonical Common-core case-package metadata and `controls_360.csv`. It emitted 120 rows, exactly matching the 40 cases x 3 engines hard-negative control scaffold. It records expected-rejection metadata and hard-negative evidence pointers only; it does not parse production retained evidence, read the legacy repo, infer fresh rejection outcomes, compute hard-negative rejection rate, compute false-accept rate, compute metrics, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

`source_positive_control_detail_adapter_v0` is complete under `scripts/dev/build_source_positive_control_detail_ledger.py` and `audits/source_positive_control_detail_adapter_v0/`. This bounded adapter emits only `control_cell` rows for `control_route in {source, positive}` from release-repo canonical Common-core case-package metadata and `controls_360.csv`. It emitted 240 rows, exactly matching the 40 cases x 3 engines x 2 source/positive control scaffold. It records SQL/config paths and source/positive retained evidence pointers only; it does not parse production retained evidence, read the legacy repo, infer fresh execution or consistency outcomes, compute source-positive rate, compute Result Consistency Rate, compute metrics, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

Control-layer adapter closeout completed under `audits/control_layer_adapter_closeout/`. This audit-only closeout reviewed `control_cell_adapter_v0`, `source_positive_control_detail_adapter_v0`, and `hard_negative_control_detail_adapter_v0`; verified 360 generic control rows, 240 source/positive detail rows, 120 hard-negative detail rows, and 360 combined detail rows; confirmed route coverage of 120/120 for source, positive, and hard-negative controls; and confirmed all adapter ledger validations and the synthetic fixture smoke passed. It did not implement adapters, parse production retained evidence, read the legacy repo, compute metrics, compute false-accept rate, compute source-positive rate, compute Result Consistency Rate, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

`rewrite_candidate_adapter_v0` Track-A scaffold is complete under `scripts/dev/build_rewrite_candidate_scaffold_ledger.py` and `audits/rewrite_candidate_adapter_v0/`. This bounded scaffold emits only `rewrite_candidate_cell` rows from release-repo Common-core Track-A denominator scaffolds and `inventory/case_registry.csv`. It emitted 600 planned scaffold rows: 120 same-engine denominator rows x five authorized main method routes (`direct_llm_original`, `direct_llm_repair_1`, `sqlglot_optimize`, `sqlglot_noop`, and `calcite_hep_fail_closed`). The scaffold records planned candidate row grain only; it does not parse production retained evidence, read the legacy repo, parse method outputs, parse timing files, compute Generation Rate, compute Execution Coverage Rate, compute Result Consistency Rate, compute timing metrics, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

Candidate evidence input-surface audit for `rewrite_candidate_adapter_v1` planning is complete under `audits/rewrite_candidate_input_surface_audit/`. This audit confirms the v0 rewrite candidate scaffold is complete and validated, classifies safe release-repo planning inputs versus unauthorized legacy/raw evidence surfaces, maps candidate ledger fields to future adapter needs, records route-specific risks for the five Track-A methods, and recommends a separately authorized non-timing `candidate_status_adapter_v0` as the safest next bounded adapter. It did not fill candidate statuses, parse production retained evidence, read the legacy repo, compute Generation Rate, compute Execution Coverage Rate, compute Result Consistency Rate, compute timing metrics, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

`candidate_status_adapter_v0` release-summary-only non-timing overlay is complete under `scripts/dev/build_candidate_status_ledger.py` and `audits/candidate_status_adapter_v0/`. This bounded adapter reads the existing 600-row rewrite candidate scaffold and approved release-repo audit metadata only, emits 600 `rewrite_candidate_cell` overlay rows, and leaves all row-level candidate statuses unresolved because no exact case_id x engine x rewrite_method release evidence was available from the allowed metadata. Row-level status rows filled: 0. Unresolved status rows: 600. Route-level summary metadata was detected for 600 rows and was not distributed into row-level statuses. It did not parse production retained evidence, read the legacy repo, parse legacy reports/results/runs, open legacy paths referenced by audit CSVs, fill timing fields, compute Generation Rate, compute Execution Coverage Rate, compute Result Consistency Rate, compute timing metrics, authorize metric input, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

Candidate retained-evidence parser approval packet completed under `audits/candidate_retained_evidence_parser_approval_packet/`. This audit/design packet reviews the unresolved `candidate_status_adapter_v0` overlay, summarizes why 600 candidate rows remain unresolved, reviews v0 input-use safety, maps candidate fields to future evidence source groups, documents route-specific risks, proposes a separated non-timing parser scope, defines validation gates, and provides a maintainer decision template. It did not implement a parser, parse production retained evidence, read the legacy repo, fill candidate row statuses, fill timing fields, authorize metric input, compute metrics, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence.

`candidate_status_parser_v0` manifest-first bounded non-timing parser is complete under `scripts/dev/build_candidate_status_parser_input_manifest.py`, `scripts/dev/parse_candidate_status_from_manifest.py`, and `audits/candidate_status_parser_v0/`. The input manifest is header-only because release-repo locator and mapping metadata did not prove any exact row-grain source at `case_id x engine x rewrite_method x candidate_id x denominator_id`. Approved manifest inputs: 0. The parser failed closed safely, emitted 600 unresolved `rewrite_candidate_cell` rows, filled 0 row-level statuses, and passed ledger validation with 600 rows checked, 0 errors, and 0 warnings. It did not parse production retained evidence, read the legacy repo, fill timing fields, authorize metric input, compute metrics, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence.

Candidate status whitelist triage for manual approval completed under `audits/candidate_status_whitelist_triage/`. This audit-only task reviewed release metadata and selected legacy inventory paths at path/header/schema-preview level only, produced a 19-row maintainer-reviewable whitelist proposal, identified four `approve_header_only_then_parser` candidates pending maintainer review, six deferred manual-review candidates, eight rejected parser inputs, and one reference-only locator row. It did not parse candidate statuses, fill timing fields, compute metrics, create a production ledger, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

Maintainer approval for `candidate_status_parser_v1` whitelist use has been recorded in `audits/candidate_status_whitelist_triage/candidate_status_manual_decision_sheet.csv` and `candidate_status_parser_v1_input_manifest_preview.csv`. Approved proposal IDs are `P001`, `P002`, `P003`, `P011`, and `P012` only, limited to non-timing status fields and the required conditions in the decision sheet. `candidate_status_parser_v1` has not been implemented by this approval-recording task; no candidate statuses were parsed or filled, no timing fields were filled, no metrics were computed, no production ledger was created, and no reports/results, denominators, paper results, case membership, legacy repo files, or raw legacy evidence were changed.

`candidate_status_parser_v1` is complete under `scripts/dev/build_candidate_status_parser_v1_manifest.py`, `scripts/dev/parse_candidate_status_v1.py`, and `audits/candidate_status_parser_v1/`. It builds a five-row approved manifest from proposals `P001`, `P002`, `P003`, `P011`, and `P012`, opens only those approved legacy CSV sources, parses approved non-timing status columns only, emits 600 `rewrite_candidate_cell` audit rows, fills 175 row-level status rows, and leaves 425 rows unresolved. The parser records `production_retained_evidence_parsed=true` and `legacy_repo_read=true` in its audit summary because approved legacy sources were read, but it does not modify the legacy repo, copy reports/results, fill timing fields, authorize metric input, compute metrics, create a production ledger, change denominators, change paper results, change case membership, or modify raw legacy evidence. The output passed the non-mutating ledger validator with 600 rows checked, 0 errors, and 0 warnings.

`candidate_status_parser_v1` closeout and metric-input readiness review is complete under `audits/candidate_status_parser_v1_closeout/`. This release-repo-only closeout reviewed the existing 600-row parser-v1 audit ledger and related audit summaries, performed no new candidate status parsing, opened no new legacy files, filled no additional statuses, authorized no metric input, and computed no metrics. It confirms 175 row-level status rows filled by the prior parser-v1 run, 425 unresolved rows, approved inputs `P001`, `P002`, `P003`, `P011`, and `P012`, P001/P002 overlap on 26 Direct LLM original rows, P002/P003 overlap on 19 Repair-1 rows, no P011/P012 Calcite overlap, 130 filled rows labeled `ready_candidate_status_only`, 45 filled rows labeled `needs_source_overlap_review`, timing fields filled: no, `metric_input_authorized` rows: 0, reports/results changed: no, denominator changed: no, paper results changed: no, and raw legacy evidence changed: no.

`metric_input_authorization_overlay_v0` is complete under `audits/metric_input_authorization_overlay_v0/`. This audit-only overlay authorizes metric-input eligibility for exactly 130 `candidate_status_parser_v1` filled rows labeled `ready_candidate_status_only`, denies the 45 filled rows labeled `needs_source_overlap_review`, and leaves the 425 unresolved rows unauthorized. It does not rewrite `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`, authorize timing fields, authorize speedup fields, compute metrics, compute Generation Rate, compute Execution Coverage Rate, compute Result Consistency Rate, compute timing metrics, render paper tables, update reports/results, change denominators, change paper results, modify the legacy repo, or modify raw legacy evidence.

`official_status_metrics_v0_limited` is complete under `scripts/dev/compute_official_status_metrics_limited.py` and `audits/official_status_metrics_v0_limited/`. This limited official status-metrics computation uses the current combined candidate-status evidence and authorization overlay to compute only Execution Coverage Rate and Result Consistency Rate, keeps Generation Rate blocked by policy, preserves 600 planned denominator rows, keeps 425 unauthorized/unresolved rows visible, and marks every output `paper_result=false` with no global leaderboard. It did not render paper tables, compute timing/performance metrics, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.

## Common-core Case-Package Counts

| Pool | Canonical complete | Common-core total | Status |
|---|---:|---:|---|
| PERF | 16 | 16 | complete |
| CONS | 9 | 9 | complete |
| PORT | 9 | 9 | complete |
| LONGTAIL | 6 | 6 | complete |
| Total | 40 | 40 | complete |

Validator snapshot:

- Full-case validator v0.3: PASS 40/40 over all fixed Common-core cases.
- Canonical-case validator v0.3: PASS 40/40 over all fixed Common-core cases.
- Canonical-case warnings are limited to the accepted transitional PostgreSQL validation alias on `PORT_0004` and `PORT_0008`.

Membership and scaffold snapshot:

- `case_sets/common_core_v0/cases.csv`: 40 fixed Common-core case rows.
- `case_sets/common_core_v0/denominator_same_engine_120.csv`: 120 planned same-engine denominator scaffold rows.
- `case_sets/common_core_v0/controls_360.csv`: 360 planned control scaffold rows.
- `inventory/case_registry.csv`: 40 Common-core registry rows.
- `inventory/source_registry.csv`: source-family registry inferred from existing migrated case manifests, with license/source notes marked `needs_later_review` where not governed.
- `audits/reports_results_retained_evidence_map/reports_results_artifact_inventory.csv`: legacy reports/results artifact map, with `copy_now=false` for all retained-evidence candidates.
- `audits/retained_evidence_ledger_mapping/retained_evidence_to_ledger_field_map.csv`: grouped retained-evidence candidate to draft ledger field mapping.
- `audits/ledger_semantics_row_grain_policy/ledger_field_semantics_review.csv`: 28 draft ledger fields reviewed against record types and denominator boundaries.
- `audits/metrics_finalization_decision_packet/metric_decision_table.csv`: 17 metric families reviewed for maintainer/team decision before implementation.
- `audits/metrics_contract_resolution/resolved_metric_contract_table.csv`: 10 updated metric-scope rows aligned to the maintainer-provided paper scope.
- `repository_spec/metrics_contract_v1.md`: formal metric contract v1 from approved paper scope.
- `audits/metrics_contract_formalization/finalized_metric_table.csv`: 10 primary metrics plus diagnostic/support rows recorded with `implementation_authorized=false`.
- `repository_spec/retained_evidence_adapter_design_v1_draft.md`: retained-evidence adapter design and validation plan.
- `audits/retained_evidence_adapter_design/adapter_input_source_matrix.csv`: adapter source-group to record-type mapping.
- `audits/retained_evidence_adapter_design/metric_to_adapter_dependency_matrix.csv`: Metrics Contract v1 metric dependencies on adapter families and ledger fields.
- `repository_spec/evidence_ledger_column_schema_v1_draft.md`: draft ledger column model.
- `audits/ledger_schema_validation_fixtures/fixture_all_record_types.csv`: 20 synthetic fixture rows covering all seven ledger record types.
- `audits/ledger_schema_validation_fixtures/fixture_expected_validation_results.csv`: expected valid/invalid fixture outcomes.
- `scripts/dev/validate_ledger_fixtures.py`: non-mutating developer validator skeleton for synthetic ledger fixtures only.
- `audits/ledger_fixture_validator_skeleton/ledger_fixture_validation_summary.json`: latest synthetic fixture validator result; 20 fixture rows checked, 14 expected-valid rows passed, 6 expected-invalid rows failed as expected, and 14/14 denominator join examples matched expectations.
- `audits/ledger_fixture_validator_hardening/ledger_fixture_hardening_summary.json`: hardened synthetic fixture validator result; 20 base rows plus 18 extra hardening rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, duplicate/status/safety/denominator checks exercised, and 14/14 denominator join examples matched expectations.
- `scripts/dev/smoke_ledger_fixtures.py`: developer-only smoke entrypoint wrapping the hardened synthetic fixture validator.
- `audits/ledger_fixture_dev_smoke/ledger_fixture_hardening_summary.json`: latest developer smoke output; 38 synthetic fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and no production retained evidence parsed.
- `.github/workflows/ledger-fixture-smoke.yml`: lightweight GitHub Actions workflow running the synthetic ledger fixture smoke validator on push, pull request, and manual dispatch.
- `audits/ledger_fixture_ci_smoke/ledger_fixture_ci_smoke_summary.json`: CI smoke wiring audit summary; workflow created and local smoke passed without production retained evidence parsing.
- `repository_spec/production_ledger_validation_policy_v1_draft.md`: policy-only future production ledger validation gate plan.
- `audits/production_ledger_validation_gates/production_ledger_gate_matrix.csv`: 24 proposed validation gates across schema, record-type, denominator, status/N.A., metric-readiness, public hygiene, mutation boundary, no-global-leaderboard, provenance, and CI-smoke families.
- `audits/production_ledger_validation_gates/record_type_production_gate_matrix.csv`: seven ledger record types covered by future production validation gates.
- `audits/production_ledger_validation_gates/metric_readiness_gate_matrix.csv`: 10 Metrics Contract v1 primary metrics mapped to pre-computation readiness gates, with `can_compute_without_gate=false`.
- `scripts/dev/build_retained_summary_ledger.py`: narrow release-repo-summary-only adapter skeleton emitting `retained_summary_artifact` rows only.
- `audits/retained_summary_adapter_v0/retained_summary_ledger_v0.csv`: 31 draft retained-summary rows, all non-metric audit rows.
- `audits/retained_summary_adapter_v0/retained_summary_adapter_v0_summary.json`: adapter summary recording `production_retained_evidence_parsed=false`, `legacy_repo_read=false`, `metrics_computed=false`, and `metric_input_authorized=false`.
- `scripts/dev/validate_ledger_csv.py`: non-mutating production ledger validator skeleton for ledger-style CSV files.
- `scripts/dev/build_control_cell_ledger.py`: bounded release-case-package-only control-cell adapter v0.
- `audits/production_ledger_validator_skeleton/ledger_validation_summary.json`: validator skeleton output over the control-cell adapter ledger; 360 rows checked, validation passed, no metrics computed.
- `audits/control_cell_adapter_v0/control_cell_ledger_v0.csv`: 360 draft `control_cell` rows, one per planned row in `controls_360.csv`.
- `audits/control_cell_adapter_v0/control_cell_adapter_v0_summary.json`: adapter summary recording 360 rows emitted, `production_retained_evidence_parsed=false`, `legacy_repo_read=false`, `metrics_computed=false`, and `metric_input_authorized=false`.
- `audits/control_cell_adapter_v0/ledger_validation/ledger_validation_summary.json`: validation output for the control-cell ledger; `validation_passed=true`.
- `scripts/dev/build_hard_negative_control_detail_ledger.py`: bounded release-case-package-only hard-negative detail adapter v0.
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_ledger_v0.csv`: 120 draft `control_cell` rows for hard-negative controls only.
- `audits/hard_negative_control_detail_adapter_v0/hard_negative_control_detail_adapter_v0_summary.json`: adapter summary recording 120 rows emitted, `hard_negative_rate_computed=false`, `production_retained_evidence_parsed=false`, `legacy_repo_read=false`, `metrics_computed=false`, and `metric_input_authorized=false`.
- `audits/hard_negative_control_detail_adapter_v0/ledger_validation/ledger_validation_summary.json`: validation output for the hard-negative detail ledger; `validation_passed=true`.
- `scripts/dev/build_source_positive_control_detail_ledger.py`: bounded release-case-package-only source/positive detail adapter v0.
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_ledger_v0.csv`: 240 draft `control_cell` rows for source and positive controls only.
- `audits/source_positive_control_detail_adapter_v0/source_positive_control_detail_adapter_v0_summary.json`: adapter summary recording 240 rows emitted, `source_positive_rate_computed=false`, `result_consistency_rate_computed=false`, `production_retained_evidence_parsed=false`, `legacy_repo_read=false`, `metrics_computed=false`, and `metric_input_authorized=false`.
- `audits/source_positive_control_detail_adapter_v0/ledger_validation/ledger_validation_summary.json`: validation output for the source/positive detail ledger; `validation_passed=true`.
- `scripts/dev/build_rewrite_candidate_scaffold_ledger.py`: bounded Track-A same-engine rewrite candidate scaffold adapter v0.
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv`: 600 draft `rewrite_candidate_cell` scaffold rows, one per 120 planned denominator rows x five authorized method routes.
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_method_scope.csv`: five included Track-A method routes and excluded prior/portability/verifier/user-run route examples.
- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_adapter_v0_summary.json`: scaffold summary recording `production_retained_evidence_parsed=false`, `legacy_repo_read=false`, `metrics_computed=false`, `metric_input_authorized=false`, and no metric rates computed.
- `audits/rewrite_candidate_adapter_v0/ledger_validation/ledger_validation_summary.json`: validation output for the rewrite candidate scaffold; 600 rows checked, `validation_passed=true`.
- `audits/rewrite_candidate_input_surface_audit/rewrite_candidate_input_surface_summary.json`: candidate input-surface audit summary; v0 scaffold confirmed, five Track-A methods reviewed, candidate statuses not filled, metrics not computed, production retained evidence not parsed, and legacy repo not read.
- `audits/rewrite_candidate_input_surface_audit/candidate_field_readiness_matrix.csv`: candidate ledger fields classified by scaffold support, release-summary planning support, retained-evidence requirements, timing requirements, and current recommended status.
- `scripts/dev/build_candidate_status_ledger.py`: bounded release-summary-only non-timing overlay adapter for the 600-row rewrite candidate scaffold.
- `audits/candidate_status_adapter_v0/candidate_status_ledger_v0.csv`: 600 draft `rewrite_candidate_cell` overlay rows; all row-level status fields remain unresolved and `metric_input_authorized=false`.
- `audits/candidate_status_adapter_v0/candidate_status_adapter_v0_summary.json`: overlay summary recording 600 rows emitted, 0 row-level status rows filled, 600 unresolved rows, `production_retained_evidence_parsed=false`, `legacy_repo_read=false`, `metrics_computed=false`, and `metric_input_authorized=false`.
- `audits/candidate_status_adapter_v0/ledger_validation/ledger_validation_summary.json`: validation output for the candidate status overlay; 600 rows checked, `validation_passed=true`.
- `audits/candidate_retained_evidence_parser_approval_packet/approval_packet_summary.md`: approval-packet summary for a future bounded candidate retained-evidence parser.
- `audits/candidate_retained_evidence_parser_approval_packet/unresolved_overlay_review.csv`: five-route review confirming 120/120 unresolved rows per Track-A candidate route.
- `audits/candidate_retained_evidence_parser_approval_packet/candidate_field_to_source_plan.csv`: candidate field to future evidence-source and validation-gate plan.
- `audits/candidate_retained_evidence_parser_approval_packet/approval_decision_template.md`: maintainer-facing template for design-only approval, bounded implementation approval, deferral, or rejection.
- `scripts/dev/build_candidate_status_parser_input_manifest.py`: manifest-first input selector for `candidate_status_parser_v0`, reading release-repo locator metadata only.
- `scripts/dev/parse_candidate_status_from_manifest.py`: bounded non-timing parser that fails closed when no approved row-level manifest inputs exist.
- `audits/candidate_status_parser_v0/candidate_status_parser_input_manifest.csv`: header-only approved input manifest; approved parser inputs = 0.
- `audits/candidate_status_parser_v0/candidate_status_parsed_ledger_v0.csv`: 600 unresolved `rewrite_candidate_cell` parser output rows.
- `audits/candidate_status_parser_v0/candidate_status_parser_v0_summary.json`: parser summary recording 600 rows emitted, 0 row-level statuses filled, 600 unresolved rows, 0 timing fields filled, 0 metric-input-authorized rows, `metrics_computed=false`, `production_retained_evidence_parsed=false`, and `legacy_repo_read=false`.
- `audits/candidate_status_parser_v0/ledger_validation/ledger_validation_summary.json`: validation output for the candidate status parser ledger; 600 rows checked, `validation_passed=true`.
- `audits/case_universe_governance/case_universe_index.csv`: 197 detected legacy case-like directories indexed for governance; 40 Common-core and 157 non-Common-core.
- `audits/overnight_investigation_bundle/proposed_staged_backlog_membership_matrix.csv`: 157 non-Common-core planning rows; planning labels only, not official membership.
- `audits/overnight_investigation_bundle/legacy_script_reference_inventory.csv`: 123 legacy script/tool files classified for redevelopment reference.
- `audits/overnight_investigation_bundle/public_release_skeleton_gap_audit.csv`: 24 intended public release layout components reviewed.
- `audits/staged_backlog_membership_preview/proposed_staged_v0_cases_preview.csv`: 61 proposed staged preview rows; not official membership.
- `audits/staged_backlog_membership_preview/proposed_backlog_v0_cases_preview.csv`: 76 proposed backlog preview rows; not official membership.
- `audits/staged_backlog_membership_preview/manual_review_and_orphan_cases.csv`: 20 manual-review/orphan rows, including all seven unregistered directories.
- `repository_spec/public_release_surface_policy_v1.md`: clean public export strategy and file classification labels.
- `audits/public_release_surface_strategy/public_release_surface_classification_seed.csv`: seed classification table for future clean-export planning.

## Explicit Boundaries

- Common-core denominator unchanged.
- Track A 120 planned rows unchanged.
- Paper results unchanged.
- Case membership unchanged.
- `case_sets/` aligned for fixed Common-core v0 membership; no membership change.
- Official `case_sets/staged_v0/` created: no.
- Official `case_sets/backlog_v0/` created: no.
- Clean release branch created: no.
- Files deleted by clean-export policy task: no.
- Git history rewritten by clean-export policy task: no.
- `inventory/` aligned for fixed Common-core v0 scope.
- `reports/` not updated by case-package migration or final closeout.
- `results/` not updated by case-package migration or final closeout.
- Reports/results retained-evidence map completed; actual release reports/results files unchanged.
- Retained evidence to ledger mapping audit completed; actual release reports/results files unchanged.
- Denominator files and paper tables not updated by case-package migration or final closeout.
- Raw legacy evidence unchanged.
- Metrics implementation authorized: limited official status metrics v0 only for Execution Coverage Rate and Result Consistency Rate; Generation Rate and all broader metrics remain unauthorized.
- Retained-evidence adapter implementation authorized: no.
- Unified reproduction interface implementation authorized: no.
- Public runner implementation authorized: no.
- Paper table rendering authorized: no.
- Production retained evidence parsed by ledger fixture validator: no.
- Production retained evidence parsed by hardened ledger fixture validator: no.
- Production retained evidence parsed by developer smoke entrypoint: no.
- Production retained evidence parsed by ledger fixture CI smoke workflow: no.
- Production retained evidence parsed by production ledger validation-gate planning: no.
- Production retained evidence parsed by retained_summary_adapter_v0: no.
- Legacy repo read by retained_summary_adapter_v0: no.
- Metrics computed by retained_summary_adapter_v0: no.
- Metric input authorized by retained_summary_adapter_v0: no.
- Production ledger validator skeleton implemented: yes, non-mutating and metrics-free.
- control_cell_adapter_v0 implemented: yes, bounded to release case-package metadata and `control_cell` rows only.
- Production retained evidence parsed by control_cell_adapter_v0: no.
- Legacy repo read by control_cell_adapter_v0: no.
- Metrics computed by control_cell_adapter_v0: no.
- Metric input authorized by control_cell_adapter_v0: no.
- hard_negative_control_detail_adapter_v0 implemented: yes, bounded to hard-negative `control_cell` rows from release case-package metadata.
- Production retained evidence parsed by hard_negative_control_detail_adapter_v0: no.
- Legacy repo read by hard_negative_control_detail_adapter_v0: no.
- Metrics computed by hard_negative_control_detail_adapter_v0: no.
- False-accept-rate computed by hard_negative_control_detail_adapter_v0: no.
- Metric input authorized by hard_negative_control_detail_adapter_v0: no.
- source_positive_control_detail_adapter_v0 implemented: yes, bounded to source/positive `control_cell` rows from release case-package metadata.
- Production retained evidence parsed by source_positive_control_detail_adapter_v0: no.
- Legacy repo read by source_positive_control_detail_adapter_v0: no.
- Metrics computed by source_positive_control_detail_adapter_v0: no.
- Source-positive rate computed by source_positive_control_detail_adapter_v0: no.
- Result Consistency Rate computed by source_positive_control_detail_adapter_v0: no.
- Metric input authorized by source_positive_control_detail_adapter_v0: no.
- Control-layer adapter closeout completed: yes, audit-only.
- Actual adapter implementation performed by control-layer closeout: no.
- Generic control rows after closeout: 360.
- Source/positive detail rows after closeout: 240.
- Hard-negative detail rows after closeout: 120.
- Combined detail rows after closeout: 360.
- Production retained evidence parsed by control-layer closeout: no.
- Legacy repo read by control-layer closeout: no.
- Metrics computed by control-layer closeout: no.
- False-accept-rate computed by control-layer closeout: no.
- Source-positive rate computed by control-layer closeout: no.
- Result Consistency Rate computed by control-layer closeout: no.
- rewrite_candidate_adapter_v0 Track-A scaffold completed: yes, bounded scaffold only.
- Rewrite candidate scaffold rows emitted: 600.
- Rewrite candidate method routes emitted: 5.
- Production retained evidence parsed by rewrite_candidate_adapter_v0 scaffold: no.
- Legacy repo read by rewrite_candidate_adapter_v0 scaffold: no.
- Metrics computed by rewrite_candidate_adapter_v0 scaffold: no.
- Generation Rate computed by rewrite_candidate_adapter_v0 scaffold: no.
- Execution Coverage Rate computed by rewrite_candidate_adapter_v0 scaffold: no.
- Result Consistency Rate computed by rewrite_candidate_adapter_v0 scaffold: no.
- Timing metrics computed by rewrite_candidate_adapter_v0 scaffold: no.
- Candidate evidence input-surface audit completed: yes.
- Candidate statuses filled by input-surface audit: no.
- Production retained evidence parsed by input-surface audit: no.
- Legacy repo read by input-surface audit: no.
- Metrics computed by input-surface audit: no.
- Generation Rate computed by input-surface audit: no.
- Execution Coverage Rate computed by input-surface audit: no.
- Result Consistency Rate computed by input-surface audit: no.
- Timing metrics computed by input-surface audit: no.
- candidate_status_adapter_v0 release-summary-only non-timing overlay completed: yes.
- candidate_status_adapter_v0 rows emitted: 600.
- candidate_status_adapter_v0 row-level status rows filled: 0.
- candidate_status_adapter_v0 unresolved status rows: 600.
- candidate_status_adapter_v0 route-level summary-only rows: 600; not distributed into row statuses.
- Production retained evidence parsed by candidate_status_adapter_v0: no.
- Legacy repo read by candidate_status_adapter_v0: no.
- Metrics computed by candidate_status_adapter_v0: no.
- Generation Rate computed by candidate_status_adapter_v0: no.
- Execution Coverage Rate computed by candidate_status_adapter_v0: no.
- Result Consistency Rate computed by candidate_status_adapter_v0: no.
- Timing metrics computed by candidate_status_adapter_v0: no.
- Metric input authorized by candidate_status_adapter_v0: no.
- Candidate retained-evidence parser approval packet completed: yes, audit/design only.
- Production retained evidence parsed by candidate parser approval packet: no.
- Legacy repo read by candidate parser approval packet: no.
- Candidate row statuses filled by candidate parser approval packet: no.
- Timing fields filled by candidate parser approval packet: no.
- Metrics computed by candidate parser approval packet: no.
- Metric input authorized by candidate parser approval packet: no.
- candidate_status_parser_v0 completed: yes, manifest-first bounded non-timing parser.
- candidate_status_parser_v0 approved manifest inputs: 0.
- candidate_status_parser_v0 row-level statuses filled: 0.
- candidate_status_parser_v0 unresolved rows: 600.
- Production retained evidence parsed by candidate_status_parser_v0: no.
- Legacy repo read by candidate_status_parser_v0: no.
- Timing fields filled by candidate_status_parser_v0: no.
- Metrics computed by candidate_status_parser_v0: no.
- Generation Rate computed by candidate_status_parser_v0: no.
- Execution Coverage Rate computed by candidate_status_parser_v0: no.
- Result Consistency Rate computed by candidate_status_parser_v0: no.
- Timing metrics computed by candidate_status_parser_v0: no.
- Metric input authorized by candidate_status_parser_v0: no.
- Candidate status whitelist triage completed: yes, audit/manual-review packet only.
- Candidate status whitelist triage files reviewed: 28.
- Candidate status whitelist proposal rows: 19.
- Candidate status whitelist proposed approve-header-only rows: 4.
- Candidate status whitelist proposed defer rows: 6.
- Candidate status whitelist rejected parser input rows: 8.
- Candidate statuses filled by whitelist triage: no.
- Timing fields filled by whitelist triage: no.
- Metrics computed by whitelist triage: no.
- Production ledger created by whitelist triage: no.
- Legacy repo modified by whitelist triage: no.
- Raw legacy evidence changed by whitelist triage: no.
- Reports/results changed by whitelist triage: no.
- Denominator changed by whitelist triage: no.
- Paper results changed by whitelist triage: no.
- Maintainer approval recorded for candidate_status_parser_v1 whitelist: yes.
- candidate_status_parser_v1 approved proposal IDs: P001, P002, P003, P011, P012.
- candidate_status_parser_v1 implemented by approval-recording task: no.
- Candidate statuses filled by approval-recording task: no.
- Timing fields filled by approval-recording task: no.
- Metrics computed by approval-recording task: no.
- Production ledger created by approval-recording task: no.
- Reports/results changed by approval-recording task: no.
- Denominator changed by approval-recording task: no.
- Paper results changed by approval-recording task: no.
- Case membership changed by approval-recording task: no.
- Raw legacy evidence changed by approval-recording task: no.
- candidate_status_parser_v1 completed: yes.
- candidate_status_parser_v1 approved manifest inputs: 5.
- candidate_status_parser_v1 row-level status rows filled: 175.
- candidate_status_parser_v1 unresolved rows: 425.
- Production retained evidence parsed by candidate_status_parser_v1: yes, limited to approved legacy CSV status columns.
- Legacy repo read by candidate_status_parser_v1: yes, read-only approved CSV sources only.
- Legacy repo modified by candidate_status_parser_v1: no.
- Timing fields filled by candidate_status_parser_v1: no.
- Metrics computed by candidate_status_parser_v1: no.
- Generation Rate computed by candidate_status_parser_v1: no.
- Execution Coverage Rate computed by candidate_status_parser_v1: no.
- Result Consistency Rate computed by candidate_status_parser_v1: no.
- Timing metrics computed by candidate_status_parser_v1: no.
- Metric input authorized by candidate_status_parser_v1: no.
- Reports/results changed by candidate_status_parser_v1: no.
- Denominator changed by candidate_status_parser_v1: no.
- Paper results changed by candidate_status_parser_v1: no.
- Raw legacy evidence changed by candidate_status_parser_v1: no.
- candidate_status_parser_v1 closeout completed: yes.
- New candidate status parsing performed by parser-v1 closeout: no.
- Row-level status rows filled by prior parser-v1 run: 175.
- Unresolved rows after parser-v1 closeout: 425.
- Timing fields filled by parser-v1 closeout: no.
- Metric input authorized rows after parser-v1 closeout: 0.
- Metrics computed by parser-v1 closeout: no.
- Generation Rate computed by parser-v1 closeout: no.
- Execution Coverage Rate computed by parser-v1 closeout: no.
- Result Consistency Rate computed by parser-v1 closeout: no.
- Timing metrics computed by parser-v1 closeout: no.
- Metric-input readiness review completed by parser-v1 closeout: yes.
- parser-v1 closeout `ready_candidate_status_only` rows: 130.
- parser-v1 closeout `needs_source_overlap_review` rows: 45.
- parser-v1 closeout `needs_status_normalization` rows: 0.
- parser-v1 closeout `not_metric_ready` rows: 0.
- Reports/results changed by parser-v1 closeout: no.
- Denominator changed by parser-v1 closeout: no.
- Paper results changed by parser-v1 closeout: no.
- Raw legacy evidence changed by parser-v1 closeout: no.
- metric_input_authorization_overlay_v0 completed: yes.
- metric_input_authorization_overlay_v0 authorized rows: 130.
- metric_input_authorization_overlay_v0 unauthorized overlap rows: 45.
- metric_input_authorization_overlay_v0 unresolved rows remain unauthorized: 425.
- Timing authorized by metric_input_authorization_overlay_v0: no.
- Metrics computed by metric_input_authorization_overlay_v0: no.
- Generation Rate computed by metric_input_authorization_overlay_v0: no.
- Execution Coverage Rate computed by metric_input_authorization_overlay_v0: no.
- Result Consistency Rate computed by metric_input_authorization_overlay_v0: no.
- Timing metrics computed by metric_input_authorization_overlay_v0: no.
- Reports/results changed by metric_input_authorization_overlay_v0: no.
- Denominator changed by metric_input_authorization_overlay_v0: no.
- Paper results changed by metric_input_authorization_overlay_v0: no.
- Raw legacy evidence changed by metric_input_authorization_overlay_v0: no.
- Original parser ledger modified by metric_input_authorization_overlay_v0: no.
- candidate status overlap review and status-only metrics dry-run plan completed: yes.
- New candidate status parsing performed by overlap/dry-run plan: no.
- Overlap rows reviewed by overlap/dry-run plan: 45.
- Currently authorized rows for status-only metric input overlay: 130.
- Unresolved candidate rows remain unauthorized after overlap/dry-run plan: 425.
- Timing fields filled by overlap/dry-run plan: no.
- Metric input authorization changed by overlap/dry-run plan: no.
- Metrics computed by overlap/dry-run plan: no.
- Generation Rate computed by overlap/dry-run plan: no.
- Execution Coverage Rate computed by overlap/dry-run plan: no.
- Result Consistency Rate computed by overlap/dry-run plan: no.
- Timing metrics computed by overlap/dry-run plan: no.
- Reports/results changed by overlap/dry-run plan: no.
- Denominator changed by overlap/dry-run plan: no.
- Paper results changed by overlap/dry-run plan: no.
- Raw legacy evidence changed by overlap/dry-run plan: no.
- status_only_metrics_dryrun_v0 completed: yes.
- Official metrics computed by status_only_metrics_dryrun_v0: no.
- Audit-only dry-run metrics computed by status_only_metrics_dryrun_v0: yes.
- Paper tables rendered by status_only_metrics_dryrun_v0: no.
- Timing metrics computed by status_only_metrics_dryrun_v0: no.
- Generation Rate dry-run created by status_only_metrics_dryrun_v0: yes.
- Execution Coverage Rate dry-run created by status_only_metrics_dryrun_v0: yes.
- Result Consistency Rate dry-run created by status_only_metrics_dryrun_v0: yes.
- Authorized input rows used by status_only_metrics_dryrun_v0: 130.
- Unauthorized overlap rows excluded by status_only_metrics_dryrun_v0: 45.
- Unresolved rows preserved by status_only_metrics_dryrun_v0: 425.
- Reports/results changed by status_only_metrics_dryrun_v0: no.
- Denominator changed by status_only_metrics_dryrun_v0: no.
- Paper results changed by status_only_metrics_dryrun_v0: no.
- Raw legacy evidence changed by status_only_metrics_dryrun_v0: no.
- status_field_normalization_v0 completed: yes.
- Authorized rows processed by status_field_normalization_v0: 130.
- Overlap rows excluded by status_field_normalization_v0: 45.
- Unresolved rows excluded by status_field_normalization_v0: 425.
- Rows needing manual mapping after status_field_normalization_v0: 0.
- Metrics computed by status_field_normalization_v0: no.
- Official metrics computed by status_field_normalization_v0: no.
- Timing fields filled by status_field_normalization_v0: no.
- Timing fields modified by status_field_normalization_v0: no.
- Paper tables rendered by status_field_normalization_v0: no.
- Reports/results changed by status_field_normalization_v0: no.
- Denominator changed by status_field_normalization_v0: no.
- Paper results changed by status_field_normalization_v0: no.
- Raw legacy evidence changed by status_field_normalization_v0: no.
- Original parser ledger modified by status_field_normalization_v0: no.
- normalized_status_only_metrics_dryrun_v1 completed: yes.
- Official metrics computed by normalized_status_only_metrics_dryrun_v1: no.
- Audit-only dry-run metrics computed by normalized_status_only_metrics_dryrun_v1: yes.
- Paper tables rendered by normalized_status_only_metrics_dryrun_v1: no.
- Timing metrics computed by normalized_status_only_metrics_dryrun_v1: no.
- Generation Rate dry-run created by normalized_status_only_metrics_dryrun_v1: yes.
- Execution Coverage Rate dry-run created by normalized_status_only_metrics_dryrun_v1: yes.
- Result Consistency Rate dry-run created by normalized_status_only_metrics_dryrun_v1: yes.
- Authorized input rows used by normalized_status_only_metrics_dryrun_v1: 130.
- Unauthorized overlap rows excluded by normalized_status_only_metrics_dryrun_v1: 45.
- Unresolved rows preserved by normalized_status_only_metrics_dryrun_v1: 425.
- Normalized overlay rows used by normalized_status_only_metrics_dryrun_v1: 130.
- Reports/results changed by normalized_status_only_metrics_dryrun_v1: no.
- Denominator changed by normalized_status_only_metrics_dryrun_v1: no.
- Paper results changed by normalized_status_only_metrics_dryrun_v1: no.
- Raw legacy evidence changed by normalized_status_only_metrics_dryrun_v1: no.
- status_inference_policy_v0 completed: yes.
- Official metrics computed by status_inference_policy_v0: no.
- Audit-only inference preview created by status_inference_policy_v0: yes.
- Parser ledgers modified by status_inference_policy_v0: no.
- Normalized overlay modified by status_inference_policy_v0: no.
- Timing fields filled by status_inference_policy_v0: no.
- Reports/results changed by status_inference_policy_v0: no.
- Denominator changed by status_inference_policy_v0: no.
- Paper results changed by status_inference_policy_v0: no.
- Raw legacy evidence changed by status_inference_policy_v0: no.
- Potential ready-implies-generated rows from status_inference_policy_v0: 94.
- Potential exact-implies-executed rows from status_inference_policy_v0: 0.
- status_inference_overlay_v0 completed: yes.
- normalized_status_only_metrics_dryrun_v2 completed: yes.
- Inference overlay rows from status_inference_overlay_v0: 94.
- Official metrics computed by normalized_status_only_metrics_dryrun_v2: no.
- Audit-only dry-run metrics computed by normalized_status_only_metrics_dryrun_v2: yes.
- Paper tables rendered by normalized_status_only_metrics_dryrun_v2: no.
- Timing metrics computed by normalized_status_only_metrics_dryrun_v2: no.
- Generation Rate dry-run created by normalized_status_only_metrics_dryrun_v2: yes.
- Execution Coverage Rate dry-run created by normalized_status_only_metrics_dryrun_v2: yes.
- Result Consistency Rate dry-run created by normalized_status_only_metrics_dryrun_v2: yes.
- Authorized input rows used by normalized_status_only_metrics_dryrun_v2: 130.
- Unauthorized overlap rows excluded by normalized_status_only_metrics_dryrun_v2: 45.
- Unresolved rows preserved by normalized_status_only_metrics_dryrun_v2: 425.
- Reports/results changed by status_inference_overlay_v0 and normalized_status_only_metrics_dryrun_v2: no.
- Denominator changed by status_inference_overlay_v0 and normalized_status_only_metrics_dryrun_v2: no.
- Paper results changed by status_inference_overlay_v0 and normalized_status_only_metrics_dryrun_v2: no.
- Raw legacy evidence changed by status_inference_overlay_v0 and normalized_status_only_metrics_dryrun_v2: no.
- candidate_status_evidence_completion_round1 completed: yes.
- Candidate statuses filled by evidence completion round1: no.
- Overlap rows reviewed by evidence completion round1: 45.
- SQLGlot candidate sources reviewed by evidence completion round1: 8.
- SQLGlot manifest preview rows from evidence completion round1: 10.
- Timing fields filled by evidence completion round1: no.
- Metrics computed by evidence completion round1: no.
- Generation Rate computed by evidence completion round1: no.
- Execution Coverage Rate computed by evidence completion round1: no.
- Result Consistency Rate computed by evidence completion round1: no.
- Timing metrics computed by evidence completion round1: no.
- Reports/results changed by evidence completion round1: no.
- Denominator changed by evidence completion round1: no.
- Paper results changed by evidence completion round1: no.
- Raw legacy evidence changed by evidence completion round1: no.
- overlap_priority_overlay_v1 completed: yes.
- normalized_status_only_metrics_dryrun_v3 completed: yes.
- Overlap rows reviewed by overlap_priority_overlay_v1: 45.
- Newly authorized overlap rows by overlap_priority_overlay_v1: 45.
- Still-blocked overlap rows after overlap_priority_overlay_v1: 0.
- v3 authorized input rows: 175.
- Official metrics computed by normalized_status_only_metrics_dryrun_v3: no.
- Audit-only dry-run metrics computed by normalized_status_only_metrics_dryrun_v3: yes.
- Paper tables rendered by normalized_status_only_metrics_dryrun_v3: no.
- Timing metrics computed by normalized_status_only_metrics_dryrun_v3: no.
- Generation Rate dry-run created by normalized_status_only_metrics_dryrun_v3: yes.
- Execution Coverage Rate dry-run created by normalized_status_only_metrics_dryrun_v3: yes.
- Result Consistency Rate dry-run created by normalized_status_only_metrics_dryrun_v3: yes.
- Unresolved rows after overlap_priority_overlay_v1 and dry-run v3: 425.
- Reports/results changed by overlap_priority_overlay_v1 and normalized_status_only_metrics_dryrun_v3: no.
- Denominator changed by overlap_priority_overlay_v1 and normalized_status_only_metrics_dryrun_v3: no.
- Paper results changed by overlap_priority_overlay_v1 and normalized_status_only_metrics_dryrun_v3: no.
- Raw legacy evidence changed by overlap_priority_overlay_v1 and normalized_status_only_metrics_dryrun_v3: no.
- SQLGlot sanitized non-timing projection completed: yes.
- SQLGlot candidate status parser completed: yes.
- SQLGlot rows filled by sqlglot_candidate_status_parser_v1: 137.
- SQLGlot rows unresolved after sqlglot_candidate_status_parser_v1: 103.
- Combined candidate status overlay v2 completed: yes.
- Combined candidate status overlay v2 filled rows: 312.
- Combined candidate status overlay v2 unresolved rows: 288.
- normalized_status_only_metrics_dryrun_v4 completed: yes.
- Official metrics computed by normalized_status_only_metrics_dryrun_v4: no.
- Audit-only dry-run metrics computed by normalized_status_only_metrics_dryrun_v4: yes.
- Paper tables rendered by normalized_status_only_metrics_dryrun_v4: no.
- Timing metrics computed by normalized_status_only_metrics_dryrun_v4: no.
- Reports/results changed by SQLGlot projection/parser v1 and dry-run v4: no.
- Denominator changed by SQLGlot projection/parser v1 and dry-run v4: no.
- Paper results changed by SQLGlot projection/parser v1 and dry-run v4: no.
- Raw legacy evidence changed by SQLGlot projection/parser v1 and dry-run v4: no.
- official_status_metrics_readiness_gate_v0 completed: yes.
- Official metrics computed by official_status_metrics_readiness_gate_v0: no.
- Paper tables rendered by official_status_metrics_readiness_gate_v0: no.
- Timing metrics computed by official_status_metrics_readiness_gate_v0: no.
- Reports/results changed by official_status_metrics_readiness_gate_v0: no.
- Denominator changed by official_status_metrics_readiness_gate_v0: no.
- Paper results changed by official_status_metrics_readiness_gate_v0: no.
- Raw legacy evidence changed by official_status_metrics_readiness_gate_v0: no.
- Combined filled rows reviewed by official_status_metrics_readiness_gate_v0: 312.
- Combined unresolved rows reviewed by official_status_metrics_readiness_gate_v0: 288.
- Generation Rate readiness: blocked_needs_policy_decision.
- Execution Coverage Rate readiness: ready_with_caveats.
- Result Consistency Rate readiness: ready_with_caveats.
- official_status_metrics_v0_limited completed: yes.
- Official status metrics computed by official_status_metrics_v0_limited: yes.
- Official Generation Rate computed by official_status_metrics_v0_limited: no.
- Official Execution Coverage Rate computed by official_status_metrics_v0_limited: yes.
- Official Result Consistency Rate computed by official_status_metrics_v0_limited: yes.
- Paper tables rendered by official_status_metrics_v0_limited: no.
- Timing metrics computed by official_status_metrics_v0_limited: no.
- Performance metrics computed by official_status_metrics_v0_limited: no.
- Reports/results changed by official_status_metrics_v0_limited: no.
- Denominator changed by official_status_metrics_v0_limited: no.
- Paper results changed by official_status_metrics_v0_limited: no.
- Raw legacy evidence changed by official_status_metrics_v0_limited: no.
- Generation Rate blocker by official_status_metrics_v0_limited: `inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap`.
- No global leaderboard.
- No new DB validation, timing rerun, evidence regeneration, benchmark result row, workload-frequency claim, production-frequency claim, speedup claim, ranking claim, or cross-engine result was created by case-package migration or final closeout.

## Completed Major Milestones

- Control-layer bootstrap completed.
- Canonical layout v1 locked.
- Static case package validator v0.3 implemented.
- Blocked PORT evidence-mapping resolved.
- Representative canonical pilots completed for PERF, CONS, PORT, and LONGTAIL.
- PERF pool canonical case-package migration complete: 16/16.
- CONS pool canonical case-package migration complete: 9/9.
- PORT pool canonical case-package migration complete: 9/9.
- LONGTAIL pool canonical case-package migration complete: 6/6.
- Common-core 40 canonical case-package migration complete: 40/40.
- Common-core v0 case-set, denominator scaffold, control scaffold, and public inventory registry alignment completed.
- Reports/results retained-evidence map completed without copying reports/results or changing metrics.
- Common-core retained evidence to draft ledger mapping audit completed without copying reports/results or implementing metrics.
- Evidence ledger semantics and adapter row-grain policy drafts completed without implementation.
- Metrics finalization decision packet completed without implementing metrics, adapters, reproduction interfaces, public runners, or paper table rendering.
- Metrics contract resolution draft completed without implementing metrics, adapters, reproduction interfaces, public runners, reports/results migration, or paper table rendering.
- Metrics Contract v1 formalized without implementing metrics, adapters, reproduction interfaces, public runners, reports/results migration, denominator changes, paper-result changes, or paper table rendering.
- Retained-evidence adapter design and validation plan completed without implementing adapters, computing metrics, creating scripts/source code, copying reports/results, rendering paper tables, changing denominators, changing paper results, or modifying raw legacy evidence.
- Ledger schema model and non-mutating validation fixtures completed without parsing production retained evidence, implementing adapters, computing metrics, creating scripts/source code, copying reports/results, rendering paper tables, changing denominators, changing paper results, or modifying raw legacy evidence.
- Ledger fixture validator skeleton completed for synthetic fixtures only, without parsing production retained evidence, implementing adapters, computing metrics, implementing a reproduction interface, rendering paper tables, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- Ledger fixture validator hardening and dev-smoke documentation completed for synthetic fixtures only, without parsing production retained evidence, implementing adapters, computing metrics, implementing a reproduction interface, rendering paper tables, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- Developer-only ledger fixture smoke entrypoint completed, wrapping the hardened synthetic validator without parsing production retained evidence, implementing adapters, computing metrics, implementing a reproduction interface, rendering paper tables, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- Ledger fixture CI smoke workflow completed, running synthetic fixture validation only and not parsing production retained evidence, implementing adapters, computing metrics, implementing a reproduction interface, rendering paper tables, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- Production ledger validation-gate planning completed without parsing production retained evidence, implementing a production ledger validator, implementing adapters, computing metrics, implementing a reproduction interface, rendering paper tables, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- retained_summary_adapter_v0 completed as a narrow release-repo-summary-only adapter skeleton, emitting 31 `retained_summary_artifact` audit rows without reading the legacy repo, parsing production retained evidence, authorizing metric input, computing metrics, implementing general adapters, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- Production ledger validator skeleton and control_cell_adapter_v0 completed as a bounded implementation, emitting and validating 360 `control_cell` rows without reading the legacy repo, parsing production retained evidence, authorizing metric input, computing metrics, implementing general adapters, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- hard_negative_control_detail_adapter_v0 completed as a bounded control-cell detail adapter, emitting and validating 120 hard-negative `control_cell` rows without reading the legacy repo, parsing production retained evidence, inferring fresh rejection outcomes, computing hard-negative rejection rate, computing false-accept rate, authorizing metric input, computing metrics, implementing general adapters, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- source_positive_control_detail_adapter_v0 completed as a bounded control-cell detail adapter, emitting and validating 240 source/positive `control_cell` rows without reading the legacy repo, parsing production retained evidence, inferring fresh execution or consistency outcomes, computing source-positive rate, computing Result Consistency Rate, authorizing metric input, computing metrics, implementing general adapters, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- Control-layer adapter closeout completed as an audit-only review, verifying 360/360 generic control rows, 240/240 source/positive detail rows, 120/120 hard-negative detail rows, 360/360 combined detail rows, exact route-level key coverage against `controls_360.csv`, passing adapter validations, and passing fixture smoke without implementing new adapters, parsing production retained evidence, reading the legacy repo, computing metrics, computing control rates, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- rewrite_candidate_adapter_v0 Track-A scaffold completed as a bounded rewrite-candidate scaffold, emitting and validating 600 planned `rewrite_candidate_cell` rows from the 120-row same-engine denominator and five authorized method routes without reading the legacy repo, parsing production retained evidence, parsing method outputs, parsing timing files, authorizing metric input, computing Generation Rate, computing Execution Coverage Rate, computing Result Consistency Rate, computing timing metrics, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- candidate_status_adapter_v0 completed as a bounded release-summary-only non-timing overlay, emitting and validating 600 `rewrite_candidate_cell` rows with 0 row-level statuses filled, 600 unresolved statuses, `metric_input_authorized=false`, and no legacy repo reads, production retained-evidence parsing, timing field fills, metric computation, reports/results changes, denominator changes, paper-result changes, or raw legacy evidence changes.
- Candidate retained-evidence parser approval packet completed as an audit/design packet, reviewing the unresolved candidate overlay and preparing maintainer decision materials without implementing a parser, parsing production retained evidence, reading the legacy repo, filling candidate row statuses, filling timing fields, authorizing metric input, computing metrics, updating reports/results, changing denominators, changing paper results, changing case membership, or modifying raw legacy evidence.
- candidate_status_parser_v0 completed as a manifest-first bounded non-timing parser, producing a header-only approved input manifest, emitting and validating 600 unresolved `rewrite_candidate_cell` rows, filling 0 row-level statuses, and keeping production retained-evidence parsing, legacy repo reads, timing fields, metric input authorization, metrics computation, reports/results changes, denominator changes, paper-result changes, case membership changes, and raw legacy evidence changes at no.
- Candidate status whitelist triage completed as an audit-only maintainer-review packet, producing a small whitelist proposal, manifest preview, manual decision sheet, rejected-source list, and review guide without parsing candidate statuses, filling timing fields, computing metrics, creating a production ledger, changing reports/results, changing denominators, changing paper results, changing case membership, modifying the legacy repo, or modifying raw legacy evidence.
- Candidate status parser v1 whitelist approval recorded for proposal IDs P001, P002, P003, P011, and P012 only, without implementing parser v1, parsing candidate statuses, filling timing fields, computing metrics, creating a production ledger, changing reports/results, changing denominators, changing paper results, changing case membership, modifying the legacy repo, or modifying raw legacy evidence.
- candidate_status_parser_v1 completed as a bounded non-timing approved-source parser, filling 175 row-level audit statuses from five approved legacy CSV sources and leaving 425 rows unresolved, without filling timing fields, authorizing metric input, computing metrics, creating a production ledger, updating reports/results, changing denominators, changing paper results, changing case membership, modifying the legacy repo, or modifying raw legacy evidence.
- candidate_status_parser_v1 closeout completed as an audit-only unresolved-row and metric-input readiness review, confirming 175 prior filled rows, 425 unresolved rows, 130 filled rows structurally ready for a future status-only authorization overlay, 45 filled rows requiring source-overlap review, approved-source contributions, documented non-blocking closeout overlap warnings, all metric/timing boundary checks passing, and no new parsing, metric-input authorization, metric computation, reports/results changes, denominator changes, paper-result changes, or raw legacy evidence changes.
- metric_input_authorization_overlay_v0 completed as an audit-only authorization overlay, authorizing 130 status-only non-timing parser-v1 rows, denying 45 overlap rows, leaving 425 unresolved rows unauthorized, and not rewriting the original parser ledger or computing metrics.
- Candidate status overlap review and status-only metrics dry-run plan completed as an audit-only planning packet, reviewing the 45 overlap-blocked rows, recommending manual source-by-source overlap selection before authorization, and planning a future status-only dry run from the 130 currently authorized rows without computing metrics, changing metric-input authorization, filling timing fields, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- status_only_metrics_dryrun_v0 completed as an audit-only dry run, creating Generation Rate, Execution Coverage Rate, and Result Consistency Rate dry-run tables from the 130 authorized status-only rows while preserving 45 unauthorized overlap rows and 425 unresolved rows in denominator/accounting outputs. It did not compute official metrics, render paper tables, compute timing metrics, update reports/results, change denominators, change paper results, or modify raw legacy evidence.
- status_field_normalization_v0 completed as an audit-only normalization overlay, processing exactly the 130 authorized candidate-status rows, excluding 45 overlap rows and 425 unresolved rows, inventorying all observed raw non-timing status values, and leaving original parser and authorization ledgers unchanged. It did not compute official metrics, render paper tables, fill or modify timing fields, update reports/results, change denominators, change paper results, or modify raw legacy evidence.
- normalized_status_only_metrics_dryrun_v1 completed as an audit-only normalized status dry run, creating Generation Rate, Execution Coverage Rate, and Result Consistency Rate dry-run tables from the 130 authorized normalized status rows while preserving 45 unauthorized overlap rows and 425 unresolved rows in denominator/accounting outputs. It did not compute official metrics, render paper tables, compute timing metrics, update reports/results, change denominators, change paper results, or modify raw legacy evidence.
- status_inference_policy_v0 completed as a policy/evidence-gap review, defining conservative observed-vs-inferred status rules, producing a preview-only inferred-status candidate overlay for 94 potential ready-implies-generated rows, confirming 0 potential exact-implies-executed rows, and documenting remaining evidence gaps without computing official metrics, changing metric input authorization, modifying parser ledgers or normalization overlays, filling timing fields, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- status_inference_overlay_v0 and normalized_status_only_metrics_dryrun_v2 completed as audit-only outputs, materializing 94 R1 inferred_generated rows as a separate overlay and creating v2 Generation Rate, Execution Coverage Rate, and Result Consistency Rate dry-run tables from 130 authorized rows while preserving 45 unauthorized overlap rows and 425 unresolved rows in denominator/accounting outputs. They did not compute official metrics, render paper tables, compute timing metrics, update reports/results, change denominators, change paper results, or modify raw legacy evidence.
- candidate_status_evidence_completion_round1 completed as an audit-only evidence-completion triage, reviewing 45 overlap-denied candidate-status rows and eight SQLGlot candidate evidence sources, producing overlap-resolution proposals, SQLGlot manual decision materials, and ten pending SQLGlot manifest-preview rows without filling statuses, changing metric-input authorization, computing metrics, filling timing fields, updating reports/results, changing denominators, changing paper results, changing case membership, or modifying raw legacy evidence.
- overlap_priority_overlay_v1 and normalized_status_only_metrics_dryrun_v3 completed as audit-only outputs, resolving all 45 overlap-denied candidate-status rows under maintainer-approved Option B, creating a combined 175-row metric-input authorization overlay, preserving 425 unresolved rows in denominator/accounting outputs, refreshing normalization for newly authorized overlap rows, and creating v3 Generation Rate, Execution Coverage Rate, and Result Consistency Rate dry-run tables. They did not compute official metrics, render paper tables, compute timing metrics, implement SQLGlot parsing, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence.
- SQLGlot sanitized non-timing projection and parser v1 completed as audit-only outputs, approving only SGL011 for sanitized non-timing status projection, creating two parser-ready SQLGlot projection files with 137 total rows, emitting 240 SQLGlot candidate-status rows with 137 filled and 103 unresolved, validating the SQLGlot ledger, building combined candidate status overlay v2 with 312 filled rows and 288 unresolved rows, and creating normalized status-only dry-run v4 outputs. It did not compute official metrics, render paper tables, compute timing/performance metrics, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.
- official_status_metrics_readiness_gate_v0 completed as a readiness-gate decision packet, reviewing combined candidate status overlay v2 and normalized dry-run v4, confirming 312 filled rows and 288 unresolved rows, classifying Generation Rate as `blocked_needs_policy_decision`, classifying Execution Coverage Rate and Result Consistency Rate as `ready_with_caveats`, and documenting denominator visibility requirements, risk controls, implementation-scope boundaries, and a maintainer decision template. It did not compute official metrics, render paper tables, compute timing/performance metrics, update reports/results, change denominators, change paper results, change case membership, or modify raw legacy evidence.
- official_status_metrics_v0_limited completed as a limited official status-metrics computation, computing official Execution Coverage Rate and Result Consistency Rate only from the authorized normalized status rows, preserving the 600-row planned denominator, keeping 425 unauthorized/unresolved rows visible, blocking Generation Rate with `inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap`, and forbidding global leaderboard output. It did not render paper tables, compute timing/performance metrics, update reports/results, change denominators, change paper results, change case membership, modify the legacy repo, or modify raw legacy evidence.
- Overnight governance and redevelopment investigation completed without migration, official staged/backlog membership creation, reports/results changes, script implementation, metrics computation, denominator changes, or raw legacy evidence changes.
- Staged/backlog membership preview completed without creating official staged/backlog case sets, migrating cases, modifying inventory, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- Clean public release export strategy adopted without deletion, history rewrite, release branch creation, migration, reports/results changes, case-set changes, denominator changes, paper-result changes, or raw legacy evidence changes.

## Remaining Non-Case-Package Blockers

- Public reports/results retained-evidence migration has not copied approved artifacts yet.
- Validation scripts are retained legacy assets, not final public user runners.
- Public runner and output policy are not done.
- Evidence ledger schema, metrics contract, retained evidence adapter, and script redevelopment plan are draft/planning artifacts unless explicitly promoted by later tasks.
- Metrics Contract v1 is formalized, retained-evidence adapter design is complete, synthetic ledger schema validation fixtures exist, a hardened synthetic-only fixture validator exists, a developer-only smoke entrypoint exists, CI wiring for synthetic fixture smoke exists, production ledger validation-gate planning is complete, retained_summary_adapter_v0 exists for release-repo summary artifacts only, control_cell_adapter_v0 exists for release case-package control rows, hard_negative_control_detail_adapter_v0 exists for release case-package hard-negative control detail rows only, source_positive_control_detail_adapter_v0 exists for release case-package source/positive control detail rows only, control-layer adapter closeout is complete, rewrite_candidate_adapter_v0 Track-A scaffold exists for planned candidate row grain only, candidate_status_adapter_v0 exists as a release-summary-only unresolved non-timing overlay, the candidate retained-evidence parser approval packet is available, candidate_status_parser_v0 exists as a fail-closed manifest-first non-timing parser with zero approved row-level inputs, candidate status whitelist triage is available, candidate_status_parser_v1 filled 175 non-timing audit rows from five approved sources and left 425 rows unresolved, parser-v1 closeout/readiness review is complete, and metric_input_authorization_overlay_v0 authorizes 130 status-only rows as audit overlay input candidates; production retained-evidence parsing beyond explicit manifest-approved row-level sources, general adapter implementation beyond the authorized bounded skeletons, metrics implementation, reproduction interface implementation, public runner implementation, and paper table rendering still require explicit authorization.
- Script inventory and reproduction path are not done.
- Case universe governance audit is complete; staged/backlog membership decisions are not yet approved.
- Overnight staged/backlog planning labels are available, but official staged/backlog membership files are not approved or created.
- Staged/backlog preview is available for maintainer review; official staged/backlog membership remains unapproved and uncreated.
- Public release skeleton gaps remain: README/docs/benchmark_spec, license/citation/contributing metadata, user/reproduction script namespaces, curated reports/results, tests, `src/`, and CI.
- Final public release surface pruning/export has not run yet; construction audits and project-control logs remain in this construction repository.
- Paper tables/results were not regenerated or changed.
- No release tag has been created.

## Current Next Safe Action

Review `audits/official_status_metrics_v0_limited/official_status_metrics_v0_limited_table.csv` and `audits/official_status_metrics_v0_limited/official_status_metrics_v0_limited_report.md`; separately decide whether to authorize SQLGlot metric-input expansion, resolve Generation Rate policy/evidence gaps, or prepare a paper-rendering decision packet. Keep timing adapter work, reports/results updates, denominator changes, and paper-result changes separate.
