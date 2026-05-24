# Validation

Required validation commands:

```bash
python scripts/dev/run_user_entry_ci_smoke.py
pytest tests/user_entry/test_sqlglot_adapter.py tests/user_entry/test_local_timing.py -q
pytest tests/user_entry -q
python -m py_compile baselines/sqlglot/sqlglot_user_adapter.py
git diff --check
git status -sb
```

Results:

- `python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `pytest tests/user_entry/test_sqlglot_adapter.py tests/user_entry/test_local_timing.py -q`: 21 passed, 1 skipped.
- `pytest tests/user_entry -q`: 239 passed, 1 skipped, 15 subtests passed.
- `python -m py_compile baselines/sqlglot/sqlglot_user_adapter.py`: passed.
- `git diff --check`: passed.
- Protected path status checks found no staged `runs/user`, repository-level `output`, top-level `reports`, or top-level `results` artifacts.

The local CI-equivalent smoke now reaches and passes module help, wrapper help, user-entry tests, dry-run smoke, dummy adapter smoke, protected-path checks, and `runs/user` cleanup checks.
