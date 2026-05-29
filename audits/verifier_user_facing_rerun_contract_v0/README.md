# verifier_user_facing_rerun_contract_v0

Verdict: contract defined as design/audit only.

This packet defines the future user-facing verifier rerun contract for SQLSolver and VeriEQL. It does not promote existing diagnostics, run new verifier rows, compute official Semantic Equivalence Rate, update paper reports/results, or promote retained evidence.

Current readiness:

- VeriEQL is integrated but coverage-limited after identity guard: 4 corrected decidable rows out of 35 exact SQLGlot-noop PostgreSQL rows.
- SQLSolver is stronger on the same exact subset: 24 corrected decidable rows out of 35 exact rows.
- Both result lines are local diagnostic support evidence only.

Required future rerun principle:

Future paper-facing or release-facing verifier evidence must be rerun through the user-facing output path under D035:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

Current audit diagnostics under `/tmp` and `audits/` must not be promoted directly.
