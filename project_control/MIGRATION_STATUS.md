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
- Overnight governance and redevelopment investigation completed without migration, official staged/backlog membership creation, reports/results changes, script implementation, metrics computation, denominator changes, or raw legacy evidence changes.
- Staged/backlog membership preview completed without creating official staged/backlog case sets, migrating cases, modifying inventory, updating reports/results, changing denominators, changing paper results, or modifying raw legacy evidence.
- Clean public release export strategy adopted without deletion, history rewrite, release branch creation, migration, reports/results changes, case-set changes, denominator changes, paper-result changes, or raw legacy evidence changes.

## Remaining Non-Case-Package Blockers

- Public reports/results retained-evidence migration has not copied approved artifacts yet.
- Validation scripts are retained legacy assets, not final public user runners.
- Public runner and output policy are not done.
- Evidence ledger schema, metrics contract, retained evidence adapter, and script redevelopment plan are draft/planning artifacts only.
- Metrics Contract v1 is formalized, retained-evidence adapter design is complete, synthetic ledger schema validation fixtures exist, a hardened synthetic-only fixture validator exists, and a developer-only smoke entrypoint exists; production retained-evidence parsing, adapter implementation, metrics implementation, reproduction interface implementation, public runner implementation, and paper table rendering still require explicit authorization.
- Script inventory and reproduction path are not done.
- Case universe governance audit is complete; staged/backlog membership decisions are not yet approved.
- Overnight staged/backlog planning labels are available, but official staged/backlog membership files are not approved or created.
- Staged/backlog preview is available for maintainer review; official staged/backlog membership remains unapproved and uncreated.
- Public release skeleton gaps remain: README/docs/benchmark_spec, license/citation/contributing metadata, user/reproduction script namespaces, curated reports/results, tests, `src/`, and CI.
- Final public release surface pruning/export has not run yet; construction audits and project-control logs remain in this construction repository.
- Paper tables/results were not regenerated or changed.
- No release tag has been created.

## Current Next Safe Action

Review the developer-only ledger fixture smoke entrypoint and decide whether to add CI wiring for synthetic fixture validation or plan separately authorized production ledger validation gates; do not parse production retained evidence, implement retained-evidence adapters, compute metrics, render paper tables, update reports/results, change denominator values, or modify raw legacy evidence without separate authorization.
