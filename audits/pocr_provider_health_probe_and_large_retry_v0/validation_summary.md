# Validation Summary

Completed:
- Provider health probe completed with 3 live calls.
- Retry batch 1 completed with 100 live calls.
- Retry batch 2 completed with 100 live calls.
- Merged annotation JSONL files were written for 8 affected route-engine combinations.
- Offline replay completed for 8 affected route-engine combinations.
- Aggregator summary was regenerated over 12 row metrics CSVs.
- CSV parse checks passed for all audit CSVs.
- JSONL parse checks passed for generated probe/retry/merged annotation JSONL files.
- Row metrics CSV parse checks passed.
- Aggregator summary CSV parse check passed with 12 route-engine rows.
- Markdown non-empty and required phrase checks passed.
- `python -m py_compile` passed for POCR modules inspected by this task.
- `pytest tests/pocr -q` passed with 143 tests.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q` passed with 28 tests.
- `git diff --check` passed before staging.

Final protected-path, secret-scan, staged diff, and final status checks are recorded in `command_log.md` during commit closeout.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No blind full retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.
