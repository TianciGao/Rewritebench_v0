# Validation/Evidence Unblock Summary

## Purpose and Scope

Task: `case_package_v2_validation_evidence_unblock_v0`. This branch-only targeted unblock updated live references that prevented a second clean-template cleanup for the five v2 pilot cases. It did not delete schema engine directories, case-local evidence, metadata, data, old validation scripts, dialect variants, or retained evidence.

Pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, `LONGTAIL_0011`.

## Blockers Before Task

The prior gap closure left 51 explicit path blockers: 15 schema engine directories, 5 case-local evidence directories, 30 legacy engine-specific validation scripts, and `PORT_0003/sql/dialect_variants/`.

## Validation Wrapper Reference Updates

Updated 10 v2 wrapper entrypoints:

- `validation/run_validation.sh` for all five cases.
- `validation/run_plan_collection.sh` for all five cases.

The wrappers now fail closed with explicit `shared v2 ... runner not implemented; use future shared runner` messages. They do not call old engine-specific scripts, do not reference case-local `schema/<engine>/`, and continue to refuse case-local `runs/` output.

## Evidence Reference Updates

Current checker, witness, manifest, and README references now prefer external `evidence/cases/<POOL>/<CASE_ID>/` paths. Case-local `evidence/` remains undeleted compatibility only and is no longer treated as the canonical current evidence location.

External evidence packages were present for all five pilot cases before these references were retargeted.

## Schema Deletion Readiness After Unblock

All 15 case-local schema engine directories are marked deletion-ready for the next cleanup task, provided the retained legacy validation scripts are deleted first or in the same cleanup task. External schema DDL/load copies are verified and v2 wrappers no longer use case-local schema paths.

## Legacy Validation Script Deletion Readiness

All 30 legacy engine-specific validation scripts are classified as `deletion_ready_after_wrapper_update`. They may contain unique legacy DB or plan-collection logic, but clean v2 wrappers fail closed and no longer delegate to those scripts. They were not deleted in this task.

## Remaining Blockers

The remaining intentional v2 retention item is `PORT_0003/sql/dialect_variants/`, which is a semantically retained optional portability asset. It should remain unless a future portability review proves it stale.

## Protected Boundary Summary

No schema engine directories, case-local evidence, metadata, data, old validation scripts, dialect variants, retained evidence, `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker outputs, or leaderboard outputs were deleted or changed.

## Validation

- Static v2 validator passed for all five pilot cases.
- Unit tests passed: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.

## Exact Next Safe Action

Authorize `case_package_v2_second_clean_template_cleanup_v0` to delete only paths now marked ready: legacy engine-specific validation scripts, case-local schema engine directories after script deletion, and case-local evidence directories after one final external evidence mapping check. Keep `PORT_0003/sql/dialect_variants/` unless a separate portability review approves deletion.
