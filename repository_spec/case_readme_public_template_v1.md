# Case README Public Template v1

Status: public-facing case README template for release case packages

## Purpose

This template defines the standard README structure for `cases/<POOL>/<CASE_ID>/README.md` files. A case README describes the case package and its benchmark boundaries. It does not record repository construction history and does not create membership, denominator, paper-result, metric, or leaderboard claims.

## Required Sections

1. Title
2. Purpose
3. Release Scope
4. Package Contents
5. Evidence Boundary
6. Benchmark Boundary
7. Notes / Future Review Status

## Section Guidance

### Title

Use only the case id as the H1 heading, for example `# PERF_0006`.

### Purpose

Describe the case package, not repository construction history. Use case-specific provenance when available from `metadata/provenance.yaml`; otherwise use pool-based wording:

- PERF: performance-oriented SQL rewrite case package.
- CONS: semantic consistency and checker-control SQL rewrite case package.
- PORT: portability-focused SQL rewrite case package.
- LONGTAIL: structural robustness and long-tail SQL rewrite case package.

### Release Scope

State whether the case is a Common-core v0 member and whether it is in the Track A same-engine denominator. Membership is governed by `case_sets/`; denominator role is governed by denominator and case-set files. A README does not create or change paper results.

For Common-core cases, use:

- Common-core v0 member: yes.
- Track A same-engine denominator member: yes, when present in `case_sets/common_core_v0/denominator_same_engine_120.csv`.
- Paper-result contributor: governed by official metric/report artifacts, not this README.

For non-Common-core cases, use:

- Common-core v0 member: no.
- Track A same-engine denominator member: no.
- Paper-result contributor: no.
- Public release role: staged/backlog canonical package candidate.

### Package Contents

Point to stable package directories such as `manifest.yaml`, `sql/`, `schema/`, `checker/`, `evidence/`, `metadata/`, and `validation/` where present.

### Evidence Boundary

State that retained evidence is indexed through `evidence/runs_retention.yaml`. Raw legacy runs are not copied wholesale by default, unsafe raw logs and private runtime traces are not public package contents, and new public runner outputs should not write into case-local legacy `runs/` directories by default.

### Benchmark Boundary

State that the README does not create or change Common-core membership, denominator values, paper results, metric outputs, case-set membership, or leaderboard claims.

### Notes / Future Review Status

For Common-core cases, state that future reports must use denominator-aware artifacts rather than README text. For non-Common-core cases, state that staged/backlog membership requires separate governance approval.

## Forbidden Terms And Patterns

Case README files must not include construction-process wording, including:

- `Codex`
- `overnight wave`
- `wave 001`
- `wave 002`
- `migration commit`
- `run-log finalization`
- `internal task`
- `pushed to origin`
- `task commit`
- `final HEAD`
- `ChatGPT`
- process-oriented agent wording

The word `migration` should be avoided in case READMEs unless it is part of stable benchmark semantics such as cross-engine query movement. It must not describe repository construction process.

## Non-actions

This template does not update `case_sets/`, denominators, reports/results, paper results, metrics, raw evidence, or case membership.
