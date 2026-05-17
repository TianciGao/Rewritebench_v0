# Combined Candidate Status Overlay v2 Report

## Purpose And Scope

This audit overlay combines existing candidate_status_parser_v1 output with SQLGlot sanitized projection parser output.
It preserves the 600-row scaffold accounting and does not modify either input ledger.

## Summary

- Total rows: 600
- SQLGlot rows filled: 137
- Total filled rows: 312
- Unresolved rows: 288

## Filled Rows By Method

- `calcite_hep_fail_closed`: 29
- `direct_llm_original`: 120
- `direct_llm_repair_1`: 26
- `sqlglot_noop`: 72
- `sqlglot_optimize`: 65

## Boundary Confirmation

- Metrics computed: false
- Timing fields filled: false
- Reports/results changed: false
- Denominator changed: false
