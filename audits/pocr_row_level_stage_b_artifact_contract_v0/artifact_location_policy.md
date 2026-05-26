# Artifact Location Policy

Future durable local user-run diagnostic output:

```text
output/results/<run_id>/pocr/stage_b/pocr_stage_b_row_metrics.csv
output/reports/<run_id>/pocr_stage_b_row_metrics_summary.md
output/logs/<run_id>/pocr_stage_b_export.log
```

The row metrics CSV is the future aggregator input. The summary report is explanatory and must not replace the row CSV.

Committed audit packet copies may include summarized or selected row-level CSVs for design or dry-run audits, but official retained promotion requires separate authorization.

Do not update top-level `reports/` or `results/` in this task.

Aggregator must not rely on /tmp replay artifacts. Durable D035 output must be used for future reviewer-facing or promotion-facing dry-runs.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
