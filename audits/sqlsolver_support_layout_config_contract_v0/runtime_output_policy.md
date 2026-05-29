# Runtime Output Policy

Runtime output policy:

- Audit probes write generated SQLSolver files under task-specific `/tmp/...` directories.
- User-facing verifier output uses D035 paths:
  - `output/results/<run_id>/verifier/`
  - `output/logs/<run_id>/verifier.log`
  - `output/reports/<run_id>/verifier_summary.md`
- SQLSolver support must not write runtime files into `runs/user/`, top-level `reports/`, top-level `results/`, retained evidence, or repository-level `output/` outside an explicit local user output root.

The wrapper writes through caller-provided `output_root` and the existing verifier output contract. Tests use temporary directories and assert the expected `output/results`, `output/logs`, and `output/reports` layout.

The all-exact SQLSolver diagnostic runtime files were written under `/tmp/sqlrb_sqlsolver_pg_noop_all_exact_identity_guard_pass_v0/` and were not committed.
