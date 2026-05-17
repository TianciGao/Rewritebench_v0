# Official Status Metrics Readiness Gate v0

## Purpose And Scope

This readiness gate reviews the current audit-only candidate-status evidence after SQLGlot projection/parser v1 and normalized status-only dry-run v4. It decides whether a separately authorized official status-only metrics implementation task is structurally safe.

No official metrics were computed. No metric values were changed. No paper tables were rendered. No reports/results, denominator, paper results, case membership, or raw legacy evidence were changed.

## Current Evidence State

- Candidate status parser v1 filled 175 non-timing rows.
- Overlap priority overlay v1 resolved 45 overlap rows and produced 175 currently authorized non-SQLGlot status rows.
- SQLGlot sanitized non-timing parser v1 filled 137 SQLGlot rows and left 103 SQLGlot rows unresolved.
- Combined candidate status overlay v2 has 312 filled rows and 288 unresolved rows across 600 planned candidate rows.
- Status inference overlay v0 has 94 audit-only inferred_generated rows; observed fields were not overwritten.
- Normalized status-only dry-run v4 is audit-only, non-paper, and non-official.

## v4 Dry-Run Evidence Summary

- Dry-run input rows: 312.
- SQLGlot projection input rows: 137.
- Inferred generated rows used in audit dry-run: 94.
- SQLGlot rows filled: 137.
- SQLGlot rows unresolved: 103.

These are readiness counts and audit dry-run facts only; they are not official metric values.

## Readiness Decision Per Metric

- Generation Rate: `blocked_needs_policy_decision`. Observed generated evidence is limited, inferred_generated is audit-only and not official-authorized, and SQLGlot/Calcite generated-ready status remains absent.
- Execution Coverage Rate: `ready_with_caveats`. Observed execution evidence exists, especially from SQLGlot, but official implementation must preserve unresolved rows and must not infer execution from exactness.
- Result Consistency Rate: `ready_with_caveats`. Observed exact/checker evidence exists, especially from SQLGlot, but official implementation must use Metrics Contract v1 denominator semantics and must keep planned-denominator coverage visible.

## Denominator Handling Requirements

- Track A same-engine planned denominator remains 120 planned case-engine rows per method route and 600 planned candidate rows across five methods.
- The 288 unresolved rows must remain visible in denominator/accounting outputs.
- Filled or authorized rows must not replace the planned denominator.
- No denominator reduction is allowed.
- No global leaderboard is allowed.

## Unresolved-Row Handling Requirements

Unresolved, unknown, not-applicable, and not-authorized rows must be represented explicitly. They must not be silently dropped, coerced to false, or treated as method-quality failures without an approved policy.

## Official Implementation Blockers

- Generation Rate requires a policy decision on whether R1 inferred_generated can be official metric input.
- SQLGlot generated/ready evidence is missing for all SQLGlot rows.
- Direct Repair-1 has 94 unresolved rows and no observed execution/exact status.
- Calcite has generated/ready unknown and 91 unresolved rows.
- SQLGlot has 103 unresolved rows after SGL011 projection/parser v1.
- Result Consistency official implementation must align with Metrics Contract v1 executed-denominator semantics, not simply copy v4 dry-run planned-denominator tables.

## Recommended Next Action

Do not compute official status metrics yet. First obtain a maintainer decision on inferred_generated official eligibility and partial-coverage acceptance. If the team wants a narrower path, authorize a scoped official implementation only for observed Execution Coverage and observed Result Consistency with strict denominator visibility and no paper rendering; otherwise complete more non-timing status evidence first.
