#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="PORT_0025"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/mysql"
PG_RUN_DIR="${CASE_DIR}/runs/pg"
SPARK_RUN_DIR="${CASE_DIR}/runs/spark"
POS_NORMALIZED_SQL="${RUN_DIR}/rewrite_pos_01.mysql_normalized.sql"
NEG_NORMALIZED_SQL="${RUN_DIR}/rewrite_neg_01.mysql_normalized.sql"
RESULT_CHECK_JSON="${RUN_DIR}/result_check.json"

# DRAFT-ONLY validation scaffold. Do not treat this as executed evidence.
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

emit_drop_table_sql() {
  awk '
    toupper($1) == "CREATE" && toupper($2) == "TABLE" {
      name = $3
      sub(/\(.*/, "", name)
      gsub(/`/, "", name)
      tables[++count] = name
    }
    END {
      for (idx = count; idx >= 1; --idx) {
        printf "drop table if exists `%s`;\n", tables[idx]
      }
    }
  ' "${CASE_DIR}/schema/mysql/ddl.sql"
}

mkdir -p "${RUN_DIR}"
rm -f "${RUN_DIR}/source.tsv" "${RUN_DIR}/rewrite_pos_01.tsv" "${RUN_DIR}/rewrite_neg_01.tsv" \
  "${POS_NORMALIZED_SQL}" "${NEG_NORMALIZED_SQL}" "${RESULT_CHECK_JSON}"

{
  printf 'use `%s`;
' "${MYSQL_DATABASE}"
  emit_drop_table_sql
  cat "${CASE_DIR}/schema/mysql/ddl.sql"
  cat "${CASE_DIR}/schema/mysql/load.sql"
} | mysql_cmd --batch --raw --skip-column-names >/dev/null

run_query() {
  local sql_file="$1"
  local out_file="$2"
  {
    printf 'use `%s`;
' "${MYSQL_DATABASE}"
    cat "${sql_file}"
  } | mysql_cmd --batch --raw --skip-column-names > "${out_file}"
}

normalize_rewrite_sql() {
  local input_sql="$1"
  local output_sql="$2"
  INPUT_SQL="${input_sql}" OUTPUT_SQL="${output_sql}" python - <<'PY'
import os
import pathlib
import re

src = pathlib.Path(os.environ["INPUT_SQL"]).read_text()
dst = re.sub(
    r"EXTRACT\s*\(\s*YEAR\s+FROM\s+CAST\s*\(\s*(.*?)\s+AS\s+TIMESTAMP\s*\)\s*\)",
    r"YEAR(\1)",
    src,
    flags=re.IGNORECASE | re.DOTALL,
)
pathlib.Path(os.environ["OUTPUT_SQL"]).write_text(dst)
PY
}

maybe_run_checker() {
  if [[ -f "${PG_RUN_DIR}/rewrite_pos_01.tsv" && -f "${PG_RUN_DIR}/rewrite_neg_01.tsv" \
    && -f "${SPARK_RUN_DIR}/rewrite_pos_01.tsv" && -f "${SPARK_RUN_DIR}/rewrite_neg_01.tsv" \
    && -f "${RUN_DIR}/source.tsv" ]]; then
    python "${CASE_DIR}/validation/check_results.py" \
      "${RUN_DIR}/source.tsv" \
      "${PG_RUN_DIR}/rewrite_pos_01.tsv" \
      "${PG_RUN_DIR}/rewrite_neg_01.tsv" \
      "${SPARK_RUN_DIR}/rewrite_pos_01.tsv" \
      "${SPARK_RUN_DIR}/rewrite_neg_01.tsv" \
      "${RESULT_CHECK_JSON}"
  fi
}

run_query "${CASE_DIR}/sql/source.sql" "${RUN_DIR}/source.tsv"
normalize_rewrite_sql "${CASE_DIR}/sql/positives/pos_01.sql" "${POS_NORMALIZED_SQL}"
normalize_rewrite_sql "${CASE_DIR}/sql/negatives/neg_01.sql" "${NEG_NORMALIZED_SQL}"
run_query "${POS_NORMALIZED_SQL}" "${RUN_DIR}/rewrite_pos_01.tsv"
run_query "${NEG_NORMALIZED_SQL}" "${RUN_DIR}/rewrite_neg_01.tsv"
maybe_run_checker
