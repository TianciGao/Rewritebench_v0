# Fix Summary

Changed file:

- `tests/user_entry/test_calcite_hep_fail_closed_route.py`

Change:

- Removed direct use of `tempfile.TemporaryDirectory(dir=REPO_ROOT / "runs" / "user")`.
- Added a unique relative output helper:
  - `runs/user/calcite_fail_closed_unit_<uuid>`
- Passed that relative path into `run_user_benchmark`.
- Cleaned only that specific test output directory in a `finally` block.

Why this is correct:

- `run_user_benchmark` already owns creation of relative user-run output directories below `runs/user`.
- The test still exercises the same user-run path and relative-output validation.
- Fresh checkouts no longer require an existing `runs/user` parent.
- Runtime artifacts are removed after the test.

No changes were made to:

- `baselines/calcite_hep_fail_closed/adapter.py`
- `.github/workflows/user_entry_smoke.yml`
- `scripts/dev/run_user_entry_ci_smoke.py`
