# PERF_0008

## Purpose

PERF_0008 is a performance-oriented SQL rewrite case package from the `PERF` pool. Source-family context is `TPC-H` and is represented in `manifest.yaml`, `schema/schema_profile.yaml`, and the external schema package.

The package is organized as a benchmark case package, not as a standalone SQL string. Clean v2 case-local assets are limited to public-readable package metadata, SQL, schema profile, checker configuration, validation wrappers, and optional witness material.

## Release Scope

- Common-core v0 member: yes.
- Track A same-engine denominator member: yes.
- Common-core membership is governed by `case_sets/`, not by this README.
- Denominator role is governed by denominator and case-set files, not by this README.
- Paper-result contributor: governed by official metric/report artifacts, not this README.
- Metrics computed in this package: no.
- Public release role: Common-core v0 clean-template-minimal v2 case package.

## Package Contents

- `manifest.yaml` is the package index and uses v2 references for SQL, schema, checker, validation, witness, and regeneration-first evidence policy.
- `sql/source.sql` is the source query.
- `sql/pos_01.sql` is the positive rewrite candidate.
- `sql/neg_01.sql` is the hard-negative rewrite candidate.
- `schema/schema_profile.yaml` is the case-facing schema profile. Executable DDL/load are external under `schemas/tpch_perf0008_v0/`.
- `checker/` contains comparison, normalization, and expected-rejection configuration only.
- `validation/run_validation.sh` and `validation/run_plan_collection.sh` are thin fail-closed wrappers over future shared logic.
- `witness/` contains optional source-as-oracle witness metadata. Static correct-result files are not fabricated.

## Evidence Boundary

Clean v2 uses `evidence_policy.static_case_evidence: not_required`. Static case evidence directories are not part of the clean public case surface, and benchmark evidence is regenerated through authorized validation/checker/baseline/report paths when those surfaces are separately approved.

This conversion did not compute official metrics, run DB/checker execution, create reports/results, or create leaderboard outputs.

## Benchmark Boundary

This README does not create or change Common-core membership, denominator values, paper results, metric outputs, case-set membership, DB/checker execution, or leaderboard claims. Reports must remain role-aware and denominator-aware.

## Notes / Future Review Status

- Legacy nested SQL compatibility paths, case-local executable schema copies, static evidence, metadata, notes, data, placeholder runs, and old engine-specific validation scripts were removed during Wave A conversion after their v2 replacements or regeneration-first policy were recorded.
- Future shared runners must resolve executable schema through `manifest.yaml` `schema_ref.profile` and must write user outputs outside case-local package directories.
