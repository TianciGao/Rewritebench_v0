# Validation Summary

Validation completed for `pocr_track_a_120_targeted_retry_quality_review_v0`.

Checks run:
- `python -m py_compile src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py src/sql_rewrite_bench/pocr/checkpointed_annotation_runner.py src/sql_rewrite_bench/pocr/user_facade.py src/sql_rewrite_bench/pocr/user_output_adapter.py` passed.
- `pytest tests/pocr -q` passed: 143 tests.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q` passed: 28 tests.
- CSV parse checks passed for all audit CSVs.
- JSONL parse checks passed for retry and merged local annotation JSONL files.
- Row metrics CSV parse checks passed for all five affected retry replay outputs.
- Aggregator summary CSV parse check passed for local retry aggregate output.
- Markdown non-empty checks passed.
- Required boundary phrase checks passed.

Key validation counts:
- Fail-closed rows decomposed: 250.
- Retry-eligible rows: 235.
- Batch1 selected rows: 150.
- Retry live calls attempted: 150.
- Retry schema-valid rows: 0.
- Remaining fail-closed row-metrics rows after retry batch: 250.
- Replay rerun count: 5 route-engine combinations.
- Aggregator summary rows: 12.

Boundary confirmation:
- This is not official POCR.
- No route-level official POCR score is emitted.
- No paper-facing metric is promoted.
- POCR@planned and POCR@candidate remain D039 promotion views.
- POCR@curated remains deferred until a predeclared curated manifest exists.
- Micro-average is diagnostic only and not the paper formula.
- Track A 120 is not a leaderboard.

Protected path checks, changed-file secret scan, staged secret scan, `git diff --check`, and final status checks are recorded in the closeout command log.
