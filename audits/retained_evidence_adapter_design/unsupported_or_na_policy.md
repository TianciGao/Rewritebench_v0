# Unsupported And N.A. Policy

Date: 2026-05-17

## Purpose

Define explicit statuses for future retained-evidence adapter output. Adapters must not silently drop missing, unsupported, unknown, or non-applicable evidence.

## Status Values

### `unsupported`

Use when a method, engine, case, verifier, or route is outside the supported scope for the evidence source.

Example: a target engine is not supported for a portability packet.

### `not_applicable`

Use when a field does not apply to a record type or route.

Example: `speedup` on `control_cell` rows.

### `unknown`

Use when the artifact may contain a value but the adapter cannot determine it safely.

Example: a mixed-scope report does not expose engine-specific execution status.

### `verifier_unknown`

Use when verifier support is absent, undecidable, unsupported, or not retained for a result-consistent candidate.

This is reported separately from Semantic Equivalence Rate.

### `timing_missing`

Use when execution or correctness evidence exists but usable timing evidence is absent.

Timing missing must not be converted to zero latency or zero speedup.

### `target_timing_missing`

Use when source-engine timing exists but paired target-engine timing needed for Speedup Retention is absent.

Speedup Retention should render as `N.A.` for these pairs unless a later approved policy says otherwise.

### `evidence_not_retained`

Use when an expected artifact was not retained or was not selected for public retention.

This differs from execution failure or correctness failure.

### `manual_review_required`

Use when row grain, public hygiene, denominator linkage, or evidence role cannot be determined safely.

Adapters should preserve the reference and avoid metric eligibility.

### `blocked`

Use when an adapter intentionally refuses to emit a metric-eligible row because required policy or authorization is missing.

Example: timing rows before timing eligibility validation is approved.

## N.A. Rendering Policy

Future reports should render `N.A.` when:

- no approved denominator exists for the metric scope;
- the record type is support-only;
- the route is outside the metric contract;
- verifier decidability is absent for Semantic Equivalence Rate;
- paired target timing is absent for Speedup Retention;
- attribution denominator or schema is not approved;
- public-safe evidence is unavailable.

`N.A.` is not a failure and is not zero.

## Ledger Representation

Adapters should populate:

- `result_status` for broad outcome;
- `failure_stage` for stage-specific failure or missingness;
- `failure_type` for stable failure buckets;
- `notes` for caveats and review status;
- null values only where the status field explains why a value is absent.

## Reporting Boundary

Future metrics may exclude unsupported or not-applicable rows from denominators only according to Metrics Contract v1 and later approved renderer rules. The adapter layer should preserve these rows for auditability.
