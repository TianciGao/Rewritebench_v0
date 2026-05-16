#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="LONGTAIL_0012"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
PLAN_DIR="${CASE_DIR}/runs/pg/plans"
SCHEMA_NAME="longtail_0003_plan_collection"
TMP_ROOT="${PLAN_DIR}/_plan_collection_workdir"
TMP_SQL="${TMP_ROOT}/_explain_input.sql"

# Load standard PostgreSQL environment settings for the current shell.
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
\i ${CASE_DIR}/validation/pg_witness_data.sql
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

collect_plan "source.sql" "source.json"
collect_plan "rewrite_pos_01.sql" "rewrite_pos_01.json"
collect_plan "rewrite_neg_01.sql" "rewrite_neg_01.json"

source_plan_present=false
positive_plan_present=false
negative_plan_present=false
if [[ -s "${PLAN_DIR}/source.json" ]]; then source_plan_present=true; fi
if [[ -s "${PLAN_DIR}/rewrite_pos_01.json" ]]; then positive_plan_present=true; fi
if [[ -s "${PLAN_DIR}/rewrite_neg_01.json" ]]; then negative_plan_present=true; fi

ok=false
status="failed"
if [[ "${source_plan_present}" == "true" && "${positive_plan_present}" == "true" && "${negative_plan_present}" == "true" ]]; then
  ok=true
  status="collected"
fi

cat > "${PLAN_DIR}/plan_check.json" <<JSON
{
  "case_id": "${CASE_ID}",
  "engine": "postgres",
  "status": "${status}",
  "ok": ${ok},
  "schema": "${SCHEMA_NAME}",
  "inputs": {
    "source": "source.sql",
    "positive_rewrite": "rewrite_pos_01.sql",
    "negative_rewrite": "rewrite_neg_01.sql",
    "witness_data": "validation/pg_witness_data.sql"
  },
  "outputs": {
    "source_plan": "runs/pg/plans/source.json",
    "positive_rewrite_plan": "runs/pg/plans/rewrite_pos_01.json",
    "negative_rewrite_plan": "runs/pg/plans/rewrite_neg_01.json"
  },
  "checks": {
    "source_plan_present": ${source_plan_present},
    "positive_plan_present": ${positive_plan_present},
    "negative_plan_present": ${negative_plan_present}
  },
  "notes": [
    "PostgreSQL-only EXPLAIN (FORMAT JSON) plan collection for LONGTAIL_0012.",
    "No MySQL or Spark validation is implied.",
    "No admission, promotion, common-core, extended, or tri-engine-closure claim is made."
  ]
}
JSON

if [[ "${ok}" == "true" ]]; then
  exit 0
fi
exit 1
