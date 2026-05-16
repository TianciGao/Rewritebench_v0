#!/usr/bin/env bash
# Canonical migration caveat:
# This retained legacy validation asset was not executed during migration.
# It is not a final public user runner. Future public runner output must not write to case-local runs/ by default.
# See notes/migration_notes.md and evidence/runs_retention.yaml.

set -euo pipefail

# Draft bundle note: this script is intended to be copied into the real case package
# before execution. It is not meant to be run from the overnight report directory.

CASE_ID="PERF_0056"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"

# Load the repo's standard MySQL shell defaults for local shell execution.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_mysql.sh"

SCHEMA="${MYSQL_DATABASE}"
MYSQL_BIN="${MYSQL_BIN:-mysql}"
MYSQL_ARGS=()
if [[ -n "${MYSQL_HOST:-}" ]]; then MYSQL_ARGS+=(--host="$MYSQL_HOST"); fi
if [[ -n "${MYSQL_PORT:-}" ]]; then MYSQL_ARGS+=(--port="$MYSQL_PORT"); fi
if [[ -n "${MYSQL_USER:-}" ]]; then MYSQL_ARGS+=(--user="$MYSQL_USER"); fi
if [[ -n "${MYSQL_PASSWORD:-}" ]]; then MYSQL_ARGS+=(--password="$MYSQL_PASSWORD"); fi
mysql_cmd() {
  "$MYSQL_BIN" "${MYSQL_ARGS[@]}" "$@"
}

PLAN_DIR="$CASE_DIR/runs/mysql/plans"
mkdir -p "$PLAN_DIR"

cleanup() {
  {
    printf 'use `%s`;\n' "$MYSQL_DATABASE"
    printf 'drop table if exists `customer_address`;\n'
    printf 'drop table if exists `customer`;\n'
    printf 'drop table if exists `store_sales`;\n'
    printf 'drop table if exists `date_dim`;\n'
    printf 'drop table if exists `item`;\n'
  } | mysql_cmd --batch --raw --skip-column-names >/dev/null 2>&1 || true
}
trap cleanup EXIT

{
  printf 'use `%s`;\n' "$MYSQL_DATABASE"
  printf 'drop table if exists `customer_address`;\n'
  printf 'drop table if exists `customer`;\n'
  printf 'drop table if exists `store_sales`;\n'
  printf 'drop table if exists `date_dim`;\n'
  printf 'drop table if exists `item`;\n'
  cat "$CASE_DIR/schema/mysql/ddl.sql"
  cat "$CASE_DIR/schema/mysql/load.sql"
} | mysql_cmd --batch --raw --skip-column-names >/dev/null

collect_plan() {
  local sql_file="$1"
  local out_file="$2"
  {
    printf 'use `%s`;\n' "$MYSQL_DATABASE"
    printf 'explain format=json\n'
    cat "$sql_file"
  } | mysql_cmd --batch --raw --skip-column-names > "$out_file"
}

collect_plan "$CASE_DIR/sql/source.sql" "$PLAN_DIR/source.json"
collect_plan "$CASE_DIR/sql/positives/pos_01.sql" "$PLAN_DIR/rewrite_pos_01.json"
collect_plan "$CASE_DIR/sql/negatives/neg_01.sql" "$PLAN_DIR/rewrite_neg_01.json"

source_plan_present=false
positive_plan_present=false
negative_plan_present=false
if test -s "$PLAN_DIR/source.json"; then source_plan_present=true; fi
if test -s "$PLAN_DIR/rewrite_pos_01.json"; then positive_plan_present=true; fi
if test -s "$PLAN_DIR/rewrite_neg_01.json"; then negative_plan_present=true; fi
ok=false
status="failed"
if $source_plan_present && $positive_plan_present && $negative_plan_present; then
  ok=true
  status="collected"
fi

cat > "$PLAN_DIR/plan_check.json" <<JSON
{
  "case_id": "$CASE_ID",
  "engine": "mysql",
  "status": "$status",
  "ok": $ok,
  "schema": "$SCHEMA",
  "inputs": {
    "source": "sql/source.sql",
    "positive_rewrite": "sql/positives/pos_01.sql",
    "negative_rewrite": "sql/negatives/neg_01.sql",
    "witness_data": "schema/mysql/load.sql"
  },
  "outputs": {
    "source_plan": "runs/mysql/plans/source.json",
    "positive_rewrite_plan": "runs/mysql/plans/rewrite_pos_01.json",
    "negative_rewrite_plan": "runs/mysql/plans/rewrite_neg_01.json"
  },
  "checks": {
    "source_plan_present": $source_plan_present,
    "positive_plan_present": $positive_plan_present,
    "negative_plan_present": $negative_plan_present
  },
  "notes": [
    "MySQL-only EXPLAIN FORMAT=JSON plan collection.",
    "Draft script intended for later reviewed execution after copy into the real case package.",
    "No PostgreSQL or Spark validation is implied.",
    "No admission, promotion, or common-core claim is made."
  ]
}
JSON

$ok
