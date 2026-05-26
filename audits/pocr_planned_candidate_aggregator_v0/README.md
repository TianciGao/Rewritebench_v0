# POCR Planned/Candidate Aggregator v0

This audit records a reusable POCR row-metrics aggregator that reads `pocr_stage_b_row_metrics.csv` and writes diagnostic route summaries.

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

This aggregator computes promotion-diagnostic POCR@planned and POCR@candidate only.

POCR@curated remains deferred until a predeclared curated manifest exists.

Macro-average over per-row OC_i is used.

Diagnostic micro-average is not the paper formula.

Runtime route-summary path:

```text
<output_root>/results/<run_id>/pocr/aggregates/pocr_route_summary.csv
```

No live API call, API key read, annotation JSONL generation, production user replay, DB/checker/timing run, baseline rerun, candidate SQL generation or mutation, official POCR computation, paper-facing metric promotion, top-level reports/results update, retained-evidence promotion, or leaderboard output occurred.
