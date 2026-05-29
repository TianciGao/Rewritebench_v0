# Local Metrics And Summarize Review

`compute-local-metrics`:

- Delegates to `sql_rewrite_bench.local_metrics.compute_and_write_local_metrics`.
- Exports through `sql_rewrite_bench.user_output.export_run_to_output`.
- Prints a local-only boundary line.
- Does not compute official metrics.
- Does not write top-level `reports/` or `results/`.
- Does not emit leaderboard/ranking/winner output.

`summarize`:

- Reads existing exported `output/reports/<run_id>/summary.md` when present.
- Falls back to `output/results/<run_id>/run_manifest.json` when summary Markdown is absent.
- Does not recompute metrics.
- Does not update any output artifacts.
- Does not touch top-level `reports/` or `results/`.

Focused tests cover delegation, output-root protection, and local-only summary output.
