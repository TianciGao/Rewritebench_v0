# candidate_status_parser_v1 Next Steps

## Option A: Metric-input Readiness Review For 175 Filled Rows

Review only the 175 filled audit rows for schema consistency, source precedence, overlap handling, denominator joins, and status vocabulary. This does not authorize metrics by itself.

Recommendation: choose this first, because parser v1 produced mixed source overlap that should be reviewed before any metric-input eligibility decision.

## Option B: Additional Non-timing Evidence Triage For 425 Unresolved Rows

Curate more row-level non-timing evidence sources for unresolved rows, especially SQLGlot optimize, SQLGlot no-op, remaining Repair-1 rows, and remaining Calcite rows. This should be a separate whitelist/approval pass.

Recommendation: run in parallel only as audit triage; do not parse more rows until sources are explicitly approved.

## Option C: Timing Adapter Planning

Plan timing parsing for already-filled candidate rows, but keep it separate from non-timing status parsing. Timing must not backfill `timed`, `latency_ms`, `speedup_ratio`, or `timing_eligible` without separate authorization.

Recommendation: defer until status precedence and metric-readiness boundaries are reviewed.

## Option D: Portability / Verifier / Explainability Adapter Planning

Stop candidate parsing and move to other adapter families. This may be useful if candidate status coverage is intentionally paused.

Recommendation: lower priority than reviewing parser-v1 row quality, because candidate rows are now partially filled and need closeout/readiness gates.

## Recommended Next Safe Action

Do not authorize metrics yet. First perform a metric-input readiness review for the 175 filled audit rows and separately triage row-level evidence for the 425 unresolved rows. Timing adapter work should remain separate.
