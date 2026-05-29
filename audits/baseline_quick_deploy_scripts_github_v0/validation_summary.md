# Validation Summary

Validation executed:

- `bash -n scripts/setup_baseline_adapters.sh`: passed.
- `bash -n scripts/check_baseline_adapters.sh`: passed.
- `bash scripts/check_baseline_adapters.sh --profile all-safe --repo-root .`: passed with `PASS=21 WARN=0 FAIL=0`; wrote a local untracked report under `output/reports/baseline_env_check_20260529T122759Z/baseline_report.txt`.
- `bash scripts/setup_baseline_adapters.sh --profile all-safe --repo-root . --no-install`: passed with `PASS=16 WARN=1 FAIL=0`; warning was expected because `--no-install` skips pip install.
- `pytest tests/pocr -q`: `143 passed`.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`: `31 passed`.
- Changed Python modules: none; `python -m py_compile` not applicable.
- Markdown non-empty checks: passed.
- Required phrase checks: passed.
- `git diff --check`: passed.
- Changed-file secret scan: passed.
- Staged secret scan: passed.
- Staged protected-path scan: passed; no `output/`, `/tmp`, `cases/`, `skills.md`, candidate SQL, `runs/user`, top-level `reports/` or `results/`, `MIGRATION_MASTER_PLAN.md`, or `DECISION_LOG.md` files were staged.

Results are recorded in `command_log.md`.
