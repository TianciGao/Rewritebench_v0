#!/usr/bin/env bash
set -euo pipefail

CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"

PYTHONPATH="${REPO_ROOT}/src${PYTHONPATH:+:${PYTHONPATH}}" python3 "${CASE_DIR}/validation/run_engine_queries.py" --mode validation "$@"
