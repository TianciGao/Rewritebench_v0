# Retained Evidence Adapter Design Summary

Date: 2026-05-17

## Purpose And Scope

This task designs how existing retained evidence should later be adapted into the formal evidence ledger under Metrics Contract v1 and the evidence row-grain policy.

No implementation was created. No scripts or source package files were added. No metrics were computed. No reports/results were copied or modified. No paper tables were rendered. No DB engines, validation scripts, LLM calls, or timing workloads were run. No denominator values, paper results, case membership, case packages, or raw legacy evidence were changed.

## Adapter Families Proposed

- `legacy_reports_adapter`
- `retained_results_adapter`
- `case_runs_adapter`
- `plan_observability_adapter`
- `hard_negative_control_adapter`
- `portability_packet_adapter`
- `verifier_support_adapter`
- `timing_record_adapter`
- `retained_summary_adapter`

## Input Source Groups

Inputs are bounded to the aligned release scaffolds and existing retained-evidence maps:

- Common-core membership and denominator scaffolds under `case_sets/common_core_v0/`.
- Common-core case facts under `inventory/`.
- Canonical case package manifests and `evidence/runs_retention.yaml`.
- Reports/results retained-evidence candidate maps.
- Retained-evidence to ledger mapping source groups.

Legacy reports/results are source references only. They are not copied by this design task.

## Output Record Types

The design covers:

- `control_cell`
- `rewrite_candidate_cell`
- `plan_observability_artifact`
- `portability_candidate_cell`
- `verifier_support_pair`
- `retained_summary_artifact`
- `user_run_candidate_cell`

`user_run_candidate_cell` is included only as a future-compatible row type. No user-run implementation is authorized.

## Denominator Boundary Handling

Adapters must join to `case_sets/common_core_v0/cases.csv`, `denominator_same_engine_120.csv`, `controls_360.csv`, and `inventory/case_registry.csv` before emitting denominator-aware rows.

Same-engine rewrite rows, hard-negative control rows, portability rows, verifier support pairs, plan artifacts, retained summary artifacts, and user-submitted rows must remain separate. No adapter may create denominator rows or collapse incompatible evidence into a global leaderboard.

## Validation Gate Overview

Future adapter output must pass row count checks, stable ID uniqueness checks, required-field checks, record-type-specific validation, denominator/control join checks, explicit missingness checks, no-metric-computation checks, no reports/results mutation checks, no case-local `runs/` output checks, and public hygiene checks for any public output paths.

## Current Blockers

- Adapter implementation is not authorized.
- Metrics computation is not authorized.
- Paper table rendering is not authorized.
- Public runner and reproduction interface implementation are not authorized.
- Attribution schema and attribution denominator need a separate implementation-ready design.
- Timing eligibility and paired target timing validation need explicit tests before performance metrics are computed.

## Status Snapshot Check

`project_control/MIGRATION_STATUS.md` already references Metrics Contract v1 and the current no-implementation boundary. No stale-status discrepancy was found.

## Next Safe Action

Review this adapter design and validation plan. The next safe task is to formalize the evidence ledger schema model and non-mutating validation fixtures, still without parsing retained evidence into a production ledger or computing metrics.
