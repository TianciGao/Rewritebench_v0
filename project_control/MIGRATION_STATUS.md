# SQL-RewriteBench Migration Status Snapshot

Date: 2026-05-17

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
- Metrics implementation authorized: no.
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
- Overnight governance and redevelopment investigation completed without migration, official staged/backlog membership creation, reports/results changes, script implementation, metrics computation, denominator changes, or raw legacy evidence changes.
- Staged/backlog membership preview completed without creating official staged/backlog case sets, migrating cases, modifying inventory, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- Clean public release export strategy adopted without deletion, history rewrite, release branch creation, migration, reports/results changes, case-set changes, denominator changes, paper-result changes, or raw legacy evidence changes.

## Remaining Non-Case-Package Blockers

- Public reports/results retained-evidence migration has not copied approved artifacts yet.
- Validation scripts are retained legacy assets, not final public user runners.
- Public runner and output policy are not done.
- Evidence ledger schema, metrics contract, retained evidence adapter, and script redevelopment plan are draft/planning artifacts unless explicitly promoted by later tasks.
- Metrics Contract v1 is formalized, retained-evidence adapter design is complete, synthetic ledger schema validation fixtures exist, a hardened synthetic-only fixture validator exists, a developer-only smoke entrypoint exists, CI wiring for synthetic fixture smoke exists, production ledger validation-gate planning is complete, retained_summary_adapter_v0 exists for release-repo summary artifacts only, control_cell_adapter_v0 exists for release case-package control rows, hard_negative_control_detail_adapter_v0 exists for release case-package hard-negative control detail rows only, source_positive_control_detail_adapter_v0 exists for release case-package source/positive control detail rows only, control-layer adapter closeout is complete, and rewrite_candidate_adapter_v0 Track-A scaffold exists for planned candidate row grain only; production retained-evidence parsing, general adapter implementation beyond the authorized bounded skeletons, metrics implementation, reproduction interface implementation, public runner implementation, and paper table rendering still require explicit authorization.
- Script inventory and reproduction path are not done.
- Case universe governance audit is complete; staged/backlog membership decisions are not yet approved.
- Overnight staged/backlog planning labels are available, but official staged/backlog membership files are not approved or created.
- Staged/backlog preview is available for maintainer review; official staged/backlog membership remains unapproved and uncreated.
- Public release skeleton gaps remain: README/docs/benchmark_spec, license/citation/contributing metadata, user/reproduction script namespaces, curated reports/results, tests, `src/`, and CI.
- Final public release surface pruning/export has not run yet; construction audits and project-control logs remain in this construction repository.
- Paper tables/results were not regenerated or changed.
- No release tag has been created.

## Current Next Safe Action

Review the `rewrite_candidate_adapter_v0` scaffold row grain and method scope before authorizing any candidate evidence adapter that parses retained method outputs, fills generated/executed/exact/timed statuses, authorizes metric input, or computes metrics. Do not parse production retained evidence, implement general candidate adapters, compute metrics, render paper tables, update reports/results, change denominator values, or modify raw legacy evidence without separate authorization.
