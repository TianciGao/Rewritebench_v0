#!/usr/bin/env bash
set -euo pipefail

# Canonical migration caveat:
# This retained legacy validation asset was not executed during migration.
# No legacy Spark plan collection script was present for this case.
# Sanitized retained Spark plans are mapped in evidence/runs_retention.yaml.
# Future public runner output must not write to case-local runs/ by default.

echo "PERF_0006 has retained sanitized Spark plan evidence; no migrated Spark plan collection runner is provided."
exit 2
