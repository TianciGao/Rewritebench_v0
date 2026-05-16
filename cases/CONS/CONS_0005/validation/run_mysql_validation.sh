#!/usr/bin/env bash
# Retained legacy validation asset for CONS_0005.
# Not executed during migration. Future public runner output must not write to case-local runs/ by default.
set -euo pipefail
CASE_ID="CONS_0005"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/mysql"
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_mysql.sh"
MYSQL_BIN="${MYSQL_BIN:-mysql}"
MYSQL_ARGS=()
if [[ -n "${MYSQL_HOST:-}" ]]; then MYSQL_ARGS+=(--host="${MYSQL_HOST}"); fi
if [[ -n "${MYSQL_PORT:-}" ]]; then MYSQL_ARGS+=(--port="${MYSQL_PORT}"); fi
if [[ -n "${MYSQL_USER:-}" ]]; then MYSQL_ARGS+=(--user="${MYSQL_USER}"); fi
if [[ -n "${MYSQL_PASSWORD:-}" ]]; then MYSQL_ARGS+=(--password="${MYSQL_PASSWORD}"); fi
mysql_cmd() { "${MYSQL_BIN}" "${MYSQL_ARGS[@]}" "$@"; }
mkdir -p "${RUN_DIR}"
{ printf 'use `%s`;
' "${MYSQL_DATABASE}"; cat "${CASE_DIR}/schema/mysql/ddl.sql"; cat "${CASE_DIR}/schema/mysql/load.sql"; } | mysql_cmd --batch --raw --skip-column-names >/dev/null
run_query() {
  local sql_file="$1"
  local out_file="$2"
  { printf 'use `%s`;
' "${MYSQL_DATABASE}"; cat "${CASE_DIR}/${sql_file}"; } | mysql_cmd --batch --raw --skip-column-names > "${RUN_DIR}/${out_file}"
}
run_query "sql/source.sql" "source.tsv"
run_query "sql/positives/pos_01.sql" "rewrite_pos_01.tsv"
run_query "sql/negatives/neg_01.sql" "rewrite_neg_01.tsv"
