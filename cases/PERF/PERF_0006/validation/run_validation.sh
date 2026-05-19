#!/usr/bin/env bash
set -euo pipefail

cat <<'MSG'
PERF_0006 case-package v2 pilot validation wrapper.

This branch pilot intentionally does not run DB engines from case-local scripts.
Existing engine-specific validation scripts are retained as legacy validation
assets, but they write to case-local runs/ and are not the v2 public output
policy. Future v2 runner work should execute through top-level runs/user/
or another explicitly authorized local output root.
MSG

exit 2
