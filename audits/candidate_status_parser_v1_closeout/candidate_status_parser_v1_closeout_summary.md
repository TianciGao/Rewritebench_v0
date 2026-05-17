# candidate_status_parser_v1 Closeout And Metric-input Readiness Summary

Date: 2026-05-17

## Purpose And Scope

This closeout reviews the already-emitted `candidate_status_parser_v1` audit ledger and assigns audit-only metric-input readiness labels to the 175 filled non-timing rows. It reads release-repo audit outputs only.

No new candidate status parsing was performed. No additional legacy files were opened. No candidate statuses were filled by this closeout. No timing fields were filled, `metric_input_authorized` remains false for every row, and no metrics were computed.

## Parser V1 Input Summary

Approved parser-v1 sources were `P001`, `P002`, `P003`, `P011`, and `P012`. Parser v1 previously read only those approved legacy CSV status sources and produced 600 audit rows. This closeout read only release-repo audit outputs.

- Approved manifest inputs: 5.
- Ledger rows reviewed: 600.
- Ledger validation: validation_passed=True, errors=0, warnings=0.

## Filled Vs Unresolved Rows

- Row-level status rows filled by prior parser v1: 175.
- Unresolved rows: 425.
- Parser status counts: row_level_status_filled=175, unresolved_no_approved_source_match=425.
- Filled by method: calcite_hep_fail_closed=29, direct_llm_original=120, direct_llm_repair_1=26.
- Unresolved by method: calcite_hep_fail_closed=91, direct_llm_repair_1=94, sqlglot_noop=120, sqlglot_optimize=120.
- Filled by pool: CONS=30, LONGTAIL=21, PERF=54, PORT=70.
- Unresolved by pool: CONS=105, LONGTAIL=69, PERF=186, PORT=65.
- Filled by engine: mysql=57, postgres=57, spark=61.
- Unresolved by engine: mysql=143, postgres=143, spark=139.

## Filled Rows By Method / Route / Pool / Engine

Detailed method x pool x engine counts are in `candidate_status_parser_v1_filled_distribution.csv`. Direct LLM original is fully filled at 120 rows through P001 with P002 overlap on 26 rows. Repair-1 has 26 filled rows. Calcite HEP fail-closed has 29 filled rows. SQLGlot optimize and SQLGlot no-op remain fully unresolved.

## Unresolved Rows By Method / Route / Pool / Engine

Detailed unresolved groups are in `candidate_status_parser_v1_unresolved_distribution.csv`. Direct LLM Repair-1 and Calcite unresolved rows remain `unresolved_no_approved_source_match`; SQLGlot optimize and SQLGlot no-op rows are `unresolved_route_not_covered_by_v1`. These rows block metric input until separately reviewed and validated.

## Per-source Contribution Summary

- `P001` `MP001`: rows_read=120, rows_matched=120, rows_filled=120, rows_rejected=0.
- `P002` `MP002`: rows_read=26, rows_matched=52, rows_filled=52, rows_rejected=0.
- `P003` `MP003`: rows_read=19, rows_matched=19, rows_filled=19, rows_rejected=0.
- `P011` `MP004`: rows_read=27, rows_matched=27, rows_filled=27, rows_rejected=0.
- `P012` `MP005`: rows_read=2, rows_matched=2, rows_filled=2, rows_rejected=0.

The sum of source matches can exceed unique filled rows because approved sources can overlap on one scaffold row. Unique filled rows remain 175.

## Overlap And Conflict Review

- P001/P002 overlap: 26 Direct LLM original rows.
- P002/P003 Repair-1 overlap: 19 rows; this is documented as failure enrichment and blocks metric-input authorization until manual overlap review.
- P011/P012 Calcite overlap: 0 rows.
- Duplicate output rows: none; parser v1 preserved one row per scaffold row.

## Metric-input Readiness Summary

Readiness labels are audit-only and do not authorize metric input.

- `needs_source_overlap_review`: 45.
- `ready_candidate_status_only`: 130.

Rows labeled `ready_candidate_status_only` are structurally ready for a future separate metric-input authorization overlay review, not for immediate metric computation. Rows labeled `needs_source_overlap_review` must be manually reviewed before any authorization because more than one approved source contributed to the row.

## Timing And Metric-input Boundary Confirmation

- `metric_input_authorized=true` rows: 0.
- `metrics_computed=true` rows: 0.
- `timed` filled rows: 0.
- `latency_ms` filled rows: 0.
- `speedup_ratio` filled rows: 0.
- `timing_eligible` filled rows: 0.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Raw legacy evidence changed: no.

## Remaining Blockers

- The 130 rows labeled `ready_candidate_status_only` still require a separate authorization overlay before metric input can be set to true.
- The 45 rows labeled `needs_source_overlap_review` require manual source-precedence review.
- The 425 unresolved rows need additional row-level non-timing evidence triage or separate parser authorization.
- Timing evidence remains outside parser-v1 scope and requires a separate timing adapter plan.

## Exact Next Safe Action

Review `candidate_status_metric_input_readiness_review.csv`. If accepted, authorize a separate `metric_input_authorization_overlay_v0` for rows labeled `ready_candidate_status_only` only; separately review overlap rows and unresolved rows. Do not compute metrics, fill timing fields, render paper tables, update reports/results, change denominators, change paper results, mutate the legacy repo, or modify raw legacy evidence without separate approval.
