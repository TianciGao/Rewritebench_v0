# Official Status Metrics v0 Limited Report

## Purpose And Scope

This task computes limited official status metrics for the two readiness-approved families only: Execution Coverage Rate and Result Consistency Rate.
Generation Rate remains blocked and is not computed.

## Official Metrics Computed

- Execution Coverage Rate: computed as a limited official status metric.
- Result Consistency Rate: computed as a limited official status metric.

## Blocked Metrics

- Generation Rate: blocked by `inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap`.
- GM_Speedup, Speedup Ratio Percentiles, Semantic Equivalence Rate, Attribution Coverage, and Cross-Engine metrics: out of scope.

## Denominator Handling

- Planned candidate rows preserved: 600.
- Authorized input rows used: 175.
- Unresolved or unauthorized rows kept visible: 425.
- Denominator reduction allowed: false.
- No global leaderboard: true.

## Unresolved And Unauthorized Handling

Rows outside the current authorization and normalization overlay remain denominator-visible non-success partitions. They are not silently dropped.

## Paper And Timing Boundaries

- Paper tables rendered: false.
- Paper result: false for every row.
- Timing and performance metrics computed: false.
- reports/ and results/ changed: false.

## Caveats

- SQLGlot rows are filled in combined overlay v2 but are not part of the current official input overlay.
- Generation Rate is blocked until inferred-generated policy and SQLGlot generated/ready gaps are resolved.
- Result Consistency Rate in this limited task uses the task-authorized planned denominator visibility model.

## Next Safe Action

Review limited official status metrics with denominator caveats; separately decide whether to authorize SQLGlot metric-input overlay and Generation Rate policy resolution.
