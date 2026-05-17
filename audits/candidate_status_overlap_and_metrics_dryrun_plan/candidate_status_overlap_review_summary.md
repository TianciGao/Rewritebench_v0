# Candidate Status Overlap Review Summary

## Purpose And Scope

This audit reviews the 45 candidate-status rows denied by `metric_input_authorization_overlay_v0` because they were labeled `needs_source_overlap_review`. It also prepares a future status-only metrics dry-run plan for the 130 already authorized non-timing candidate-status rows.

No new candidate status parsing was performed. No legacy files were opened. No parser-v1 ledger rows or overlay rows were changed. No metrics, diagnostic rates, timing metrics, paper tables, reports/results updates, denominator changes, or paper-result changes were produced.

## Current Inputs Reviewed

- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_denied_rows.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_metric_input_readiness_review.csv`
- `audits/candidate_status_parser_v1_closeout/candidate_status_parser_v1_overlap_conflict_review.csv`
- `audits/candidate_status_parser_v1/candidate_status_parser_v1_source_use_log.csv`
- Metrics Contract v1 and ledger validation policy drafts

## Overlap Rows Reviewed

- Denied overlap rows reviewed: 45
- Overlap source combinations: P001|P002: 26, P002|P003: 19
- Methods affected: direct_llm_original: 26, direct_llm_repair_1: 19
- Proposed overlap categories: overlap_requires_manual_source_selection: 19, overlap_resolvable_by_priority_rule: 26

All rows remain unauthorized in this audit. `proposed_authorization_after_review=false` is used for every reviewed row.

## Recommended Overlap Resolution Policy

Recommended immediate policy: Option C, require manual source-by-source selection before authorizing any of the 45 overlap rows.

A future approved parser or overlay could apply a narrower priority rule: P001 may provide generation/preflight readiness, P002 may provide original/repair candidate-set status, and P003 may enrich Repair-1 failures only. That rule should be explicitly approved before any overlap row becomes metric-input eligible.

## Status-Only Dry-Run Plan Summary

A future dry run could consume only the 130 rows authorized by `metric_input_authorization_overlay_v0`. It must keep the 120-row per-method Track A same-engine denominator visible, retain the 45 overlap rows as unauthorized, retain the 425 unresolved rows as unresolved, and emit partial-coverage warnings. This task does not implement or compute Generation Rate, Execution Coverage Rate, Result Consistency Rate, or diagnostics.

## Risks

- P001/P002 overlap can conflate preflight readiness with candidate-set status if field precedence is not explicit.
- P002/P003 overlap can let failure enrichment override a successful candidate status if precedence is not guarded.
- Route-level or aggregate counts must not be distributed into row-level statuses.
- Timing fields remain absent and unauthorized.
- The 130 authorized rows cover only part of the 600-row scaffold and must not be treated as a complete denominator.

## Next Safe Action

Maintainer reviews `candidate_status_overlap_review.csv` and chooses an overlap policy. Separately authorize any status-only metrics dry-run implementation; do not compute metrics, fill timing fields, render paper tables, update reports/results, change denominators, change paper results, mutate the legacy repo, or modify raw legacy evidence.
