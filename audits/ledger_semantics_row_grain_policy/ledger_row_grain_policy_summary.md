# Ledger Row-grain Policy Summary

Date: 2026-05-16

## Purpose And Scope

This audit formalizes the draft evidence ledger field semantics, row-grain policy, and record-type boundaries before any retained-evidence adapter, metrics computation, report renderer, reproduction CLI, or public runner is implemented.

It uses:

- `repository_spec/evidence_ledger_schema_v1_draft.md`
- `repository_spec/metrics_contract_v1_draft.md`
- `audits/retained_evidence_ledger_mapping/`
- `case_sets/common_core_v0/`
- `inventory/case_registry.csv`

No implementation was created. No metrics were computed. No reports/results were copied. No denominator values, paper results, case membership, case packages, or raw legacy evidence were changed.

## Why This Policy Is Needed

The retained-evidence mapping audit processed 3,439 retained candidates and represented all 28 draft ledger fields, but it also showed that row grain, record type, and denominator semantics must be explicit before adapters can safely parse legacy artifacts.

Without this policy, future code could accidentally:

- treat hard-negative controls as method failures;
- mix verifier support with rewrite-generation baselines;
- use plan artifacts as speedup denominator rows;
- collapse PORT portability rows into Track A same-engine rows;
- treat old paper summaries as canonical metric rows;
- recompute timing or speedup before metric definitions are finalized.

## Record Types

This policy defines seven draft record types:

- `control_cell`
- `rewrite_candidate_cell`
- `plan_observability_artifact`
- `portability_candidate_cell`
- `verifier_support_pair`
- `retained_summary_artifact`
- `user_run_candidate_cell`

Each row must have a `record_type` discriminator in the next schema revision.

## Denominator Boundaries

Track A same-engine rows remain bounded by `case_sets/common_core_v0/denominator_same_engine_120.csv`.

Control rows are governed by `case_sets/common_core_v0/controls_360.csv` and are not rewrite performance rows.

PORT portability rows have separate cross-engine semantics and must not be mixed into same-engine Track A performance denominators.

Plan observability artifacts, verifier support pairs, retained summaries, raw logs, and archive references are support or traceability rows unless a later metric contract explicitly defines otherwise.

## What Remains Blocked

Still blocked:

- retained-evidence adapter implementation;
- metrics computation;
- unified reproduction CLI;
- public runner implementation;
- paper table rendering;
- reports/results migration;
- timing reruns;
- DB validation;
- denominator updates.

## Next Safe Action

Review and approve these policy drafts. After approval, the next safe implementation-adjacent task is to design adapter validation tests and a non-mutating retained-ledger builder skeleton, still without metrics computation or paper rendering.
