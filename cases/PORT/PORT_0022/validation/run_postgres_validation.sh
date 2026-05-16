#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="PORT_0022"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/pg"
SCHEMA_NAME="port_0022_validation"

# DRAFT-ONLY validation scaffold. Do not treat this as executed evidence.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_postgres.sh"

mkdir -p "${RUN_DIR}"

psql_base=(psql -X -v ON_ERROR_STOP=1)
psql_query=(psql -X -q -v ON_ERROR_STOP=1 -A -t -F $'	')

"${psql_base[@]}" <<SQL
drop schema if exists ${SCHEMA_NAME} cascade;
create schema ${SCHEMA_NAME};
set search_path to ${SCHEMA_NAME};
\i ${CASE_DIR}/schema/postgres/ddl.sql
\i ${CASE_DIR}/schema/postgres/load.sql
SQL

run_query() {
  local query_file="$1"
  local output_file="$2"
  {
    printf 'set search_path to %s;
' "${SCHEMA_NAME}"
    printf '\i %s/%s
' "${CASE_DIR}" "${query_file}"
  } | "${psql_query[@]}" > "${RUN_DIR}/${output_file}"
}

run_query "sql/positives/pos_01.sql" "rewrite_pos_01.tsv"
run_query "sql/negatives/neg_01.sql" "rewrite_neg_01.tsv"
