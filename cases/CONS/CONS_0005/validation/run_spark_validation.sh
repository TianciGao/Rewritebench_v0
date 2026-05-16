#!/usr/bin/env bash
# Retained legacy validation asset for CONS_0005.
# Not executed during migration. Future public runner output must not write to case-local runs/ by default.
set -euo pipefail
CASE_ID="CONS_0005"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/spark"
PYTHON_BIN="${PYTHON_BIN:-python}"
mkdir -p "${RUN_DIR}"
echo "${CASE_ID}: retained legacy Spark validation asset; adapt output location before public runner use." >&2
exit 2
