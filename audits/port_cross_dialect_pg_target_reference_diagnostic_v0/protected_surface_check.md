# Protected Surface Check

Status: passed.

Expected mutation boundary:

- Allowed controlled adapter: `examples/user/port_postgres_target_reference_adapter.py`.
- Allowed lightweight tests: `tests/user_entry/test_port_target_reference_adapter.py`.
- Allowed audit packet: `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/`.
- Allowed project control updates: `project_control/MIGRATION_STATUS.md` and `project_control/MIGRATION_RUN_LOG.md`.
- Local run outputs: `runs/user/port_pg_target_reference_controlled/`, ignored and not staged.

Protected surfaces that must remain unchanged:

- source code under `src/`
- scripts
- docs
- cases
- manifests
- SQL files
- schema files
- checker files
- validation files
- `case_sets/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- raw retained evidence
- `.github/workflows/`
- release tags or branches

## Observed Local Output Boundary

- `runs/user/port_pg_target_reference_controlled/` exists as local diagnostic
  output.
- `runs/user/port_pg_target_reference_controlled/` is ignored by
  `runs/.gitignore`.
- `git ls-files runs/user/port_pg_target_reference_controlled` returned no
  tracked files.
- Local run outputs were not staged.

## Diff Boundary

Only these repository surfaces were intentionally changed:

- `examples/user/port_postgres_target_reference_adapter.py`
- `tests/user_entry/test_port_target_reference_adapter.py`
- `audits/port_cross_dialect_pg_target_reference_diagnostic_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

No changes were made to source code under `src/`, scripts, docs, cases,
manifests, SQL files, schema files, checker files, validation files,
`case_sets/`, `reports/`, `results/`, `benchmark_spec/`, `repository_spec/`,
raw retained evidence, `.github/workflows/`, release tags, or release branches.

## Validation

- `git diff --check`: passed.
- `PYTHONPATH=src python -m py_compile examples/user/port_postgres_target_reference_adapter.py`: passed.
- `PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry/test_port_target_reference_adapter.py`: passed, 3 tests.
- `PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry`: passed, 82 passed and 2 skipped after installing `pytest` and `PyYAML` in a temporary `/tmp` virtualenv.
- JSON parse check for `live_run_summary.json`: passed.
- CSV parse checks for audit CSV files: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface diff check: passed.
- Staged run-output check: passed; no `runs/user/port_pg_target_reference_controlled/`
  files were staged.
