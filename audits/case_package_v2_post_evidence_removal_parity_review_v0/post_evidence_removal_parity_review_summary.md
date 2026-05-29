# Post Evidence Removal Parity Review Summary

Task: `case_package_v2_post_evidence_removal_parity_review_v0`

Branch: `feature/case-package-v2-external-schema`

## Purpose and Scope

This branch-only read-only review rechecked the five v2 pilot cases after `evidence_ref` was replaced by regeneration-first `evidence_policy` and the five top-level static `evidence/cases/<POOL>/<CASE_ID>/` packages were deleted.

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

No case package, schema, evidence, report/result, inventory, or case-set files were modified by this review.

## Clean Template Result

All five pilot cases have the required tracked clean-template assets:

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- `sql/pos_01.sql`
- `sql/neg_01.sql`
- `schema/schema_profile.yaml`
- `checker/checker.yaml`
- `checker/normalization.yaml`
- `checker/compare_config.yaml`
- `checker/expected_rejections.yaml`
- `validation/run_validation.sh`
- `validation/run_plan_collection.sh`
- optional `witness/` files where applicable

All five manifests now use regeneration-first `evidence_policy` and do not contain `evidence_ref`.

## Evidence Surface Result

The five top-level static evidence packages are absent:

- `evidence/cases/PERF/PERF_0006/`
- `evidence/cases/PERF/PERF_0007/`
- `evidence/cases/CONS/CONS_0005/`
- `evidence/cases/PORT/PORT_0003/`
- `evidence/cases/LONGTAIL/LONGTAIL_0011/`

Case-local `evidence/` directories are also absent for all five pilot cases.

## Remaining Extra Path

The only tracked extra path group in the five pilot branch surface is:

- `cases/PORT/PORT_0003/sql/dialect_variants/spark/`

It contains Spark-specific draft dialect variants:

- `pos_02_spark.sql`
- `neg_02_spark.sql`

This path is treated as an optional semantic v2 asset for the PORT case, not a blocker. It is intentionally retained because portability dialect variants can carry semantic adaptation information that is not equivalent to generic compatibility residue.

Local empty untracked directories such as `sql/positives/`, `sql/negatives/`, and `notes/` still exist in the current working tree from prior deletions, but they contain no files, are not tracked by git, and are not part of the branch/public release surface.

## Acceptance

The five-case pilot is acceptable as the clean-template-minimal v2 pilot template with optional dialect variants retained for `PORT_0003`.

Remaining tracked extra path groups: 1.

Remaining blockers: 0.

Ready for Common-core 40 planning: yes, planning only.

## Validation

Static v2 validation passed for all five pilot cases. Unit tests under `tests/case_package_v2` passed. No DB/checker execution was run.

## Protected Boundary Summary

Protected surfaces were unchanged:

- cases modified: no
- evidence modified: no
- schemas modified: no
- `case_sets/` changed: no
- inventory changed: no
- reports/results changed: no
- denominator changed: no
- paper results changed: no
- official metrics computed: no
- DB/checker execution run: no
- global leaderboard created: no

## Exact Next Safe Action

Authorize `case_package_v2_common_core40_conversion_plan_v0` as a read-only Common-core 40 planning task using the five-case pilot as the accepted clean-template-minimal v2 template. Do not perform conversion until that plan is reviewed.
