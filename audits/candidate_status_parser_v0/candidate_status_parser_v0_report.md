# candidate_status_parser_v0 Report

## Purpose And Scope

`candidate_status_parser_v0` is a manifest-first, bounded non-timing parser for Track-A same-engine `rewrite_candidate_cell` rows.
It reads the 600-row scaffold and an explicit input manifest, then fills only approved non-timing fields when exact row grain is proven.

## Manifest Creation Summary

- Approved manifest inputs: 0
- Manifest inputs parsed: 0
- Manifest inputs rejected: 0

## Parser Execution Summary

- Rows emitted: 600
- Row-level status rows filled: 0
- Unresolved rows: 600
- Parser status counts: {'no_approved_row_level_inputs': 600}

## Approved Inputs Parsed

- None in the current run.

## Inputs Rejected Or Deferred

- No manifest rows were present; no manifest inputs were rejected by the parser.

## Rows Filled Vs Unresolved

The current manifest has no approved row-level inputs. The parser therefore emits 600 unresolved rows with `parser_status=no_approved_row_level_inputs`.

## Why No Metrics Were Computed

The parser does not aggregate rows, compute rates, compute correctness denominators, compute speedups, or authorize metric input. `metrics_computed=false` and `metric_input_authorized=false` for every output row.

## Why Timing Fields Remain Excluded

`timed`, `latency_ms`, `speedup_ratio`, `timing_eligible`, `plan_available`, and `plan_artifact_path` are excluded from this parser and require separate authorization.

## Why metric_input_authorized Remains False

This output is audit-only and unresolved. Metric input authorization requires a later validated production ledger and separate maintainer approval.

## Fail-closed Behavior

If no approved row-level sources exist, or if source row grain is ambiguous, rows remain unresolved rather than inferred from route-level summaries.

## Validation Result

- scaffold row count = 600: PASS (actual=600)
- output row count = 600: PASS (actual=600)
- only rewrite_candidate_cell emitted: PASS (record_types=['rewrite_candidate_cell'])
- no timing fields filled: PASS (timed_non_na=0;timing_eligible_non_na=0;latency_values=0)
- no speedup fields filled: PASS (speedup_values=0)
- metric_input_authorized=false for all rows: PASS (values=['false'])
- metrics_computed=false: PASS (values=['false'])
- no reports/results changed: PASS (parser writes only under audits/candidate_status_parser_v0)
- denominator unchanged: PASS (parser reads scaffold only and does not write case_sets)
- paper results unchanged: PASS (no paper-facing outputs written)
- route-level summaries not distributed: PASS (parser never distributes route-level counts)
- ambiguous row-grain sources rejected: PASS (approved sources must pass exact row-grain validation before parsing)
- all approved manifest inputs parsed or explicitly rejected: PASS (approved_manifest_inputs=0;rejected_manifest_inputs=0)
- output passes ledger validator: PASS (validation_passed=True;errors=0;warnings=0)

## Next Safe Action

Review the header-only manifest and unresolved parser output. If row-level non-timing retained evidence is curated later, approve a revised input manifest before parsing. Keep timing, metrics, paper rendering, and production ledger promotion separate.
