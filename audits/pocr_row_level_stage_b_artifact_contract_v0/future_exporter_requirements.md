# Future Exporter Requirements

A future modification or wrapper for `sqlrb user pocr-diagnostic` should write:

```text
output/results/<run_id>/pocr/stage_b/pocr_stage_b_row_metrics.csv
```

Exporter requirements:

- Include one row per planned/candidate-bound route x case_id x engine row.
- Include expected operation atom counts per row from `skills.md`.
- Include Stage-B-supported operation atom counts per row.
- Include presence-only, insufficient-transformation-evidence, rejected-noop, schema-invalid, and semantic guard counts.
- Include fail-closed rows instead of dropping them.
- Include candidate identity fields and candidate SHA when candidate-bound.
- Include route, method, case, engine, denominator scope, and skills hash binding.
- Include boundary constants: `diagnostic_only=true`, `official_pocr_computed=false`, `route_level_pocr_aggregated=false`, and `paper_metric_promoted=false` by default.
- Do not compute official metrics by default.
- Keep promotion mode explicit, default-off, and separately authorized.

The exporter should also write:

```text
output/reports/<run_id>/pocr_stage_b_row_metrics_summary.md
output/logs/<run_id>/pocr_stage_b_export.log
```

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
