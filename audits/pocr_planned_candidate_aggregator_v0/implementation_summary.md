# Implementation Summary

Implemented `src/sql_rewrite_bench/pocr/pocr_aggregator.py` as a small library-only aggregator.

Primary functions:

- `read_stage_b_row_metrics(...)`
- `aggregate_pocr_rows(...)`
- `write_pocr_route_summary(...)`
- `write_pocr_aggregate_outputs(...)`

The aggregator consumes one or more `pocr_stage_b_row_metrics.csv` files, validates required columns and diagnostic boundary constants, groups rows by `run_id`, `case_set_id`, `denominator_scope`, `method_id`, `route_id`, and `engine`, and writes route-level diagnostic summaries.

The route summary CSV is:

```text
<output_root>/results/<run_id>/pocr/aggregates/pocr_route_summary.csv
```

The optional Markdown report is:

```text
<output_root>/reports/<run_id>/pocr_route_summary.md
```

The implementation intentionally does not modify `local_metrics.py`, does not add a user-facing CLI command, and does not compute official POCR.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
