#!/usr/bin/env bash
set -euo pipefail

# Canonical migration caveat:
# This retained legacy validation asset was not executed during migration.
# No legacy Spark plan collection script was present for PERF_0008.
# Sanitized retained Spark plans are mapped in evidence/runs_retention.yaml.
# Future public runner output must not write to case-local runs/ by default.

echo "PERF_0008 has retained sanitized Spark plan evidence; no migrated Spark plan collection runner is provided."
exit 2
