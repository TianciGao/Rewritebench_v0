# Implementation Summary

Implemented a minimal POCR Stage B row metrics exporter in `src/sql_rewrite_bench/pocr/stage_b_row_metrics.py`.

The exporter writes exactly one durable runtime CSV for future aggregation input:

```text
<output_root>/results/<run_id>/pocr/stage_b/pocr_stage_b_row_metrics.csv
```

It is wired into the existing user-facing `pocr-diagnostic` replay output flow through `write_pocr_diagnostic_user_outputs`, after diagnostic rows and pool summaries are available.

The exported row granularity is one row per diagnostic route x case_id x engine row. The CSV includes identity fields, denominator membership flags, annotation and binding status fields, Stage B operation atom counts, semantic guard counts, per-row `oc_i` / `oc_i_fail_closed`, fail-closed status, curated-denominator placeholder, and diagnostic boundary constants.

The exporter does not compute route-level POCR@planned, POCR@candidate, POCR@curated, official POCR, paper metrics, retained evidence, or leaderboard output.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
