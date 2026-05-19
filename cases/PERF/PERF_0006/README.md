# PERF_0006

## Purpose

PERF_0006 is a performance-oriented SQL rewrite case package from the `PERF` pool. Source-family context is `TPC-H` and is represented in `manifest.yaml`, `schema/schema_profile.yaml`, and the external schema package.

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

PERF_0006 is part of the branch-only case-package v2 clean-template pilot on `feature/case-package-v2-external-schema`.

- Case ID: `PERF_0006`.
- Pool: `PERF`.
- Source SQL: `sql/source.sql`.
- Positive SQL: `sql/pos_01.sql`.
- Negative SQL: `sql/neg_01.sql`.
- Schema policy: clean v2 uses case-local `schema/schema_profile.yaml` as the case-facing profile. Executable DDL/load are external under `schemas/tpch_common_core_v0/`; case-local per-engine schema compatibility copies were removed after external schema verification.
- Checker policy: `checker/` stores configuration only. Shared checker and validation implementation lives under `src/sql_rewrite_bench/`, not in this case package.
- Validation policy: `validation/run_validation.sh` and `validation/run_plan_collection.sh` are thin fail-closed wrappers over future shared logic. They do not call retained engine-specific scripts, do not require case-local `schema/<engine>/`, and must not write to case-local `runs/`.
- Witness policy: runtime checking uses source-as-oracle. This case retains optional static witness files where present.
- Evidence policy: clean v2 uses `evidence_policy.static_case_evidence: not_required`; committed static evidence is not required and benchmark evidence is regenerated through validation/checker/baseline/report scripts when separately authorized.
- Metadata/data policy: case-local `metadata/` and `data/` were removed after their stable content was represented by `manifest.yaml`, `schema/schema_profile.yaml`, external schema load files, witness policy, evidence policy, and project-level case-set controls.
- Runs policy: case-local `runs/` placeholder content was removed by the accepted empty-runs cleanup. User runs belong under top-level `runs/user/<run_id>/`.
- Benchmark boundary: no denominator change, paper-result change, official metric computation, DB/checker execution, or global leaderboard is authorized by this package.

## Package Contents

- `manifest.yaml` is the package index and uses v2 references for SQL, schema, checker, validation, witness, regeneration-first evidence policy, and compatibility state.
- `sql/` contains direct source, positive, and hard-negative SQL paths.
- `schema/schema_profile.yaml` links this case to the external reusable schema profile.
- `checker/` contains comparison, normalization, and expected-rejection configuration.
- `validation/` contains the v2 wrapper entrypoints `run_validation.sh` and `run_plan_collection.sh`.
- `witness/` contains optional witness metadata/static files.
- Static evidence directories are not part of the clean public case surface; benchmark evidence is regenerated through authorized validation/checker/report paths.

## Benchmark Boundary

This README does not create or change Common-core membership, denominator values, paper results, metric outputs, case-set membership, DB/checker execution, or leaderboard claims. Reports must remain role-aware and denominator-aware.

## Remaining Clean-template Blockers

- No schema, evidence, or legacy validation-script cleanup blockers remain after the second clean-template cleanup.
- `PORT_0003` dialect variants are unrelated to this case.
