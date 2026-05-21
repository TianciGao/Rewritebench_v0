# Environment Check

Command:

```bash
set -a
[ -f scripts/env_mysql.local.sh ] && source scripts/env_mysql.local.sh
[ -f scripts/env_postgres.local.sh ] && source scripts/env_postgres.local.sh
set +a
python scripts/dev/check_local_engine_env.py
```

Result:

- PostgreSQL client/config/probe: ok.
- MySQL client/config/probe: ok.
- Spark: deferred/fail-closed; probe skipped.

The checker printed redacted configuration state only. No passwords or connection strings were recorded in this audit packet.
