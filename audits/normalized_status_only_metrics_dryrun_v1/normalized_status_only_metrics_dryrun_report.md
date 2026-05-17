# normalized_status_only_metrics_dryrun_v1 Report

## Purpose And Scope

This is an audit-only normalized status metrics dry run over the normalized non-timing candidate-status overlay.

It is not official metrics computation, not a paper result, not reports/results migration, not timing computation, and not a production ledger.

## Input Files

- `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`
- `audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`

## Authorization Boundary

Only rows with `metric_input_authorized_overlay=true`, `readiness_label=ready_candidate_status_only`, and a normalized overlay row were used.

Authorized normalized input rows: 130

Unauthorized overlap rows excluded: 45

Unresolved rows preserved in accounting: 425

## Normalization Overlay Used

The dry run uses `normalized_generated`, `normalized_executed`, and `normalized_exact` for metric numerator membership. It also carries normalized readiness, result status, failure, parse, and checker fields for caveat reporting.

## Metrics Dry-Runed

- Generation Rate
- Execution Coverage Rate
- Result Consistency Rate

Every output row is marked `audit_only=true`, `official_metric=false` via `dry_run_value_is_official=false`, and `paper_result=false`.

## Denominator Handling

The planned Track A same-engine denominator remains visible. Unauthorized overlap rows and unresolved rows are counted as not authorized/unresolved, not dropped, and not used as success evidence.

## Partial Coverage Warnings

The dry run is partial: 130 authorized rows are available, 45 overlap rows remain unauthorized, and 425 rows remain unresolved.

## Status Normalization Caveats

Unknown normalized fields are reported separately. `normalized_ready=true` does not imply `normalized_generated=true`. `normalized_exact=true` does not imply `normalized_executed=true`.

## Difference From status_only_metrics_dryrun_v0

v0 used raw parser status fields and therefore produced broad `needs_status_normalization` caveats. v1 uses the separate normalization overlay and distinguishes true, false, unknown, not_applicable, and needs_manual_mapping status values.

## Timing And Paper Boundaries

No timing fields are parsed or filled. GM_Speedup and Speedup Ratio Percentiles are not computed. No paper tables are rendered and no reports/results paths are written.

## Next Safe Action

Review the normalized dry-run table and caveats. If accepted, separately authorize an official metric-computation task or additional evidence parsing; keep timing, overlap resolution, reports/results updates, and paper rendering separate.
