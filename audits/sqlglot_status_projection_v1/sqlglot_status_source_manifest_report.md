# SQLGlot Status Source Manifest Report

## Purpose And Scope

This audit manifest selects reviewed SQLGlot sources for sanitized non-timing status projection.
It does not parse candidate statuses, compute metrics, authorize metric input, or touch timing fields.

## Manifest Result

- Manifest rows: 10
- Approved projection rows: 2
- Approved parser rows: 2
- Pending rows: 2
- Rejected rows: 6

## Approved Source

- `SGL011` / `sqlglot_optimize`: Approved for non-timing executed/exact/checker status projection; artifact path payload columns are not retained.
- `SGL011` / `sqlglot_noop`: Approved for non-timing executed/exact/checker status projection; artifact path payload columns are not retained.

## Fail-Closed Decisions

- P006 remains pending because deterministic engine expansion was not explicitly approved.
- P009 is rejected for this manifest because of mixed portability scope plus timing/path risk.
- SGL012 is held out as a duplicate of SGL011.
- SGL013 is rejected for raw-log pointer risk and missing denominator_id.
- P007/P008/P010 remain excluded by round1 review.

## Boundary Confirmation

- Timing sources approved: false
- Raw-log sources approved: false
- Prompt/token sources approved: false
- Metrics computed: false
