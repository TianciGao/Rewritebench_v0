#!/usr/bin/env bash
set -euo pipefail

cat <<'MSG'
PERF_0006 case-package v2 pilot plan-collection wrapper.

This branch pilot intentionally does not collect plans or write case-local
runs/ outputs. Existing engine-specific plan scripts are retained as legacy
validation assets until v2 validators and runners are updated for external
schema_ref resolution and safe local output roots.
MSG

exit 2
