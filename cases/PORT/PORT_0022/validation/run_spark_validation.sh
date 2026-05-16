#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="PORT_0022"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/spark"
PYTHON_BIN="${PYTHON_BIN:-python}"
TMP_ROOT="${RUN_DIR}/_tmp_spark_validation"
MYSQL_RUN_DIR="${CASE_DIR}/runs/mysql"
PG_RUN_DIR="${CASE_DIR}/runs/pg"
SOURCE_NORMALIZED_SQL="${RUN_DIR}/source.spark_normalized.sql"
RESULT_CHECK_JSON="${RUN_DIR}/result_check.json"

# DRAFT-ONLY validation scaffold. Do not treat this as executed evidence.
# Spark runs target rewrites only for this portability case.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_spark.sh"

cleanup() { rm -rf "${TMP_ROOT}"; }
trap cleanup EXIT

rm -rf "${TMP_ROOT}"
mkdir -p "${RUN_DIR}" "${TMP_ROOT}"
rm -f "${RUN_DIR}/source.tsv" "${RUN_DIR}/rewrite_pos_01.tsv" "${RUN_DIR}/rewrite_neg_01.tsv" \
  "${SOURCE_NORMALIZED_SQL}" "${RESULT_CHECK_JSON}"

CASE_DIR="${CASE_DIR}" RUN_DIR="${RUN_DIR}" CASE_ID="${CASE_ID}" TMP_ROOT="${TMP_ROOT}" SOURCE_NORMALIZED_SQL="${SOURCE_NORMALIZED_SQL}" "${PYTHON_BIN}" - <<'PY2'
import os
import pathlib
import re
from pyspark.sql import SparkSession


def strip_comments(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not re.match(r"^\s*--", line))


def read_statements(path: pathlib.Path):
    text = strip_comments(path.read_text())
    return [stmt.strip() for stmt in text.split(";") if stmt.strip()]


def read_query(path: pathlib.Path) -> str:
    return strip_comments(path.read_text()).strip().rstrip(";")

def normalize_source_query(text: str) -> str:
    text = re.sub(r"AS\s+DATETIME", "AS TIMESTAMP", text, flags=re.IGNORECASE)
    text = text.replace("'%Y'", "'yyyy'")
    return text


def write_rows(path: pathlib.Path, rows) -> None:
    lines = ["\t".join("NULL" if value is None else str(value) for value in row) for row in rows]
    lines.sort()
    path.write_text("".join(f"{line}\n" for line in lines))


case_dir = pathlib.Path(os.environ["CASE_DIR"])
run_dir = pathlib.Path(os.environ["RUN_DIR"])
case_id = os.environ["CASE_ID"]
warehouse_dir = pathlib.Path(os.environ["TMP_ROOT"]) / "warehouse"
source_normalized_sql = pathlib.Path(os.environ["SOURCE_NORMALIZED_SQL"])
database_name = f"{case_id.lower()}_spark_validation"
warehouse_dir.mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder.master("local[*]")
    .appName(f"{case_id}_draft_validation")
    .config("spark.ui.enabled", "false")
    .config("spark.sql.shuffle.partitions", "1")
    .config("spark.sql.warehouse.dir", str(warehouse_dir))
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

try:
    spark.sql(f"DROP DATABASE IF EXISTS {database_name} CASCADE")
    spark.sql(f"CREATE DATABASE {database_name}")
    spark.sql(f"USE {database_name}")

    for stmt in read_statements(case_dir / "schema/spark/ddl.sql"):
        spark.sql(stmt)
    for stmt in read_statements(case_dir / "schema/spark/load.sql"):
        spark.sql(stmt)

    source_query = normalize_source_query(read_query(case_dir / "sql/source.sql"))
    source_normalized_sql.write_text(source_query + "\n")
    source_rows = spark.sql(source_query).collect()
    positive = spark.sql(read_query(case_dir / "sql/positives/pos_01.sql")).collect()
    negative = spark.sql(read_query(case_dir / "sql/negatives/neg_01.sql")).collect()

    write_rows(run_dir / "source.tsv", source_rows)
    write_rows(run_dir / "rewrite_pos_01.tsv", positive)
    write_rows(run_dir / "rewrite_neg_01.tsv", negative)
finally:
    spark.stop()
PY2

maybe_run_checker() {
  if [[ -f "${MYSQL_RUN_DIR}/source.tsv" && -f "${PG_RUN_DIR}/rewrite_pos_01.tsv" \
    && -f "${PG_RUN_DIR}/rewrite_neg_01.tsv" && -f "${RUN_DIR}/rewrite_pos_01.tsv" \
    && -f "${RUN_DIR}/rewrite_neg_01.tsv" ]]; then
    python "${CASE_DIR}/validation/check_results.py" \
      "${MYSQL_RUN_DIR}/source.tsv" \
      "${PG_RUN_DIR}/rewrite_pos_01.tsv" \
      "${PG_RUN_DIR}/rewrite_neg_01.tsv" \
      "${RUN_DIR}/rewrite_pos_01.tsv" \
      "${RUN_DIR}/rewrite_neg_01.tsv" \
      "${RESULT_CHECK_JSON}"
    cp "${RESULT_CHECK_JSON}" "${MYSQL_RUN_DIR}/result_check.json"
  fi
}

maybe_run_checker
