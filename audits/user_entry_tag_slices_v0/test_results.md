# Test Results

## Coverage

- `tests/user_entry/test_tag_slices.py` verifies `tag_slices.csv` is written for
  dry-run and adapter-capture smoke runs.
- The tests verify tag rows come from retained manifest taxonomy metadata, not
  SQL text.
- The tests verify smoke slices for `PERF_0006` and `CONS_0005` retained tags.
- The tests verify boundary flags: `local_diagnostic_only=true`,
  `official_metric=false`, and `leaderboard_input=false`.
- The tests verify no tag score, ranking, timing, or speedup fields are added.
- Existing quality-report tests were updated so `quality_summary.json` and
  `quality_report.md` record that tag slices are available.

## Validation Result

- `PYTHONPATH=src pytest tests/user_entry`: passed, 59 passed and 1 skipped.
- No live DB/checker execution was run.
- No official metrics were computed.
- No paper tables were rendered.
- No reports/results were updated.
