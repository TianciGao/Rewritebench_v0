#!/usr/bin/env bash
set -euo pipefail

CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$CASE_DIR/manifest.yaml"

if [[ ! -f "$MANIFEST" ]]; then
  echo "missing manifest: $MANIFEST" >&2
  exit 2
fi

echo "PERF_0035: shared v2 validation runner not implemented; use future shared runner" >&2
exit 2
