# SQLGlot Schema-Aware Optimize Track A Checker Diagnostic

Task: `sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0`

Branch: `feature/case-package-v2-external-schema`

This packet records a local-only Track A diagnostic execution/checker pass for:

- `method_id = sqlglot`
- `route_id = sqlglot_optimize_schema_aware`
- adapter option: `--route optimize_schema_aware`
- scope: Common-core v0, 40 cases x PostgreSQL/MySQL/Spark = 120 planned rows

The diagnostic selected all 120 planned rows. It generated 105 candidates, recorded 20 fail-closed rows, executed/checker-attempted 91 candidate rows, and found 66 exact/result-consistent rows under the current strict checker policy.

This is not official or paper-facing evidence. No timing, verifier pass, official metric, Semantic Equivalence Rate, Regression@20, POCR, leaderboard output, retained-evidence promotion, or top-level `reports/`/`results/` update was created.
