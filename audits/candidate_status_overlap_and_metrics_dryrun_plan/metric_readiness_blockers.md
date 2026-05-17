# Metric Readiness Blockers

Before any status-only metrics dry run can be implemented, these blockers remain:

- Only 130 rows are currently authorized for status-only metric input.
- 45 overlap rows are blocked by source-overlap review.
- 425 unresolved rows are blocked by missing approved row-level status evidence.
- SQLGlot optimize has zero filled rows.
- SQLGlot no-op has zero filled rows.
- Timing fields are absent and unauthorized.
- A metric computation script is not implemented or authorized.
- Production ledger promotion is not done.
- Paper renderer is not authorized.
- Reports/results updates are not authorized.
- Denominator and paper-result changes are not authorized.
