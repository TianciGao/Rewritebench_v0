# SQLGlot Candidate Status Parser v1 Report

## Purpose And Scope

This parser emits audit-only SQLGlot rewrite_candidate_cell rows from sanitized non-timing projections.
It reads no raw logs, timing arrays, prompt/token traces, or artifact payloads.

## Parser Summary

- SQLGlot scaffold rows expected: 240
- Rows emitted: 240
- Row-level status rows filled: 137
- Unresolved SQLGlot rows: 103
- Methods covered: sqlglot_noop, sqlglot_optimize

## Method Coverage

- `sqlglot_noop`: 72 filled rows
- `sqlglot_optimize`: 65 filled rows

## Boundary Confirmation

- Timing fields filled: 0
- metric_input_authorized rows: 0
- Metrics computed: false
- Reports/results changed: false

## Limitation

SGL011 supports executed/exact/checker outcome fields only. Generated and ready are not inferred from checker artifact path existence.
