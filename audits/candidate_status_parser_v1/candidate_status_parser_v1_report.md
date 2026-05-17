# candidate_status_parser_v1 Report

## Purpose And Scope

`candidate_status_parser_v1` is a bounded non-timing parser for Track-A same-engine `rewrite_candidate_cell` rows.
It uses only the maintainer-approved P001, P002, P003, P011, and P012 whitelist entries.

## Approved Manifest Inputs

- `P001` `MP001`: `legacy:reports/evaluation/common_core_v0/direct_llm_preflight/direct_llm_generation_matrix.csv`
- `P002` `MP002`: `legacy:reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_execute_repair_candidate_set_v1.csv`
- `P003` `MP003`: `legacy:reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_1shot_01/repair_failures.csv`
- `P011` `MP004`: `legacy:reports/evaluation/common_core_v0/calcite_hep_120_post93_frontier_audit_v1.csv`
- `P012` `MP005`: `legacy:reports/evaluation/common_core_v0/runs/calcite_hep_120_recovery_round3c_numeric_scale_canary_02_01/run_event_long.csv`

## Rejected Or Deferred Inputs

- `P004`: reject_route_level_only (do not use in candidate_status_parser_v1)
- `P005`: reject_timing_or_performance (do not use in candidate_status_parser_v1)
- `P006`: defer_manual_review (manual review before any parser use)
- `P007`: defer_manual_review (manual review before any parser use)
- `P008`: defer_manual_review (manual review before any parser use)
- `P009`: reject_timing_or_performance (do not use in candidate_status_parser_v1)
- `P010`: reject_route_level_only (do not use in candidate_status_parser_v1)
- `P013`: not_approved_for_candidate_status_parser_v1 (requires separate maintainer approval before parser use)
- `P014`: defer_manual_review (manual review before any parser use)
- `P015`: reject_route_level_only (do not use in candidate_status_parser_v1)
- `P016`: reject_timing_or_performance (do not use in candidate_status_parser_v1)
- `P017`: reject_timing_or_performance (do not use in candidate_status_parser_v1)
- `P018`: retain_reference_only (retain as locator/reference metadata only)
- `P019`: reject_timing_or_performance (do not use in candidate_status_parser_v1)

## Parser Execution Summary

- Rows emitted: 600
- Row-level status rows filled: 175
- Unresolved rows: 425
- Parser status counts: {'row_level_status_filled': 175, 'unresolved_no_approved_source_match': 425}

## Per-source Fill Summary

- `P001`: rows_read=120, rows_matched=120, rows_rejected=0
- `P002`: rows_read=26, rows_matched=52, rows_rejected=0
- `P003`: rows_read=19, rows_matched=19, rows_rejected=0
- `P011`: rows_read=27, rows_matched=27, rows_rejected=0
- `P012`: rows_read=2, rows_matched=2, rows_rejected=0

## Failure And Skip Reasons

- Rows without an approved source match remain `unresolved_no_approved_source_match`.
- Source rows with non-unique, missing, or non-scaffold row grain are rejected by the source parser.
- P013 and all deferred/rejected/reference-only proposals remain excluded.

## Why No Metrics Were Computed

The parser only copies approved non-timing row status evidence into audit ledger rows. It performs no aggregation, rate calculation, denominator calculation, speedup calculation, leaderboard construction, or metric input authorization.

## Why Timing Fields Remain Excluded

`timed`, `latency_ms`, `speedup_ratio`, `timing_eligible`, `plan_available`, and `plan_artifact_path` remain `N.A.` or empty. Timing requires a separate adapter and separate authorization.

## Why metric_input_authorized Remains False

This output is audit-only and not a production metrics ledger. Metric input authorization requires a separate validation and approval task.

## Validation Result

- scaffold row count = 600: PASS (actual=600)
- output row count = 600: PASS (actual=600)
- only rewrite_candidate_cell emitted: PASS (record_types=['rewrite_candidate_cell'])
- only approved manifest files opened: PASS (opened=['P001', 'P002', 'P003', 'P011', 'P012'])
- no unapproved sources opened: PASS (opened=['P001', 'P002', 'P003', 'P011', 'P012'])
- no timing fields filled: PASS (timed/timing_eligible remain N.A. and latency_ms empty)
- no speedup fields filled: PASS (speedup_ratio empty for all rows)
- metric_input_authorized=false for all rows: PASS (values=['false'])
- metrics_computed=false: PASS (values=['false'])
- reports/results unchanged: PASS (parser writes only under audits/candidate_status_parser_v1)
- denominator unchanged: PASS (parser reads scaffold and never writes case_sets)
- paper results unchanged: PASS (no paper-facing outputs written)
- route-level summaries not distributed: PASS (only approved row-level source rows were parsed)
- ambiguous row-grain sources rejected: PASS (source-specific parsers reject missing or duplicate row grains)
- output passes ledger validator: PASS (validation_passed=True;errors=0;warnings=0)

## Next Safe Action

Review parser-v1 filled/unresolved rows and decide whether to authorize a validation-hardening pass before any metric-input or timing work. Do not compute metrics or promote this audit output to a production ledger without separate authorization.
