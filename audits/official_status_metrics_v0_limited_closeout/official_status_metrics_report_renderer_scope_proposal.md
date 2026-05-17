# Official Status Metrics Report Renderer Scope Proposal

## Purpose

Define a possible future renderer scope for limited official status metrics. This proposal does not implement a renderer and does not render paper tables.

## Proposed Inputs

- `audits/official_status_metrics_v0_limited/official_status_metrics_v0_limited_table.csv`
- `audits/official_status_metrics_v0_limited/official_status_metrics_denominator_audit.csv`
- `audits/official_status_metrics_v0_limited/official_status_metrics_blocked_generation_rate.csv`
- `audits/official_status_metrics_v0_limited_closeout/limited_status_metrics_closeout_matrix.csv`
- `audits/official_status_metrics_v0_limited_closeout/limited_status_metrics_denominator_review.csv`
- Metrics Contract v1 and status inference policy draft.

## Proposed Outputs

A future renderer could produce a status-only audit report table and an appendix-style denominator table after explicit authorization. It must not write to `reports/` or `results/` unless the authorization specifically allows those targets.

## Validation Gates

- Verify no official Generation Rate rows are computed or rendered as values.
- Verify every rendered row has `paper_result=false` unless a separate paper-result authorization changes that flag.
- Verify denominator partitions include planned rows, authorized rows, and unresolved/unauthorized rows.
- Verify no timing/performance metric names appear.
- Verify no global leaderboard, winner language, or collapsed cross-method ranking is produced.
- Verify output paths are explicitly authorized and do not mutate retained evidence.

## Labeling Requirements

Limited official status metrics must be labeled as limited official status metrics, not full benchmark results. Generation Rate must be shown as blocked, not blank or zero. Execution Coverage Rate and Result Consistency Rate must carry denominator and unresolved-row caveats.

## Blocked Generation Rate Handling

A renderer must show the blocker `inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap` and must not substitute inferred-generated rows for observed generated evidence.

## Denominator Partition Handling

The renderer must show unresolved and unauthorized rows explicitly. Authorized input rows must not replace the planned denominator.

## No Global Leaderboard

A renderer must group by metric, method, pool, and engine or another approved denominator-aware partition. It must not produce a global method ranking.

## Timing And Performance Boundary

Timing/performance metrics remain out of scope. GM_Speedup, Speedup Ratio Percentiles, and timing diagnostics require separate adapter and metric authorization.

## Separate Authorization Required

Paper or report rendering is a distinct implementation phase. This closeout only prepares decision material.
