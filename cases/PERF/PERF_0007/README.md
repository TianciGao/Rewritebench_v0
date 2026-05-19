# PERF_0007

## Purpose

PERF_0007 is a performance-oriented SQL rewrite case package from the `PERF` pool. Source-family context is `TPC-H` and is represented in `manifest.yaml`, `schema/schema_profile.yaml`, and the external schema package.

The package is organized as a benchmark case package, not as a standalone SQL string. Clean v2 case-local assets are limited to public-readable package metadata, SQL, schema profile, checker configuration, validation wrappers, and optional witness material.

## Release Scope

- Common-core v0 member: yes.
- Track A same-engine denominator member: yes.
- Common-core membership is governed by `case_sets/`, not by this README.
- Denominator role is governed by denominator and case-set files, not by this README.
- Paper-result contributor: governed by official metric/report artifacts, not this README.
- Metrics computed in this package: no.
- Public release role: Common-core v0 canonical case package.

## Case Package v2 Status

PERF_0007 is part of the branch-only case-package v2 clean-template pilot on `feature/case-package-v2-external-schema`.

- Case ID: `PERF_0007`.
- Pool: `PERF`.
- Source SQL: `sql/source.sql`.
- Positive SQL: `sql/pos_01.sql`.
- Negative SQL: `sql/neg_01.sql`.
- Schema policy: clean v2 uses case-local `schema/schema_profile.yaml` as the case-facing profile. Executable DDL/load are external under `schemas/tpch_perf0007_v0/`; retained case-local per-engine schema files are compatibility-blocked until legacy validation script cleanup.
- Checker policy: `checker/` stores configuration only. Shared checker and validation implementation lives under `src/sql_rewrite_bench/`, not in this case package.
- Validation policy: `validation/run_validation.sh` and `validation/run_plan_collection.sh` are thin wrappers. Retained engine-specific scripts are compatibility-blocked because they contain legacy DB execution logic. New outputs must not be written to case-local `runs/`.
- Witness policy: runtime checking uses source-as-oracle. Static witness files remain optional and are not fabricated.
- Evidence policy: `evidence_ref` points to `evidence/cases/PERF/PERF_0007/`. Case-local `evidence/` is retained for now because checker/witness configuration still references it and checker/witness edits are out of scope for the clean-template gap closure task.
- Metadata/data policy: case-local `metadata/` and `data/` were removed after their stable content was represented by `manifest.yaml`, `schema/schema_profile.yaml`, external schema load files, witness policy, evidence refs, and project-level case-set controls.
- Runs policy: case-local `runs/` placeholder content was removed by the accepted empty-runs cleanup. User runs belong under top-level `runs/user/<run_id>/`.
- Benchmark boundary: no denominator change, paper-result change, official metric computation, DB/checker execution, or global leaderboard is authorized by this package.

## Package Contents

- `manifest.yaml` is the package index and uses v2 references for SQL, schema, checker, validation, witness, evidence, and compatibility state.
- `sql/` contains direct source, positive, and hard-negative SQL paths.
- `schema/schema_profile.yaml` links this case to the external reusable schema profile.
- `checker/` contains comparison, normalization, and expected-rejection configuration.
- `validation/` contains v2 wrapper entrypoints plus retained engine-specific compatibility scripts where present.
- `witness/` contains optional witness metadata/static files.
- Case-local `evidence/` remains a blocked compatibility surface; public-safe external evidence is under `evidence/cases/PERF/PERF_0007/`.

## Benchmark Boundary

This README does not create or change Common-core membership, denominator values, paper results, metric outputs, case-set membership, DB/checker execution, or leaderboard claims. Reports must remain role-aware and denominator-aware.

## Remaining Clean-template Blockers

- Case-local `evidence/` cannot be removed until checker/witness references are updated or explicitly remapped.
- Case-local `schema/<engine>/` cannot be removed while retained engine-specific validation scripts still depend on it.
- Engine-specific validation scripts cannot be removed until their unique legacy DB execution logic is replaced or declared out of scope.
- `PORT_0003` dialect variants remain semantically meaningful and require explicit portability review before cleanup.
