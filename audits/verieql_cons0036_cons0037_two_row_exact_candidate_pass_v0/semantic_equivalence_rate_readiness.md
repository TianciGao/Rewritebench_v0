# Semantic Equivalence Rate Readiness

Local diagnostic summary:
- `local_two_row_semantic_equivalence_rate = 1.0`
- Computed over `decidable_count = 1`.
- Formula: `equivalent_count / (equivalent_count + non_equivalent_count)`.
- Counts used: `1 / (1 + 0)`.

Verifier decidability:
- `verifier_decidability_rate = 0.5`
- Formula: `decidable_count / verifier_attempted_rows`.
- Counts used: `1 / 2`.

Verifier eligibility:
- `verifier_eligibility_rate = 1.0`
- Formula: `verifier_attempted_rows / exact_candidate_rows`.
- Counts used: `2 / 2`.

Boundary:
- This is a local two-row diagnostic readiness signal only.
- It is not official Semantic Equivalence Rate.
- It is not paper evidence.
- It is not retained evidence.
- It is not leaderboard input.
- Local checker exactness was not substituted for formal verifier evidence.

Readiness conclusion:
- The end-to-end source-vs-candidate VeriEQL path remains working for the positive-control row `CONS_0036`.
- `CONS_0037` confirms the DDL parser blocker is resolved, but introduces a timeout blocker at the current bound and timeout.
- A bounded feature-aware one-baseline exact-candidate subset pass is reasonable only if it remains small, local-only, and timeout-aware.
- A full Common-core exact-candidate verifier pass remains blocked.

