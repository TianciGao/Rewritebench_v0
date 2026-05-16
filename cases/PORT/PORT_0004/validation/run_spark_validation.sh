#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="PORT_0004"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/spark"
MYSQL_RUN_DIR="${CASE_DIR}/runs/mysql"
PG_RUN_DIR="${CASE_DIR}/runs/pg"
PYTHON_BIN="${PYTHON_BIN:-python}"

# DRAFT-ONLY validation scaffold. Do not treat this as executed evidence.
# Spark runs only the target rewrites for this portability case.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_spark.sh"

mkdir -p "${RUN_DIR}"

CASE_DIR="${CASE_DIR}" RUN_DIR="${RUN_DIR}" CASE_ID="${CASE_ID}" "${PYTHON_BIN}" - <<'PY'
import os
import pathlib
import re
import shutil
from pyspark.sql import SparkSession


def strip_comments(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not re.match(r"^\s*--", line))


def read_statements(path: pathlib.Path) -> list[str]:
    text = strip_comments(path.read_text())
    return [stmt.strip() for stmt in text.split(";") if stmt.strip()]


def read_query(path: pathlib.Path) -> str:
    return strip_comments(path.read_text()).strip().rstrip(";")


def write_rows(path: pathlib.Path, rows) -> None:
    lines = ["\t".join("NULL" if value is None else str(value) for value in row) for row in rows]
    lines.sort()
    path.write_text("".join(f"{line}\n" for line in lines))


case_dir = pathlib.Path(os.environ["CASE_DIR"])
run_dir = pathlib.Path(os.environ["RUN_DIR"])
case_id = os.environ["CASE_ID"]
warehouse_dir = run_dir / "warehouse"
database_name = f"{case_id.lower()}_validation"

spark = (
    SparkSession.builder.master("local[*]")
    .appName(f"{case_id}_draft_validation")
    .config("spark.ui.enabled", "false")
    .config("spark.sql.warehouse.dir", str(warehouse_dir))
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

try:
    if warehouse_dir.exists():
        shutil.rmtree(warehouse_dir)

    spark.sql(f"DROP DATABASE IF EXISTS {database_name} CASCADE")
    spark.sql(f"CREATE DATABASE {database_name}")
    spark.sql(f"USE {database_name}")

    for stmt in read_statements(case_dir / "schema/spark/ddl.sql"):
        spark.sql(stmt)
    for stmt in read_statements(case_dir / "schema/spark/load.sql"):
        spark.sql(stmt)

    positive = spark.sql(read_query(case_dir / "sql/dialect_variants/spark/pos_02_spark.sql")).collect()
    negative = spark.sql(read_query(case_dir / "sql/dialect_variants/spark/neg_02_spark.sql")).collect()

    write_rows(run_dir / "rewrite_pos_02_spark.tsv", positive)
    write_rows(run_dir / "rewrite_neg_02_spark.tsv", negative)
finally:
    spark.stop()
PY

if [[ -f "${MYSQL_RUN_DIR}/source.tsv" && -f "${PG_RUN_DIR}/rewrite_pos_01.tsv" && -f "${PG_RUN_DIR}/rewrite_neg_01.tsv" ]]; then
  "${PYTHON_BIN}" "${CASE_DIR}/validation/check_results.py" \
    "${MYSQL_RUN_DIR}/source.tsv" \
    "${PG_RUN_DIR}/rewrite_pos_01.tsv" \
    "${PG_RUN_DIR}/rewrite_neg_01.tsv" \
    "${RUN_DIR}/rewrite_pos_02_spark.tsv" \
    "${RUN_DIR}/rewrite_neg_02_spark.tsv" \
    "${RUN_DIR}/result_check.json"
fi
