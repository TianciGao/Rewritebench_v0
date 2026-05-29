# User Commands

Evaluate command:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware" \
  --output-root /tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_canonical_user_rerun_v0/output \
  --run-id sqlglot_optimize_schema_aware_track_a_120_canonical_v0 \
  --enable-db-execution \
  --enable-checker \
  --collect-timing
```

Canonical aggregate metrics command:

```bash
python -m cli.main user compute-local-metrics \
  --run-id-prefix sqlglot_optimize_schema_aware_track_a_120_canonical_v0 \
  --engines postgres,mysql,spark \
  --aggregate-run-id sqlglot_optimize_schema_aware_track_a_120_canonical_v0 \
  --source-run-root runs/user \
  --output-root /tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_canonical_user_rerun_v0/output
```

Both commands are user-facade commands under `src/cli`. No audit helper computed route metrics.
