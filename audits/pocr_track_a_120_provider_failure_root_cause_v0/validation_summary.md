# Validation Summary

Validation completed:
- CSV parse checks passed for `failure_decomposition.csv`, `provider_error_taxonomy.csv`, and `prompt_size_and_shape_review.csv`.
- Markdown non-empty checks passed for all audit Markdown files.
- Required phrase checks passed.
- `python -m py_compile src/sql_rewrite_bench/pocr/annotation_client.py src/sql_rewrite_bench/pocr/prompt_builder.py src/sql_rewrite_bench/pocr/checkpointed_annotation_runner.py src/sql_rewrite_bench/pocr/annotation_schema.py src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py` passed.
- `pytest tests/pocr -q` passed: 143 tests.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q` passed: 28 tests.

Static audit counts:
- Failure rows decomposed: 250.
- Retry calls reviewed: 150.
- Retry schema-valid rows: 0.
- Most common likely cause: provider_config_issue_insufficient_balance_or_unauthorized (196).

Closeout validation completed:
- `git diff --check` passed.
- Staged `git diff --cached --check` passed.
- Protected-path checks found no tracked or staged changes under `cases/`, `runs/user/`, candidate SQL roots, top-level `reports/`, top-level `results/`, or `output/`.
- Changed-file secret-value scan found no credential values.
- Staged secret-value scan found no credential values.
- No `output/` or `/tmp` artifacts were staged.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No bulk retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists.
