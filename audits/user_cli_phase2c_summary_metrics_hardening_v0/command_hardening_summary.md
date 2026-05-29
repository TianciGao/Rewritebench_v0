# Command Hardening Summary

## summarize

Before: printed `output/reports/<run_id>/summary.md` when present, otherwise printed `run_manifest.json`.

After: prints a composite local diagnostic summary:

- output roots
- run summary or run manifest
- failure buckets
- tag slices
- local metrics
- verifier status
- boundary

Missing optional reports are shown as explicit `N.A.` sections.

## compute-local-metrics

Before: printed the source metrics directory, exported metrics path, and a short boundary.

After: also prints:

- user-facing metrics output path
- user-facing `metrics_summary.md` report path
- Semantic Equivalence Rate `N.A.` without verifier evidence
- POCR deferred
- full local-only boundary flags

The command still delegates to `sql_rewrite_bench.local_metrics.compute_and_write_local_metrics` and `sql_rewrite_bench.user_output.export_run_to_output`.

## show-boundary

The generic boundary text now explicitly says:

- Not official metrics.
- Not paper results.
- Not retained evidence.
- Not leaderboard input.
- Semantic Equivalence Rate is `N.A.` until formal VeriEQL or SQLSolver evidence exists.
- POCR remains deferred pending external skill-adapter integration.
