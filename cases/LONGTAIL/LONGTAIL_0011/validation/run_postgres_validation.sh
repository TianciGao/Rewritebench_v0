#!/usr/bin/env bash
set -euo pipefail

# Retained legacy validation asset; not executed during migration.
# Future public runner outputs must not write to case-local runs/ by default.

CASE_ID="LONGTAIL_0011"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/pg"
SCHEMA_NAME="longtail_0003_validation"

# Load standard PostgreSQL environment settings for the current shell.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_postgres.sh"

mkdir -p "${RUN_DIR}"

psql_base=(psql -X -v ON_ERROR_STOP=1)
psql_query=(psql -X -q -v ON_ERROR_STOP=1 -A -t -F $'\t')

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
    printf 'set search_path to %s;\n' "${SCHEMA_NAME}"
    printf '\\i %s/%s\n' "${CASE_DIR}" "${query_file}"
  } | "${psql_query[@]}" > "${RUN_DIR}/${output_file}"
}

run_query "sql/source.sql" "source.tsv"
run_query "sql/pos_01.sql" "rewrite_pos_01.tsv"
run_query "sql/neg_01.sql" "rewrite_neg_01.tsv"

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
  "engine": "postgres",
  "status": "${status}",
  "ok": ${ok},
  "schema": "${SCHEMA_NAME}",
  "inputs": {
    "source": "sql/source.sql",
    "positive_rewrite": "sql/pos_01.sql",
    "negative_rewrite": "sql/neg_01.sql",
    "witness_data": "schema/postgres/load.sql"
  },
  "outputs": {
    "source": "runs/pg/source.tsv",
    "positive_rewrite": "runs/pg/rewrite_pos_01.tsv",
    "negative_rewrite": "runs/pg/rewrite_neg_01.tsv"
  },
  "checks": {
    "source_positive_equal": ${source_positive_equal},
    "source_negative_different": ${source_negative_different}
  },
  "notes": [
    "PostgreSQL-only witness validation for LONGTAIL_0011.",
    "No MySQL or Spark validation is implied.",
    "No admission, promotion, common-core, extended, or tri-engine-closure claim is made."
  ]
}
JSON

if [[ "${ok}" == "true" ]]; then
  exit 0
fi
exit 1
