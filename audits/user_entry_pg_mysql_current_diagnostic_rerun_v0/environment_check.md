# Environment Check

Local engine environment was sourced with:

```bash
source scripts/env_mysql.local.sh
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py
```

Result:

- PostgreSQL probe: ok.
- MySQL probe: ok.
- Spark status: deferred/fail-closed; Spark local execution is not implemented.

Passwords, DSN values, and connection strings are not recorded in this audit.
