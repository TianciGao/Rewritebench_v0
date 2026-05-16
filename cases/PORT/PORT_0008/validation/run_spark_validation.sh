#!/usr/bin/env bash
set -euo pipefail

CASE_ID="PORT_0008"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/spark"
PYTHON_BIN="${PYTHON_BIN:-python}"
TMP_ROOT="${RUN_DIR}/_tmp_spark_validation"

# DRAFT-ONLY validation scaffold. Do not treat this as executed evidence.
# Spark runs target rewrites only for this portability case.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_spark.sh"

cleanup() { rm -rf "${TMP_ROOT}"; }
trap cleanup EXIT

rm -rf "${TMP_ROOT}"
mkdir -p "${RUN_DIR}" "${TMP_ROOT}"
rm -f "${RUN_DIR}/source.tsv" "${RUN_DIR}/rewrite_pos_01.tsv" "${RUN_DIR}/rewrite_neg_01.tsv"

CASE_DIR="${CASE_DIR}" RUN_DIR="${RUN_DIR}" CASE_ID="${CASE_ID}" TMP_ROOT="${TMP_ROOT}" "${PYTHON_BIN}" - <<'PY2'
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


def write_rows(path: pathlib.Path, rows) -> None:
    lines = ["\t".join("NULL" if value is None else str(value) for value in row) for row in rows]
    lines.sort()
    path.write_text("".join(f"{line}\n" for line in lines))


case_dir = pathlib.Path(os.environ["CASE_DIR"])
run_dir = pathlib.Path(os.environ["RUN_DIR"])
case_id = os.environ["CASE_ID"]
warehouse_dir = pathlib.Path(os.environ["TMP_ROOT"]) / "warehouse"
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

    for stmt in read_statements(case_dir / "schema/ddl_spark.sql"):
        spark.sql(stmt)
    for stmt in read_statements(case_dir / "validation/spark_witness_data.sql"):
        spark.sql(stmt)

    positive = spark.sql(read_query(case_dir / "rewrite_pos_01.sql")).collect()
    negative = spark.sql(read_query(case_dir / "rewrite_neg_01.sql")).collect()

    write_rows(run_dir / "rewrite_pos_01.tsv", positive)
    write_rows(run_dir / "rewrite_neg_01.tsv", negative)
finally:
    spark.stop()
PY2
