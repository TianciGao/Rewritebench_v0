# Implementation Sequence Plan

Date: 2026-05-17

## Purpose

Propose a future implementation sequence for retained-evidence adapters and downstream metric/report work.

This plan is not implementation authorization.

## Phase 1: Ledger Schema Model And Validation Fixtures

Define an implementation-ready ledger row model, allowed enums, record-type validators, and fixture CSVs.

No retained evidence parsing and no metric computation should occur in this phase.

## Phase 2: Retained Summary Adapter

Implement `retained_summary_adapter` for reference-only artifacts first.

Expected output: `retained_summary_artifact` rows for paper-facing summaries, denominator references, archive-only groups, and manual-review references.

Metric eligibility: false by default.

## Phase 3: Control Cell And Hard-negative Control Adapters

Implement control row adapters joined to `controls_360.csv`.

Expected output: source, positive, and hard-negative `control_cell` rows.

Boundary: hard negatives remain checker controls, not method failures.

## Phase 4: Same-engine Rewrite Candidate Adapter

Implement `rewrite_candidate_cell` adapter for method output references only after row-grain parsing is stable.

Expected output: candidate rows with explicit generated, ready, executed, result, and missingness states.

Boundary: no metric aggregation.

## Phase 5: Timing And Performance Evidence Adapter

Implement timing parsing only after timing eligibility fixtures and validation checks are approved.

Expected output: timing fields on candidate rows or timing-specific support rows.

Boundary: no GM_Speedup, percentile, Regression@20, or speedup-retention computation in the adapter layer.

## Phase 6: Portability And Verifier Support Adapters

Implement `portability_packet_adapter` and `verifier_support_adapter`.

Expected output: `portability_candidate_cell` and `verifier_support_pair` rows with separate denominator semantics.

Boundary: no same-engine Track A mixing and no verifier baseline claims.

## Phase 7: Metrics Computation

Implement metrics only after:

- adapter validation passes;
- Metrics Contract v1 remains active;
- maintainer explicitly authorizes metrics implementation;
- denominator join tests pass;
- N.A. and unsupported policies are tested.

## Phase 8: Paper Table Renderer

Implement paper table rendering only after metric outputs are validated and paper rendering is explicitly authorized.

Renderer inputs should be ledger and metric outputs, not legacy paper tables as canonical data model.

## Phase 9: Public Runner Outputs

Implement public runner outputs last under the public output policy.

Outputs must go outside case-local `runs/`, avoid secrets and local paths, and produce ledger-compatible rows.

## Stop Conditions

Stop implementation if:

- denominator rows are missing or duplicated;
- case membership changes are implied;
- raw local paths or private logs would be published;
- metric aggregation appears in an adapter layer;
- outputs would write into case-local `runs/`;
- reports/results mutation is needed without separate authorization.
