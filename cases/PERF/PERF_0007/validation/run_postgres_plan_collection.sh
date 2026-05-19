#!/usr/bin/env bash
# Canonical migration caveat:
# This retained legacy validation asset was not executed during migration.
# It is not a final public user runner. Future public runner output must not write to case-local runs/ by default.
# See evidence/cases/PERF/PERF_0007/notes/migration_notes.md and evidence/runs_retention.yaml.
set -euo pipefail

case_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
plan_dir="${case_dir}/runs/pg/plans"
schema_name="perf_0007_plan_collection"
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
collect_plan "sql/pos_01.sql" "rewrite_pos_01.json"
collect_plan "sql/neg_01.sql" "rewrite_neg_01.json"

cat > "${plan_dir}/plan_check.json" <<JSON
{
  "case_id": "PERF_0007",
  "engine": "postgres",
  "status": "collected",
  "ok": true,
  "schema": "${schema_name}",
  "inputs": {
    "source": "sql/source.sql",
    "positive_rewrite": "sql/pos_01.sql",
    "negative_rewrite": "sql/neg_01.sql",
    "witness_data": "schema/postgres/load.sql"
  },
  "outputs": {
    "source_plan": "runs/pg/plans/source.json",
    "positive_rewrite_plan": "runs/pg/plans/rewrite_pos_01.json",
    "negative_rewrite_plan": "runs/pg/plans/rewrite_neg_01.json"
  },
  "notes": [
    "PostgreSQL-only EXPLAIN (FORMAT JSON) plan collection.",
    "Plans were collected against the case-local PostgreSQL witness schema.",
    "No MySQL or Spark validation is implied.",
    "No admission, promotion, or common-core claim is made."
  ]
}
JSON
