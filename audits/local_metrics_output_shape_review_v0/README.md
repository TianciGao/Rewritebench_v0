# local_metrics_output_shape_review_v0

Verdict: `completed_with_minor_output_shape_note`

This audit reviewed the output shape of the non-official local metrics calculator before any broader local diagnostic projection.

Reviewed existing bounded SQLGlot noop timing smoke metrics outputs:

- `runs/user/timing_sqlglot_noop_postgres_smoke/metrics/`
- `runs/user/timing_sqlglot_noop_mysql_smoke/metrics/`
- `runs/user/timing_sqlglot_noop_spark_smoke/metrics/`

No Common-core rerun was performed. No calculator code, formulas, source files, tests, scripts, case packages, case sets, `reports/`, `results/`, retained evidence, or `runs/user/` outputs were modified.

## Review Summary

- `local_metrics_summary.json` contains the required identity, grouping, metric-definition, summary, per-denominator, diagnostic, deferred-metric, prohibited-output, and local-only boundary sections for all three reviewed runs.
- `local_metrics_by_engine.csv` and `local_metrics_by_pool.csv` expose the required D033 local metric fields, diagnostic-only funnel fields, timing fields, deferred metric statuses, and boundary flags.
- `local_timing_speedup_rows.csv` is row-grained and marks row-level timing inclusion only; it does not rank methods or select winners.
- Performance summaries use strict exact + timed rows only. Each reviewed bounded smoke run has 2 selected rows, 2 exact rows, 2 timed rows, and speedup denominator 2.
- Deferred metrics are explicit: Regression@20 is not implemented, Semantic Equivalence Rate is `not_applicable`, Cross-Engine GM Speedup Ratio is `not_applicable`, and POCR is deferred with `skill_adapter_pending=true`.
- No output sets `official_metric_input=true`, `paper_result_input=true`, or `retained_evidence_promoted=true`.

## Issue Note

The reviewed files intentionally include explicit false leaderboard boundary fields such as `leaderboard_input=false` and `leaderboard_output_created=false`. This is a boundary guard, not a leaderboard artifact, ranking, winner selection, or official output.

Because the review checklist also asked to confirm that no output includes the literal token `leaderboard`, this audit records a minor wording/shape ambiguity: the token appears only in negative boundary fields and prohibited-output guards.

## Recommendation

Proceed only after accepting this boundary-field wording. If the project wants a literal zero occurrence of `leaderboard` in local metrics files, authorize a separate output-shape patch; otherwise keep the explicit false boundary guard because it is clear and consistent with prior local-only artifacts.
