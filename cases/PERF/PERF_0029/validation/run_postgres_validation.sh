#!/usr/bin/env bash
set -euo pipefail

case_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_dir="${case_dir}/runs/pg"
schema_name="perf_0029_validation"

mkdir -p "${run_dir}"

psql_base=(psql -X -v ON_ERROR_STOP=1)
psql_query=(psql -X -q -v ON_ERROR_STOP=1 -A -t -F $'\t')

"${psql_base[@]}" <<SQL
drop schema if exists ${schema_name} cascade;
create schema ${schema_name};
set search_path to ${schema_name};
\i ${case_dir}/schema/ddl_pg.sql
\i ${case_dir}/validation/pg_witness_data.sql
SQL

run_query() {
  local query_file="$1"
  local output_file="$2"

  {
    printf 'set search_path to %s;\n' "${schema_name}"
    printf '\\i %s/%s\n' "${case_dir}" "${query_file}"
  } | "${psql_query[@]}" > "${run_dir}/${output_file}"
}

run_query "source.sql" "source.tsv"
run_query "rewrite_pos_01.sql" "rewrite_pos_01.tsv"
run_query "rewrite_neg_01.sql" "rewrite_neg_01.tsv"

if cmp -s "${run_dir}/source.tsv" "${run_dir}/rewrite_pos_01.tsv"; then
  source_positive_equal=true
else
  source_positive_equal=false
fi

if cmp -s "${run_dir}/source.tsv" "${run_dir}/rewrite_neg_01.tsv"; then
  source_negative_different=false
else
  source_negative_different=true
fi

if [[ "${source_positive_equal}" == "true" && "${source_negative_different}" == "true" ]]; then
  ok=true
  status="validated"
else
  ok=false
  status="failed"
fi

cat > "${run_dir}/result_check.json" <<JSON
{
  "case_id": "PERF_0029",
  "engine": "postgres",
  "status": "${status}",
  "ok": ${ok},
  "schema": "${schema_name}",
  "inputs": {
    "source": "source.sql",
    "positive_rewrite": "rewrite_pos_01.sql",
    "negative_rewrite": "rewrite_neg_01.sql",
    "witness_data": "validation/pg_witness_data.sql"
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
    "PostgreSQL-only witness validation.",
    "No MySQL or Spark validation is implied.",
    "No plans were collected."
  ]
}
JSON

if [[ "${ok}" == "true" ]]; then
  exit 0
fi

exit 1
