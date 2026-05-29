# Implementation Summary

Updated `src/cli/main.py` to add `sqlrb user verify`.

Implemented behavior:

- Adds `user verify` parser with `--run-id`, `--tool`, `--output-root`, `--tool-cmd`, `--timeout`, and `--pair-scope`.
- Supports only `--pair-scope synthetic-smoke` in this phase.
- Writes synthetic SQL pair files under the verifier tool directory before invoking the existing wrapper.
- Delegates VeriEQL output handling to `write_verieql_canary`.
- Delegates SQLSolver output handling to `write_sqlsolver_smoke`.
- Preserves `sqlrb user evaluate --verifier ...` fail-closed behavior.
- Uses `build_output_paths` so protected top-level `reports/` and `results/` output roots are rejected before verifier artifacts are written.

No verifier adapter logic was broadened beyond the existing wrappers.
