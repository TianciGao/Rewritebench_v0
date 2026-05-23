# Validation

Fresh-copy reproduction before the fix:

- Archive copy had no `runs/user` directory.
- Focused Calcite test failed with `FileNotFoundError`.

Fresh-copy validation after the fix:

- Archive-style working copy had no `runs/user` directory.
- `pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q`: 3 passed.
- `git status --short runs/user` in the fresh copy produced no output.

Repository validation after the fix:

```text
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
3 passed

python scripts/dev/run_user_entry_ci_smoke.py
user-entry ci smoke passed

pytest tests/user_entry -q
227 passed, 1 skipped, 15 subtests passed

python -m py_compile baselines/calcite_hep_fail_closed/adapter.py
passed
```

Notes:

- An earlier parallel validation attempt ran the CI smoke script and full test suite at the same time in the same working tree; that created expected runtime directory-set interference in tests that assert no outputs are created by read-only commands.
- Sequential validation passed and is the relevant result.
