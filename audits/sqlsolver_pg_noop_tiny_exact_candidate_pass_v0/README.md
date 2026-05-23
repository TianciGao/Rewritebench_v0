# sqlsolver_pg_noop_tiny_exact_candidate_pass_v0

Verdict: completed as local verifier-support diagnostics.

Source run: `runs/user/common_core_pg_noop_db_checker`.

Selected rows:

- `CONS_0036`
- `CONS_0037`
- `LONGTAIL_0023`
- `PORT_0003`
- `PORT_0005`

All five rows passed the exact/result-consistency gate before SQLSolver execution. SQLSolver then ran three logical pair checks for each exact row:

- source-vs-source
- candidate-vs-candidate
- source-vs-candidate

Runtime files were written only under `/tmp/sqlrb_sqlsolver_pg_noop_tiny_exact_candidate_pass_v0/`.

Summary:

- Selected rows: 5.
- Exact candidate rows: 5.
- Verifier attempted rows: 5.
- Verifier attempted pairs: 15.
- Identity passed rows: 3.
- Identity failed rows: 2.
- Corrected equivalent rows: 3.
- Corrected non-equivalent rows: 0.
- Corrected decidable rows: 3.
- Corrected local SQLSolver tiny SER: 1.0 over 3 corrected decidable rows.
- Corrected SQLSolver decidability rate: 3/5.

This is not official Semantic Equivalence Rate, not paper evidence, not retained evidence, and not leaderboard input.
