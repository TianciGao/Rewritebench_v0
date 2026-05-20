# PORT_0008

## Purpose

PORT_0008 is a portability-focused SQL rewrite case package from the `PORT` pool. Source-family context is `PARROT/BIRD` and is represented in `manifest.yaml`, `schema/schema_profile.yaml`, and the external schema package.

The package is organized as a benchmark case package, not as a standalone SQL string. Clean v2 case-local assets are limited to public-readable package metadata, SQL, schema profile, checker configuration, validation entrypoints, and optional witness material.

## Release Scope

- Common-core v0 member: yes.
- Track A same-engine denominator member: yes.
- Common-core membership is governed by `case_sets/`, not by this README.
- Denominator role is governed by denominator and case-set files, not by this README.
- Paper-result contributor: governed by official metric/report artifacts, not this README.
- Metrics computed in this package: no.
- Public release role: Common-core v0 canonical case package.

## Case Package v2 Status

PORT_0008 is part of Wave C subwave 2 on `feature/case-package-v2-external-schema`.

- Case ID: `PORT_0008`.
- Pool: `PORT`.
- Source SQL: `sql/source.sql`.
- Positive SQL: `sql/pos_01.sql`.
- Negative SQL: `sql/neg_01.sql`.
- Dialect variants: none currently retained for this case; do not create variants unless a future portability review requires them.
- Schema policy: clean v2 uses case-local `schema/schema_profile.yaml` as the case-facing profile. Executable DDL/load are external under `schemas/parrot_bird_port0008_v0/`; case-local per-engine schema compatibility copies were removed after external schema verification.
- Checker policy: `checker/` stores configuration only. Shared checker and validation implementation lives under `src/sql_rewrite_bench/`, not in this case package.
- Validation policy: `validation/run_validation.sh`, `validation/run_plan_collection.sh`, and `validation/run_engine_queries.py` implement the repaired three-file validation contract. They are thin fail-closed entrypoints, do not require case-local `schema/<engine>/`, and must not write to case-local `runs/`.
- Witness policy: runtime checking uses source-as-oracle. Static witness result files are not fabricated.
- Evidence policy: clean v2 uses `evidence_policy.static_case_evidence: not_required`; committed static evidence is not required and benchmark evidence is regenerated through validation/checker/baseline/report scripts when separately authorized.
- Metadata/data/notes policy: stable semantic content is represented by `manifest.yaml`, `schema/schema_profile.yaml`, external schema load files, witness policy, evidence policy, and project-level case-set controls.
- Runs policy: user runs belong under top-level `runs/user/<run_id>/`, not case-local `runs/`.
- Benchmark boundary: no denominator change, paper-result change, official metric computation, DB/checker execution, or global leaderboard is authorized by this package.

## Package Contents

- `manifest.yaml` is the package index and uses v2 semantic references for SQL, schema, checker, validation, witness, regeneration-first evidence policy, and explicit caveats.
- `sql/` contains direct source, positive, and hard-negative SQL paths.
- `schema/schema_profile.yaml` links this case to the external per-case schema profile.
- `checker/` contains comparison, normalization, and expected-rejection configuration.
- `validation/` contains the v2 entrypoints `run_validation.sh`, `run_plan_collection.sh`, and the thin shared-runner shim `run_engine_queries.py`.
- `witness/` contains optional source-as-oracle witness metadata.
- Static evidence directories are not part of the clean public case surface; benchmark evidence is regenerated through authorized validation/checker/report paths.

## Evidence Boundary

Static case-local `evidence/` is not required for clean v2. Raw legacy runs, stdout/stderr/debug payloads, token/API/model traces, and private runtime artifacts are not part of the public package surface.

Generated local runner outputs must not write into case-local `runs/`. Future local outputs should use caller-provided output roots such as top-level `runs/user/<run_id>/`.

## Benchmark Boundary

This README does not create or change Common-core membership, denominator values, paper results, metric outputs, case-set membership, DB/checker execution, or leaderboard claims. Reports must remain role-aware and denominator-aware.

## Notes / Future Review Status

- Static inference remains subject to future execution review; no DB/checker execution was run during this conversion.
- Cases without a recovered distinct draft artifact retain an explicit non-blocking draft-origin caveat in `manifest.yaml`.
