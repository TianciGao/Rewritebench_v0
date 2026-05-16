# Metrics Contract Patch Notes

This file explains the changes made to `repository_spec/metrics_contract_v1_draft.md`.

## Updated Structure

The draft now uses the maintainer-provided updated paper metric layers:

- Coverage
- Correctness
- Performance
- Explainability
- Generalization

## Added Or Clarified Metrics

- Added `Generation Rate` as candidate SQL generation only.
- Added `Execution Coverage Rate`.
- Added `Result Consistency Rate`.
- Added `Semantic Equivalence Rate`, with verifier decidability caveats.
- Retained `GM_Speedup`.
- Added `Speedup Ratio Percentiles`.
- Added `Attribution Coverage`, with implementation deferred.
- Added `Cross-Engine Execution`.
- Added `Cross-Engine Consistency`.
- Added `Speedup Retention`, with paired timing and `N.A.` caveats.

## Removed Or Demoted From Primary Status

- `Candidate Failure Rate` is not primary; failure buckets are diagnostic.
- `Regression@20` is not primary; it may be diagnostic or a legacy comparator only.
- Extraction/readiness variants are not primary Generation Rate variants.
- PlanFrontier/observability are folded into explainability via Attribution Coverage.
- Support Layer is removed as an independent layer; verifier evidence is folded into correctness.

## Preserved Boundaries

- Metrics implementation remains unauthorized.
- Retained-evidence adapters remain unauthorized.
- Reproduction CLI and public runner implementation remain unauthorized.
- Paper table rendering remains unauthorized.
- Common-core 40 and Track A 120 planned rows are unchanged.
- No global leaderboard is allowed.

## Known Follow-up Work

- Approve the aligned draft or produce a final contract.
- Define attribution schema and denominator.
- Define Speedup Retention pairing keys and `N.A.` policy.
- Define semantic-equivalence verifier coverage policy.
- Implement adapters only after approval.
- Render paper/public tables only after separate approval.
