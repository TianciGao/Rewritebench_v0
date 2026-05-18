# PORT_0022

## Purpose

PORT_0022 is a portability-focused SQL rewrite case package. Provenance is recorded in `metadata/provenance.yaml`; source-family metadata currently records `PARROT`.

The package is organized as a benchmark case package, not as a standalone SQL string. It includes SQL assets, schema context, checker configuration, retained-evidence indexing, and denominator-eligibility metadata.

## Release Scope

- Common-core v0 member: yes.
- Track A same-engine denominator member: yes.
- Common-core membership is governed by `case_sets/`, not by this README.
- Denominator role is governed by denominator and case-set files, not by this README.
- Paper-result contributor: governed by official metric/report artifacts, not this README.
- Metrics computed in this package: no.
- Public release role: Common-core v0 canonical case package.

## Package Contents

- `manifest.yaml` is the package index.
- `sql/` contains the source SQL and approved rewrite SQL assets for this case.
- `schema/` contains engine-specific DDL/load assets and schema profile metadata where available.
- `checker/` contains comparison, normalization, and expected-rejection configuration where applicable.
- `evidence/` contains retained-evidence indexes and public-safe evidence summaries.
- `metadata/` contains provenance, taxonomy, engine support, denominator eligibility, and artifact-path metadata.
- `validation/` contains retained validation entrypoints where available; these are package assets, not evidence that a new validation run has been performed.

## Evidence Boundary

Retained evidence is indexed through `evidence/runs_retention.yaml`. Raw legacy runs are not copied wholesale by default; unsafe raw logs, stdout/stderr/debug payloads, token/API/model traces, and private runtime artifacts are not part of the public package surface.

New public runner outputs should not write into case-local legacy `runs/` directories by default. Generated outputs belong in an explicitly authorized external output root.

## Benchmark Boundary

This README does not create or change Common-core membership, denominator values, paper results, metric outputs, case-set membership, or leaderboard claims. Reports must remain role-aware and denominator-aware.

## Notes / Future Review Status

Common-core v0 package; future reports must use denominator-aware artifacts rather than README text.
