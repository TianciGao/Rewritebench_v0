# Blocked Family Boundary

Quoted identifier / NULL ordering remains outside current SQLSolver support.

DENSE_RANK / CTE ranking remains outside current SQLSolver support.

These families should be reported as `support_scope_verdict=no_verifier_support` with normalized verifier verdict `unsupported` in SQLSolver summaries and row metadata.

They must be excluded from the decidable SER denominator and reported separately.

They must not be counted as rewrite-method failures, checker failures, paper results, retained evidence, or leaderboard inputs.
