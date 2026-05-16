# SQL-RewriteBench Migration Status Snapshot

Date: 2026-05-16

## Repository Roles

- Legacy/source repository: `sql-rewrite-bench-artifact-clean`.
- Public release repository: `Rewritebench_v0`.
- Chronological execution history lives in `project_control/MIGRATION_RUN_LOG.md`.
- This file is the concise current-state snapshot.

## Current Status Summary

Common-core case-package migration is complete at canonical-layout package level: 40/40 Common-core cases now have canonical public-release case packages.

This status is based on release-repo files and validator v0.3 outputs, including the LONGTAIL final bounded canonical migration audit under `audits/longtail_final_bounded_migration/`.

Common-core 40 blind/bulk migration was not started. Completed work remained bounded, explicit, and case-package scoped.

## Common-core Case-Package Counts

| Pool | Canonical complete | Common-core total | Status |
|---|---:|---:|---|
| PERF | 16 | 16 | complete |
| CONS | 9 | 9 | complete |
| PORT | 9 | 9 | complete |
| LONGTAIL | 6 | 6 | complete |
| Total | 40 | 40 | complete |

Validator snapshot:

- Full-case validator v0.3: PASS 40/40 over all canonical Common-core case packages.
- Canonical-case validator v0.3: PASS 40/40 over all canonical Common-core case packages.
- `PORT_0004` is canonical after the PORT final bounded batch.
- `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` are canonical after the LONGTAIL final bounded batch.

## Explicit Boundaries

- Common-core denominator unchanged.
- Track A 120 planned rows unchanged.
- Paper results unchanged.
- Case membership unchanged.
- `case_sets/` not updated by migration batches.
- `reports/` and `results/` not updated by migration batches.
- Raw legacy evidence unchanged.
- No global leaderboard.
- No new DB validation, timing rerun, evidence regeneration, benchmark result row, workload-frequency claim, production-frequency claim, speedup claim, ranking claim, or cross-engine result was created by case-package migration.

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
- Common-core case-package migration complete: 40/40 canonical packages.

## Current Blockers

- Validation scripts are retained legacy assets, not final public user runners.
- Reports/results retained evidence map is not done.
- Script inventory and public runner path are not done.
- Case universe 197 vs 190 governance reconciliation is still pending.
- No case-set, report, result, denominator, or paper-table update should occur without a separate approved task.

## Current Next Safe Action

Review the final LONGTAIL migration audit under `audits/longtail_final_bounded_migration/`, then perform a separate Common-core 40 case-package completion closeout if desired. Do not touch `case_sets/`, `reports/`, `results/`, denominator files, or paper tables yet.
