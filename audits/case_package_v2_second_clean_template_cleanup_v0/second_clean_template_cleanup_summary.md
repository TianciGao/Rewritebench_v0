# Second Clean-template Cleanup Summary

## Purpose and Scope

`case_package_v2_second_clean_template_cleanup_v0` was a branch-only writable cleanup for the five v2 pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`. It deleted only paths readiness-marked by the clean-template gap closure and validation/evidence unblock audits.

This task did not run DB/checker execution, compute official metrics, update reports/results, change denominators, alter case membership, render paper tables, or create leaderboard output.

## Deletion Set Source

- `schema_cleanup_readiness_after_unblock.csv`: 15 case-local schema engine directories marked ready.
- `legacy_validation_script_cleanup_readiness.csv`: 30 legacy engine-specific validation scripts marked ready after wrapper update.
- `evidence_reference_unblock_results.csv` plus prior skipped-manifest context: 5 case-local evidence directories ready after external mapping verification.

## Actions Performed

- Deleted 30 old engine-specific validation scripts after confirming v2 wrappers do not call them.
- Deleted 15 case-local `schema/<engine>/` directories after verifying byte-identical external DDL/load under `schemas/<SCHEMA_ID>/`.
- Deleted 5 case-local `evidence/` compatibility copies after verifying byte-identical external evidence under `evidence/cases/<POOL>/<CASE_ID>/`.
- Updated manifest compatibility statuses and README wording so live references no longer describe those paths as retained current compatibility assets.

## Skipped or Retained

- `PORT_0003/sql/dialect_variants/` was retained as a semantically meaningful optional v2 portability asset. It is not a clean-template blocker.
- No metadata, data, reports/results, case sets, inventory, unsafe evidence, retained external evidence, or dialect variants were deleted.

## Post-cleanup Status

All five pilot cases pass the static v2 validator after cleanup. All clean-template-required tracked assets are present. The only remaining path group in the post-cleanup gap matrix is `PORT_0003/sql/dialect_variants/`, retained as an optional v2 semantic asset; blocker count is zero.

## Protected Boundary Summary

Protected benchmark surfaces were unchanged: no `case_sets/`, inventory, reports/results, denominator, paper-result, official metric, DB/checker execution, or leaderboard output changed. Retained evidence was preserved externally under `evidence/cases/`; this task removed only verified case-local compatibility copies.

## Exact Next Safe Action

Authorize pilot acceptance or a read-only Common-core 40 conversion plan using the five-case clean-template-minimal pilot; keep `PORT_0003/sql/dialect_variants/` unless a future portability review approves cleanup.
