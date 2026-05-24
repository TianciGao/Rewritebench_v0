# Guard Policy

Known unsupported or unstable SQLSolver families should be classified before SQLSolver invocation.

Quoted identifier plus `NULLS FIRST` / `NULLS LAST` ordering is currently scoped out of SQLSolver support and reported through `support_scope_verdict=no_verifier_support` with normalized verifier verdict `unsupported`.

`DENSE_RANK` / CTE ranking / window-over-CTE shapes are currently scoped out of SQLSolver support and reported through `support_scope_verdict=no_verifier_support` with normalized verifier verdict `unsupported`.

The fail-closed guard does not mean the rewrite method failed. It records a verifier-support boundary.

Guard output is verifier-support boundary evidence only. It is not SER evidence, not a paper result, not retained evidence, and not leaderboard input.
