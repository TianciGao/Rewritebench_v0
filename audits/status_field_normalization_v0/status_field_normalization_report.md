# status_field_normalization_v0 Report

## Purpose And Scope

This task normalizes non-timing status fields for the 130 candidate-status rows authorized by `metric_input_authorization_overlay_v0`.

The output is an audit-only normalization overlay. It is not official metrics computation, not a paper result, not reports/results migration, and not timing adapter work.

## Input Files

- `audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv`
- `audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv`

## Rows Normalized

- Authorized rows processed: 130
- Overlap rows excluded: 45
- Unresolved rows excluded: 425
- Rows needing manual mapping: 0

## Fields Normalized

`generated`, `ready`, `executed`, `exact`, `result_status`, `failure_stage`, `failure_type`, `parse_status`, and `checker_status`.

## Observed Raw-Value Summary

The observed-value inventory contains 28 field/raw-value rows. Each row records the mapping rule, normalized value, occurrence count, affected methods, and affected record IDs.

## Manual Mapping Needs

Manual-review rows emitted: 0.

If this count is non-zero, those rows remain unsuitable for any future official metric task until the maintainer approves explicit mapping rules.

## Readiness By Method

- `direct_llm_original`: authorized=94, generated_known=0, ready_known=94, executed_known=0, exact_known=0, manual_mapping_rows=0, ready_for_status_dryrun=false
- `direct_llm_repair_1`: authorized=7, generated_known=7, ready_known=7, executed_known=0, exact_known=0, manual_mapping_rows=0, ready_for_status_dryrun=false
- `calcite_hep_fail_closed`: authorized=29, generated_known=0, ready_known=0, executed_known=2, exact_known=2, manual_mapping_rows=0, ready_for_status_dryrun=false

## Why No Metrics Were Computed

Normalization converts status vocabulary only. It does not aggregate rows, compute rates, or produce benchmark results.

## Why Timing Remains Untouched

Timing fields are outside this task. The script does not normalize, fill, parse, or infer `timed`, `latency_ms`, `speedup_ratio`, or `timing_eligible`.

## Why The Original Parser Ledger Was Not Modified

The normalization output is a separate overlay under `audits/status_field_normalization_v0/`. The parser-v1 ledger and metric-input authorization overlay remain unchanged.

## Next Safe Action

Review `normalized_candidate_status_overlay_v0.csv` and `status_normalization_observed_values.csv`. If accepted, authorize a separate status-only metrics dry-run v1 over normalized fields; keep official metrics, overlap resolution, timing, reports/results updates, and paper rendering separate.
