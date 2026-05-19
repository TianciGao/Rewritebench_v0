# Evidence Reference Removal Execution Summary

Task: `case_package_v2_evidence_reference_removal_execution_v0`

Branch: `feature/case-package-v2-external-schema`

## Purpose and Scope

This branch-only writable task removed static evidence directory dependency from the five v2 pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

The task updated live case references from mandatory static evidence paths to regeneration-first evidence policy and deleted only the five pilot top-level static evidence packages after live references were removed.

## Reference Updates

All five manifests now use:

```yaml
evidence_policy:
  static_case_evidence: not_required
  regeneration_policy: regenerable_by_validation_and_report_scripts
  retained_static_artifacts: none
```

`evidence_ref` was removed from all five pilot manifests. README evidence wording now states that committed static evidence is not required and evidence is regenerated through authorized validation/checker/baseline/report paths.

Checker and witness YAML files that contained `evidence/cases/<POOL>/<CASE_ID>/` paths now use runtime/regenerated artifact labels and local `evidence_policy` metadata instead of static paths.

Live reference files updated: 24.

## Static Evidence Surfaces Deleted

Case-local `evidence/` directories were already absent for all five pilot cases, so no case-local evidence directory was deleted in this task.

Deleted top-level static evidence packages:

- `evidence/cases/PERF/PERF_0006/`
- `evidence/cases/PERF/PERF_0007/`
- `evidence/cases/CONS/CONS_0005/`
- `evidence/cases/PORT/PORT_0003/`
- `evidence/cases/LONGTAIL/LONGTAIL_0011/`

No evidence outside these five pilot package paths was deleted.

## Validation

Static v2 validation passed for all five pilot cases after reference removal and static evidence deletion. Unit tests under `tests/case_package_v2` passed. No DB/checker execution was run.

## Protected Boundary Summary

Protected surfaces were unchanged:

- audits deleted: no
- reports/results changed: no
- denominator changed: no
- paper results changed: no
- official metrics computed: no
- DB/checker execution run: no
- global leaderboard created: no
- `case_sets/` changed: no
- inventory changed: no

## Exact Next Safe Action

Run `case_package_v2_post_evidence_removal_parity_review_v0` as a read-only parity review to confirm the five pilot cases remain clean-template-minimal without static evidence surfaces before Common-core 40 planning.
