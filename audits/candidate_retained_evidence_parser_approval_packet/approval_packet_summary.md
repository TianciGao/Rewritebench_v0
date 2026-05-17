# Candidate Retained-evidence Parser Approval Packet

Date: 2026-05-17

## Purpose And Scope

This approval packet reviews the unresolved `candidate_status_adapter_v0` overlay and prepares a bounded approval decision for a future candidate retained-evidence parser. It is audit/design work only.

This task did not implement a parser, parse production retained evidence, read the legacy repository, fill candidate row statuses, fill timing fields, authorize metric input, compute metrics, update reports/results, change denominator values, change paper results, change case membership, or modify raw legacy evidence.

## What Was Reviewed

- `audits/candidate_status_adapter_v0/`
- `audits/rewrite_candidate_input_surface_audit/`
- `audits/rewrite_candidate_adapter_v0/`
- `repository_spec/retained_evidence_adapter_design_v1_draft.md`
- `repository_spec/evidence_ledger_column_schema_v1_draft.md`
- `repository_spec/evidence_ledger_validation_rules_v1_draft.md`
- `repository_spec/production_ledger_validation_policy_v1_draft.md`
- `repository_spec/metrics_contract_v1.md`
- Project-control files under `project_control/`

## Current Overlay Finding

`candidate_status_adapter_v0` emitted 600 `rewrite_candidate_cell` rows, one for each Track-A same-engine scaffold row across five method routes.

- Row-level status rows filled: 0.
- Unresolved status rows: 600.
- Route-level summary-only rows: 600.
- Current `result_status`: `evidence_not_adapted_yet`.
- Current `metric_input_authorized`: `false`.
- Ledger validation: passed, 600 rows checked, 0 errors, 0 warnings.

## Why The Overlay Remains Unresolved

The release-repo audit metadata contains route-level or group-level retained-evidence references, but it does not provide trusted row-grain evidence for each exact `case_id x engine x rewrite_method` row. The input-use log also confirms that no legacy paths were opened and no production retained evidence was parsed.

The overlay therefore correctly refused to distribute route-level counts or paper summary statements into row-level statuses.

## What Can Be Safely Parsed Next

A future bounded parser can be considered only for non-timing candidate status fields and only after explicit maintainer authorization. It should parse selected retained-evidence source groups only when they provide exact row grain:

`case_id x engine x rewrite_method x candidate_id x denominator_id`

Potential non-timing fields for a future parser:

- `generated`
- `ready`
- `executed`
- `exact`
- `result_status`
- `failure_stage`
- `failure_type`
- `parse_status`
- `checker_status`
- `retained_artifact_path`
- `evidence_source`
- `notes`

## What Cannot Be Safely Parsed In That Scope

The next non-timing parser must not parse or fill:

- `timed`
- `latency_ms`
- `speedup_ratio`
- `timing_eligible`
- plan/attribution fields
- portability rows
- verifier support rows
- metric aggregates
- paper-rendering outputs
- `metric_input_authorized=true`

## Explicit Authorization Boundary

This packet does not authorize implementation. A future approval must explicitly choose whether to authorize design only, implementation of a bounded non-timing parser, deferral, or rejection.

Even if implementation is approved later, the future parser must:

- remain non-mutating;
- not modify legacy/raw evidence;
- not mutate reports/results;
- not update denominators or paper results;
- not compute any metric;
- keep `metric_input_authorized=false` unless a later task explicitly changes that;
- fail closed when row grain is ambiguous;
- preserve route identity and no-global-leaderboard boundaries.

## Recommended Approval Path

Approve implementation only if the maintainer accepts a narrow parser scope:

- input manifest limited to explicit retained-evidence source groups;
- output remains an audit ledger under `audits/`, not `results/retained`;
- only non-timing candidate status fields may be filled;
- row-grain proof is required before a field is populated;
- production ledger validation must pass before any downstream use.

## Next Safe Action

Maintainer should review `approval_decision_template.md` and choose one of the four decisions. The safest next technical step is design approval or a tightly bounded implementation authorization for a non-timing candidate retained-evidence parser. Do not authorize timing parsing, metric input, metrics computation, paper rendering, or production ledger promotion in the same step.
