#!/usr/bin/env bash
# Retained legacy validation asset for CONS_0005.
# Not executed during migration. Future public runner output must not write to case-local runs/ by default.
set -euo pipefail
CASE_ID="CONS_0005"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "${CASE_ID}: retained Spark plan-collection asset; sanitized retained plans are under evidence/retained_plans/spark/." >&2
exit 2
