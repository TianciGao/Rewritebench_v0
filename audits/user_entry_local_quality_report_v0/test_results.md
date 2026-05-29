# Test Results

## Coverage

- `tests/user_entry/test_quality_report.py` verifies `quality_summary.json` and `quality_report.md` are written for dry-run and adapter-capture smoke runs.
- The tests verify local boundary flags: `official_metrics=false`, `paper_results_updated=false`, `retained_evidence_input=false`, and `leaderboard_created=false`.
- The tests verify funnel counts for dry-run and adapter-capture smoke rows.
- The tests verify U4 does not create `tag_slices.csv`.
- The tests verify no speedup or official metric-name fields are added to `quality_summary.json`.

## Validation Result

- `PYTHONPATH=src pytest tests/user_entry`: passed, 55 passed and 1 skipped.
- No live DB/checker execution was run.
- No official metrics were computed.
- No paper tables were rendered.
- No reports/results were updated.
