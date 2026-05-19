# Post-cleanup V2 Template Parity Review

Task: `case_package_v2_post_cleanup_parity_review_v0`

Date: 2026-05-19

Branch: `feature/case-package-v2-external-schema`

## Purpose And Scope

This branch-only read-only review re-ran the clean-template parity review after `case_package_v2_reference_cleanup_execution_v0`.

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

No case package, schema package, evidence package, run artifact, case set, inventory, report, result, denominator, paper-result, metric, DB/checker execution output, or leaderboard output was modified by this review.

## Previous Cleanup Summary

The previous cleanup selected 10 `deletion_ready_after_reference_update` candidates and removed only:

- tracked nested SQL compatibility paths: `sql/positives/` and `sql/negatives/`
- tracked copied case-local notes: `notes/`

It skipped 5 placeholder-only case-local `runs/` candidates because those require retention mapping or explicit retained-runs cleanup approval.

## Post-cleanup Parity Status

All five pilot cases retain every clean-template-required asset:

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- `sql/pos_01.sql`
- `sql/neg_01.sql`
- `schema/schema_profile.yaml`
- checker configuration files
- canonical validation wrappers

All five pilot cases pass the static v2 validator after cleanup. They are acceptable as a functional v2 pilot with compatibility residues.

They are not yet clean-template-minimal. Remaining tracked extra path groups total 66:

- 15 case-local executable schema engine directories
- 5 case-local retained evidence directories
- 5 metadata directories
- 5 data fixture/profile directories
- 5 placeholder-only case-local `runs/` directories
- 30 retained engine-specific validation scripts
- 1 `PORT_0003` dialect-variant SQL directory

## Remaining Gaps By Category

- `removed_by_previous_cleanup`: tracked `sql/positives/`, `sql/negatives/`, and `notes/` have been removed for all five cases.
- `retained_evidence_mapping_required`: case-local `evidence/` remains for all five and must not be deleted without retention mapping.
- `retained_runs_mapping_required`: case-local `runs/README.md` remains for all five and needs an explicit retained-runs cleanup/mapping decision.
- `runner_validator_migration_required`: case-local `schema/<engine>/` DDL/load copies remain until v2-only runner/schema-profile resolution is fully accepted for cleanup.
- `source_of_truth_review_required`: case-local `metadata/` remains until manifest/external-reference source-of-truth review is complete.
- `witness_data_policy_review_required`: case-local `data/` remains until witness/data fixture policy confirms redundancy or externalization.
- `shared_logic_audit_required`: retained engine-specific validation scripts remain until shared wrappers fully replace legacy scripts and caller references are audited.
- `manual_review_required`: `PORT_0003` retains `sql/dialect_variants/spark/` for portability-specific review.

## Remaining Runs/Evidence Retention Blockers

Remaining retention blockers count: 10.

- 5 case-local `evidence/` directories require retained-evidence mapping before deletion.
- 5 case-local `runs/README.md` placeholders require explicit retained-runs cleanup approval.

These blockers prevent clean-template-minimal parity, but they do not block planning the broader Common-core 40 v2 conversion because the functional v2 case structure and static validator compatibility are in place.

## Functional Pilot Acceptance

Functional v2 pilot status: `accepted_with_retained_compatibility_gaps`.

Rationale:

- required v2 assets exist for all five pilot cases
- profile-first schema references validate
- direct SQL paths validate
- checker and validation canonical refs validate
- witness/evidence refs validate
- optional witness static files follow source-as-oracle policy
- no protected benchmark surfaces changed

## Clean-template Pilot Acceptance

Clean-template pilot status: `not_clean_template_minimal`.

The pilot is not clean-template-minimal because retained evidence, placeholder runs, case-local schema engine copies, metadata, data fixtures, old validation scripts, and `PORT_0003` dialect variants remain.

## Recommended Next Action

Authorize `case_package_v2_common_core40_conversion_plan_v0` as a read-only planning task only. It should use the five-case pilot as a functional v2 template, preserve the same protected boundaries, and explicitly carry forward retained-evidence/runs/schema/metadata/data/validation cleanup as separate non-blocking cleanup tracks.
