# Validation Summary

Completed:
- Final retry selected 68 retry-eligible rows under the 100-call cap.
- Final retry wrote safe annotation JSONL rows for 68 rows.
- Offline replay completed for 11 affected route-engine combinations.
- Row metrics CSVs were produced for replay outputs.
- Aggregator summary was produced at `output/results/pocr_aggregate_track_a120_final_retry_v0/pocr/aggregates/pocr_route_summary.csv`.
- CSV parse checks passed for all audit CSVs.
- JSONL parse checks passed for final retry and merged annotation JSONL files.
- Row metrics CSV parse checks passed for affected replay outputs.
- Aggregator summary CSV parse check passed with 12 route-engine rows.
- Markdown non-empty and required phrase checks passed.
- `python -m py_compile` passed for POCR modules inspected by this task.
- `pytest tests/pocr -q` passed with 143 tests.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q` passed with 28 tests.
- `git diff --check` passed before staging.

Final protected-path, secret-scan, staged diff, and status checks are recorded in `command_log.md` during commit closeout.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula. Track A 120 is not a leaderboard.
