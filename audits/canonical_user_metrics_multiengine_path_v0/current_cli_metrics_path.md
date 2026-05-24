# Current CLI Metrics Path

Single-run canonical command:

```bash
python -m cli.main user compute-local-metrics \
  --run-id <run_id> \
  --source-run-root runs/user \
  --output-root <output_root>
```

Multi-engine evaluate behavior:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "<adapter command>" \
  --output-root <output_root> \
  --run-id <run_id> \
  --enable-db-execution \
  --enable-checker \
  --collect-timing
```

The current facade creates one source run per engine:

- `runs/user/<run_id>__postgres/`
- `runs/user/<run_id>__mysql/`
- `runs/user/<run_id>__spark/`

New aggregate canonical command:

```bash
python -m cli.main user compute-local-metrics \
  --run-id-prefix <run_id> \
  --engines postgres,mysql,spark \
  --aggregate-run-id <run_id> \
  --source-run-root runs/user \
  --output-root <output_root>
```

This command consumes the per-engine run directories, writes canonical metrics under `runs/user/<aggregate_run_id>/metrics/`, then exports the aggregate to:

- `output/results/<aggregate_run_id>/`
- `output/logs/<aggregate_run_id>/`
- `output/reports/<aggregate_run_id>/`

The aggregate command is local diagnostic only and does not compute official metrics, Semantic Equivalence Rate, formal Regression@20, POCR, or leaderboard output.
