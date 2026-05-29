# user_cli_facade_phase2b_review_v0

Verdict: completed_with_hardening.

This packet reviews and hardens the Phase 2B user-facing CLI facade added in `user_cli_facade_phase2b_v0`.

Review result:

- All implemented `sqlrb user ...` commands were reviewed.
- Help text now carries a shared local-only boundary across command-level help.
- `--verifier verieql` and `--verifier sqlsolver` fail closed before evaluation and state that Semantic Equivalence Rate remains `N.A.` without verifier evidence.
- `evaluate` and `compute-local-metrics` validate D035 output roots before invoking the internal runner or metrics calculator.
- D035 output roots remain `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
- Top-level `reports/` and `results/` remain protected.
- No leaderboard/ranking/winner command exists.

Bounded smoke:

- Route: SQLGlot noop.
- Engine: PostgreSQL only.
- Cases: `PERF_0006`, `CONS_0005`.
- Result: selected/generated/source-executable/candidate-executable/checker/exact/mismatch = `2/2/2/2/2/2/0`.
- Timing: disabled.
- Verifier: disabled.
- Runtime outputs were cleaned up and not committed.

Metadata correction:

- The prior `user_cli_facade_phase2b_v0` run-log entry still recorded commit/push as pending.
- Final commit for that task was `5344770`.
- Push result was pushed to `origin/feature/case-package-v2-external-schema`.

Boundary: local diagnostic review/hardening only. No VeriEQL/SQLSolver implementation, no full Common-core run, no official metrics, no timing, no reports/results update, no retained-evidence promotion, and no leaderboard output.
