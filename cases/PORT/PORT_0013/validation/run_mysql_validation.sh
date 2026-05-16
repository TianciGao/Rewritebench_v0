#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="PORT_0013"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/mysql"
CHECKER="${CASE_DIR}/validation/check_results.py"
MYSQL_SOURCE_TSV="${RUN_DIR}/source.tsv"
PG_POS_TSV="${CASE_DIR}/runs/pg/rewrite_pos_01.tsv"
PG_NEG_TSV="${CASE_DIR}/runs/pg/rewrite_neg_01.tsv"
SPARK_POS_TSV="${CASE_DIR}/runs/spark/rewrite_pos_01.tsv"
SPARK_NEG_TSV="${CASE_DIR}/runs/spark/rewrite_neg_01.tsv"
RESULT_CHECK_JSON="${RUN_DIR}/result_check.json"

# DRAFT-ONLY validation scaffold. Do not treat this as executed evidence.
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

emit_drop_table_sql() {
  awk '
    toupper($1) == "CREATE" && toupper($2) == "TABLE" {
      name = $3
      sub(/\(.*/, "", name)
      gsub(/`/, "", name)
      tables[++count] = name
    }
    END {
      for (idx = count; idx >= 1; --idx) {
        printf "drop table if exists `%s`;\n", tables[idx]
      }
    }
  ' "${CASE_DIR}/schema/ddl_mysql.sql"
}

mkdir -p "${RUN_DIR}"
rm -f "${RUN_DIR}/source.tsv" "${RUN_DIR}/rewrite_pos_01.tsv" "${RUN_DIR}/rewrite_neg_01.tsv" "${RESULT_CHECK_JSON}"

{
  printf 'use `%s`;\n' "${MYSQL_DATABASE}"
  emit_drop_table_sql
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

if [[ -f "${MYSQL_SOURCE_TSV}" && -f "${PG_POS_TSV}" && -f "${PG_NEG_TSV}" && -f "${SPARK_POS_TSV}" && -f "${SPARK_NEG_TSV}" ]]; then
  "${REPO_ROOT}/.venv/bin/python" "${CHECKER}" \
    "${MYSQL_SOURCE_TSV}" \
    "${PG_POS_TSV}" \
    "${PG_NEG_TSV}" \
    "${SPARK_POS_TSV}" \
    "${SPARK_NEG_TSV}" \
    "${RESULT_CHECK_JSON}"
else
  echo "Skipping engine-local result_check generation for ${CASE_ID} MySQL: required cross-engine TSVs are not all present." >&2
fi
