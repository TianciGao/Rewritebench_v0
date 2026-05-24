# User Commands

Environment preflight used local environment scripts:
- `source scripts/env_postgres.local.sh`
- `source scripts/env_mysql.local.sh`
- `source scripts/env_spark.local.sh`

Evaluate command used:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root /tmp/sqlrb_sqlglot_noop_track_a_120_canonical_user_rerun_v0/output \
  --run-id sqlglot_noop_track_a_120_canonical_v0 \
  --enable-db-execution \
  --enable-checker \
  --collect-timing
```

Canonical aggregate metrics command used:

```bash
python -m cli.main user compute-local-metrics \
  --run-id-prefix sqlglot_noop_track_a_120_canonical_v0 \
  --engines postgres,mysql,spark \
  --aggregate-run-id sqlglot_noop_track_a_120_canonical_v0 \
  --source-run-root runs/user \
  --output-root /tmp/sqlrb_sqlglot_noop_track_a_120_canonical_user_rerun_v0/output
```

Evaluate produced per-engine source runs, so the aggregate `compute-local-metrics` form was used.
