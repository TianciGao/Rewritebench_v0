#!/usr/bin/env bash
# Canonical migration caveat:
# This retained legacy validation asset was not executed during migration.
# It is not a final public user runner. Future public runner output must not write to case-local runs/ by default.
# See notes/migration_notes.md and evidence/runs_retention.yaml.

set -euo pipefail

case_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_id="$(basename "${case_dir}")"
plan_dir="${case_dir}/runs/pg/plans"
schema_name="${case_id,,}_plan_collection"
tmp_root="${plan_dir}/_tmp_plan_collection"
tmp_sql="${tmp_root}/_explain_input.sql"

mkdir -p "${plan_dir}" "${tmp_root}"

psql_base=(psql -X -v ON_ERROR_STOP=1)
psql_query=(psql -X -q -v ON_ERROR_STOP=1 -A -t)

cleanup() {
  rm -rf "${tmp_root}"
}
trap cleanup EXIT

"${psql_base[@]}" <<SQL
drop schema if exists ${schema_name} cascade;
create schema ${schema_name};
set search_path to ${schema_name};
\i ${case_dir}/schema/postgres/ddl.sql
\i ${case_dir}/schema/postgres/load.sql
SQL

split_query() {
  local query_file="$1"
  local stmt_dir="$2"

  python - "${case_dir}/${query_file}" "${stmt_dir}" <<'PY'
from pathlib import Path
import sys

src = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

lines = [line for line in src.read_text().splitlines() if not line.lstrip().startswith("--")]
text = "\n".join(lines).strip()
statements = []
buf = []
in_single = False
i = 0

while i < len(text):
    ch = text[i]
    buf.append(ch)
    if ch == "'":
        if in_single and i + 1 < len(text) and text[i + 1] == "'":
            buf.append(text[i + 1])
            i += 1
        else:
            in_single = not in_single
    elif ch == ";" and not in_single:
        stmt = "".join(buf).strip()
        if stmt:
            statements.append(stmt)
        buf = []
    i += 1

tail = "".join(buf).strip()
if tail:
    statements.append(tail if tail.endswith(";") else tail + ";")

if not statements:
    raise SystemExit(f"no SQL statements found in {src}")

for idx, stmt in enumerate(statements, 1):
    (out / f"statement_{idx:02d}.sql").write_text(stmt + "\n")

print(len(statements))
PY
}

collect_one_statement_plan() {
  local stmt_file="$1"
  local output_file="$2"

  {
    printf 'set search_path to %s;\n' "${schema_name}"
    printf 'explain (format json)\n'
    cat "${stmt_file}"
  } > "${tmp_sql}"

  "${psql_query[@]}" -f "${tmp_sql}" > "${output_file}"
}

collect_plan() {
  local query_file="$1"
  local output_file="$2"
  local stem="${output_file%.json}"
  local stmt_dir="${tmp_root}/${stem}_statements"
  local stmt_plan_dir="${tmp_root}/${stem}_plans"
  local stmt_count

  mkdir -p "${stmt_dir}" "${stmt_plan_dir}"
  stmt_count="$(split_query "${query_file}" "${stmt_dir}")"

  if [[ "${stmt_count}" == "1" ]]; then
    collect_one_statement_plan "${stmt_dir}/statement_01.sql" "${plan_dir}/${output_file}"
    printf '%s\n' "${stmt_count}"
    return
  fi

  local stmt_plans=()
  local idx
  for idx in $(seq 1 "${stmt_count}"); do
    local stmt_file
    local stmt_plan
    stmt_file="${stmt_dir}/statement_$(printf '%02d' "${idx}").sql"
    stmt_plan="${stmt_plan_dir}/statement_$(printf '%02d' "${idx}").json"
    collect_one_statement_plan "${stmt_file}" "${stmt_plan}"
    stmt_plans+=("${stmt_plan}")
  done

  python - "${case_id}" "${query_file}" "${stmt_count}" "${plan_dir}/${output_file}" "${stmt_plans[@]}" <<'PY'
import json
from pathlib import Path
import sys

case_id, query_file, stmt_count, output_file, *plan_files = sys.argv[1:]
payload = {
    "case_id": case_id,
    "engine": "postgres",
    "query_file": query_file,
    "statement_count": int(stmt_count),
    "plans": []
}

for idx, plan_file in enumerate(plan_files, 1):
    with Path(plan_file).open() as fh:
        payload["plans"].append({
            "statement_index": idx,
            "plan": json.load(fh)
        })

Path(output_file).write_text(json.dumps(payload, indent=2) + "\n")
PY

  printf '%s\n' "${stmt_count}"
}

source_statement_count="$(collect_plan "sql/source.sql" "source.json")"
positive_statement_count="$(collect_plan "sql/positives/pos_01.sql" "rewrite_pos_01.json")"
negative_statement_count="$(collect_plan "sql/negatives/neg_01.sql" "rewrite_neg_01.json")"

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
  "case_id": "${case_id}",
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
  "statement_counts": {
    "source": ${source_statement_count},
    "positive_rewrite": ${positive_statement_count},
    "negative_rewrite": ${negative_statement_count}
  },
  "notes": [
    "PostgreSQL-only EXPLAIN (FORMAT JSON) plan collection.",
    "Plans were collected against the case-local PostgreSQL witness schema.",
    "No MySQL or Spark validation is implied.",
    "No admission, promotion, common-core, extended, or tri-engine-closure claim is made."
  ]
}
JSON

if [[ "${ok}" == "true" ]]; then
  exit 0
fi

exit 1
