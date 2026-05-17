# Candidate Status Evidence Completion Round 1

## Purpose And Scope

This audit-only round reviews two candidate-status evidence gaps:

- the 45 overlap rows denied by `metric_input_authorization_overlay_v0`;
- SQLGlot row-level non-timing evidence candidates for `sqlglot_optimize` and `sqlglot_noop`.

No new candidate status parsing was performed. No metric-input authorization changed. No official or audit-only metrics were computed. No timing, speedup, report, result, denominator, paper-result, case-set, or raw legacy evidence file was modified.

## Current State Before This Round

- `candidate_status_parser_v1` emitted 600 audit rows.
- Prior parser-v1 filled 175 non-timing row-level statuses and left 425 rows unresolved.
- `metric_input_authorization_overlay_v0` authorized 130 filled rows and denied 45 overlap rows.
- SQLGlot routes remain unresolved: 120 `sqlglot_optimize` rows and 120 `sqlglot_noop` rows.
- `status_inference_overlay_v0` and normalized dry-run v2 remain audit-only and unchanged.

## Overlap-Row Review Summary

Reviewed 45 denied overlap rows from `metric_input_authorization_denied_rows.csv`.

- 26 `direct_llm_original` rows have overlap sources `P001|P002`.
- 19 `direct_llm_repair_1` rows have overlap sources `P002|P003`.
- No overlap row is authorized by this task.
- Every row in `overlap_rows_resolution_proposal.csv` keeps `would_change_metric_input_authorization=false`.

Recommended next policy: approve a priority policy in a separate task where P001 supplies generation/readiness, P002 supplies primary candidate status, and P003 supplies Repair-1 failure enrichment only.

## SQLGlot Evidence Triage Summary

Reviewed 8 SQLGlot candidate sources at release-metadata and safe header/schema-preview level only.

- 1 source is recommended as `approve_header_only_then_parser` pending explicit maintainer approval.
- 4 sources are recommended as `needs_sanitized_projection` before any parser approval.
- 1 source remains `defer_manual_review` because row grain is not proven.
- 2 sources are rejected for parser use in their current form.
- Manifest preview rows created: 10.

The strongest SQLGlot candidates are the checker/event sources with `case_id`, `engine`, `route_id`, `method_id`, and `denominator_id`, but they require sanitized projections and duplicate-source/source-priority decisions before parser use.

## Proposed Manual Decisions

- Decide whether to authorize the overlap priority policy for a future overlay v1.
- Decide whether P006 can use an explicit engine-row expansion rule or must remain deferred.
- Decide whether SGL011 or SGL012 should be the canonical SQLGlot checker-event source if one is later approved.
- Decide whether P009/SGL013 should be sanitized into non-timing projections before parser review.
- Keep P010 rejected because it is route-level aggregate only.

## Remaining Blockers

- SQLGlot row grain is not yet approved for parser input.
- Several promising SQLGlot sources carry timing, raw-log pointer, local-path pointer, duplicate-source, or mixed PORT/same-engine risks.
- Overlap rows require a maintainer-approved source-priority rule before metric-input authorization can change.
- No official metric computation is authorized.

## Boundary Confirmation

- Candidate statuses filled: no.
- Metric input authorization changed: no.
- Metrics computed: no.
- Timing fields filled: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Raw legacy evidence changed: no.
- Legacy repo modified: no.

## Exact Next Safe Action

Maintainer reviews `overlap_rows_resolution_proposal.csv` and `sqlglot_candidate_manual_decision_sheet.csv`; if accepted, separately authorize an overlap-priority authorization overlay v1 and/or a sanitized SQLGlot projection/parser task.
