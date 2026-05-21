# Environment Check

Date: 2026-05-21.

Command:

```bash
bash -lc '
source scripts/env_mysql.local.sh
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py
'
```

## Result

PostgreSQL:

- `psql` CLI: found at `/usr/bin/psql`.
- Config: present after sourcing `scripts/env_postgres.local.sh`.
- Probe: ok.
- Version prefix observed: `PostgreSQL 17.9`.

MySQL:

- `mysql` CLI: found at `/usr/bin/mysql`.
- Config: present after sourcing `scripts/env_mysql.local.sh`.
- Probe: ok.
- Password and DSN values were not printed.

Spark:

- `SPARK_LOCAL_IP`: unset.
- Status: deferred/fail-closed.
- Probe: skipped.

## Boundary

- This was a local readiness probe only.
- No official metrics were computed.
- No timing/speedup was computed.
- No reports/results were updated.
- Spark execution remains unimplemented and fail-closed.
