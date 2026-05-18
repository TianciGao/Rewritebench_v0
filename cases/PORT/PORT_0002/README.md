# PORT_0002

## Purpose

PORT_0002 is a portability-focused SQL rewrite case package. Its provenance is recorded in `metadata/provenance.yaml`, including the retained PARROT/BIRD-style source context already captured in package metadata.

The package is organized as a case package, not as a standalone SQL string. It includes source SQL, rewrite SQL, schema assets, checker configuration, retained-evidence indexing, and denominator-eligibility metadata.

## Release Scope

- Common-core v0 member: no.
- Track A same-engine denominator member: no.
- Paper-result contributor: no.
- Metrics computed in this package: no.
- Public release role: staged/backlog canonical package candidate.

## Package Contents

- `manifest.yaml` is the package index.
- `sql/` contains source, positive rewrite, hard-negative rewrite, and Spark dialect variant SQL.
- `schema/` contains engine-specific DDL/load assets and schema profile metadata.
- `checker/` contains comparison, normalization, and expected-rejection configuration.
- `evidence/` contains retained-evidence indexes and public-safe evidence summaries.
- `metadata/` contains provenance, taxonomy, engine support, denominator eligibility, and artifact-path metadata.
- `validation/` contains retained validation entrypoints where available; these are package assets, not evidence that a new validation run has been performed.

## Evidence Boundary

Raw legacy runs are not copied wholesale into this package. Retained evidence is indexed through `evidence/runs_retention.yaml`, which records what is public-safe, what remains an original legacy reference, and what must not be treated as new benchmark output.

Public runner outputs must not write into case-local legacy `runs/` by default. Unsafe raw logs, stdout/stderr/debug payloads, prompt/token/API traces, and private runtime artifacts are not part of this public package.

## Benchmark Boundary

This package does not change Common-core v0 membership, denominator values, paper results, or case-set membership. It does not create metric outputs, paper-table rows, or leaderboard claims.
