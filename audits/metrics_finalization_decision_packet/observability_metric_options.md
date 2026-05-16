# Observability Metric Options

This file discusses observability metric choices. It does not finalize metric definitions.

## Observability Scope

SQL-RewriteBench treats plan observability and failure visibility as first-class evidence dimensions. Observability should describe what the workbench can inspect from external SQL rewrite events, not claim access to internal optimizer reasoning beyond retained artifacts.

## PlanAvailability

Possible wording:

- `PlanAvailability`: fraction of eligible plan-observability rows with public-safe retained or generated plan artifacts.
- `PlanArtifactCoverage`: count and fraction of rows with plan artifacts by case, engine, route, and method role.

Open questions:

- Is the denominator candidate rows, plan collection attempts, or selected plan-observability opportunities?
- Are sanitized public copies and private archive references both counted?
- Should source/positive/hard-negative controls be counted separately from method candidates?

Recommended direction:

- Keep `PlanAvailability` as an observability family, not a performance metric.
- Require `plan_available`, `plan_artifact_path`, `record_type`, `route`, and `evidence_source`.

## PlanFrontier

Possible wording:

- `PlanFrontier`: selected case-study or feature-summary coverage for plan/failure observability.
- `PlanObservabilityFrontier`: a report section identifying what observability evidence is available and what remains opaque.

Open questions:

- Is PlanFrontier a metric, a report section, or a qualitative evidence label?
- Does it count plan attribution features or only artifact availability?

Recommended direction:

- Treat PlanFrontier as a report section first. Add a metric only after feature schema is approved.

## Failure Bucket Coverage

Failure visibility should include:

- generation failures;
- extraction failures;
- parse failures;
- preflight-blocked rows;
- execution failures;
- checker failures;
- semantic mismatches;
- hard-negative false accepts;
- unsupported rows;
- timeouts;
- timing-missing rows;
- source-like/no-op candidates;
- no-candidate rows;
- unknown/manual-review rows.

Recommended direction:

- Report failure bucket distribution as diagnostic and route-aware.
- Do not collapse failures into one non-success count without a breakdown.

## Evidence Layer Versus Metric Family

Observability can be both:

- an evidence layer that records whether relevant artifacts exist;
- a metric family for public workbench summaries.

It should not be primary rewrite quality or speedup evidence.

## Avoiding Overclaiming

Wording should avoid implying internal optimizer insight. Recommended phrasing:

- "external plan/failure observability evidence"
- "retained plan artifact availability"
- "public-safe plan evidence coverage"
- "failure-stage visibility"

Avoid:

- "optimizer understanding"
- "complete plan frontier"
- "full internal optimizer observability"

## Alignment With Paper Framing

The paper framing treats SQL rewrite events as externally observable through generated SQL, execution behavior, checker results, failures, and plan artifacts. Observability metrics should stay within that external-observable boundary.
