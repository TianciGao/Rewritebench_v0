# SQL-RewriteBench Migration Status Snapshot

Date: 2026-05-16

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

Current phase: Workbench redevelopment phase.

The next phase is redevelopment-led public workbench construction around canonical Common-core 40 packages, an evidence ledger schema, metrics contract, runner/output policy, retained evidence adapter, user-facing candidate runner, reproduction/report renderer, and public documentation. Legacy scripts, reports, and results are reference inputs, retained evidence sources, or adapter targets, not the architecture to copy wholesale.

Important blocker: before implementing a unified reproduction CLI, paper table renderer, or metrics computation, the maintainer/team must confirm final metric definitions after team discussion.

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

## Explicit Boundaries

- Common-core denominator unchanged.
- Track A 120 planned rows unchanged.
- Paper results unchanged.
- Case membership unchanged.
- `case_sets/` aligned for fixed Common-core v0 membership; no membership change.
- `inventory/` aligned for fixed Common-core v0 scope.
- `reports/` not updated by case-package migration or final closeout.
- `results/` not updated by case-package migration or final closeout.
- Reports/results retained-evidence map completed; actual release reports/results files unchanged.
- Retained evidence to ledger mapping audit completed; actual release reports/results files unchanged.
- Denominator files and paper tables not updated by case-package migration or final closeout.
- Raw legacy evidence unchanged.
- Metrics implementation authorized: no.
- Unified reproduction interface implementation authorized: no.
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

## Remaining Non-Case-Package Blockers

- Public reports/results retained-evidence migration has not copied approved artifacts yet.
- Validation scripts are retained legacy assets, not final public user runners.
- Public runner and output policy are not done.
- Evidence ledger schema, metrics contract, retained evidence adapter, and script redevelopment plan are draft/planning artifacts only.
- Final metric definitions are not approved for implementation.
- Script inventory and reproduction path are not done.
- Case universe 197 vs 190 governance reconciliation is still pending.
- Paper tables/results were not regenerated or changed.
- No release tag has been created.

## Current Next Safe Action

Review the redevelopment draft specs and resolve the open metric/reproduction-interface questions with the maintainer/team. Do not implement metrics computation, a unified reproduction CLI, paper table renderer, reports/results migration, denominator changes, paper table changes, or raw evidence changes until those definitions are confirmed.
