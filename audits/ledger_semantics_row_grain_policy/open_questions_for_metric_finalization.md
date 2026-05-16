# Open Questions For Metric Finalization

The following questions remain before metrics implementation, paper table rendering, unified reproduction CLI implementation, retained-evidence adapter implementation for metric rows, or public runner output.

## Performance Regression

- Should the prior Regression@20-style metric remain?
- Should it be replaced by quartile or distribution-based reporting?
- Should both be reported with distinct names?
- What is the exact eligible row set for performance regression?

## Parseability And Extractability

- What distinguishes SQL extractability from parser acceptance?
- Which parser or dialect parser defines parseability?
- Should failed extraction be counted before or outside execution readiness?

## Runnable SQL Status

- What is the boundary between parseable SQL and engine-runnable SQL?
- Should unsupported syntax count as parse failure, run failure, or unsupported?
- How should preflight-blocked cases be represented?

## Observability Metrics

- What is the final wording for observability evidence?
- Is PlanAvailability a binary row metric, an artifact coverage metric, or both?
- Is PlanFrontier a separate metric, a case-study label, or a report section?

## User Submission Status Fields

- What is the required user submission format?
- How is `candidate_id` assigned for user submissions?
- Which fields must a user run manifest contain?
- Which output root is final?

## Retained LLM Evidence

- Is retained LLM evidence frozen-only for public v0?
- Are LLM baseline reruns in scope later?
- If reruns are out of scope, how should retained prompt/model traces be represented without exposing sensitive material?

## Missing, Unsupported, And Timing-missing

- What is the exact policy for timing missing on otherwise exact rows?
- How should unsupported engines or syntax be separated from execution failure?
- How should preflight-blocked rows affect coverage metrics?

## Ready Versus Generated Naming

- Should `ready` mean SQL generated, SQL parse-ready, execution-ready, or checker-ready?
- Should there be separate future fields for generation readiness, execution readiness, and checker readiness?
