#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="PORT_0003"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
PLAN_DIR="${CASE_DIR}/runs/spark/plans"
PYTHON_BIN="${PYTHON_BIN:-python}"

# DRAFT-ONLY plan collection scaffold. Do not treat this as executed evidence.
# Spark collects only target-engine rewrite plans for this portability case.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_spark.sh"

mkdir -p "${PLAN_DIR}"

CASE_DIR="${CASE_DIR}" \
PLAN_DIR="${PLAN_DIR}" \
CASE_ID="${CASE_ID}" \
SPARK_LOCAL_IP="${SPARK_LOCAL_IP}" \
SPARK_DRIVER_MEMORY="${SPARK_DRIVER_MEMORY}" \
"${PYTHON_BIN}" - <<'PY'
import io
import os
import pathlib
import re
import shutil
import tempfile
from contextlib import redirect_stdout

from pyspark.sql import SparkSession


def strip_comment_lines(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if re.match(r"^\s*--", line):
            continue
        lines.append(line)
    return "\n".join(lines)


def read_statements(path: pathlib.Path) -> list[str]:
    text = strip_comment_lines(path.read_text())
    return [stmt.strip() for stmt in text.split(";") if stmt.strip()]


def read_query(path: pathlib.Path) -> str:
    return strip_comment_lines(path.read_text()).strip().rstrip(";")


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
warehouse_dir = pathlib.Path(tempfile.mkdtemp(prefix=f"{case_id.lower()}_spark_plan_"))

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
    for statement in read_statements(case_dir / "schema/ddl_spark.sql"):
        spark.sql(statement)
    for statement in read_statements(case_dir / "validation/load_witness_spark.sql"):
        spark.sql(statement)

    positive_text = collect_plan_text(spark, case_dir / "rewrite_pos_02_spark.sql")
    negative_text = collect_plan_text(spark, case_dir / "rewrite_neg_02_spark.sql")

    (plan_dir / "rewrite_pos_02_spark.txt").write_text(positive_text)
    (plan_dir / "rewrite_neg_02_spark.txt").write_text(negative_text)
finally:
    spark.stop()
    shutil.rmtree(warehouse_dir, ignore_errors=True)
PY
