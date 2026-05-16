#!/usr/bin/env bash
# Retained legacy validation asset; not executed during public-release migration.
# Future public runner outputs must not write to case-local runs/ by default.
set -euo pipefail

CASE_ID="PORT_0005"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/spark"
PYTHON_BIN="${PYTHON_BIN:-python}"

# DRAFT-ONLY validation scaffold. Do not treat this as executed evidence.
# Spark runs only the target rewrites for this portability case.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_spark.sh"

mkdir -p "${RUN_DIR}"

CASE_DIR="${CASE_DIR}" RUN_DIR="${RUN_DIR}" CASE_ID="${CASE_ID}" "${PYTHON_BIN}" - <<'PY'
import pathlib
import re
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


case_dir = pathlib.Path(__import__("os").environ["CASE_DIR"])
run_dir = pathlib.Path(__import__("os").environ["RUN_DIR"])
case_id = __import__("os").environ["CASE_ID"]

spark = (
    SparkSession.builder.master("local[*]")
    .appName(f"{case_id}_draft_validation")
    .config("spark.ui.enabled", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

try:
    for stmt in read_statements(case_dir / "schema/ddl_spark.sql"):
        spark.sql(stmt)
    for stmt in read_statements(case_dir / "validation/load_witness_spark.sql"):
        spark.sql(stmt)

    positive = spark.sql(read_query(case_dir / "rewrite_pos_02_spark.sql")).collect()
    negative = spark.sql(read_query(case_dir / "rewrite_neg_02_spark.sql")).collect()

    write_rows(run_dir / "rewrite_pos_02_spark.tsv", positive)
    write_rows(run_dir / "rewrite_neg_02_spark.tsv", negative)
finally:
    spark.stop()
PY
