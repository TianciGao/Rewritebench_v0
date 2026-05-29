# POCR Minimal Stage B Row Metrics Exporter v0

This audit records the implementation of the minimal durable row-level POCR Stage B exporter.

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

This exporter only writes one durable row-level Stage B metrics CSV.

Runtime CSV path:

```text
<output_root>/results/<run_id>/pocr/stage_b/pocr_stage_b_row_metrics.csv
```

POCR@planned and POCR@candidate remain D039 promotion views.

POCR@curated remains deferred until a predeclared curated manifest exists.

No experiment was run. No live API call was made. No API key was read. No annotation JSONL was generated. No DB/checker/timing run, baseline rerun, candidate SQL generation or mutation, official POCR computation, route-level aggregation, paper-facing metric promotion, top-level reports/results update, retained-evidence promotion, or leaderboard output occurred.
