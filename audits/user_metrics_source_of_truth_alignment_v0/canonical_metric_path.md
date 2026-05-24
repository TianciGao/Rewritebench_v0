# Canonical Metric Path

Authoritative implementation:

- `src/sql_rewrite_bench/local_metrics.py`
- public facade: `python -m cli.main user compute-local-metrics`
- direct internal API: `compute_and_write_local_metrics(run_dir)`

Canonical source-run inputs:

- `runs/user/<run_id>/ledger.csv`
- `runs/user/<run_id>/config.yaml`
- `runs/user/<run_id>/timing/rows/*.json`, when timing exists

Canonical metrics outputs:

- `runs/user/<run_id>/metrics/local_metrics_summary.json`
- `runs/user/<run_id>/metrics/local_metrics_by_engine.csv`
- `runs/user/<run_id>/metrics/local_metrics_by_pool.csv`
- `runs/user/<run_id>/metrics/local_timing_speedup_rows.csv`
- `runs/user/<run_id>/metrics/local_metrics_boundary.md`

D035 user-facing exported outputs:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

Actual CLI shape in this repo:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines <engine_or_comma_list> \
  --adapter-command "<adapter command>" \
  --output-root <tmp_or_output_root> \
  --run-id <run_id> \
  --enable-db-execution \
  --enable-checker \
  --collect-timing
```

For multiple engines, the facade currently writes source runs and exports with per-engine run ids:

- `<run_id>__postgres`
- `<run_id>__mysql`
- `<run_id>__spark`

Compute local metrics per produced source run:

```bash
python -m cli.main user compute-local-metrics \
  --run-id <run_id_or_run_id__engine> \
  --source-run-root runs/user \
  --output-root <tmp_or_output_root>
```

Important correction: the current CLI does not expose `--run-dir`; it exposes `--run-id` and `--source-run-root`.

Audit helpers may validate CSV headers, count rows, inspect boundary flags, and summarize whether canonical outputs exist. They must not hand-compute route-level local metrics or produce authoritative route cards.
