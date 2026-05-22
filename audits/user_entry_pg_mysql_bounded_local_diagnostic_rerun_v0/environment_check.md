# Environment Check

Command:

```bash
source scripts/env_mysql.local.sh && source scripts/env_postgres.local.sh && python scripts/dev/check_local_engine_env.py
```

Observed result:

- PostgreSQL probe result: ok (`psql` found; `SELECT version()` succeeded).
- MySQL probe result: ok (`mysql` found; `SELECT VERSION()` succeeded).
- Spark status: deferred/fail-closed (`SPARK_LOCAL_IP` unset; probe skipped).
- Secrets: no passwords, DSN values, or connection strings are printed in this audit.

The diagnostic reruns proceeded only after both PostgreSQL and MySQL probes passed.
