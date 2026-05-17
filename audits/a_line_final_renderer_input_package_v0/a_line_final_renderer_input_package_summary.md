# A-line Final Renderer Input Package v0

## Purpose And Scope

This package collects the final A-line v0 metric states into stable inputs for a future paper/report renderer task.

No new metrics were computed. No official metrics were recomputed. No paper tables were rendered. No `reports/` or `results/` files were created or updated. Denominator values, paper results, case membership, raw legacy evidence, and prior metric outputs were unchanged.

## A-line v0 Metric State Summary

All ten Metrics Contract v1 primary metrics are represented.

- Execution Coverage Rate: include as limited official metric input.
- Result Consistency Rate: include as limited official metric input.
- Generation Rate: report as blocked.
- GM_Speedup: report as blocked.
- Speedup Ratio Percentiles: report as blocked.
- Speedup Retention: report as N.A.
- Semantic Equivalence Rate: include audit-only support only.
- Attribution Coverage: defer post-release.
- Cross-Engine Execution: defer post-release.
- Cross-Engine Consistency: defer post-release.

## Official Limited Metric Inputs

The future renderer may reference `audits/official_status_metrics_v0_limited/official_status_metrics_v0_limited_table.csv` for Execution Coverage Rate and Result Consistency Rate only after separate renderer authorization.

These metrics are limited official status metrics. They are denominator-aware, keep unresolved and unauthorized rows visible, and are not paper results.

## Blocked Metric Records

Generation Rate remains blocked by `inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap`.

GM_Speedup and Speedup Ratio Percentiles remain blocked because no timing adapter, timing eligibility policy, exact+timed denominator, or validated speedup-ratio rows are available for v0.

## N.A. Metric Records

Speedup Retention is N.A. for v0 because paired source-engine and target-engine result-consistent timing is unavailable. N.A. must not be rendered as zero, failure, or missing implementation success.

## Audit-only Support Records

Semantic Equivalence Rate has verifier-support references only as audit support. No official Semantic Equivalence Rate is available because no verifier-decidable row-level denominator or verifier adapter has been approved.

## Post-release Backlog Records

Attribution Coverage, Cross-Engine Execution, and Cross-Engine Consistency are post-release backlog metrics. They require future attribution or portability adapters, denominator policies, validation gates, and separate authorization before any renderer can show metric values.

## Denominator And No-global-leaderboard Requirements

Common-core v0 contains 40 canonical case packages. Track A same-engine has 120 planned denominator rows. The rewrite-candidate scaffold has 600 planned rows across five method routes.

Denominator reduction is forbidden. Unresolved, unauthorized, blocked, N.A., and post-release partitions must remain visible. No global leaderboard is allowed.

Hard negatives are checker controls, not method failures. Timing and performance metrics are not available in this A-line v0 renderer-input package.

## Caveat Package Summary

Future rendering must label the two official status metrics as limited official status metrics, not full benchmark results. Generation Rate must be shown as blocked. Semantic Equivalence Rate must be shown as support-only. Performance metrics must be shown as blocked, Speedup Retention as N.A., and attribution/cross-engine metrics as post-release backlog.

## Exact Next Safe Action

Run `b_line_reproduction_report_renderer_design_v0` to design the reproduction/report renderer boundary and validation gates without rendering paper tables, writing `reports/` or `results/`, computing metrics, or changing denominators.
