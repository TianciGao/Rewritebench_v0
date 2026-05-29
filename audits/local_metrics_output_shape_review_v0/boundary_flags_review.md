# Boundary Flags Review

## Local-Only Flags

All reviewed summary JSON files set:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

All reviewed by-engine, by-pool, and timing-speedup CSV rows expose the same boundary flags with the same false official/paper/retained/leaderboard status.

All reviewed `local_metrics_boundary.md` files state local diagnostic only and explicitly mark official metric input, paper result input, retained evidence promotion, leaderboard input, reports/results update, and paper table rendering as false.

## Prohibited Output Fields

`local_metrics_summary.json` includes:

- `method_selection_output_emitted=false`
- `method_ordering_output_emitted=false`
- `leaderboard_output_created=false`
- `paper_table_rendered=false`
- `reports_results_updated=false`
- `retained_evidence_promoted=false`

No reviewed output contains `official_metric_input=true`, `paper_result_input=true`, or `retained_evidence_promoted=true`.

## Literal Token Note

The literal token `leaderboard` appears in boundary guard fields and markdown boundary text:

- `leaderboard_input=false`
- `leaderboard_output_created=false`
- `Leaderboard input: false`

This is not a leaderboard artifact, ranking, or method-selection output. It is an explicit negative claim boundary. If future consumers require a zero-token policy for the word `leaderboard`, that should be handled in a separate output-shape patch because it would alter the existing boundary vocabulary.

## Verdict

Boundary flags are correct. The only issue is a non-blocking wording ambiguity between the desired "no leaderboard output" property and the intentional use of explicit false leaderboard boundary fields.
