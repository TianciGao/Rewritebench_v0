# metric_input_authorization_overlay_v0 Report

Date: 2026-05-17

## Purpose And Scope

This audit-only overlay authorizes future metric-input eligibility for exactly the `candidate_status_parser_v1` filled rows labeled `ready_candidate_status_only` in `audits/candidate_status_parser_v1_closeout/candidate_status_metric_input_readiness_review.csv`.

It does not rewrite `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`. It does not compute metrics, fill timing fields, render paper tables, update reports/results, change denominators, change paper results, or modify raw legacy evidence.

## Maintainer Authorization Statement

The maintainer authorized `metric_input_authorization_overlay_v0` only for non-timing candidate-status rows with `readiness_label=ready_candidate_status_only`. The authorization excludes overlap rows, unresolved rows, timing fields, speedup fields, metric computation, paper table rendering, reports/results updates, denominator changes, and paper-result changes.

## Input Readiness File

- Input: `audits/candidate_status_parser_v1_closeout/candidate_status_metric_input_readiness_review.csv`
- Filled rows reviewed: 175
- Ready rows authorized: 130
- Overlap rows denied: 45
- Unresolved rows not reviewed by overlay: 425

## Authorized Row Count

`metric_input_authorized_overlay=true` rows: 130.

These rows are authorized only as status-only, non-timing candidate evidence for a future separate metrics pipeline. This overlay does not itself compute any metric.

## Unauthorized Rows

`metric_input_authorized_overlay=false` rows: 45.

These rows correspond to `needs_source_overlap_review` and remain unauthorized until manual source-overlap review is complete.

## Unresolved Rows Status

The 425 unresolved parser-v1 rows are not included in this overlay and remain unauthorized.

## Why This Is Not Metrics Computation

The overlay records eligibility decisions only. It performs no aggregation, numerator/denominator calculation, rate calculation, speedup calculation, leaderboard construction, or paper-table rendering.

## Why Timing Remains Unauthorized

All timing and speedup fields remain unauthorized: `timed`, `latency_ms`, `speedup_ratio`, and `timing_eligible`. Timing requires a separate adapter and separate authorization.

## Why The Original Parser Ledger Is Not Rewritten

The parser-v1 ledger remains immutable audit output from the bounded parser task. This overlay stores authorization as a separate file so downstream tasks can join by `record_id` without mutating source evidence.

## Next Safe Action

Do not compute metrics yet. Either perform manual overlap review for the 45 denied rows or prepare a status-only metrics dry-run plan that explicitly handles partial denominator coverage. Keep timing adapter work separate.
