# Ledger Schema Validation Plan

Date: 2026-05-17

## Purpose

Define a future non-mutating validation flow for synthetic ledger fixtures and later production ledgers.

This plan does not implement validators or adapters.

## Stage 1: Schema Load

- Load `repository_spec/evidence_ledger_column_schema_v1_draft.md`.
- Load allowed record types and status values.
- Confirm required columns exist in fixture or production ledger input.

## Stage 2: Fixture Validation

- Load `fixture_all_record_types.csv`.
- Confirm every row has `fixture_only=true`.
- Confirm every row has `evidence_source=synthetic_fixture`.
- Confirm every row has `not_paper_evidence=true`.
- Confirm no fixture row is treated as retained evidence or paper evidence.

## Stage 3: Record-type Rule Validation

- Apply common required-field rules.
- Apply record-type-specific required-field rules.
- Apply record-type-specific forbidden-field rules.
- Validate stable identity fields such as `record_id`, `candidate_id`, `artifact_id`, and `support_pair_id`.

## Stage 4: Denominator Join Validation

- Check `control_cell` denominator IDs against `controls_360.csv`.
- Check same-engine `rewrite_candidate_cell` rows against `denominator_same_engine_120.csv`.
- Check benchmark-scoped `user_run_candidate_cell` rows against `denominator_same_engine_120.csv`.
- Check support-only rows do not use Track A denominator IDs.
- Check portability rows do not reuse Track A denominator IDs by default.

## Stage 5: N.A. And Unsupported Policy Validation

- Validate `na_reason` exists when `status=N.A.`.
- Validate `timing_missing` rows do not carry zero-filled timing.
- Validate `target_timing_missing` applies only to portability rows.
- Validate `verifier_unknown` applies only to verifier or semantic support rows.
- Validate `manual_review_required` rows are not metric eligible.

## Stage 6: No-global-leaderboard Guard

- Reject rows or summaries that collapse record types into a global rank.
- Reject mixed control/candidate/support rows presented as one comparable metric denominator.
- Require all future aggregates to retain denominator and method context.

## Stage 7: No-metric-computation Guard

- Reject aggregate metric columns or rows in fixture validation.
- Reject computed metric names such as Generation Rate, GM_Speedup, or Speedup Retention in adapter output.
- Allow only row-level evidence fields before metrics implementation is authorized.

## Stage 8: Public Hygiene Guard

Future materialized ledgers should scan public output paths for:

- absolute local paths;
- raw stdout/stderr traces;
- WSL or host-specific paths;
- localhost or private endpoints;
- API keys or tokens;
- prompt/model traces;
- unsanitized raw logs.

## Stage 9: Future Production Ledger Validation

Production validation must run only after retained-evidence adapter implementation is separately authorized. Production validation should read adapter outputs, not legacy reports/results directly, and must remain non-mutating unless a later task explicitly authorizes output generation.

## Failure Behavior

Validators should fail closed for identity errors, forbidden fields, denominator mismatches, unsafe paths, or metric aggregates. Warnings are acceptable only for nullable support fields when explicit `status`, `na_reason`, and `notes` explain the missingness.
