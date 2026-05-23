# CI User-Entry Smoke Calcite Layout Failure Fix

Task: `ci_user_entry_smoke_calcite_layout_failure_fix_v0`

Verdict: fixed with a minimal test-side change.

The CI failure was reproduced locally from a clean archive copy that had no `runs/user` directory. The new Calcite route test attempted to create a temporary directory with:

```python
tempfile.TemporaryDirectory(dir=REPO_ROOT / "runs" / "user")
```

On a fresh checkout this parent directory does not exist, so the test failed with `FileNotFoundError` during the `user-entry-smoke` test phase.

The fix removes the pre-existing-parent assumption. The test now uses a unique relative `runs/user/<id>` output path and lets `run_user_benchmark` create the required directories, then removes that one test output path in `finally`.

No workflow or Calcite adapter change was required.
