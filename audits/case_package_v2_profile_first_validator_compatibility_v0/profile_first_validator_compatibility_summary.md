# case_package_v2_profile_first_validator_compatibility_v0

## Purpose and Scope

This branch-only task updates the static case-package v2 resolver, validator CLI, and tests so the profile-first `schema_ref` shape introduced by the folder-ordered conversion pilot is accepted:

```yaml
schema_ref:
  schema_id: <SCHEMA_ID>
  profile: schemas/<SCHEMA_ID>/schema_profile.yaml
```

The task is compatibility-only. It does not convert cases, modify schema packages, run DB/checker execution, compute metrics, render paper tables, update reports/results, change denominators, or create leaderboard output.

## Profile-First Schema Ref Behavior

The resolver now supports two schema reference shapes:

- Canonical v2 profile-first: `schema_ref.profile` points to `schemas/<SCHEMA_ID>/schema_profile.yaml`, and engine DDL/load paths are resolved from that external profile.
- Legacy/compatibility: `schema_ref.engines.<engine>.ddl/load` remains accepted for static validation context.

For profile-first manifests, the resolver validates the external schema profile, verifies the profile `schema_id` matches the manifest `schema_ref.schema_id`, and resolves `postgres`, `mysql`, and `spark` DDL/load paths through the external profile.

## Resolver Changes

- Added safe YAML loading for already-resolved schema profile references.
- Added required profile-first path validation when `schema_ref.engines` is absent.
- Added case-local `schema/schema_profile.yaml` existence validation.
- Kept legacy `schema_ref.engines` accepted as compatibility.
- Changed missing validation wrappers to warning-only findings because checker/validation layers are intentionally not converted yet.
- Updated directory classification for `schema/` to reflect the profile-only clean-v2 policy plus retained compatibility copies.

## Validator Changes

The dev validator now reports `profile_first_schema_ref_supported=true` and inherits the resolver behavior. It remains static and non-destructive: it does not run DB engines, checkers, timing, metrics, retained-evidence parsing, or paper rendering.

## Test Changes

The unit suite now covers:

- profile-first `schema_ref` resolving through external `schema_profile.yaml`
- legacy `schema_ref.engines` compatibility
- missing external schema profile failure
- missing engine DDL/load in external profile failure
- absolute path rejection
- optional witness file warnings
- all five pilot cases validating with profile-first schema refs

## Five Pilot Case Validation Summary

All five pilot cases pass static validation:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

`PERF_0006` has no remaining static findings. The other four cases have expected warning-only findings for later layers: missing `evidence_ref`, missing witness policy fields, and missing validation wrapper references. These are not failures because this task only addresses profile-first schema compatibility.

## Protected Boundary Summary

- Case files modified: no.
- Schemas modified: no.
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

Authorize `case_package_v2_checker_validation_layers_pilot_v0` to convert only the checker and validation layers for the five pilot cases, still branch-only and without DB/checker execution, reports/results updates, denominator changes, paper-result changes, or leaderboard output.
