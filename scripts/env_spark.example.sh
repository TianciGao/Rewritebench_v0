#!/usr/bin/env bash
# Spark local diagnostic environment template.
#
# Spark live SQL execution remains deferred in the current user-entry path.
# These variables are preparatory only. They let the local environment checker
# report Spark readiness signals, but they do not enable live Spark execution.
#
# Usage:
#   cp scripts/env_spark.example.sh scripts/env_spark.local.sh
#   source scripts/env_spark.local.sh
#
# Do not commit scripts/env_spark.local.sh if you add local-only settings.

export SPARK_LOCAL_IP=127.0.0.1

# Optional future live-backend settings. Leave commented unless needed locally.
# export SPARK_HOME=/path/to/spark
# export PYSPARK_PYTHON="$(command -v python)"
# export SQLRB_SPARK_MASTER=local[1]
