# normalized_status_only_metrics_dryrun_v2 Report

## Purpose And Scope

This is an audit-only normalized status metrics dry-run using observed normalized fields plus `status_inference_overlay_v0` for R1 inferred generated support.

It is not official metrics computation, not a paper result, not timing computation, and not reports/results migration.

## Inputs

- `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`
- `audits/status_field_normalization_v0/normalized_candidate_status_overlay_v0.csv`
- `audits/status_inference_overlay_v0/status_inference_overlay_v0.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`

## Inference Overlay Use

The dry-run uses 94 rows with `inferred_generated=true`. Inference is used only for Generation Rate dry-run logic and only when `normalized_generated=unknown`.

## Difference From v1

V1 used observed normalized values only. V2 keeps the same observed counts and adds R1 inferred-generated rows separately. Execution Coverage Rate and Result Consistency Rate remain observed-only.

## Denominator Handling

The 600 planned Track A same-engine candidate rows remain visible. The 130 authorized rows are inputs, 45 overlap rows remain unauthorized, and 425 unresolved rows remain outside success evidence.

## Partial Coverage Warnings

The dry-run remains partial and audit-only. SQLGlot routes still have no authorized normalized status rows. Inference does not resolve execution, exactness, timing, overlap, or unresolved-row gaps.

## Why No Official Metrics

Every dry-run table row has `dry_run_value_is_official=false`, `paper_result=false`, and `audit_only=true`. Official metrics require separate authorization.

## Why No Paper Tables

No paper renderer is implemented or invoked, and no reports/results paths are written.

## Why Timing Remains Separate

Timing, latency, speedup, and timing eligibility are not parsed or computed. GM_Speedup and Speedup Ratio Percentiles are not computed.

## Next Safe Action

Review the v2 delta and caveats. If accepted, separately authorize either official metric readiness review, additional evidence parsing, or overlap resolution; keep timing and paper rendering separate.
