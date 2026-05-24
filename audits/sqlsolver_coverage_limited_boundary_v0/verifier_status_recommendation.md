# Verifier Status Recommendation

## Current SQLSolver status for release v0

SQLSolver should be reported as `coverage_limited verifier support`.

- `official_SER=false`
- Route/scope SER status should be `coverage_limited` when bounded verifier-support evidence is shown.
- Route/scope SER status should be `N.A.` when no formal verifier evidence is included for that output context.

## User-facing wording

Recommended diagnostic summary wording:

`SQLSolver verifier support is coverage-limited. Bounded checks found 2/2 attempted actual pairs equivalent after identity guards, while 3/8 selected pairs were outside current verifier support and 3/8 still had identity-guard blockers. No official SER is computed.`

## Future paper/report boundary wording

Recommended paper/report boundary wording:

`SQLSolver was evaluated as coverage-limited verifier support only. Non-decidable and no-verifier-support rows are reported separately and excluded from the decidable verifier denominator. The bounded support ratio is not an official Semantic Equivalence Rate.`

No broader SQLSolver pass should run until residual blockers are solved or explicitly scoped out in a separately authorized task.
