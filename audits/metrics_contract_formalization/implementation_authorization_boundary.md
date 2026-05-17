# Implementation Authorization Boundary

Date: 2026-05-17

## Formalized But Not Implemented

Metrics Contract v1 is formalized in `repository_spec/metrics_contract_v1.md`.

This does not authorize implementation.

## Still Not Authorized

- Metrics computation.
- Retained-evidence adapter implementation.
- Unified reproduction CLI implementation.
- Public runner implementation.
- Paper table rendering.
- Reports/results migration.
- DB validation.
- Evidence regeneration.
- Timing reruns.
- Denominator updates.
- Paper-result updates.
- Case membership changes.
- Case package modification.
- Raw legacy evidence modification.

## Required Before Implementation

- Approved evidence ledger materialization plan.
- Adapter row-grain tests and denominator join validation.
- Public output-root policy finalization.
- Attribution schema and attribution denominator approval.
- Timing eligibility and paired timing handling tests.
- Public hygiene policy for generated reports/results.
- Explicit maintainer authorization for metrics computation and paper/report rendering.

## No-global-leaderboard Boundary

No future implementation may collapse incompatible methods, engines, routes, controls, portability rows, verifier support, plan artifacts, or user submissions into a global leaderboard.

All reports must state denominator, eligibility gates, N.A. policy, and diagnostic exclusions.
