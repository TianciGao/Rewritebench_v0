# case_package_v2_readme_validator_closeout_pilot_v0

## Purpose and Scope

This branch-only closeout updated public-readable README wording and rechecked the static v2 validator for the five case-package v2 pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

The task did not perform structural conversion. It did not modify SQL, schema, external schemas, checker configuration, validation wrappers, witness files, evidence files, metadata files, notes files, or runs directories.

## README Update Summary

Each pilot README now documents:

- case ID and pool
- v2 branch pilot status
- direct SQL paths
- profile-first schema policy
- checker configuration-only policy
- thin validation wrapper policy
- source-as-oracle witness policy
- external `evidence_ref` policy
- metadata, notes, and runs compatibility state
- benchmark boundaries for denominators, paper results, official metrics, and global leaderboard output

## Validator Expectation Summary

The existing static v2 validator was re-run unchanged. No validator or test expectation update was needed.

The validator checks direct SQL paths, case-local `schema/schema_profile.yaml`, profile-first `schema_ref`, checker config paths, validation wrappers, witness policy, external evidence references, absolute/local path safety, forbidden case-local checker scripts, and case-local runs output boundaries.

## Per-case Closeout Status

All five pilot cases passed static validation after README wording updates. Unit tests under `tests/case_package_v2` also passed.

## Remaining Compatibility Directories

The pilot cases still retain compatibility surfaces by design:

- case-local `schema/<engine>/` executable DDL/load copies
- nested `sql/positives/` and `sql/negatives/` compatibility paths
- case-local `evidence/`
- case-local `metadata/`
- case-local `notes/`
- case-local `runs/README.md` placeholders
- legacy engine-specific validation scripts
- optional case-local `data/`

These are documented compatibility assets. No deletion was performed.

## Protected Boundary Summary

- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- Case-local runs deleted: no.
- Evidence deleted: no.
- Structural layers reconverted: no.
- Legacy repo modified: no.

## Exact Next Safe Action

Review and accept the five-case v2 pilot closeout on `feature/case-package-v2-external-schema`; if accepted, authorize a branch-only Common-core 40 conversion plan that uses the folder-ordered rulebook without merging to `main`.
