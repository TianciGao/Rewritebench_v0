# Local Engine Setup

This page describes local environment setup for optional SQL-RewriteBench diagnostic engines. These settings are for local diagnostics only. They do not define official metrics, paper tables, report updates, result updates, retained evidence, timing, speedup, or leaderboard rows.

## Scope

The user-entry runner can run non-DB adapter capture without any database environment. Database execution remains opt-in through local diagnostic flags such as `--enable-db-execution` and, when desired, `--enable-checker`.

Local outputs belong under `runs/user/<run_id>/`. Do not write local outputs into case packages, `case_sets/`, `reports/`, `results/`, or retained evidence surfaces.

## PostgreSQL

Current PostgreSQL diagnostics use the `psql` CLI. Configure either:

- `SQLRB_POSTGRES_DSN`
- or libpq environment variables: `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, and optionally `PGPASSWORD`

Example setup:

```bash
cp scripts/env_postgres.example.sh scripts/env_postgres.local.sh
# Edit scripts/env_postgres.local.sh for your local user, database, and password.
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py
```

`SQLRB_POSTGRES_DSN` takes precedence when set. Otherwise the backend relies on libpq variables. The checker helper and docs never need to print passwords.

## MySQL

Current MySQL diagnostics support bounded same-engine local execution and manifest-declared PORT cross-dialect source-reference/target-candidate diagnostics.

The current backend reads:

- `SQLRB_MYSQL_HOST`
- `SQLRB_MYSQL_PORT`
- `SQLRB_MYSQL_USER`
- optional `SQLRB_MYSQL_PASSWORD`

The local MySQL user must be allowed to create and drop temporary diagnostic databases. The runner uses temporary database names for local diagnostics and removes them during cleanup.

Example setup:

```bash
cp scripts/env_mysql.example.sh scripts/env_mysql.local.sh
# Edit scripts/env_mysql.local.sh for your local user, password, and host.
source scripts/env_mysql.local.sh
python scripts/dev/check_local_engine_env.py
```

## Spark

Spark local execution remains deferred and fail-closed in the current user-entry path. This branch includes only a Spark environment detector and fail-closed execution skeleton; it does not implement live Spark SQL execution.

`SPARK_LOCAL_IP`, `SPARK_HOME`, and `PYSPARK_PYTHON` may be useful for future local Spark diagnostics, so `scripts/env_spark.example.sh` documents them as preparatory settings only. Setting them does not enable Spark SQL execution.

When `--engine spark --enable-db-execution` is selected, Spark rows fail closed with local diagnostic statuses until a future live Spark backend is authorized. PostgreSQL and MySQL remain the current live local diagnostic backends.

## Convenience Sourcing

To source whichever local engine files exist:

```bash
source scripts/env_all.example.sh
python scripts/dev/check_local_engine_env.py
```

`scripts/env_all.example.sh` does not contain secrets. It sources these files only when present:

- `scripts/env_postgres.local.sh`
- `scripts/env_mysql.local.sh`
- `scripts/env_spark.local.sh`

It prints a short set/unset summary without printing passwords.

## Security

- Never commit real passwords, DSNs with passwords, private hostnames, tokens, or local-only credentials.
- Copy example files to `scripts/env_*.local.sh` before adding secrets.
- `scripts/env_*.local.sh`, `.env`, and `.env.local` are ignored by git.
- Example files are templates only; edit local copies for your machine.

## Boundaries

Local engine setup is not a benchmark-result surface.

- No official metrics are computed by these environment files or the checker helper.
- No timing or speedup is computed.
- No paper tables are rendered.
- No `reports/` or `results/` files are updated.
- No retained evidence is created or promoted.
- No case files, manifests, SQL, schemas, checkers, validation scripts, or case-set membership are changed.
- No global leaderboard is created.
