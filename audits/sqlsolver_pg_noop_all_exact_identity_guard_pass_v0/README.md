# sqlsolver_pg_noop_all_exact_identity_guard_pass_v0

Verdict: completed as local verifier-support diagnostics.

Source run: `runs/user/common_core_pg_noop_db_checker`.

Scope:

- Method/route: SQLGlot noop / `noop`.
- Engine: PostgreSQL.
- Selected rows: 40.
- Exact/result-consistent rows: 35.
- Non-exact ineligible rows: 5.
- SQLSolver logical pairs run: 105, three for each exact row.

Identity sanity checks were run for every exact row:

- source-vs-source
- candidate-vs-candidate
- source-vs-candidate

Corrected summary:

- Identity checked rows: 35.
- Identity passed rows: 24.
- Identity failed rows: 11.
- Corrected equivalent rows: 24.
- Corrected non-equivalent rows: 0.
- Corrected decidable rows: 24.
- Corrected local SQLSolver PG noop SER: 1.0 over 24 corrected decidable rows.
- Corrected decidable coverage over exact rows: 24/35.

This is not official Semantic Equivalence Rate, not paper evidence, not retained evidence, and not leaderboard input.
