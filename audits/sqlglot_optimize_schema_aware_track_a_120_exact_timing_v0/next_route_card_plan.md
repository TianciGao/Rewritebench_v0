# Next Route-Card Plan

Recommended next task:

- Build a local-only route-card projection for `sqlglot_optimize_schema_aware` using:
  - `audits/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/`
  - `audits/sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/`

The route card should:

- keep selected rows = 120 as the planned denominator;
- use selected rows for local generation, execution coverage, and result consistency rates;
- use only exact-timed rows for diagnostic speedup summaries;
- preserve fail-closed, mismatch, candidate execution failure, unsupported, and parse/schema/optimizer frontier buckets;
- stay local-only and non-paper-facing.

Do not include:

- verifier output;
- official metrics;
- official Semantic Equivalence Rate;
- formal Regression@20;
- POCR;
- leaderboard output;
- top-level reports/results updates.
