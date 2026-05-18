# PERF_0015

## Purpose

PERF_0015 is a performance-oriented SQL rewrite case package. Provenance is recorded in `metadata/provenance.yaml`; source-family metadata currently records `TPC-H`.

The package is organized as a canonical benchmark case package, not as a standalone SQL string. It includes SQL assets, schema context, checker configuration, retained-evidence indexing, and denominator-eligibility metadata.

## Release Scope

- Common-core v0 member: no.
- Track A same-engine denominator member: no.
- Common-core membership is governed by `case_sets/`, not by this README.
- Denominator role is governed by denominator and case-set files, not by this README.
- Paper-result contributor: no.
- Metrics computed in this package: no.
- Public release role: staged/backlog canonical package candidate.

## Package Contents

- `manifest.yaml` is the package index.
- `sql/` contains the source SQL and rewrite SQL assets for this case.
- `schema/` contains engine-specific DDL/load assets and schema profile metadata where available.
- `checker/` contains comparison, normalization, and expected-rejection configuration.
- `evidence/` contains retained-evidence indexes and public-safe evidence summaries.
- `metadata/` contains provenance, taxonomy, engine support, denominator eligibility, and artifact-path metadata.
- `validation/` contains static package entrypoints and retained witness assets where available; these are package assets, not evidence that a new validation run has been performed.

## Evidence Boundary

Retained evidence is indexed through `evidence/runs_retention.yaml`. Raw legacy runs are not copied wholesale by default; unsafe raw logs, stdout/stderr/debug payloads, private runtime traces, and local machine artifacts are not part of the public package surface.

New public runner outputs should not write into case-local legacy run directories by default. Generated outputs belong in an explicitly authorized external output root.

## Benchmark Boundary

This README does not create or change Common-core membership, denominator values, paper results, metric outputs, case-set membership, or leaderboard claims. Denominator values are unchanged by this package. Paper results are unchanged by this package. Reports must remain role-aware and denominator-aware.

## Notes / Future Review Status

Non-Common-core package; any staged/backlog membership decision requires separate governance approval.
