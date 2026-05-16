#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="PORT_0004"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/mysql"
CHECKER_JSON="${RUN_DIR}/result_check.json"
CHECKER_PY="${CASE_DIR}/validation/check_results.py"
PG_POS="${CASE_DIR}/runs/pg/rewrite_pos_01.tsv"
PG_NEG="${CASE_DIR}/runs/pg/rewrite_neg_01.tsv"
SPARK_POS="${CASE_DIR}/runs/spark/rewrite_pos_02_spark.tsv"
SPARK_NEG="${CASE_DIR}/runs/spark/rewrite_neg_02_spark.tsv"
PYTHON_BIN="${PYTHON_BIN:-python}"

# DRAFT-ONLY validation scaffold. Do not treat this as executed evidence.
# MySQL is the source-reference engine for this portability case.
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

{
  printf 'use `%s`;\n' "${MYSQL_DATABASE}"
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

# PORT_0004 treats MySQL as the source-reference engine. There is no
# MySQL-target positive rewrite artifact in this case package, so the MySQL
# closure step materializes the reference output and, when the full cross-engine
# TSV set exists, emits the closure checker JSON for the package.
if [[ -f "${PG_POS}" && -f "${PG_NEG}" && -f "${SPARK_POS}" && -f "${SPARK_NEG}" ]]; then
  "${PYTHON_BIN}" "${CHECKER_PY}" \
    "${RUN_DIR}/source.tsv" \
    "${PG_POS}" \
    "${PG_NEG}" \
    "${SPARK_POS}" \
    "${SPARK_NEG}" \
    "${CHECKER_JSON}"
fi
