# Official Status Metrics Implementation Scope Proposal

## Purpose

This is a proposal for a possible future implementation task. It does not implement official metrics and does not authorize paper rendering.

## Inputs

- `audits/combined_candidate_status_overlay_v2/combined_candidate_status_ledger_v2.csv`
- `audits/overlap_priority_overlay_v1/combined_metric_input_authorization_overlay_v1.csv`
- `audits/status_inference_overlay_v0/status_inference_overlay_v0.csv`, only if inferred_generated is separately approved for official input
- `case_sets/common_core_v0/denominator_same_engine_120.csv`
- Metrics Contract v1 and status inference policy

## Outputs

A future task should write only to a new audit or official-metrics staging directory approved by the maintainer. It must not write to `reports/` or `results/` unless a separate reports/results task is authorized.

## Validation Gates

- Join every candidate row to the Track A same-engine denominator.
- Verify 600 planned candidate rows remain visible.
- Verify unresolved rows are reported by method/pool/engine.
- Verify inferred fields are stored separately from observed fields.
- Verify no timing, speedup, or paper-result columns are populated.
- Verify no global leaderboard output exists.

## Official Vs Audit Labels

Official outputs, if later authorized, must explicitly set official status and include provenance. Audit dry-run outputs must remain labeled audit-only and non-paper.

## Inferred Fields

Inferred fields must remain separate from observed fields. If R1 inferred_generated is approved for official use, official tables must expose observed-generated and inferred-generated components separately.

## Unresolved Rows

Unresolved rows must remain visible in denominator accounting and must not be dropped from planned denominator summaries.

## Paper Rendering Boundary

Paper table rendering remains separate because it requires final metric validation, public wording review, and explicit renderer authorization.
