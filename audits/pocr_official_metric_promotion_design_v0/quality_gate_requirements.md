# Quality Gate Requirements

No official freeze occurs until the promotion gates are reviewed.

Required gates:

- Route mismatch rows must be zero, or fail-closed and manually reviewed.
- Candidate mismatch rows must be zero, or fail-closed and manually reviewed.
- Schema-valid and fail-closed rows must all be accounted for.
- No-op possible over-accept must be zero or fully justified by manual review.
- Provider failures after retry must be retained explicitly.
- SQLGlot optimize missing candidates must remain missing/fail-closed unless true optimize candidates are generated or found.
- Candidate SHA, route, method, engine, case, and skills-contract bindings must be stable.

Manual review is required for:

- No-op routes with transformation-supported operation atoms.
- High POCR rows that are non-exact in the correctness layer.
- Exact rows with unexpectedly low POCR.
- Malformed, timeout, or provider-failed rows after retry.
- Stage B under-accept concentration by pool, case family, or atom type.

Stage A annotation alone is not counted. Stage B transformation-aware validation is required. Semantic guard atoms are excluded from the operation coverage numerator and denominator.

No route-level POCR score is emitted in this task. No paper-facing metric is promoted in this task. No global leaderboard is produced.
