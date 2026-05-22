# Output Directory Contract

The v0 user-facing output contract follows D035:

```text
output/
  results/
    <run_id>/
  logs/
    <run_id>/
  reports/
    <run_id>/
```

The older `output/<run_id>/results|logs|reports` shape is superseded and should be mentioned only as historical context.

## Results Root

`output/results/<run_id>/` contains machine-readable artifacts:

```text
output/results/<run_id>/
  run_manifest.json
  ledger.csv
  quality_summary.json
  failure_buckets.csv
  tag_slices.csv
  candidates/
  execution/
  checker/
  timing/
  metrics/
  verifier/
```

## Logs Root

`output/logs/<run_id>/` contains logs and environment diagnostics:

```text
output/logs/<run_id>/
  command.log
  adapter_stdout.log
  adapter_stderr.log
  engine_env.json
  failures.log
  timing.log
  verifier.log
```

## Reports Root

`output/reports/<run_id>/` contains human-readable summaries:

```text
output/reports/<run_id>/
  summary.md
  failure_buckets.md
  tag_slices.md
  metrics_summary.md
  verifier_summary.md
  boundary.md
```

These paths are local/user-run outputs. They are not top-level official `reports/` or `results/` surfaces.
