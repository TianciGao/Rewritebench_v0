#!/usr/bin/env bash
set -euo pipefail

CASE_ID="PORT_0004"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
PLAN_DIR="${CASE_DIR}/runs/pg/plans"
SCHEMA_NAME="port_0004_plan_collection"
TMP_ROOT="${PLAN_DIR}/_tmp_plan_collection"
TMP_SQL="${TMP_ROOT}/_explain_input.sql"

# DRAFT-ONLY plan collection scaffold. Do not treat this as executed evidence.
# PostgreSQL collects only target-engine rewrite plans for this portability case.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_postgres.sh"

mkdir -p "${PLAN_DIR}" "${TMP_ROOT}"

psql_base=(psql -X -v ON_ERROR_STOP=1)
psql_query=(psql -X -q -v ON_ERROR_STOP=1 -A -t)

cleanup() {
  rm -rf "${TMP_ROOT}"
}
trap cleanup EXIT

"${psql_base[@]}" <<SQL
drop schema if exists ${SCHEMA_NAME} cascade;
create schema ${SCHEMA_NAME};
set search_path to ${SCHEMA_NAME};
\i ${CASE_DIR}/schema/ddl_pg.sql
\i ${CASE_DIR}/validation/load_witness_pg.sql
SQL

collect_plan() {
  local query_file="$1"
  local output_file="$2"

  {
    printf 'set search_path to %s;\n' "${SCHEMA_NAME}"
    printf 'explain (format json)\n'
    cat "${CASE_DIR}/${query_file}"
  } > "${TMP_SQL}"

  "${psql_query[@]}" -f "${TMP_SQL}" > "${PLAN_DIR}/${output_file}"
}

collect_plan "rewrite_pos_01.sql" "rewrite_pos_01.json"
collect_plan "rewrite_neg_01.sql" "rewrite_neg_01.json"
