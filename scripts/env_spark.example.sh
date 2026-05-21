#!/usr/bin/env bash
# Spark local diagnostic environment placeholder.
#
# Spark execution remains deferred and fail-closed in the current user-entry
# path. This file is a placeholder for future local Spark diagnostics only; it
# does not enable a Spark backend.
#
# Usage:
#   cp scripts/env_spark.example.sh scripts/env_spark.local.sh
#   source scripts/env_spark.local.sh
#
# Do not commit scripts/env_spark.local.sh if you add local-only settings.

export SPARK_LOCAL_IP=127.0.0.1
