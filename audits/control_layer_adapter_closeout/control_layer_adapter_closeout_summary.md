# Control-layer Adapter Closeout

## Purpose And Scope

This closeout reviews the existing Common-core control-layer ledger-style adapter outputs before any method-candidate adapter work. It verifies generic control scaffold coverage, source/positive detail coverage, hard-negative detail coverage, route-level join consistency, and validator status.

This task did not implement a new adapter, parse production retained evidence, read the legacy repo, compute metrics, compute false-accept rate, compute source-positive rate, compute Result Consistency Rate, migrate reports/results, change denominators, or update paper results.

## Components Reviewed

| Component | Expected rows | Actual rows | Routes | Validation |
|---|---:|---:|---|---|
| `control_cell_adapter_v0` | 360 | 360 | source; positive; hard_negative | passed |
| `source_positive_control_detail_adapter_v0` | 240 | 240 | source; positive | passed |
| `hard_negative_control_detail_adapter_v0` | 120 | 120 | hard_negative | passed |

## Coverage Summary

- Generic control-cell coverage is complete: 360/360 rows.
- Source/positive detail coverage is complete: 240/240 rows.
- Hard-negative detail coverage is complete: 120/120 rows.
- Combined detail coverage is complete: 360/360 rows.
- Source route coverage: generic 120/120, detail 120/120.
- Positive route coverage: generic 120/120, detail 120/120.
- Hard-negative route coverage: generic 120/120, detail 120/120.

## Join And Consistency Summary

The generic control ledger and the combined detail ledgers cover the same `(case_id, engine, control_route)` key universe as `case_sets/common_core_v0/controls_360.csv`. No route group has missing or extra rows.

The detail layer is split by route-specific adapter scope: source/positive detail rows cover source and positive controls, while hard-negative detail rows cover hard-negative controls. Together they reconstruct the full 360-row control scaffold.

## Validator Summary

All adapter ledger validations passed:

- `control_cell_adapter_v0`: 360 rows checked, 0 errors, 0 warnings.
- `source_positive_control_detail_adapter_v0`: 240 rows checked, 0 errors, 0 warnings.
- `hard_negative_control_detail_adapter_v0`: 120 rows checked, 0 errors, 0 warnings.

The synthetic fixture smoke remains passing with 38 fixture rows checked, 17 expected-valid rows passed, 21 expected-invalid rows failed as expected, and zero unexpected pass/fail rows.

## Evidence-index Caveats

- Generic control rows include 95 rows without direct retained artifact paths in the generic scaffold view; route-specific detail outputs provide more precise evidence-index status.
- Source/positive detail rows include 179 `indexed_not_recomputed` rows and 61 `evidence_not_retained` rows.
- Hard-negative detail rows include 97 `indexed_not_recomputed` rows and 23 `evidence_not_retained` rows.

These caveats do not block this coverage closeout because no scaffold rows are missing. They do block metrics/report consumption until separately authorized retained-evidence parsing, outcome validation, and metric computation exist.

## Hard-negative Approval Caveats

Hard-negative expected-rejection approval status remains mixed:

- `maintainer_approved_for_migration`: 45 rows.
- `migration_planning_static_inference_needs_review_if_not_explicit_in_legacy`: 72 rows.
- `manual_review_required`: 3 rows.

These approval states are visible and non-blocking for control-layer scaffold closeout, but they must be resolved before hard-negative metrics or paper-facing claims.

## Remaining Blockers Before Candidate Adapters

- Candidate adapter scope must be authorized separately; this closeout does not authorize implementation.
- Production retained-evidence parsing remains unauthorized.
- Metrics computation remains unauthorized.
- Candidate rows must preserve Track A denominator boundaries and must not mix controls with rewrite-method rows.
- Evidence-index gaps and hard-negative approval caveats remain blockers for metric consumption.

## Next Safe Action

Begin `rewrite_candidate_adapter_v0` planning only, or request explicit maintainer authorization for a bounded candidate adapter. Do not compute metrics, parse legacy/raw retained evidence, render paper tables, update reports/results, change denominators, or modify raw legacy evidence without separate approval.
