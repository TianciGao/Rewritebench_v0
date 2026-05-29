# Implementation Summary

Implemented `src/sql_rewrite_bench/verifier_support/sqlsolver.py`.

The wrapper provides:

- SQLSolver command detection from explicit command, `SQLRB_SQLSOLVER_CMD`, `SQLSOLVER_COMMAND`, `SQLSOLVER_BIN`, or likely PATH command names.
- Fail-closed unavailable handling with `not_attempted` verdict rows.
- Bounded pair invocation when a SQLSolver command is explicitly available.
- SQLSolver-like output normalization into the shared verifier vocabulary.
- D035 verifier output writing under `output/results/<run_id>/verifier/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/` when called with an output root.
- Local-only boundary flags on summary and verdict artifacts.

The public `sqlrb user evaluate --verifier sqlsolver` path remains fail-closed. Broad user-facing verifier execution was not implemented.

VeriEQL code was not changed or run.
