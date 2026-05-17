# Status-Only Metrics Dry-Run Plan

## Future Dry-Run Purpose

A future dry run could test status-only metric plumbing against explicitly authorized non-timing candidate-status rows without rendering paper tables or changing official reports/results. This task only plans that dry run; it does not compute any metric.

## Inputs

- Authorized overlay rows: 130 rows from `metric_input_authorization_overlay_v0.csv` where `metric_input_authorized_overlay=true`.
- Denied overlap rows: 45 rows remain unauthorized.
- Unresolved rows: 425 rows remain unauthorized.
- Denominator scaffold: Track A same-engine, 120 planned rows per method route and 600 scaffold rows across five method routes.

## Outputs For A Future Dry Run

A future dry-run output, if separately authorized, should be audit-only and clearly labeled as partial-coverage dry-run output. It should not write `results/retained`, `reports/evaluation`, paper tables, or official production ledgers.

## Denominator Handling

The future dry run must keep the planned denominator visible. The 130 authorized rows do not replace the 120-row per-method denominator or the 600-row scaffold. Unauthorized overlap rows and unresolved rows must remain visible as blocked or unresolved denominator members.

## Partial Coverage Warnings

Every future dry-run table must state that only 130 filled rows are authorized, 45 overlap rows remain unauthorized, and 425 rows remain unresolved. Any method with partial or zero authorized rows must be reported as partial coverage, not omitted.

## No-Global-Leaderboard Guard

Outputs must be grouped by method route, engine, pool, and denominator scope. They must not collapse Direct LLM, Repair-1, SQLGlot, Calcite, timing-eligible, and non-timing rows into a single ranking.

## No Timing Fields

The dry run may not read, fill, derive, or summarize `timed`, `latency_ms`, `speedup_ratio`, or `timing_eligible`. Timing adapter work remains separate.

## No Paper Tables Or Reports/Results Updates

The dry run must not render paper tables, update `reports/`, update `results/`, change denominators, or change paper results.

## Validation Gates

- Input rows must join to the Track A same-engine denominator by `case_id`, `engine`, and `denominator_id`.
- Only rows with `metric_input_authorized_overlay=true` may be used as metric inputs.
- Overlap and unresolved rows must remain visible in denominator accounting.
- Timing and speedup fields must be empty or ignored.
- No global leaderboard output may be produced.
- Metrics implementation must be separately authorized before any rate or ratio is computed.

## Exact Authorization Needed Before Implementation

A future task must explicitly authorize a status-only metrics dry-run implementation, name the allowed metric families, define output paths, and reaffirm that timing, paper rendering, reports/results updates, denominator changes, and paper-result changes remain out of scope unless separately approved.
