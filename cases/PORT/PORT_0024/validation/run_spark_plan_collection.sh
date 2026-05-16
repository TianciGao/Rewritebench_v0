#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="PORT_0024"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
PLAN_DIR="${CASE_DIR}/runs/spark/plans"
PYTHON_BIN="${PYTHON_BIN:-python}"
TMP_ROOT="${PLAN_DIR}/_tmp_spark_plan_collection"

# DRAFT-ONLY plan collection scaffold. Do not treat this as executed evidence.
# Spark collects target-engine rewrite plans only for this portability case.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_spark.sh"

cleanup() { rm -rf "${TMP_ROOT}"; }
trap cleanup EXIT

rm -rf "${TMP_ROOT}"
mkdir -p "${PLAN_DIR}" "${TMP_ROOT}"
rm -f "${PLAN_DIR}/source.txt" "${PLAN_DIR}/rewrite_pos_01.txt" "${PLAN_DIR}/rewrite_neg_01.txt"

CASE_DIR="${CASE_DIR}" PLAN_DIR="${PLAN_DIR}" CASE_ID="${CASE_ID}" TMP_ROOT="${TMP_ROOT}" SPARK_LOCAL_IP="${SPARK_LOCAL_IP}" SPARK_DRIVER_MEMORY="${SPARK_DRIVER_MEMORY}" "${PYTHON_BIN}" - <<'PY2'
import io
import os
import pathlib
import re
from contextlib import redirect_stdout
from pyspark.sql import SparkSession


def strip_comments(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not re.match(r"^\s*--", line))


def read_statements(path: pathlib.Path):
    text = strip_comments(path.read_text())
    return [stmt.strip() for stmt in text.split(";") if stmt.strip()]


def read_query(path: pathlib.Path) -> str:
    return strip_comments(path.read_text()).strip().rstrip(";")


def collect_plan_text(spark: SparkSession, query_path: pathlib.Path) -> str:
    df = spark.sql(read_query(query_path))
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        df.explain(mode="formatted")
    return buffer.getvalue()


case_dir = pathlib.Path(os.environ["CASE_DIR"])
plan_dir = pathlib.Path(os.environ["PLAN_DIR"])
case_id = os.environ["CASE_ID"]
spark_local_ip = os.environ["SPARK_LOCAL_IP"]
spark_driver_memory = os.environ["SPARK_DRIVER_MEMORY"]
warehouse_dir = pathlib.Path(os.environ["TMP_ROOT"]) / "warehouse"
database_name = f"{case_id.lower()}_spark_plan_collection"
warehouse_dir.mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder.master("local[*]")
    .appName(f"{case_id}_spark_plan_collection")
    .config("spark.ui.enabled", "false")
    .config("spark.sql.shuffle.partitions", "1")
    .config("spark.sql.warehouse.dir", str(warehouse_dir))
    .config("spark.driver.host", spark_local_ip)
    .config("spark.driver.bindAddress", spark_local_ip)
    .config("spark.driver.memory", spark_driver_memory)
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

    (plan_dir / "rewrite_pos_01.txt").write_text(collect_plan_text(spark, case_dir / "sql/positives/pos_01.sql"))
    (plan_dir / "rewrite_neg_01.txt").write_text(collect_plan_text(spark, case_dir / "sql/negatives/neg_01.sql"))
finally:
    spark.stop()
PY2
