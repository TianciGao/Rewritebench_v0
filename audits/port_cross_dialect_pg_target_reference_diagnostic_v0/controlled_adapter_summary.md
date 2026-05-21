# Controlled Adapter Summary

Adapter path: `examples/user/port_postgres_target_reference_adapter.py`.

Purpose: validate the cross-dialect local diagnostic chain with controlled target-side PostgreSQL SQL. This adapter is not a user method, not a benchmark baseline, and not a paper-result input.

Behavior:

- Reads `SQLRB_CASE_DIR` from the runner environment.
- Reads `SQLRB_CANDIDATE_SQL_PATH` from the runner environment.
- Reads `manifest.yaml` from the case directory.
- Requires `local_diagnostic.diagnostic_mode == cross_dialect_reference`.
- Requires `local_diagnostic.target_reference.role == positive_reference`.
- Requires `local_diagnostic.target_reference.engine == postgres`.
- Requires `local_diagnostic.target_reference.use_for_checker_oracle == false`.
- Copies only `local_diagnostic.target_reference.query` to the candidate path.
- Does not guess `pos_01.sql` by filename.
- Does not execute SQL.
- Does not compute metrics, timing, speedup, reports/results, or leaderboard outputs.
- Fails closed with a nonzero exit if metadata is missing or malformed.

Validation:

- `PYTHONPATH=src python -m py_compile examples/user/port_postgres_target_reference_adapter.py`: passed.
- `PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry/test_port_target_reference_adapter.py`: passed, 3 tests.
- `PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry`: passed, 82 passed and 2 skipped after installing `pytest` and `PyYAML` in a temporary `/tmp` virtualenv.
