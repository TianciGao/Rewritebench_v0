#!/usr/bin/env bash
# Canonical migration caveat:
# This retained legacy validation asset was not executed during migration.
# It is not a final public user runner. Future public runner output must not write to case-local runs/ by default.
# See notes/migration_notes.md and evidence/runs_retention.yaml.
set -euo pipefail

case_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
plan_dir="${case_dir}/runs/pg/plans"
schema_name="perf_0013_plan_collection"
tmp_sql="${plan_dir}/_explain_input.sql"

mkdir -p "${plan_dir}"

psql_base=(psql -X -v ON_ERROR_STOP=1)
psql_query=(psql -X -q -v ON_ERROR_STOP=1 -A -t)

cleanup() {
  rm -f "${tmp_sql}"
}
trap cleanup EXIT

"${psql_base[@]}" <<SQL
drop schema if exists ${schema_name} cascade;
create schema ${schema_name};
set search_path to ${schema_name};
\i ${case_dir}/schema/postgres/ddl.sql
\i ${case_dir}/schema/postgres/load.sql
SQL

collect_plan() {
  local query_file="$1"
  local output_file="$2"

  {
    printf 'set search_path to %s;\n' "${schema_name}"
    printf 'explain (format json)\n'
    sed '/^[[:space:]]*--/d' "${case_dir}/${query_file}"
  } > "${tmp_sql}"

  "${psql_query[@]}" -f "${tmp_sql}" > "${plan_dir}/${output_file}"
}

collect_plan "sql/source.sql" "source.json"
collect_plan "sql/positives/pos_01.sql" "rewrite_pos_01.json"
collect_plan "sql/negatives/neg_01.sql" "rewrite_neg_01.json"

source_plan_present=false
positive_plan_present=false
negative_plan_present=false

if [[ -s "${plan_dir}/source.json" ]]; then
  source_plan_present=true
fi

if [[ -s "${plan_dir}/rewrite_pos_01.json" ]]; then
  positive_plan_present=true
fi

if [[ -s "${plan_dir}/rewrite_neg_01.json" ]]; then
  negative_plan_present=true
fi

if [[ "${source_plan_present}" == "true" && "${positive_plan_present}" == "true" && "${negative_plan_present}" == "true" ]]; then
  ok=true
  status="collected"
else
  ok=false
  status="failed"
fi

cat > "${plan_dir}/plan_check.json" <<JSON
{
  "case_id": "PERF_0013",
  "engine": "postgres",
  "status": "${status}",
  "ok": ${ok},
  "schema": "${schema_name}",
  "inputs": {
    "source": "sql/source.sql",
    "positive_rewrite": "sql/positives/pos_01.sql",
    "negative_rewrite": "sql/negatives/neg_01.sql",
    "witness_data": "schema/postgres/load.sql"
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
    "PostgreSQL-only EXPLAIN (FORMAT JSON) plan collection.",
    "Plans were collected against the case-local PostgreSQL witness schema.",
    "No MySQL or Spark validation is implied.",
    "No admission, promotion, or common-core claim is made."
  ]
}
JSON

if [[ "${ok}" == "true" ]]; then
  exit 0
fi

exit 1
