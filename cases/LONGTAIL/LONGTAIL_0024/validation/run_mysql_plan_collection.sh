#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="LONGTAIL_0024"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
PLAN_DIR="${CASE_DIR}/runs/mysql/plans"

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

mkdir -p "${PLAN_DIR}"

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

collect_plan() {
  local sql_file="$1"
  local out_file="$2"
  {
    printf 'use `%s`;\n' "${MYSQL_DATABASE}"
    printf 'explain format=json\n'
    cat "${sql_file}"
  } | mysql_cmd --batch --raw --skip-column-names > "${out_file}"
}

collect_plan "${CASE_DIR}/source.sql" "${PLAN_DIR}/source.json"
collect_plan "${CASE_DIR}/rewrite_pos_01.sql" "${PLAN_DIR}/rewrite_pos_01.json"
collect_plan "${CASE_DIR}/rewrite_neg_01.sql" "${PLAN_DIR}/rewrite_neg_01.json"

source_plan_present=false
positive_plan_present=false
negative_plan_present=false
if test -s "${PLAN_DIR}/source.json"; then source_plan_present=true; fi
if test -s "${PLAN_DIR}/rewrite_pos_01.json"; then positive_plan_present=true; fi
if test -s "${PLAN_DIR}/rewrite_neg_01.json"; then negative_plan_present=true; fi

ok=false
status="failed"
if [[ "${source_plan_present}" == "true" && "${positive_plan_present}" == "true" && "${negative_plan_present}" == "true" ]]; then
  ok=true
  status="collected"
fi

cat > "${PLAN_DIR}/plan_check.json" <<JSON
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
    "source_plan": "runs/mysql/plans/source.json",
    "positive_rewrite_plan": "runs/mysql/plans/rewrite_pos_01.json",
    "negative_rewrite_plan": "runs/mysql/plans/rewrite_neg_01.json"
  },
  "checks": {
    "source_plan_present": ${source_plan_present},
    "positive_plan_present": ${positive_plan_present},
    "negative_plan_present": ${negative_plan_present}
  },
  "notes": [
    "MySQL-only EXPLAIN FORMAT=JSON plan collection for LONGTAIL_0024.",
    "This is a manual/hybrid Stack-substrate draft case.",
    "No PostgreSQL or Spark validation is implied.",
    "No admission, promotion, common-core, extended, or tri-engine-closure claim is made."
  ]
}
JSON

if [[ "${ok}" == "true" ]]; then
  exit 0
fi
exit 1
