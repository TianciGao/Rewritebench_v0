#!/usr/bin/env bash
# Canonical migration caveat:
# This retained legacy validation asset was not executed during migration.
# It is not a final public user runner. Future public runner output must not write to case-local runs/ by default.
# See notes/migration_notes.md and evidence/runs_retention.yaml.

set -euo pipefail

CASE_ID="PERF_0054"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
PLAN_DIR="${CASE_DIR}/runs/spark/plans"
PYTHON_BIN="${PYTHON_BIN:-python}"

# Load the repo's standard Spark shell defaults for local shell execution.
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
import json
import os
import pathlib
import re
import shutil
import sys
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
    for statement in read_statements(case_dir / "schema/spark/ddl.sql"):
        spark.sql(statement)
    for statement in read_statements(case_dir / "schema/spark/load.sql"):
        spark.sql(statement)

    source_text = collect_plan_text(spark, case_dir / "sql/source.sql")
    positive_text = collect_plan_text(spark, case_dir / "sql/positives/pos_01.sql")
    negative_text = collect_plan_text(spark, case_dir / "sql/negatives/neg_01.sql")

    (plan_dir / "source.txt").write_text(source_text)
    (plan_dir / "rewrite_pos_01.txt").write_text(positive_text)
    (plan_dir / "rewrite_neg_01.txt").write_text(negative_text)

    source_plan_present = bool(source_text.strip())
    positive_plan_present = bool(positive_text.strip())
    negative_plan_present = bool(negative_text.strip())
    ok = source_plan_present and positive_plan_present and negative_plan_present
    status = "collected" if ok else "failed"

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
            "source_plan": "runs/spark/plans/source.txt",
            "positive_rewrite_plan": "runs/spark/plans/rewrite_pos_01.txt",
            "negative_rewrite_plan": "runs/spark/plans/rewrite_neg_01.txt",
        },
        "checks": {
            "source_plan_present": source_plan_present,
            "positive_plan_present": positive_plan_present,
            "negative_plan_present": negative_plan_present,
        },
        "notes": [
            "Spark-only explain-formatted plan collection.",
            "Plans were collected against case-local Spark DDL and Spark witness data.",
            "No PostgreSQL or MySQL validation is implied.",
            "No admission, promotion, or common-core claim is made.",
        ],
    }
    (plan_dir / "plan_check.json").write_text(json.dumps(payload, indent=2) + "\n")
finally:
    spark.stop()
    shutil.rmtree(warehouse_dir, ignore_errors=True)

sys.exit(0 if ok else 1)
PY
