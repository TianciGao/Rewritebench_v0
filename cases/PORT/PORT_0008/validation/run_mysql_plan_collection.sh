#!/usr/bin/env bash
set -euo pipefail

CASE_ID="PORT_0008"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
PLAN_DIR="${CASE_DIR}/runs/mysql/plans"

# DRAFT-ONLY plan collection scaffold. Do not treat this as executed evidence.
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

mkdir -p "${PLAN_DIR}"
rm -f "${PLAN_DIR}/source.json" "${PLAN_DIR}/rewrite_pos_01.json" "${PLAN_DIR}/rewrite_neg_01.json"

{
  printf 'use `%s`;\n' "${MYSQL_DATABASE}"
  emit_drop_table_sql
  cat "${CASE_DIR}/schema/ddl_mysql.sql"
  cat "${CASE_DIR}/validation/mysql_witness_data.sql"
} | mysql_cmd --batch --raw --skip-column-names >/dev/null

collect_plan() {
  local sql_file="$1"
  local out_file="$2"
  {
    printf 'use `%s`;\n' "${MYSQL_DATABASE}"
    printf 'explain format=json\n'
    cat "${sql_file}"
  } | mysql_cmd --batch --raw --skip-column-names > "${out_file}"
}

collect_plan "${CASE_DIR}/rewrite_pos_01.sql" "${PLAN_DIR}/rewrite_pos_01.json"
collect_plan "${CASE_DIR}/rewrite_neg_01.sql" "${PLAN_DIR}/rewrite_neg_01.json"
