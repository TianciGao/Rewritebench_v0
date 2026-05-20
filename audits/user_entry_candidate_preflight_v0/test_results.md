# Test Results

## Unit And Smoke Coverage

- `tests/user_entry/test_candidate_preflight.py` covers valid SELECT and WITH candidates, empty candidate failure, unsafe SQL failure, multi-statement failure, unsupported statement type failure, trailing semicolon acceptance, source-like diagnostic status, changed diagnostic status, preflight status vocabulary, mocked DB/checker skip on preflight failure, public smoke adapter-capture preflight fields, and public smoke dry-run behavior.
- Existing user-entry tests continue to cover case selection, user-run output files, optional PostgreSQL/checker schema resolution, SQLGlot adapter behavior, and U2 module split behavior.

## Validation Result

- `PYTHONPATH=src pytest tests/user_entry`: passed, 52 passed and 1 skipped.
- No live DB/checker execution was run.
- No official metrics were computed.
- No paper tables were rendered.
- No reports/results were updated.
