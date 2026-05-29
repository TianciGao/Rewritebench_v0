#!/usr/bin/env bash
# Spark local diagnostic environment template.
#
# Spark local diagnostics use PySpark when it is available. These variables
# configure local-mode Spark execution for diagnostic runs only; they do not
# enable official metrics, timing, reports/results updates, or leaderboard rows.
#
# Usage:
#   cp scripts/env_spark.example.sh scripts/env_spark.local.sh
#   source scripts/env_spark.local.sh
#
# Do not commit scripts/env_spark.local.sh if you add local-only settings.

export SPARK_LOCAL_IP=127.0.0.1

# Optional live-backend settings. Leave commented unless needed locally.
# export SPARK_HOME=/path/to/spark
# export PYSPARK_PYTHON="$(command -v python)"
# export SQLRB_SPARK_MASTER=local[1]
# export SQLRB_SPARK_APP_NAME=sql-rewritebench-local-diagnostic
