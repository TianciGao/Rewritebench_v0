# Command Log

Initial checks:
- `pwd`
- `git branch --show-current`
- `git status -sb --untracked-files=normal`
- Read required project-control files, audit packets, POCR modules, and tests.

Live gate:
- Checked `SQLRB_LLM_ALLOW_LIVE=1` and API key environment-variable presence without printing key values.
- Provider label: openai_compatible.
- Model label: gpt-5.4.
- Base URL host: api.gptsapi.net.

Provider probe:
- `run_checkpointed_annotation` for `pocr_provider_health_probe_after_balance_fix_repair1_spark_v0`, 1 row.
- `run_checkpointed_annotation` for `pocr_provider_health_probe_after_balance_fix_sqlglot_optimize_mysql_v0`, 1 row.
- `run_checkpointed_annotation` for `pocr_provider_health_probe_after_balance_fix_sqlglot_noop_mysql_v0`, 1 row.

Retry batch 1:
- `run_checkpointed_annotation` for `pocr_annotation_track_a120_retry_large_batch1_after_provider_fix_direct_llm_repair1_spark_v0`, 36 rows.
- `run_checkpointed_annotation` for `pocr_annotation_track_a120_retry_large_batch1_after_provider_fix_sqlglot_optimize_mysql_v0`, 31 rows.
- `run_checkpointed_annotation` for `pocr_annotation_track_a120_retry_large_batch1_after_provider_fix_sqlglot_optimize_spark_v0`, 33 rows.

Retry batch 2:
- `run_checkpointed_annotation` for `pocr_annotation_track_a120_retry_large_batch2_after_provider_fix_sqlglot_optimize_spark_v0`, 6 rows.
- `run_checkpointed_annotation` for `pocr_annotation_track_a120_retry_large_batch2_after_provider_fix_sqlglot_noop_mysql_v0`, 35 rows.
- `run_checkpointed_annotation` for `pocr_annotation_track_a120_retry_large_batch2_after_provider_fix_sqlglot_noop_spark_v0`, 35 rows.
- `run_checkpointed_annotation` for `pocr_annotation_track_a120_retry_large_batch2_after_provider_fix_direct_llm_original_mysql_v0`, 9 rows.
- `run_checkpointed_annotation` for `pocr_annotation_track_a120_retry_large_batch2_after_provider_fix_direct_llm_original_postgres_v0`, 7 rows.
- `run_checkpointed_annotation` for `pocr_annotation_track_a120_retry_large_batch2_after_provider_fix_direct_llm_original_spark_v0`, 7 rows.
- `run_checkpointed_annotation` for `pocr_annotation_track_a120_retry_large_batch2_after_provider_fix_direct_llm_repair1_mysql_v0`, 1 row.

Replay:
- Ran `python -m cli.main user pocr-diagnostic ... --output-root output` for the eight affected route-engine combinations recorded in `retry_replay_manifest.csv`.

Aggregation:
- Ran `pocr_aggregator.py` library functions over 12 `pocr_stage_b_row_metrics.csv` inputs and wrote `output/results/pocr_aggregate_track_a120_retry_large_after_provider_fix_v0/pocr/aggregates/pocr_route_summary.csv`.

Validation:
- Parsed all audit CSVs.
- Parsed generated probe/retry/merged annotation JSONL files.
- Parsed row metrics CSVs and aggregate summary CSV.
- Checked audit Markdown files are non-empty and contain required boundary phrases.
- Ran `python -m py_compile` for POCR modules inspected by this task.
- Ran `pytest tests/pocr -q` with 143 passing tests.
- Ran `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q` with 28 passing tests.
- Ran `git diff --check`.

No API key values were printed, written, staged, or committed.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No blind full retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.
