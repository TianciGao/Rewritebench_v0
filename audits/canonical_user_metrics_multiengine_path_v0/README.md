# Canonical User Metrics Multi-Engine Path

Task: `canonical_user_metrics_multiengine_path_v0`

Branch: `feature/case-package-v2-external-schema`

This packet records the correction from audit-helper route-card projections to the canonical local metrics path.

Verdict:
- `src/sql_rewrite_bench/local_metrics.py` remains the single source of truth for local diagnostic metrics.
- Single-run metrics remain available through `compute_and_write_local_metrics(run_dir)`.
- Multi-engine Track A-style metrics are now available through `compute_and_write_aggregate_local_metrics(...)`.
- The user-facing CLI now supports canonical aggregation of per-engine source runs created by multi-engine `user evaluate`.

No candidate generation, execution/checker run, timing run, verifier pass, official metrics computation, paper output update, retained-evidence promotion, leaderboard output, denominator change, or case membership change was performed.
