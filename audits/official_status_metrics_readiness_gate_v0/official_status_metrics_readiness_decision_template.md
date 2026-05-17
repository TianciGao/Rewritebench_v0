# Official Status Metrics Readiness Decision Template

## Decision Choices

- [ ] Approve official status-only metrics implementation with caveats.
- [ ] Approve another audit-only dry-run only.
- [ ] Defer until unresolved rows are reduced.
- [ ] Defer until SQLGlot generated/ready evidence is improved.
- [ ] Reject official computation for now.

## Required Maintainer Notes

- May R1 inferred_generated be used as official metric input for Generation Rate?
- Should official Generation Rate be deferred until SQLGlot generated/ready evidence improves?
- Are Execution Coverage and Result Consistency acceptable for official implementation with partial evidence and explicit denominator visibility?
- Should SQLGlot parsed rows from overlay v2 receive formal metric-input authorization before official implementation?
- What output directory and labeling should a future official implementation use?

## Boundary Confirmation

- Paper table rendering remains separate.
- Timing/performance metrics remain separate.
- Reports/results updates remain separate.
- Denominator changes are not allowed.
- No global leaderboard is allowed.
