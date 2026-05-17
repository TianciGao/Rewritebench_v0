# status_inference_policy_v0 Summary

## Purpose And Scope

This audit defines a conservative status-inference policy before any official status-only metric computation. It reviews normalized candidate-status dry-run outputs and separates source-observed normalized fields from possible future inferred fields.

No official metrics were computed. No parser ledgers, authorization overlays, normalization overlays, reports/results files, denominator files, paper results, timing fields, or raw legacy evidence were modified.

## Input Artifacts Reviewed

- `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`
- `audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv`
- `audits/status_field_normalization_v0/status_normalization_observed_values.csv`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_metrics_dryrun_table.csv`
- `audits/normalized_status_only_metrics_dryrun_v1/normalized_status_only_status_caveats.csv`
- `repository_spec/metrics_contract_v1.md`

## Current Caveats From Normalized Dry-run v1

- Candidate parser v1 filled 175 non-timing row-level statuses.
- Metric-input authorization overlay v0 authorized 130 rows.
- The normalized overlay processed 130 authorized rows.
- 45 overlap rows remain unauthorized.
- 425 candidate rows remain unresolved.
- 94 rows have `normalized_ready=true` and `normalized_generated=unknown`.
- 0 rows have `normalized_exact=true` and `normalized_executed=unknown`.
- All 130 authorized rows still have at least one unknown normalized primary metric field.

## Policy Decisions

### R1: ready implies generated

Not allowed now. It may become allowed only in a future inference overlay if source-specific semantics document that `ready=true` means candidate SQL exists and passed extraction/readiness. The inferred field must be recorded as `inferred_generated`, not by overwriting `normalized_generated`.

### R2: exact implies executed

Not allowed now. It may become allowed only in a future inference overlay if exactness is documented as checker output after execution. Current affected rows: 0.

### R3: failure implies generated

Not allowed now. Failure labels require source-specific stage mapping. Some failures imply candidate existence; others imply generation failure or missing evidence. Generic failed/blocked/mismatch labels are insufficient.

### R4: unknown stays unknown

Allowed and active. Unknown, N.A., not-applicable, and missing evidence must not be coerced to false or treated as failures.

## Potentially Inferable Later

- `inferred_generated` from `normalized_ready=true`: 94 preview rows.
- `inferred_executed` from `normalized_exact=true`: 0 preview rows.
- Failure-stage-derived generated/executed fields: blocked until source-specific semantics are approved.

## Source-observed Only For Now

- `normalized_generated`
- `normalized_executed`
- `normalized_exact`
- timing, latency, speedup, and timing-eligibility fields
- official metric numerator fields

## Evidence Gaps

- Direct LLM original has readiness evidence but lacks observed generated/executed/exact fields for its 94 authorized rows.
- Direct LLM repair-1 has 7 authorized rows with generated/ready status but lacks executed/exact status.
- Calcite HEP fail-closed has 29 authorized rows, only 2 of which have observed executed/exact status.
- SQLGlot optimize and SQLGlot no-op have zero authorized normalized rows.
- 45 overlap rows require source-overlap resolution.
- 425 unresolved rows require additional approved row-level evidence.

## Next Safe Action

Review this policy, especially R1. If accepted, separately authorize a `status_inference_overlay_v0` or `normalized_status_only_metrics_dryrun_v2`; keep official metrics, timing, reports/results updates, paper rendering, denominator changes, and paper-result changes separate.
