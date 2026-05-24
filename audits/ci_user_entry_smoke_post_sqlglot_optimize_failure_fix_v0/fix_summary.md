# Fix Summary

Modified:

- `tests/user_entry/test_user_run_outputs.py`

Change:

- Replaced stale documentation expectations for internal runner flags with D035 facade expectations.
- The test now checks for `--engines`, `--output-root`, `--run-id`, `python -m cli.main user evaluate`, `sqlrb user evaluate`, `output/results/<run_id>/`, and `runs/user/<run_id>/`.
- The internal `parse_args` checks remain in place to preserve coverage for the internal user-run parser.

Not changed:

- `scripts/dev/run_user_entry_ci_smoke.py`
- `.github/workflows/user_entry_smoke.yml`
- `baselines/sqlglot/sqlglot_user_adapter.py`
- docs
- cases
- schemas
- reports/results
- repository-level output
- `runs/user`

This is the smallest fix because the implementation and docs already match the intended D035 user-facing contract; only the test had drifted.
