# Production Ledger Validation Gates Summary

Date: 2026-05-17

## Purpose And Scope

This audit defines validation gates for a future production evidence ledger. The gates are policy only: no production retained evidence was parsed, no production ledger validator was implemented, no adapters were implemented, no metrics were computed, and no production ledger files were created.

The planning is scoped to Common-core v0 and Metrics Contract v1. It builds on the synthetic ledger fixtures, the hardened fixture validator, the developer smoke entrypoint, the CI smoke workflow, the retained-evidence adapter design, and the evidence row-grain policy.

## Why Gates Are Needed

Future retained-evidence adapters will convert heterogeneous retained artifacts into a typed long-format ledger. That ledger must be validated before any downstream metric computation or paper rendering because different row types have incompatible denominators and evidence roles.

Without a production validation gate, the workbench could accidentally mix same-engine rewrite rows with controls, portability rows, verifier support pairs, plan artifacts, or retained summary artifacts. That would violate Metrics Contract v1 and the no-global-leaderboard boundary.

## Proposed Gates

The gate matrix defines 24 proposed gates across these families:

- schema
- record_type
- denominator
- status_na
- metric_readiness
- public_hygiene
- mutation_boundary
- no_global_leaderboard
- provenance
- ci_smoke

The gates are fail-closed. They should block metrics computation, paper rendering, and public runner output whenever required columns, record-type fields, denominator joins, status semantics, public hygiene, or provenance are unsafe or ambiguous.

## Unauthorized Work

This task does not authorize:

- production retained-evidence parsing;
- production ledger validator implementation;
- retained-evidence adapter implementation;
- metrics computation;
- reproduction CLI implementation;
- public runner implementation;
- paper table rendering;
- reports/results migration;
- denominator changes;
- paper-result changes;
- raw legacy evidence changes.

## Future Implementation Sequence

1. Keep the synthetic fixture smoke workflow as the first developer/CI gate.
2. Implement a separate non-mutating production ledger validator only after authorization.
3. Require adapter output to pass production ledger validation before metrics.
4. Require metric validation before paper table rendering.
5. Keep public runner outputs outside case-local `runs/` and validate their ledger rows separately.

## Next Safe Action

Review and approve the production ledger validation gate policy. Do not parse production retained evidence, implement adapters, compute metrics, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate authorization.
