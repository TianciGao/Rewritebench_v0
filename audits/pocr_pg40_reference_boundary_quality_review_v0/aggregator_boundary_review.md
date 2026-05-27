# Aggregator Boundary Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

The aggregator at `src/sql_rewrite_bench/pocr/pocr_aggregator.py` was reviewed.

Boundary checks:

- The aggregator consumes one or more `pocr_stage_b_row_metrics.csv` files.
- It validates required row-metrics columns and diagnostic boundary constants.
- It does not read source SQL, positive SQL, candidate SQL, no-op candidates, or taxonomy metadata.
- It does not infer operation atoms.
- It groups rows by run, case set, denominator scope, method, route, and engine.
- It computes POCR@planned and POCR@candidate promotion-diagnostic values from row-level `oc_i_fail_closed`.
- It uses macro-average over per-row OC_i.
- It keeps diagnostic micro-average separately labeled as `diagnostic_micro_average_supported_over_expected`.
- It emits `pocr_curated=NA` and `pocr_curated_status=curated_manifest_missing`.
- It emits `official_pocr_computed=false`, `route_level_official_pocr_score_emitted=false`, `paper_metric_promoted=false`, and `leaderboard_output=false`.

Verdict: `pass`.

The aggregator cannot convert positive SQL or no-op control evidence into numerator support because it only aggregates already exported Stage B row metrics.

Boundary retained: POCR@curated remains deferred until a predeclared curated manifest exists.
