# Implementation Summary

## Module

Added:

```text
src/sql_rewrite_bench/user_output.py
```

Primary exported functions:

- `build_output_paths(output_root, run_id, repo_root=None)`
- `export_run_to_output(run_dir, output_root, run_id=None, repo_root=None, git_commit=None)`
- `write_run_manifest(...)`
- `write_boundary_report(report_root)`
- `write_summary_report(...)`
- `write_failure_bucket_report(report_root, rows)`
- `write_tag_slice_report(source_tag_slices, report_root)`
- `write_metrics_summary_report(source_metrics_dir, report_root)`

## Behavior

The exporter reads an existing source run under `runs/user/<run_id>/` and writes a user-facing local output tree under:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

It copies source artifacts when present and writes explicit N.A. or not-available reports when optional artifacts are missing.

## Boundaries

The module does not:

- invoke adapters
- execute database backends
- run checkers
- collect timing
- compute metrics
- implement verifier integrations
- write top-level `reports/` or `results/`
- promote retained evidence
- render paper tables
- create leaderboard output
