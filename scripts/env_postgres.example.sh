#!/usr/bin/env bash
# PostgreSQL local diagnostic environment template.
#
# Usage:
#   cp scripts/env_postgres.example.sh scripts/env_postgres.local.sh
#   # Edit scripts/env_postgres.local.sh for your local password, user, and DB.
#   source scripts/env_postgres.local.sh
#
# Do not commit scripts/env_postgres.local.sh or real passwords.

export PGHOST=127.0.0.1
export PGPORT=5432
export PGDATABASE=postgres
export PGUSER=postgres
export PGPASSWORD=change-me

# Optional DSN form accepted by the current backend. If set, this takes
# precedence over libpq variables in SQL-RewriteBench local diagnostics.
# export SQLRB_POSTGRES_DSN="postgresql://postgres:change-me@127.0.0.1:5432/postgres"
