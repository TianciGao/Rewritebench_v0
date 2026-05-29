# Clean Template Gap Closure Execution Summary

## Purpose and Scope

Task: `case_package_v2_clean_template_gap_closure_execution_v0`. This branch-only cleanup attempted to close remaining clean-template gaps for the five v2 pilot cases without changing benchmark protected surfaces or running DB/checker execution.

Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, `LONGTAIL_0011`.

## Remaining Gaps Before Task

The latest post-empty-runs parity review recorded `61` remaining extra path groups and 5 retention-blocker cases. The pilot was functionally accepted as v2 with compatibility gaps, but not clean-template-minimal.

## Cleanup Actions Attempted

- Verified profile-first schema references and external schema profiles for all five cases.
- Verified case-local schema engine files are byte-identical to external `schemas/<SCHEMA_ID>/<engine>/` copies.
- Verified case-local evidence files have byte-identical external copies under `evidence/cases/<POOL>/<CASE_ID>/`, mapping `retained_plans/` to external `plans/`.
- Removed case-local `metadata/` directories after stable metadata was represented in manifest/README compatibility summaries and existing project controls.
- Removed case-local `data/` directories after data context was represented by external schema load files and source-as-oracle witness policy.
- Updated manifests and READMEs to remove stale metadata/data/runs compatibility path references.

## Files and Directories Deleted

Deleted path groups: 10.

- `metadata/` for all five pilot cases.
- `data/` for all five pilot cases.

Tracked deleted files are listed in `gap_closure_deletions_manifest.csv` at the directory-group level and in git diff at file level.

## Files and Directories Skipped

Skipped path groups: 51.

- `schema/postgres/`, `schema/mysql/`, and `schema/spark/` for each case: external copies are verified, but retained legacy validation scripts still reference case-local schema paths.
- case-local `evidence/` for each case: external copies are verified, but checker/witness references still point to case-local evidence and those layers are out of this task's write scope.
- old engine-specific validation scripts for each case: retained because they contain unique legacy DB execution or plan collection behavior not yet covered by shared wrappers.
- `PORT_0003/sql/dialect_variants/`: retained as semantically meaningful portability material.

## Blockers Remaining

Post-task extra path groups: 51. Post-task blockers: 51.

The five cases remain `functional_v2_with_explicit_blockers`, not clean-template-minimal. The blockers require a future targeted task for checker/witness evidence reference cleanup, validation legacy-script migration, and an explicit PORT dialect-variant decision.

## Protected Boundary Summary

No case_sets, inventory, reports, results, denominators, paper results, retained evidence, or unsafe evidence were changed. No DB/checker execution, official metrics, paper rendering, or global leaderboard creation was performed.

## Validation

- Static v2 validator passed for all five pilot cases.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v` passed: 9 tests.

## Exact Next Safe Action

Run a second targeted cleanup/planning task to update checker/witness evidence references and retire or replace legacy engine-specific validation scripts; only after that should schema engine compatibility directories and case-local evidence be reconsidered for deletion. Common-core 40 planning can proceed only if these explicit blockers are accepted as pilot carry-forward constraints.
