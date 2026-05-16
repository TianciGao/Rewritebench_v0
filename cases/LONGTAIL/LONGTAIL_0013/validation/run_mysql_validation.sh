#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="LONGTAIL_0013"
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
  for table in $(sed -n 's/^CREATE TABLE \([^ (][^ (]*\).*/\1/p' "${CASE_DIR}/schema/ddl_mysql.sql"); do
    {
      printf 'use `%s`;\n' "${MYSQL_DATABASE}"
      printf 'drop table if exists `%s`;\n' "${table}"
    } | mysql_cmd --batch --raw --skip-column-names >/dev/null 2>&1 || true
  done
}
trap cleanup EXIT

{
  printf 'use `%s`;\n' "${MYSQL_DATABASE}"
  for table in $(sed -n 's/^CREATE TABLE \([^ (][^ (]*\).*/\1/p' "${CASE_DIR}/schema/ddl_mysql.sql"); do
    printf 'drop table if exists `%s`;\n' "${table}"
  done
  cat "${CASE_DIR}/schema/ddl_mysql.sql"
  cat "${CASE_DIR}/validation/mysql_witness_data.sql"
} | mysql_cmd --batch --raw --skip-column-names >/dev/null

run_query() {
  local sql_file="$1"
  local out_file="$2"
  {
    printf 'use `%s`;\n' "${MYSQL_DATABASE}"
    cat "${sql_file}"
  } | mysql_cmd --batch --raw --skip-column-names > "${out_file}"
}

run_query "${CASE_DIR}/source.sql" "${RUN_DIR}/source.tsv"
run_query "${CASE_DIR}/rewrite_pos_01.sql" "${RUN_DIR}/rewrite_pos_01.tsv"
run_query "${CASE_DIR}/rewrite_neg_01.sql" "${RUN_DIR}/rewrite_neg_01.tsv"

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
    "source": "source.sql",
    "positive_rewrite": "rewrite_pos_01.sql",
    "negative_rewrite": "rewrite_neg_01.sql",
    "witness_data": "validation/mysql_witness_data.sql"
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
    "MySQL-only witness validation for LONGTAIL_0013.",
    "No PostgreSQL or Spark validation is implied.",
    "No admission, promotion, common-core, extended, or tri-engine-closure claim is made."
  ]
}
JSON

if [[ "${ok}" == "true" ]]; then
  exit 0
fi
exit 1
