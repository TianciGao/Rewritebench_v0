#!/usr/bin/env bash
# Convenience template for loading local SQL-RewriteBench engine environments.
#
# This file contains no secrets. It sources local files only when they exist:
#   scripts/env_postgres.local.sh
#   scripts/env_mysql.local.sh
#   scripts/env_spark.local.sh
#
# Usage from the repository root:
#   source scripts/env_all.example.sh

_sqlrb_env_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

_sqlrb_source_if_present() {
  local file="$1"
  local label="$2"
  if [ -f "$file" ]; then
    # shellcheck source=/dev/null
    source "$file"
    printf "%s: sourced\n" "$label"
  else
    printf "%s: not present\n" "$label"
  fi
}

_sqlrb_is_set() {
  local name="$1"
  if [ -n "${!name:-}" ]; then
    printf "set"
  else
    printf "unset"
  fi
}

_sqlrb_source_if_present "$_sqlrb_env_script_dir/env_postgres.local.sh" "PostgreSQL local env"
_sqlrb_source_if_present "$_sqlrb_env_script_dir/env_mysql.local.sh" "MySQL local env"
_sqlrb_source_if_present "$_sqlrb_env_script_dir/env_spark.local.sh" "Spark local env"

printf "PostgreSQL SQLRB_POSTGRES_DSN: %s\n" "$(_sqlrb_is_set SQLRB_POSTGRES_DSN)"
printf "PostgreSQL libpq vars: PGHOST=%s PGPORT=%s PGDATABASE=%s PGUSER=%s PGPASSWORD=%s\n" \
  "$(_sqlrb_is_set PGHOST)" \
  "$(_sqlrb_is_set PGPORT)" \
  "$(_sqlrb_is_set PGDATABASE)" \
  "$(_sqlrb_is_set PGUSER)" \
  "$(_sqlrb_is_set PGPASSWORD)"
printf "MySQL SQLRB vars: HOST=%s PORT=%s USER=%s PASSWORD=%s\n" \
  "$(_sqlrb_is_set SQLRB_MYSQL_HOST)" \
  "$(_sqlrb_is_set SQLRB_MYSQL_PORT)" \
  "$(_sqlrb_is_set SQLRB_MYSQL_USER)" \
  "$(_sqlrb_is_set SQLRB_MYSQL_PASSWORD)"
printf "Spark SPARK_LOCAL_IP: %s\n" "$(_sqlrb_is_set SPARK_LOCAL_IP)"

unset -f _sqlrb_source_if_present
unset -f _sqlrb_is_set
unset _sqlrb_env_script_dir
