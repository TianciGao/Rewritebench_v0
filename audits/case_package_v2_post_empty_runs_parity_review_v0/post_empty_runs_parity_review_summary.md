# Post-empty-runs V2 Template Parity Review

Task: `case_package_v2_post_empty_runs_parity_review_v0`

Date: 2026-05-19

Branch: `feature/case-package-v2-external-schema`

## Purpose And Scope

This branch-only read-only review re-ran clean-template parity checks for the five v2 pilot cases after `case_package_v2_empty_runs_cleanup_v0` deleted audited placeholder-only case-local `runs/` directories.

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

No case package, schema package, evidence package, run artifact, case set, inventory, report, result, denominator, paper-result, metric, DB/checker execution output, or leaderboard output was modified by this review.

## Previous Cleanup Summary

The empty-runs cleanup selected 99 audited placeholder-only case-local `runs/` directories across the branch and deleted all 99. For the five pilot cases, no tracked `runs/` files remain. The audited absent case remained out of scope.

This review counts branch-tracked content as the public-release parity surface. Some empty local directories left by previous tracked-file deletions may exist in the working filesystem, but they are not branch-tracked assets and are not counted as clean-template gaps.

## Post-empty-runs Parity Status

All five pilot cases retain every clean-template-required asset:

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- `sql/pos_01.sql`
- `sql/neg_01.sql`
- `schema/schema_profile.yaml`
- checker configuration files
- canonical validation wrappers

Static v2 validation passed for all five pilot cases after the empty-runs cleanup.

## Remaining Extra Paths

Remaining tracked extra path groups: 61.

Breakdown:

- 15 case-local executable schema engine directories
- 5 case-local retained evidence directories
- 5 metadata directories
- 5 data fixture/profile directories
- 30 retained engine-specific validation scripts
- 1 `PORT_0003` dialect-variant SQL directory
- 0 tracked case-local `runs/` directories or files for the five pilot cases

## Remaining Retention Blockers

Remaining retention blockers: 5.

Only case-local `evidence/` remains retention-blocked for the five pilot cases. The prior five placeholder-only `runs/` blockers are gone after the accepted runs policy refinement and cleanup.

## Case Classifications

All five pilot cases classify as `functional_v2_with_compatibility_gaps`.

No pilot case is `clean_template_minimal` yet because case-local evidence, case-local schema engine copies, metadata, data/profile files, old validation scripts, and the `PORT_0003` dialect variant remain.

No pilot case is `manual_review_required` for functional v2 validation. Manual review remains only for cleanup of specific compatibility assets, especially retained evidence and `PORT_0003` dialect variants.

## Clean-template Minimal Decision

The five-case pilot cannot yet be accepted as clean-template-minimal.

The pilot can be accepted as a functional v2 pilot with compatibility gaps because required assets and v2 references validate, protected benchmark surfaces are unchanged, and remaining gaps are cleanup-track issues rather than functional v2 blockers.

## Common-core 40 Planning Decision

Common-core 40 conversion planning is safe as a read-only planning task. The plan should use the five-case pilot as the functional v2 template and keep evidence/schema/metadata/data/validation-script cleanup as separate cleanup tracks.

## Protected Boundary Summary

- Cases modified: no.
- Schemas modified: no.
- Evidence modified: no.
- Runs deleted in this task: no.
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

Authorize `case_package_v2_common_core40_conversion_plan_v0` as a read-only planning task using the five-case pilot as a functional v2 template. Keep clean-template-minimal cleanup separate and blocked on retained-evidence mapping, schema cleanup approval, metadata/data review, validation-script caller audit, and `PORT_0003` dialect-variant manual review.
