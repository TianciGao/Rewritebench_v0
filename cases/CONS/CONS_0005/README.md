# CONS_0005

## Purpose

CONS_0005 is a semantic consistency and checker-control SQL rewrite case package. Provenance is recorded in `metadata/provenance.yaml`; source-family metadata currently records `Calcite`.

The package is organized as a benchmark case package, not as a standalone SQL string. It includes SQL assets, schema context, checker configuration, retained-evidence indexing, and denominator-eligibility metadata.

## Release Scope

- Common-core v0 member: yes.
- Track A same-engine denominator member: yes.
- Common-core membership is governed by `case_sets/`, not by this README.
- Denominator role is governed by denominator and case-set files, not by this README.
- Paper-result contributor: governed by official metric/report artifacts, not this README.
- Metrics computed in this package: no.
- Public release role: Common-core v0 canonical case package.

## Case Package v2 Pilot Status

CONS_0005 is part of the branch-only case-package v2 pilot on `feature/case-package-v2-external-schema`.

- Case ID: `CONS_0005`.
- Pool: `CONS`.
- Source SQL: `sql/source.sql`.
- Positive SQL: `sql/pos_01.sql`.
- Negative SQL: `sql/neg_01.sql`.
- Schema policy: clean v2 uses case-local `schema/schema_profile.yaml` as the case-facing profile. Executable DDL/load are external under `schemas/calcite_core_sql_tests_cons0005_v0/`; any case-local per-engine schema files are compatibility assets only.
- Checker policy: `checker/` stores configuration only. Shared checker and validation implementation lives under `src/sql_rewrite_bench/`, not in this case package.
- Validation policy: `validation/run_validation.sh` and `validation/run_plan_collection.sh` are thin wrappers. New outputs must not be written to case-local `runs/`.
- Witness policy: runtime checking uses source-as-oracle. Static witness files are optional.
- Evidence policy: `evidence_ref` points to `evidence/cases/CONS/CONS_0005/`. Case-local `evidence/` remains compatibility retained evidence only.
- Metadata and notes policy: case-local `metadata/` and `notes/` remain compatibility/reference assets; public-safe notes are also copied under `evidence/cases/CONS/CONS_0005/notes/`.
- Runs policy: case-local `runs/` is legacy retained evidence only. User runs belong under top-level `runs/user/<run_id>/`.
- Benchmark boundary: no denominator change, paper-result change, official metric computation, or global leaderboard is authorized by this package.

## Package Contents

- `manifest.yaml` is the package index and uses v2 references for SQL, schema, checker, validation, witness, evidence, metadata compatibility, notes compatibility, and runs compatibility.
- `sql/` contains direct source, positive, and hard-negative SQL paths.
- `schema/schema_profile.yaml` links this case to the external reusable schema profile.
- `checker/` contains comparison, normalization, and expected-rejection configuration.
- `validation/` contains v2 wrapper entrypoints plus retained engine-specific compatibility scripts where present.
- `witness/` contains optional witness metadata/static files.
- `evidence/`, `metadata/`, `notes/`, and `runs/` remain compatibility or retained-reference surfaces, not new run-output locations.

## Benchmark Boundary

This README does not create or change Common-core membership, denominator values, paper results, metric outputs, case-set membership, or leaderboard claims. Reports must remain role-aware and denominator-aware.

## Notes / Future Review Status

Common-core v0 package; future reports must use denominator-aware artifacts rather than README text. This branch must not merge to `main` until the v2 pilot closeout, validator, and runner compatibility are accepted.
