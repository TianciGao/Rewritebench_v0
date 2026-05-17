# status_only_metrics_dryrun_v0 Report

## Purpose And Scope

This is an audit-only dry run for status-only metric logic over candidate-status rows authorized by `metric_input_authorization_overlay_v0`.

It is not official metrics computation, not a paper result, not reports/results migration, not timing computation, and not a production ledger.

## Input Files

- `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`

## Authorization Boundary

Only rows with `metric_input_authorized_overlay=true` and `readiness_label=ready_candidate_status_only` were used as dry-run inputs.

Authorized input rows: 130

Unauthorized overlap rows excluded: 45

Unresolved rows preserved in accounting: 425

## Metrics Dry-Runed

- Generation Rate
- Execution Coverage Rate
- Result Consistency Rate

All rows are marked `dry_run_value_is_official=false` and `paper_result=false`.

## Denominator Handling

The planned Track A same-engine denominator remains visible. Each method route keeps the 120 planned case-engine rows through method/pool/engine groups. Unauthorized overlap rows and unresolved rows are counted as not authorized or unresolved; they are not silently dropped and are not used as success evidence.

## Partial Coverage Warnings

The dry run is partial. Only 130 of 600 scaffold rows are authorized as status-only inputs. The 45 overlap rows remain unauthorized and the 425 unresolved rows remain uncomputed.

## Status Normalization Caveats

Numerator membership uses explicit boolean fields only: `generated`, `executed`, and `exact`. Rows with `N.A.`, `requires_production_retained_evidence`, or other non-boolean status values are counted under `needs_status_normalization_rows` and do not force success/failure.

## Timing And Paper Boundaries

No timing fields are parsed or filled. GM_Speedup and Speedup Ratio Percentiles are not computed. No paper tables are rendered and no reports/results paths are written.

## Validation Result

Checks passed: true.

## Next Safe Action

Review the dry-run outputs and status-normalization caveats. If accepted, authorize a separate status-normalization and official metric-computation task; keep overlap resolution, timing, reports/results updates, and paper rendering separate.
