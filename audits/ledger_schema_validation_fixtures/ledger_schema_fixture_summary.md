# Ledger Schema Fixture Summary

Date: 2026-05-17

## Purpose And Scope

This task creates a draft ledger column schema, validation rules, fixture policy, and synthetic validation fixtures for all evidence ledger record types.

No production retained evidence was parsed. The 3,439 retained-evidence candidate rows were not loaded into a production ledger. No retained-evidence adapter was implemented. No metrics were computed. No scripts or source package files were created. No reports/results were copied or modified. No denominator values, paper results, case membership, case packages, or raw legacy evidence were changed.

## Fixture Record Types Included

The combined fixture table includes:

- `control_cell`
- `rewrite_candidate_cell`
- `plan_observability_artifact`
- `portability_candidate_cell`
- `verifier_support_pair`
- `retained_summary_artifact`
- `user_run_candidate_cell`

The table includes valid synthetic rows and intentionally invalid rows.

## Validation Expectations

The fixture set tests:

- common required fields;
- record-type-specific required fields;
- forbidden fields;
- denominator ID usage;
- same-engine denominator joins;
- control scaffold joins;
- support-only row boundaries;
- unsupported and N.A. status representation;
- no-global-leaderboard boundaries;
- no-metric-computation boundaries.

## Next Safe Action

Review the schema and fixture drafts. The next safe implementation-adjacent task is a non-mutating validator design or test plan that reads these synthetic fixtures only, without parsing production retained evidence or computing metrics.
