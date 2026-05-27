# Command Log

Initial checks:
- `pwd`, `git branch --show-current`, and `git status -sb`.
- Read project control files and required POCR audits/source/tests.

Metric-definition checkpoint:
- Follows D039.
- POCR@planned and POCR@candidate remain promotion-diagnostic views.
- POCR@curated remains NA / curated_manifest_missing until a predeclared curated manifest exists.
- Macro-average over per-row OC_i is the formula.
- Diagnostic micro-average is not the paper formula.

Live gate check:
- SQLRB_LLM_ALLOW_LIVE=1 present: true.
- API key environment variable present: true.
- API key values were not printed or written.

Commands/actions run:
- `run_checkpointed_annotation(run_id=pocr_annotation_track_a120_retry_direct_llm_repair1_spark_batch1_v0, method_id=direct_llm_repair_1, route_id=direct_llm_repair_1_tri_engine_pocr_pilot_v0, engine=spark, case_count=37, max_live_calls=37)`
- `run_checkpointed_annotation(run_id=pocr_annotation_track_a120_retry_sqlglot_optimize_mysql_batch1_v0, method_id=sqlglot_optimize_schema_aware, route_id=sqlglot_optimize_schema_aware_pg40_pocr_diagnostic, engine=mysql, case_count=32, max_live_calls=32)`
- `run_checkpointed_annotation(run_id=pocr_annotation_track_a120_retry_sqlglot_optimize_spark_batch1_v0, method_id=sqlglot_optimize_schema_aware, route_id=sqlglot_optimize_schema_aware_pg40_pocr_diagnostic, engine=spark, case_count=39, max_live_calls=39)`
- `run_checkpointed_annotation(run_id=pocr_annotation_track_a120_retry_sqlglot_noop_mysql_batch1_v0, method_id=sqlglot_noop, route_id=sqlglot_noop_tri_engine_pocr_sanity_control_v0, engine=mysql, case_count=22, max_live_calls=22)`
- `run_checkpointed_annotation(run_id=pocr_annotation_track_a120_retry_sqlglot_noop_spark_batch1_v0, method_id=sqlglot_noop, route_id=sqlglot_noop_tri_engine_pocr_sanity_control_v0, engine=spark, case_count=20, max_live_calls=20)`
- `python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/direct_llm_repair_1_track_a_120_canonical_v0__spark/candidate_sql --annotation-jsonl output/results/pocr_annotation_track_a120_retry_direct_llm_repair1_spark_batch1_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_tri_engine_pocr_pilot_v0/spark/merged_safe_annotation_outputs.jsonl --method-id direct_llm_repair_1 --route-id direct_llm_repair_1_tri_engine_pocr_pilot_v0 --engine spark --run-id pocr_user_replay_track_a120_retry_direct_llm_repair1_spark_v0 --output-root output`
- `python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__mysql/candidate_sql --annotation-jsonl output/results/pocr_annotation_track_a120_retry_sqlglot_optimize_mysql_batch1_v0/pocr/annotations/sqlglot_optimize_schema_aware/sqlglot_optimize_schema_aware_pg40_pocr_diagnostic/mysql/merged_safe_annotation_outputs.jsonl --method-id sqlglot_optimize_schema_aware --route-id sqlglot_optimize_schema_aware_pg40_pocr_diagnostic --engine mysql --run-id pocr_user_replay_track_a120_retry_sqlglot_optimize_mysql_v0 --output-root output`
- `python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__spark/candidate_sql --annotation-jsonl output/results/pocr_annotation_track_a120_retry_sqlglot_optimize_spark_batch1_v0/pocr/annotations/sqlglot_optimize_schema_aware/sqlglot_optimize_schema_aware_pg40_pocr_diagnostic/spark/merged_safe_annotation_outputs.jsonl --method-id sqlglot_optimize_schema_aware --route-id sqlglot_optimize_schema_aware_pg40_pocr_diagnostic --engine spark --run-id pocr_user_replay_track_a120_retry_sqlglot_optimize_spark_v0 --output-root output`
- `python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/common_core_mysql_noop_db_checker/candidate_sql --annotation-jsonl output/results/pocr_annotation_track_a120_retry_sqlglot_noop_mysql_batch1_v0/pocr/annotations/sqlglot_noop/sqlglot_noop_tri_engine_pocr_sanity_control_v0/mysql/merged_safe_annotation_outputs.jsonl --method-id sqlglot_noop --route-id sqlglot_noop_tri_engine_pocr_sanity_control_v0 --engine mysql --run-id pocr_user_replay_track_a120_retry_sqlglot_noop_mysql_v0 --output-root output`
- `python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/common_core_spark_noop_db_checker/candidate_sql --annotation-jsonl output/results/pocr_annotation_track_a120_retry_sqlglot_noop_spark_batch1_v0/pocr/annotations/sqlglot_noop/sqlglot_noop_tri_engine_pocr_sanity_control_v0/spark/merged_safe_annotation_outputs.jsonl --method-id sqlglot_noop --route-id sqlglot_noop_tri_engine_pocr_sanity_control_v0 --engine spark --run-id pocr_user_replay_track_a120_retry_sqlglot_noop_spark_v0 --output-root output`
- `aggregate_pocr_rows over 12 pocr_stage_b_row_metrics.csv inputs`

Validation commands:
- `python -m py_compile src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py src/sql_rewrite_bench/pocr/checkpointed_annotation_runner.py src/sql_rewrite_bench/pocr/user_facade.py src/sql_rewrite_bench/pocr/user_output_adapter.py`
- `pytest tests/pocr -q`
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`
- CSV parse checks for all audit CSVs.
- JSONL parse checks for retry and merged local annotation JSONL.
- Row metrics CSV parse checks for affected replay outputs.
- Aggregator summary CSV parse check.
- Markdown non-empty and required phrase checks.
- Protected-path review, changed-file secret scan, staged secret scan, `git diff --check`, final `git status -sb`, and final `git diff --name-status`.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula. Track A 120 is not a leaderboard.
