# Baseline Reproduction Examples

These examples point to the user-facing baseline reproduction manual:

- `docs/baseline_reproduction.md`

The examples are local diagnostic reproduction patterns only. They do not compute official metrics, update paper-facing reports/results, promote retained evidence, or create leaderboard output.

## SQLGlot No-Op Track A Pattern

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root output \
  --run-id sqlglot_noop_track_a_120_local \
  --enable-db-execution \
  --enable-checker \
  --collect-timing \
  --timing-repetitions 5 \
  --timing-timeout 30
```

Then aggregate local diagnostics:

```bash
PYTHONPATH=src python -m cli.main user compute-local-metrics \
  --run-id-prefix sqlglot_noop_track_a_120_local \
  --engines postgres,mysql,spark \
  --aggregate-run-id sqlglot_noop_track_a_120_local \
  --source-run-root runs/user \
  --output-root output
```

Do not commit output/.
