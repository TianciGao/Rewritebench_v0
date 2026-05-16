#!/usr/bin/env bash
# Canonical migration caveat:
# This retained legacy validation asset was not executed during migration.
# It is not a final public user runner. Future public runner output must not write to case-local runs/ by default.
# See notes/migration_notes.md and evidence/runs_retention.yaml.

set -euo pipefail

CASE_ID="CONS_0007"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/mysql"

# Load standard MySQL environment settings for the current shell.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_mysql.sh"

MYSQL_BIN="${MYSQL_BIN:-mysql}"
MYSQL_ARGS=()
if [[ -n "${MYSQL_HOST:-}" ]]; then MYSQL_ARGS+=(--host="${MYSQL_HOST}"); fi
if [[ -n "${MYSQL_PORT:-}" ]]; then MYSQL_ARGS+=(--port="${MYSQL_PORT}"); fi
if [[ -n "${MYSQL_USER:-}" ]]; then MYSQL_ARGS+=(--user="${MYSQL_USER}"); fi
if [[ -n "${MYSQL_PASSWORD:-}" ]]; then MYSQL_ARGS+=(--password="${MYSQL_PASSWORD}"); fi

mysql_cmd() {
  "${MYSQL_BIN}" "${MYSQL_ARGS[@]}" "$@"
}

mkdir -p "${RUN_DIR}"

cleanup() {
  local table
  for table in $(sed -n 's/^CREATE TABLE \([^ (][^ (]*\).*/\1/p' "${CASE_DIR}/schema/mysql/ddl.sql"); do
    {
      printf 'use `%s`;\n' "${MYSQL_DATABASE}"
      printf 'drop table if exists `%s`;\n' "${table}"
    } | mysql_cmd --batch --raw --skip-column-names >/dev/null 2>&1 || true
  done
}
trap cleanup EXIT

{
  printf 'use `%s`;\n' "${MYSQL_DATABASE}"
  for table in $(sed -n 's/^CREATE TABLE \([^ (][^ (]*\).*/\1/p' "${CASE_DIR}/schema/mysql/ddl.sql"); do
    printf 'drop table if exists `%s`;\n' "${table}"
  done
  cat "${CASE_DIR}/schema/mysql/ddl.sql"
  cat "${CASE_DIR}/schema/mysql/load.sql"
} | mysql_cmd --batch --raw --skip-column-names >/dev/null

run_query() {
  local sql_file="$1"
  local out_file="$2"
  {
    printf 'use `%s`;\n' "${MYSQL_DATABASE}"
    cat "${sql_file}"
  } | mysql_cmd --batch --raw --skip-column-names > "${out_file}"
}

run_query "${CASE_DIR}/sql/source.sql" "${RUN_DIR}/source.tsv"
run_query "${CASE_DIR}/sql/positives/pos_01.sql" "${RUN_DIR}/rewrite_pos_01.tsv"
run_query "${CASE_DIR}/sql/negatives/neg_01.sql" "${RUN_DIR}/rewrite_neg_01.tsv"

source_positive_equal=false
source_negative_different=false
if cmp -s "${RUN_DIR}/source.tsv" "${RUN_DIR}/rewrite_pos_01.tsv"; then
  source_positive_equal=true
fi
if ! cmp -s "${RUN_DIR}/source.tsv" "${RUN_DIR}/rewrite_neg_01.tsv"; then
  source_negative_different=true
fi

ok=false
status="failed"
if [[ "${source_positive_equal}" == "true" && "${source_negative_different}" == "true" ]]; then
  ok=true
  status="validated"
fi

cat > "${RUN_DIR}/result_check.json" <<JSON
{
  "case_id": "${CASE_ID}",
  "engine": "mysql",
  "status": "${status}",
  "ok": ${ok},
  "schema": "${MYSQL_DATABASE}",
  "inputs": {
    "source": "sql/source.sql",
    "positive_rewrite": "sql/positives/pos_01.sql",
    "negative_rewrite": "sql/negatives/neg_01.sql",
    "witness_data": "schema/mysql/load.sql"
  },
  "outputs": {
    "source": "runs/mysql/source.tsv",
    "positive_rewrite": "runs/mysql/rewrite_pos_01.tsv",
    "negative_rewrite": "runs/mysql/rewrite_neg_01.tsv"
  },
  "checks": {
    "source_positive_equal": ${source_positive_equal},
    "source_negative_different": ${source_negative_different}
  },
  "notes": [
    "MySQL-only witness validation for CONS_0007.",
    "No PostgreSQL or Spark validation is implied.",
    "No admission, promotion, common-core, extended, or tri-engine-closure claim is made."
  ]
}
JSON

if [[ "${ok}" == "true" ]]; then
  exit 0
fi
exit 1
