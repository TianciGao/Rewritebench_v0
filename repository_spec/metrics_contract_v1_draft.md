# Metrics Contract v1 Draft

Status: draft, not implementation-authorizing

Purpose: draft the metric contract for the public workbench without finalizing changed metrics.

No implementation, metric recomputation, denominator update, paper result update, paper table change, or leaderboard is authorized by this draft.

## Current Paper Metric Families

The current paper-facing metric families are retained as reference categories:

- correctness and exactness over denominator-aware rows;
- execution/readiness status;
- timing and speedup only for exact and timed eligible rows;
- hard-negative checker guardrail behavior;
- plan observability and plan artifact availability;
- portability/generalization evidence for PORT routes;
- verifier/support evidence as a separate support role, not a rewrite-generation baseline;
- failure buckets for unsupported, failed, mismatched, missing-artifact, timing-missing, checker-failed, no-op/source-like, and other non-success states.

## Candidate Future Adjustments

Candidate future fields may include:

- parseability status;
- SQL extractability status;
- runnable SQL status;
- generation readiness versus execution readiness;
- exactness after checker normalization;
- fallback/regression reporting by quantiles, quartiles, or other distribution summaries;
- observability coverage as a first-class metric family;
- route-specific failure accounting.

These are candidates only. Final definitions require maintainer/team confirmation before implementation.

## Denominator Handling

The metrics contract must preserve:

- Common-core v0 = 40 cases;
- Track A same-engine planned rows = 120;
- engines = PostgreSQL, MySQL, Spark;
- no global leaderboard;
- role-aware denominator slices.

Each reported metric must state:

- denominator set;
- included rows;
- excluded rows;
- readiness gate;
- correctness gate;
- timing eligibility gate where applicable.

## Correctness Gate

Correctness metrics should be computed only after:

- candidate SQL is available or marked missing;
- candidate SQL parse/extract status is known when relevant;
- execution status is known where execution is part of the route;
- checker status is known where a checker applies;
- hard negatives are treated as checker controls, not method-generated failures.

## Exact / Executed / Timed Handling

The contract should keep these states distinct:

- generated versus not generated;
- ready versus not ready;
- executed versus not executed;
- exact versus not exact;
- timed versus timing missing;
- timing eligible versus not timing eligible.

Speedup or latency interpretation must remain limited to exact and timed eligible rows. Blank or missing timing must not be interpreted as zero.

## Performance Distribution Reporting

Future performance reporting may use:

- median latency;
- geometric mean for approved exact/timed slices;
- quantiles or quartiles for fallback/regression reporting;
- per-engine and per-route distributions;
- explicit timing-missing counts.

The final performance contract is TBD and requires maintainer/team confirmation.

## Observability Metrics

Observability metrics may include:

- plan availability;
- plan artifact public-safety state;
- plan attribution feature availability;
- selected plan case-study coverage;
- engine/route plan collection status.

Final wording is TBD. Observability should not be collapsed into correctness or performance leaderboards.

## Parseability / Extractability / Runnable SQL

Possible future status fields:

- `parse_status`;
- `extractability_status`;
- `runnable_sql_status`;
- `execution_readiness_status`;
- `candidate_sql_available`.

These fields must distinguish method generation, SQL extraction, parser acceptance, engine runnable status, and checker correctness.

## Fallback / Regression Reporting

The prior Regression@20-style reporting may be revised. Candidate alternatives include:

- quantile-based regression summaries;
- quartile-based degradation bands;
- per-route fallback categories;
- exact/timed distribution deltas.

TBD: maintainer/team must confirm whether Regression@20 remains, is replaced, or is supplemented.

## Implementation Gate

Before implementing the unified reproduction interface, report renderer, or metric computation:

- maintainer/team must approve final metric definitions;
- denominator and route semantics must be frozen in a metrics contract;
- evidence ledger schema must be compatible with retained evidence and user-run outputs;
- no paper table renderer may change existing paper results without explicit approval.

This draft records direction only.
