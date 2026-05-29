# Boundary Flags Review

The projected local metrics outputs set the required local-only boundary flags:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

The summary JSON files also report prohibited-output guards:

- `method_selection_output_emitted=false`
- `method_ordering_output_emitted=false`
- `leaderboard_output_created=false`
- `paper_table_rendered=false`
- `reports_results_updated=false`
- `retained_evidence_promoted=false`

No output sets `official_metric_input=true`, `paper_result_input=true`, or `retained_evidence_promoted=true`.

As recorded in `local_metrics_output_shape_review_v0`, the literal token `leaderboard` appears only in explicit false boundary/prohibited-output fields. No leaderboard artifact, winner field, rank field, best-method field, or method-selection output was produced.

This projection did not update `reports/` or `results/`, did not promote retained evidence, did not render paper tables, and did not create a release/export/tag.
