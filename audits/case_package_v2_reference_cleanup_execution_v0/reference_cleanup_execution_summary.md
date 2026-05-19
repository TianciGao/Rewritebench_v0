# V2 Compatibility Reference Cleanup Execution Summary

Task: `case_package_v2_reference_cleanup_execution_v0`

Date: 2026-05-19

Branch: `feature/case-package-v2-external-schema`

## Purpose And Scope

This branch-only writable cleanup task updated live compatibility references and removed only candidates classified as `deletion_ready_after_reference_update` in the reference cleanup plan.

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Out of scope and untouched: `runs/`, `evidence/`, schema engine DDL/load files, `metadata/` deletion, `data/`, validation engine-specific script deletion, retained evidence, `case_sets/`, inventory, reports/results, denominators, paper results, DB/checker execution, official metrics, and leaderboard output.

## Selected Candidates

Selected candidates count: 10.

- Five nested SQL compatibility directory pairs: `sql/positives/` and `sql/negatives/`.
- Five copied case-local notes directories: `notes/`.

Skipped candidates count: 5.

- The five placeholder-only `runs/` candidates remain skipped because they are classified as `deletion_ready_after_retention_mapping`, not `deletion_ready_after_reference_update`.

## Live References Updated

Reference update rows recorded: 62.

Updated live references included:

- Manifest compatibility fields for nested SQL and notes.
- README wording for externalized notes.
- Checker config and expected-rejection paths.
- Metadata artifact path references.
- Retained validation-script references from nested SQL to direct SQL paths.
- Retained validation-script comments from case-local notes to external evidence notes where present.

Historical audit and repository-spec references were not rewritten.

## Files And Directories Removed

Deleted candidates count: 10.

Removed only:

- `sql/positives/`
- `sql/negatives/`
- `notes/`

No retained evidence, case-local evidence, schema engine files, metadata files, data files, validation scripts, or runs files were deleted.

## Validation Summary

Static v2 validation passed for all five pilot cases after cleanup. Unit tests passed. JSON boundary assertions passed. Protected path checks passed. `git diff --check` passed.

## Protected Boundary Summary

- Retained evidence deleted: no.
- Runs deleted: no.
- Evidence deleted: no.
- Schema engine files deleted: no.
- Metadata deleted: no.
- Data deleted: no.
- Validation engine-specific scripts deleted: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- Legacy repo modified: no.

## Exact Next Safe Action

Authorize `case_package_v2_post_cleanup_parity_review_v0` to re-run a read-only clean-template parity review for the five pilot cases after reference cleanup, with no DB/checker execution, retained-evidence deletion, protected benchmark-surface changes, official metrics, paper rendering, or leaderboard output.
