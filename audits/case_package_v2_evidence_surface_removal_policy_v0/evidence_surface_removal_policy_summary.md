# Evidence Surface Removal Policy Summary

Task: `case_package_v2_evidence_surface_removal_policy_v0`

Branch: `feature/case-package-v2-external-schema`

## Purpose and Scope

This branch-only policy revision removes the assumption that clean v2 public case packages require static evidence directories. It updates policy/spec wording and static validator expectations, and it plans live reference removal for five pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

No case files or evidence files were modified or deleted in this task.

## Clean v2 Evidence Policy

Clean v2 case packages do not require:

- `cases/<POOL>/<CASE_ID>/evidence/`
- `evidence/cases/<POOL>/<CASE_ID>/`

The final public case surface should be regeneration-first. Evidence rows should be regenerated from validation wrappers, checker configuration, baselines, scripts, and separately authorized reports/results surfaces. Static evidence may remain only as optional retained-artifact material when separately authorized.

The clean manifest policy is:

```yaml
evidence_policy:
  static_case_evidence: not_required
  regeneration_policy: regenerable_by_validation_and_report_scripts
  retained_static_artifacts: none
```

`evidence_ref` remains optional compatibility metadata for retained static artifacts. It is not required for clean v2 validation.

## Paper and Artifact Interpretation

Removing static evidence from the clean v2 public surface does not change paper results, denominator values, case-set membership, official metric inputs, or leaderboard policy. `reports/` and `results/` remain separately authorized paper/reporting surfaces. `runs/user/<run_id>/` remains local-only user output and must not be committed as benchmark evidence.

## Validator Impact

The static v2 resolver now:

- accepts `evidence_policy` as an approved top-level manifest key;
- accepts `evidence_policy.static_case_evidence: not_required`;
- does not fail when `evidence_ref` is absent;
- retains compatibility validation for `evidence_ref` when it is present;
- continues to check SQL, schema profile/profile-first schema refs, checker config paths, validation wrappers, witness policy, and path safety.

Unit tests were updated to cover regeneration-first evidence policy and invalid evidence-policy values.

## Five-case Reference-removal Plan

Case-local `evidence/` is already absent for all five pilot cases. Top-level `evidence/cases/<POOL>/<CASE_ID>/` exists for all five and is still referenced by live case files:

- `manifest.yaml` in all five cases;
- `README.md` in all five cases;
- checker config files in all five cases;
- `witness/data_profile.yaml` for `PERF_0006`.

These live references must be updated before deleting top-level static evidence packages. Historical audit references can remain and should not block cleanup.

## Deletion Not Performed

This task performed no evidence deletion. A future execution task should update the five pilot manifests/READMEs/checker/witness references, replace `evidence_ref` with `evidence_policy`, and then delete static evidence surfaces only after confirming no live references remain.

## Protected Boundary Summary

Protected surfaces were unchanged:

- case packages modified: no
- evidence deleted: no
- reports/results changed: no
- denominator changed: no
- paper results changed: no
- official metrics computed: no
- DB/checker execution run: no
- global leaderboard created: no

## Exact Next Safe Action

Authorize `case_package_v2_evidence_reference_removal_execution_v0` to update live five-case references from static `evidence_ref`/`evidence/cases/` paths to regeneration-first `evidence_policy`, then delete only unreferenced static evidence surfaces with protected-boundary checks.
