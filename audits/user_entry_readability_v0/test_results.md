# Test Results

## Coverage

- `tests/user_entry/test_readability_commands.py` verifies `--list-cases`,
  `--explain-selection`, and `--show-output-schema`.
- The tests verify command-only helpers do not invoke adapters or create
  `runs/user/...` output directories.
- The tests verify `--list-cases --pool PERF` filters to PERF rows.
- The tests verify smoke selection explanation reports two selected rows and
  two unique cases.
- Existing smoke, quality, and tag-slice output tests continue to pass.

## Validation Result

- `PYTHONPATH=src pytest tests/user_entry`: passed, 65 passed and 1 skipped.
- No live DB/checker execution was run.
- No timing or speedup was computed.
- No official metrics were computed.
- No paper tables were rendered.
- No reports/results were updated.
