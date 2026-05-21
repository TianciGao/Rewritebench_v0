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

- MySQL client/config/probe: ok.
- PostgreSQL client/config/probe: ok.
- Spark: deferred/fail-closed; probe skipped.

The environment checker printed redacted configuration state only. No passwords, DSNs, or local secrets are included in this audit packet.

PostgreSQL was ready for this task, but the `--engine mysql` trial did not execute PostgreSQL target diagnostics. The five cross-dialect PORT rows failed closed as unsupported for MySQL target selection before PostgreSQL execution.
