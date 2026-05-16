#!/usr/bin/env bash
# Canonical migration caveat:
# This retained legacy validation asset was not executed during migration.
# It is not a final public user runner. Future public runner output must not write to case-local runs/ by default.
# See notes/migration_notes.md and evidence/runs_retention.yaml.

set -euo pipefail

CASE_ID="CONS_0009"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/spark"
PYTHON_BIN="${PYTHON_BIN:-python}"

# Load standard Spark environment settings for local shell execution.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_spark.sh"

mkdir -p "${RUN_DIR}"

CASE_DIR="${CASE_DIR}" \
RUN_DIR="${RUN_DIR}" \
CASE_ID="${CASE_ID}" \
SPARK_LOCAL_IP="${SPARK_LOCAL_IP}" \
SPARK_DRIVER_MEMORY="${SPARK_DRIVER_MEMORY}" \
"${PYTHON_BIN}" - <<'PY'
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile

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


def normalize_value(value) -> str:
    if value is None:
        return "NULL"
    return str(value)


def collect_lines(spark: SparkSession, query_path: pathlib.Path) -> list[str]:
    rows = spark.sql(read_query(query_path)).collect()
    lines = ["\t".join(normalize_value(value) for value in row) for row in rows]
    lines.sort()
    return lines


def write_lines(path: pathlib.Path, lines: list[str]) -> None:
    path.write_text("".join(f"{line}\n" for line in lines))


case_dir = pathlib.Path(os.environ["CASE_DIR"])
run_dir = pathlib.Path(os.environ["RUN_DIR"])
case_id = os.environ["CASE_ID"]
spark_local_ip = os.environ["SPARK_LOCAL_IP"]
spark_driver_memory = os.environ["SPARK_DRIVER_MEMORY"]
warehouse_dir = pathlib.Path(tempfile.mkdtemp(prefix=f"{case_id.lower()}_spark_validation_"))

spark = (
    SparkSession.builder.master("local[*]")
    .appName(f"{case_id}_spark_validation")
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
    for statement in read_statements(case_dir / "schema/spark/ddl.sql"):
        spark.sql(statement)
    for statement in read_statements(case_dir / "schema/spark/load.sql"):
        spark.sql(statement)

    source_lines = collect_lines(spark, case_dir / "sql/source.sql")
    positive_lines = collect_lines(spark, case_dir / "sql/positives/pos_01.sql")
    negative_lines = collect_lines(spark, case_dir / "sql/negatives/neg_01.sql")

    write_lines(run_dir / "source.tsv", source_lines)
    write_lines(run_dir / "rewrite_pos_01.tsv", positive_lines)
    write_lines(run_dir / "rewrite_neg_01.tsv", negative_lines)

    source_positive_equal = source_lines == positive_lines
    source_negative_different = source_lines != negative_lines
    ok = source_positive_equal and source_negative_different
    status = "validated" if ok else "failed"

    payload = {
        "case_id": case_id,
        "engine": "spark",
        "status": status,
        "ok": ok,
        "schema": "spark_catalog.default",
        "inputs": {
            "source": "sql/source.sql",
            "positive_rewrite": "sql/positives/pos_01.sql",
            "negative_rewrite": "sql/negatives/neg_01.sql",
            "witness_data": "schema/spark/load.sql",
        },
        "outputs": {
            "source": "runs/spark/source.tsv",
            "positive_rewrite": "runs/spark/rewrite_pos_01.tsv",
            "negative_rewrite": "runs/spark/rewrite_neg_01.tsv",
        },
        "checks": {
            "source_positive_equal": source_positive_equal,
            "source_negative_different": source_negative_different,
        },
        "notes": [
            "Spark-only witness validation for CONS_0009.",
            "No PostgreSQL or MySQL validation is implied.",
            "No admission, promotion, common-core, extended, or tri-engine-closure claim is made.",
        ],
    }
    (run_dir / "result_check.json").write_text(json.dumps(payload, indent=2) + "\n")
finally:
    spark.stop()
    shutil.rmtree(warehouse_dir, ignore_errors=True)

sys.exit(0 if ok else 1)
PY
