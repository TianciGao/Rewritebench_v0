# Implementation Phase Plan

Recommended phases, each requiring separate authorization:

## Phase 1: Timing Artifact Schema Design

Finalize timing artifact fields, N.A. conditions, sample array requirements, environment metadata, and local-vs-official claim boundaries.

## Phase 2: Exact-Gated Local Timing Diagnostic Implementation

Implement local timing collection only for result-consistent rows. Write local timing artifacts under `runs/user/`. Do not compute official metrics.

## Phase 3: Non-Official Local Metrics Calculator

Compute local diagnostic summaries for Coverage, Correctness, Performance, and Generalization from local artifacts. Keep outputs non-official and outside reports/results.

## Phase 4: POCR External Skill-Adapter Integration

After collaborator script/schema readiness, design and implement operation atom ingestion and validation. Do not infer atoms.

## Phase 5: Retained-Evidence / Official Metrics Promotion

Define promotion gates from local or retained artifacts to official metric input. Validate denominator joins and evidence provenance.

## Phase 6: Paper Table Renderer

Render paper-facing tables only after official metric inputs and contracts are approved.

## Cross-Phase Requirements

- No global leaderboard.
- Preserve denominator and role boundaries.
- Preserve unsupported/fail-closed visibility.
- Keep local diagnostics separate from official evidence until promotion.
