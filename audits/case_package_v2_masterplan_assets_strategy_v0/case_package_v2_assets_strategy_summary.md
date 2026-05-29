# Case Package v2 Master Plan / Assets Strategy v0

## Purpose and Scope

This task records the case package v2 strategy after the `PERF_0006` external-schema branch pilot.

Branch:

`feature/case-package-v2-external-schema`

This is strategy and policy documentation only. It does not convert cases, run DB engines, run checkers, collect timing, compute official metrics, render paper tables, migrate reports/results, update retained evidence, update case sets, change denominators, change paper results, delete case-local `runs/`, modify raw legacy evidence, or create a leaderboard.

## Current State From PERF_0006 Pilot

The `PERF_0006` branch pilot proved a copy-first v2 direction:

- direct SQL paths under `sql/source.sql`, `sql/pos_01.sql`, and `sql/neg_01.sql`
- external reusable schema package under `schemas/tpch_common_core_v0/`
- manifest `schema_ref`
- retained case-local `schema/` compatibility copy
- retained case-local `runs/` as legacy retained evidence only
- new v2 validation wrapper names without executing DB engines

Runner and validator compatibility for `schema_ref` and future `evidence_ref` is still a known gap.

## v2 Overall Opinion Summary

v2 should make each case package smaller and more stable by keeping case-local files focused on the SQL problem, checker policy, validation entrypoints, and manifest references.

Reusable schema assets belong under `schemas/<SCHEMA_ID>/`. Heavy retained evidence belongs under `evidence/cases/<POOL>/<CASE_ID>/` or equivalent curated evidence references. User-run outputs remain local under `runs/user/<run_id>/`.

v1 remains compatibility context until branch validation and runner compatibility are approved.

## Schema Externalization Strategy

Schemas move to:

`schemas/<SCHEMA_ID>/`

Case manifests use `schema_ref` as the stable reference surface. Case-local `schema/` directories remain compatibility artifacts until a separate cleanup task proves validator and runner compatibility and explicitly authorizes deletion.

## Evidence Externalization Strategy

Heavy evidence moves or is referenced through:

`evidence/cases/<POOL>/<CASE_ID>/`

Case manifests use `evidence_ref` to point to package validation summaries, runs-retention metadata, retained controls, hard-negative evidence, and plan evidence.

`evidence/` is not `results/retained/`, and neither is user-run output.

## Validation Consolidation Strategy

v2 validation entrypoints converge to:

- `validation/run_validation.sh`
- `validation/run_plan_collection.sh`

Case-local scripts should be thin wrappers that resolve manifest references and dispatch to shared logic in `scripts/` or `src/`. Existing engine-specific scripts remain compatibility assets until wrapper validation is complete.

## Runtime Witness/Data Profile Strategy

For local user-run DB/checker execution, source SQL execution is the default oracle. The checker compares runtime source result artifacts to candidate result artifacts.

`data_profile.yaml` is optional, generated, or external. `correct_result.csv` is optional and not required for runtime checking when source-as-oracle execution is available.

## Runs / Results / Evidence Boundary

- `runs/user/<run_id>/`: local user-run outputs only; ignored and not retained paper evidence.
- case-local `runs/`: legacy retained evidence only; do not delete without retention mapping and explicit approval.
- `evidence/cases/<POOL>/<CASE_ID>/`: external case evidence/reference material.
- `results/retained/`: curated retained result/reporting surface only after separate authorization.
- `reports/`: curated release reports only after separate authorization.

No global leaderboard is created by any of these surfaces.

## Master Plan Updates

`project_control/MIGRATION_MASTER_PLAN.md` now includes a case package v2 target addendum that records:

- v1 as compatibility context
- v2 as branch-adoption target
- target case-local layout
- external schema layout
- external evidence layout
- `schema_ref`
- `evidence_ref`
- validation entrypoint policy
- source-as-oracle witness policy
- artifact boundaries
- branch-only adoption roadmap

## Decision Log Updates

`project_control/DECISION_LOG.md` now records:

- D020: Case package v2 target layout
- D021: External schema strategy through `schema_ref`
- D022: External evidence strategy through `evidence_ref`
- D023: Validation entrypoint consolidation
- D024: Runtime source-as-oracle witness policy

## Repository Spec Drafts Created

- `repository_spec/case_package_contract_v2_draft.md`
- `repository_spec/external_schema_contract_v1_draft.md`
- `repository_spec/external_evidence_contract_v1_draft.md`
- `repository_spec/validation_entrypoint_policy_v1_draft.md`
- `repository_spec/runtime_witness_policy_v1_draft.md`

## Remaining Compatibility Gaps

- Runner code still needs a non-destructive `schema_ref` resolver.
- Validator code still needs v2 manifest and external asset validation.
- Future `evidence_ref` paths are policy-defined but not implemented in case manifests beyond future planning.
- Existing v1 case-local schema/evidence/script paths remain compatibility assets.
- Clean export classification must decide which construction audits and branch-pilot artifacts remain public final surface.

## Protected Boundary Summary

This task changed only project-control, repository spec drafts, and audit outputs.

No case files, schema asset files, `case_sets/`, inventory, reports/results, denominators, paper results, raw legacy evidence, official metrics, paper tables, or leaderboard files were changed.

## Exact Next Safe Action

Authorize `case_package_v2_runner_validator_compatibility_v0` on the feature branch to implement non-destructive `schema_ref` and `evidence_ref` resolution checks, recheck `PERF_0006`, and avoid any bulk case conversion.
