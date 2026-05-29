# Root Cause

The CI smoke script runs:

```bash
pytest tests/user_entry -q
```

`tests/user_entry/test_user_run_outputs.py::UserRunOutputTests::test_documented_examples_match_current_cli_options` was stale after the D035 user-facing output/docs cleanup.

The stale assertions required the user guide to contain internal runner details:

- `--engine`
- `--out`
- `python -m sql_rewrite_bench.user_run`
- `python scripts/user/run_user_benchmark.py`

The current guide intentionally documents the public D035 facade instead:

- `PYTHONPATH=src python -m cli.main user evaluate`
- `sqlrb user evaluate`
- `--engines`
- `--output-root`
- `--run-id`
- `output/results/<run_id>/`
- `runs/user/<run_id>/` only as internal transitional staging

Therefore the failure was a test expectation drift, not a SQLGlot adapter regression, not a CI workflow bug, and not a Node.js warning issue.
