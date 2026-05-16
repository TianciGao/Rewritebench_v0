# Proposed Metrics Contract Patch Plan

Do not modify `repository_spec/metrics_contract_v1_draft.md` directly in this task. This file lists proposed updates for a future approved patch.

## Sections To Update Later

- Current Paper Metric Families.
- Denominator Handling.
- Correctness Gate.
- Exact / Executed / Timed Handling.
- Performance Distribution Reporting.
- Observability Metrics.
- Parseability / Extractability / Runnable SQL.
- Fallback / Regression Reporting.
- Implementation Gate.

## Terms To Finalize

- `generated`
- `ready`
- `executed`
- `exact`
- `timed`
- `timing_eligible`
- `parse_status`
- `extractability_status`
- `runnable_sql_status`
- `result_status`
- `failure_stage`
- `failure_type`
- `PlanAvailability`
- `PlanFrontier`

## Metrics To Keep

Candidate keep list:

- `Exact@planned`
- `ExecutionCoverage`
- hard-negative expected rejection reporting
- `GM_Speedup` on exact and timed eligible rows

All still require final wording before implementation.

## Metrics To Rename Or Clarify

Candidates:

- `result_consistency_rate`
- `ValidRewriteYield`
- `Regression@20`
- `PlanFrontier`
- verifier `SupportRate`

## Metrics To Add

Candidates:

- quartile/distribution performance summary;
- parseability/extractability diagnostic status;
- runnable SQL status;
- failure bucket distribution;
- pipeline state counts for generated, ready, executed, exact, timed.

## Metrics To Mark Support-only

Candidates:

- verifier support evidence;
- retained summary artifacts;
- plan artifact evidence unless used only for observability;
- hard-negative controls outside checker metrics.

## Implementation Prerequisites

- approved metric definitions;
- approved evidence ledger schema and record types;
- approved failure bucket taxonomy;
- retained-evidence adapter row-grain tests;
- public output policy confirmation;
- curated retained evidence copy or reference plan;
- no changes to denominator or paper results without separate authorization.

## Team Decisions Needed

- Regression@20 retained, replaced, supplemented, or diagnostic-only.
- Distribution/quartile summary naming and table placement.
- Parseability/extractability/runnable SQL field definitions.
- PlanAvailability versus PlanFrontier split.
- Failure bucket taxonomy.
- User submission format and candidate ID policy.
- Retained LLM evidence frozen-only versus rerunnable.
- Timing-missing, unsupported, and preflight-blocked semantics.
- Exact public table names.
