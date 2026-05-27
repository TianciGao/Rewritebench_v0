# Command Log

Initial checks:
- `pwd`
- `git branch --show-current`
- `git status -sb --untracked-files=normal`
- Read required project-control files, audit packets, POCR modules, and tests.

Decomposition:
- Parsed the previous large-retry row metrics from `audits/pocr_provider_health_probe_and_large_retry_v0/retry_row_metrics_summary.csv`.
- Classified 83 remaining fail-closed rows: 68 retry-eligible schema-invalid rows and 15 non-retryable SQLGlot optimize no-candidate rows.

Live final retry:
- Confirmed live gate using environment presence only; no API key value was printed.
- Ran `run_checkpointed_annotation` for 11 route-engine groups under run id `pocr_annotation_track_a120_final_retry_v0`.
- Final retry live calls attempted: 68.
- Final retry status counts: {'malformed_json': 15, 'schema_valid': 48, 'timeout': 4, 'schema_invalid': 1}.

Merge/replay/aggregate:
- Wrote merged annotation JSONL files under `output/results/pocr_annotation_track_a120_final_retry_merged_<method>_<engine>_v0/...`.
- Ran `python -m cli.main user pocr-diagnostic ... --output-root output` for 11 affected route-engine combinations.
- Ran `pocr_aggregator.py` library functions over 12 row metrics CSVs and wrote `output/results/pocr_aggregate_track_a120_final_retry_v0/pocr/aggregates/pocr_route_summary.csv`.

Validation:
- Parsed all audit CSVs.
- Parsed final retry and merged annotation JSONL files.
- Parsed affected row metrics CSVs and aggregate summary CSV.
- Checked audit Markdown files are non-empty and contain required boundary phrases.
- Ran `python -m py_compile` for POCR modules inspected by this task.
- Ran `pytest tests/pocr -q` with 143 passing tests.
- Ran `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q` with 28 passing tests.
- Ran `git diff --check`.

No API key values were printed, written, staged, or committed.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula. Track A 120 is not a leaderboard.
