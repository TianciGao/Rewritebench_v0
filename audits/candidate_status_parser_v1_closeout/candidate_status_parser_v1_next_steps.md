# candidate_status_parser_v1 Next Steps

## Option A: Future Metric-input Authorization Overlay For Ready Rows

Authorize a separate `metric_input_authorization_overlay_v0` for rows labeled `ready_candidate_status_only` in `candidate_status_metric_input_readiness_review.csv`. This would be an authorization overlay only and must not compute metrics.

Recommendation: possible next step after maintainer review of the readiness CSV.

## Option B: Manual Overlap Review

Review rows labeled `needs_source_overlap_review`, especially P001/P002 and P002/P003 overlaps. Define source precedence and whether overlap rows can later become metric-input eligible.

Recommendation: required before any overlap row is authorized for metric input.

## Option C: Additional Non-timing Evidence For Unresolved Rows

Curate additional row-level non-timing evidence sources for the 425 unresolved rows, especially SQLGlot optimize, SQLGlot no-op, remaining Repair-1 rows, and remaining Calcite rows.

Recommendation: keep this as a separate whitelist/approval pass.

## Option D: Timing Adapter Planning

Plan timing parsing separately. Timing must not backfill `timed`, `latency_ms`, `speedup_ratio`, or `timing_eligible` without separate authorization.

Recommendation: defer until non-timing status readiness is resolved.

## Option E: Portability / Verifier / Explainability Planning

Defer candidate metrics and move to other adapter families if candidate status coverage is intentionally paused.

Recommendation: lower priority than reviewing parser-v1 readiness, because non-timing candidate rows are now partially filled.

## Recommended Next Safe Action

Do not compute metrics yet. First review `candidate_status_metric_input_readiness_review.csv`. If enough rows are accepted, authorize a separate `metric_input_authorization_overlay_v0` for status-only rows labeled `ready_candidate_status_only`; keep timing adapter work separate.
