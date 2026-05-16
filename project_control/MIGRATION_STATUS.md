# SQL-RewriteBench Migration Status Snapshot

Date: 2026-05-16

## Repository Roles

- Legacy/source repository: `sql-rewrite-bench-artifact-clean`.
- Public release repository: `Rewritebench_v0`.
- Chronological execution history lives in `project_control/MIGRATION_RUN_LOG.md`.
- This file is the concise current-state snapshot.

## Current Status Summary

Common-core case-package migration is partially complete at canonical-layout package level. PERF, CONS, and PORT are complete; LONGTAIL has one completed representative canonical package and five remaining cases.

This status snapshot is based on release-repo file inspection and validator v0.3 closeout outputs under `audits/common_core40_case_package_closeout/`.

Common-core 40 blind/bulk migration is still not started. Completed migration work remains bounded, explicit, and case-package scoped.

## Common-core Case-Package Counts

| Pool | Canonical complete | Common-core total | Status |
|---|---:|---:|---|
| PERF | 16 | 16 | complete |
| CONS | 9 | 9 | complete |
| PORT | 9 | 9 | complete |
| LONGTAIL | 1 | 6 | remaining cases not yet canonical |
| Total | 35 | 40 | not complete |

Validator snapshot:

- Full-case validator v0.3: PASS 35/35 over current canonical-complete cases.
- Canonical-case validator v0.3: PASS 35/35 over current canonical-complete cases.
- `PORT_0004` is now canonical after the PORT final bounded batch.

## Remaining Common-core Cases

The remaining not-yet-canonical Common-core cases are:

- `LONGTAIL_0012`
- `LONGTAIL_0013`
- `LONGTAIL_0022`
- `LONGTAIL_0023`
- `LONGTAIL_0024`

## Explicit Boundaries

- Common-core 40 case-package migration is not complete.
- Common-core denominator unchanged.
- Track A 120 planned rows unchanged.
- Paper results unchanged.
- Case membership unchanged.
- `case_sets/` not updated by migration batches.
- `reports/` and `results/` not updated by migration batches.
- Raw legacy evidence unchanged.
- No global leaderboard.
- No new DB validation, timing rerun, evidence regeneration, benchmark result row, or cross-engine result was created by the migration closeout.

## Completed Major Milestones

- Control-layer bootstrap completed.
- Canonical layout v1 locked.
- Static case package validator v0.3 implemented.
- Blocked PORT evidence-mapping resolved.
- Representative canonical pilots completed for PERF, CONS, PORT, and LONGTAIL.
- PERF pool canonical case-package migration complete: 16/16.
- CONS pool canonical case-package migration complete: 9/9.
- PORT pool canonical case-package migration complete: 9/9.
- `LONGTAIL_0011` representative canonical pilot complete.

## Current Blockers

- Remaining LONGTAIL cases need structure and hard-negative review before migration.
- Validation scripts are retained legacy assets, not final public user runners.
- Hard-negative static approvals and review sweep may still be needed for final polish.
- Reports/results retained evidence map is not done.
- Script inventory and public runner path are not done.
- Case universe 197 vs 190 governance reconciliation is still pending.

## Current Next Safe Action

Review the closeout under `audits/common_core40_case_package_closeout/`, then plan the remaining LONGTAIL bounded wave. Do not touch `case_sets/`, `reports/`, `results/`, denominator files, or paper tables yet.
