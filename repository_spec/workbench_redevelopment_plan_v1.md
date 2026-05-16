# Workbench Redevelopment Plan v1

Status: planning

Purpose: define the high-level redevelopment path after Common-core 40 canonical case-package migration.

This plan does not authorize implementation, DB validation, evidence regeneration, metric recomputation, reports/results updates, paper table updates, denominator changes, or case membership changes.

## Strategic Direction

The public workbench should be rebuilt around canonical release assets rather than copied wholesale from legacy scripts and reports.

Primary inputs:

- canonical Common-core 40 case packages;
- `case_sets/common_core_v0/`;
- `inventory/`;
- retained evidence mappings;
- future evidence ledger;
- future metrics contract.

Legacy scripts and reports remain reference inputs, adapter targets, or retained evidence sources.

## Phase 1: Evidence Ledger Schema

Define a stable evidence ledger that can represent:

- controls;
- method candidates;
- retained legacy evidence;
- user-run outputs;
- denominator IDs;
- route and method roles;
- correctness, execution, timing, and observability states.

Deliverable: approved `evidence_ledger_schema_v1`.

## Phase 2: Retained Evidence Adapter

Build adapters that read:

- case package `evidence/runs_retention.yaml`;
- retained report/result maps;
- public-safe retained evidence files;
- selected private/archive references.

Adapters should emit ledger rows without changing legacy evidence or recomputing metrics.

## Phase 3: Metrics Contract

Finalize metric definitions before implementation.

The contract must specify:

- denominator handling;
- exact/executed/timed gates;
- correctness gates;
- performance distribution rules;
- observability metrics;
- parseability/extractability/runnable SQL statuses;
- fallback/regression reporting.

Maintainer/team confirmation is required before implementation.

## Phase 4: Runner/Output Policy

Finalize where new outputs go and how run manifests are recorded.

New outputs must not write into case-local `runs/` by default.

## Phase 5: User Runner Design

Design the public candidate runner around:

- case set selection;
- engine selection;
- candidate SQL input;
- output root;
- checker invocation policy;
- evidence ledger output.

No LLM dependency should be a startup requirement.

## Phase 6: Reproduction CLI Design

Design a reproducibility interface that can:

- validate package structure;
- read retained evidence;
- optionally run public-safe checks;
- render evidence summaries;
- avoid mutating case packages.

## Phase 7: Report Renderer Design

Build report renderers from the evidence ledger and metrics contract, not from ad hoc legacy report scripts.

Renderers should preserve role-aware and denominator-aware reporting and avoid global leaderboard framing.

## Phase 8: Documentation And README

Document:

- benchmark unit = case package;
- Common-core v0 membership;
- evidence ledger;
- retained evidence policy;
- output policy;
- how to run user candidates;
- how to reproduce retained reports.

## Phase 9: Tests/CI Smoke

Add smoke tests for:

- case-set loading;
- inventory loading;
- evidence ledger parsing;
- metric contract validation;
- runner output root behavior;
- report renderer input validation.

## Phase 10: Later Non-Common-Core Governance

After Common-core v0 release path stabilizes, reconcile and govern non-common-core cases and the 197 vs 190 case universe issue.

Non-common-core cases remain backlog/universe, not v0 denominator.

## Immediate Next Safe Action

Resolve open metric and runner-interface questions with maintainer/team before implementing unified reproduction CLI, paper table renderer, or metric computation.
