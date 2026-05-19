# PERF_0006

## Purpose

PERF_0006 is a performance-oriented SQL rewrite case package. Provenance is recorded in `metadata/provenance.yaml`; source-family metadata currently records `TPC-H`.

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

- `manifest.yaml` is the package index and now uses the canonical v2 internal reference shape for SQL, schema, checker, witness, validation, and evidence references.
- `sql/` contains the source SQL and approved rewrite SQL assets for this case. In the v2 branch pilot, `sql/pos_01.sql` and `sql/neg_01.sql` are the direct rewrite paths; the previous `sql/positives/` and `sql/negatives/` paths are retained as compatibility copies during the pilot.
- `schema_ref` in `manifest.yaml` points to the external reusable schema package `schemas/tpch_common_core_v0/`.
- `schema/` is retained as a case-local compatibility copy during this branch pilot and is not deleted.
- `witness/` contains the v2 pilot witness data profile and retained-source-derived correct result.
- `checker/` contains comparison, normalization, and expected-rejection configuration where applicable.
- `evidence_ref` in `manifest.yaml` records pending external evidence adoption. `evidence/` remains the case-local compatibility location for retained-evidence indexes and public-safe evidence summaries.
- `metadata/` contains provenance, taxonomy, engine support, denominator eligibility, and artifact-path metadata.
- `validation/` contains v2 wrapper entrypoints plus retained engine-specific validation entrypoints where available; these are package assets, not evidence that a new validation run has been performed.

## Evidence Boundary

Retained evidence is indexed through `evidence/runs_retention.yaml`. Raw legacy runs are not copied wholesale by default; unsafe raw logs, stdout/stderr/debug payloads, token/API/model traces, and private runtime artifacts are not part of the public package surface.

New public runner outputs should not write into case-local legacy `runs/` directories by default. Generated outputs belong in an explicitly authorized external output root.

The case-local `runs/` directory is retained as legacy evidence only. It was not deleted or rewritten by the v2 external-schema branch pilot.

External evidence has not yet been copied into top-level `evidence/cases/`; this branch keeps the retained case-local evidence as compatibility material until a separate copy-first externalization task is authorized.

## Benchmark Boundary

This README does not create or change Common-core membership, denominator values, paper results, metric outputs, case-set membership, or leaderboard claims. Reports must remain role-aware and denominator-aware.

## Notes / Future Review Status

Common-core v0 package; future reports must use denominator-aware artifacts rather than README text. This branch must not merge to `main` until broader v2 pilot, validator, and runner compatibility are approved.
