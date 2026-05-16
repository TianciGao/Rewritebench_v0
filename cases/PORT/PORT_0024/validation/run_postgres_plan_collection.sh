#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="PORT_0024"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
PLAN_DIR="${CASE_DIR}/runs/pg/plans"
SCHEMA_NAME="port_0024_plan_collection"
TMP_ROOT="${PLAN_DIR}/_tmp_plan_collection"
TMP_SQL="${TMP_ROOT}/_explain_input.sql"

# DRAFT-ONLY plan collection scaffold. Do not treat this as executed evidence.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_postgres.sh"

mkdir -p "${PLAN_DIR}" "${TMP_ROOT}"

psql_base=(psql -X -v ON_ERROR_STOP=1)
psql_query=(psql -X -q -v ON_ERROR_STOP=1 -A -t)

cleanup() { rm -rf "${TMP_ROOT}"; }
trap cleanup EXIT

"${psql_base[@]}" <<SQL
drop schema if exists ${SCHEMA_NAME} cascade;
create schema ${SCHEMA_NAME};
set search_path to ${SCHEMA_NAME};
\i ${CASE_DIR}/schema/postgres/ddl.sql
\i ${CASE_DIR}/schema/postgres/load.sql
SQL

collect_plan() {
  local query_file="$1"
  local output_file="$2"
  {
    printf 'set search_path to %s;
' "${SCHEMA_NAME}"
    printf 'explain (format json)
'
    cat "${CASE_DIR}/${query_file}"
  } > "${TMP_SQL}"
  "${psql_query[@]}" -f "${TMP_SQL}" > "${PLAN_DIR}/${output_file}"
}

collect_plan "sql/positives/pos_01.sql" "rewrite_pos_01.json"
collect_plan "sql/negatives/neg_01.sql" "rewrite_neg_01.json"
