# Status Inference Policy v1 Draft

Status: draft policy, not implementation-authorizing

## Purpose

Define conservative rules for distinguishing source-observed candidate status fields from inferred candidate status fields before any official status-only metric computation.

This draft is based on `candidate_status_parser_v1`, `metric_input_authorization_overlay_v0`, `status_field_normalization_v0`, and `normalized_status_only_metrics_dryrun_v1` audit outputs.

## Non-goals

- Do not compute official metrics.
- Do not render paper tables.
- Do not update reports or results.
- Do not change denominator values or case membership.
- Do not fill timing, latency, speedup, or timing-eligibility fields.
- Do not modify parser ledgers or normalization overlays.
- Do not authorize inferred fields for metric input.

## Relation To Metrics Contract v1

Metrics Contract v1 defines Generation Rate from emitted candidate SQL, Execution Coverage Rate from execution status, and Result Consistency Rate from result/checker consistency under approved denominator boundaries. This policy does not change those definitions. It only defines when a future task may create a separate inferred-status overlay for audit dry runs or later authorization review.

Official metric computation remains blocked until a separately authorized implementation reads validated metric inputs and applies the Metrics Contract v1 denominator rules. Inference cannot convert a diagnostic field into a paper result.

## Observed Vs Inferred Fields

Source-observed fields are parsed or normalized directly from approved row-level evidence. Inferred fields are derived from a documented relationship between source-observed fields and target status fields.

Inferred fields must:

- be stored separately from source-observed fields;
- use names such as `inferred_generated` or `inferred_executed`;
- record the inference rule and source field;
- never overwrite `normalized_generated`, `normalized_executed`, or any other observed normalized field;
- remain ineligible for official metric input until separately authorized.

## Allowed Inference Rules

The following rules are conditionally allowed only for future overlay tasks:

- R1: `normalized_ready=true` may imply `inferred_generated=true` only if source documentation states that ready means candidate SQL exists and passed extraction/readiness.
- R2: `normalized_exact=true` may imply `inferred_executed=true` only if source documentation states exactness was produced by a checker after execution.
- R3: failure-stage or failure-type labels may imply generated/executed status only when a source-specific failure-stage mapping is reviewed and approved.
- R4: unknown, N.A., not-applicable, and missing evidence remain unknown/not-applicable. This rule is active and does not require future authorization.

Current audit preview counts:

- Potential R1 rows: 94
- Potential R2 rows: 0
- Rows in inference preview requiring future authorization: 94

## Forbidden Inference Rules

- Do not infer generated from ready as a blanket rule.
- Do not infer executed from exact as a blanket rule.
- Do not infer generated, executed, or exact from `result_status` alone.
- Do not infer from aggregate, route-level, or summary-only counts.
- Do not infer from missing evidence, `N.A.`, or unknown values.
- Do not coerce unknown or not-applicable to false.
- Do not use inferred timing, latency, speedup, plan, portability, verifier, or paper-table fields in this policy.
- Do not use inferred fields for official metrics without a separate authorization task.

## Source-specific Prerequisites

A future inference overlay must document, for each source family:

- source artifact identity;
- row grain and denominator join;
- source-specific meaning of ready, exact, failure_stage, and failure_type;
- whether values are source-observed or parser-derived;
- whether the relation supports dry-run only or official metric-input review;
- manual review outcome and approval scope.

## Denominator Boundary

Inference cannot add, remove, or rewrite denominator rows. Track A same-engine remains 120 planned case-engine rows per method route and 600 planned rows across the five Track-A same-engine methods. Unauthorized overlap rows and unresolved rows remain visible and cannot disappear from denominator/accounting outputs.

## Why Inference Cannot Create Paper Results

Inference is a modeling layer over existing audit evidence. It does not parse new retained evidence, validate execution, validate exactness, authorize timing, or compute official metrics. Paper results require separately authorized metric computation, validation gates, and renderer approval.

## Future Implementation Requirements

A future `status_inference_overlay_v0` or `normalized_status_only_metrics_dryrun_v2` must:

- read this policy draft and approved manual decisions;
- emit inferred fields separately from observed fields;
- preserve original parser and normalization ledgers;
- preserve unresolved and unauthorized rows in denominator accounting;
- write only audit outputs unless separately authorized;
- fail closed when source-specific semantics are ambiguous.

## Explicit Non-authorization

This draft does not authorize official metrics, paper results, timing metrics, report generation, result publication, denominator changes, case membership changes, or mutation of raw legacy evidence.
