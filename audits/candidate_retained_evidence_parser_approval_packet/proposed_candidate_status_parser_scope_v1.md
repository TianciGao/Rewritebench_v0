# Proposed Candidate Status Parser Scope v1

Status: proposed scope only; not implemented and not authorized by this packet.

## Purpose

Define the next bounded parser scope for converting approved retained candidate evidence into non-timing `rewrite_candidate_cell` status fields.

## Proposed Non-timing Parser Scope

The proposed parser may fill only non-timing candidate status fields when exact row-grain evidence exists:

- `generated`
- `ready`
- `executed`
- `exact`
- `result_status`
- `failure_stage`
- `failure_type`
- `parse_status`
- `checker_status`
- `candidate_sql_path`
- `retained_artifact_path`
- `evidence_source`
- `notes`

Required row grain:

`case_id x engine x rewrite_method x candidate_id x denominator_id`

Allowed record type:

`rewrite_candidate_cell`

Allowed routes:

- `direct_llm_original`
- `direct_llm_repair_1`
- `sqlglot_optimize`
- `sqlglot_noop`
- `calcite_hep_fail_closed`

## Input Manifest Requirement

Before implementation, the maintainer must approve an explicit input manifest identifying:

- exact retained-evidence source groups;
- public-safe source path handling;
- route-to-method normalization rules;
- row-grain keys available in each source;
- fields each source is allowed to populate;
- expected unresolved/manual-review behavior.

## Timing Parsing Separation

Timing parsing is out of scope. The non-timing parser must not populate:

- `timed`
- `latency_ms`
- `speedup_ratio`
- `timing_eligible`

Timing requires a separate timing adapter and timing eligibility policy.

## Metric Computation Separation

The non-timing parser must not compute:

- Generation Rate
- Execution Coverage Rate
- Result Consistency Rate
- Semantic Equivalence Rate
- GM_Speedup
- Speedup Ratio Percentiles
- Attribution Coverage
- Cross-Engine metrics
- diagnostic rates

All output rows must keep `metric_input_authorized=false` unless a later explicit authorization changes that.

## Paper Rendering Separation

The parser must not render paper tables, update paper result rows, or write paper-facing reports. Paper rendering requires validated metrics and separate authorization.

## Production Ledger Promotion Separation

The parser output should remain an audit artifact under `audits/` until:

1. the parser input manifest is approved;
2. parser output passes production ledger validation;
3. public hygiene checks pass;
4. metric-readiness gates pass where relevant;
5. maintainer separately authorizes promotion to a production retained evidence ledger.

## Failure Behavior

The parser must fail closed or mark rows unresolved when:

- source row grain is ambiguous;
- route identity is ambiguous;
- engine mapping is ambiguous;
- candidate ID cannot be made stable;
- a source is route-level summary only;
- a retained path is not public-safe;
- timing fields appear in the non-timing parser input;
- any output attempts to set `metric_input_authorized=true`.

## Recommended Implementation Phases

1. Parser design review and input manifest approval.
2. Non-timing parser implementation for one method route with row-grain fixtures.
3. Extend to remaining four routes after route-specific risk gates pass.
4. Validate all 600 candidate rows with the production ledger validator.
5. Defer timing, metrics, paper rendering, and production ledger promotion to separate approvals.
