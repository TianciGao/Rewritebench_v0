# Exported Output Shape

The Phase 2A exporter writes the following user-facing output shape.

## Results

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

Notes:

- `ledger.csv`, `quality_summary.json`, `tag_slices.csv`, `candidates/`, `timing/`, and `metrics/` are copied only when source artifacts exist.
- `failure_buckets.csv` is derived from existing source ledger/failure artifacts.
- `execution/` and `checker/` are exported from existing source workspace subdirectories when present.
- `verifier/verifier_status.json` is an explicit N.A. placeholder; no verifier is implemented.

## Logs

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

Notes:

- Adapter stdout/stderr logs are aggregated from existing workspace logs when present.
- `engine_env.json` uses timing environment metadata when present, otherwise a safe not-available payload.
- `verifier.log` states verifier support was not run.

## Reports

```text
output/reports/<run_id>/
  summary.md
  failure_buckets.md
  tag_slices.md
  metrics_summary.md
  verifier_summary.md
  boundary.md
```

Reports are local diagnostic summaries only and are derived from source or exported artifacts.
