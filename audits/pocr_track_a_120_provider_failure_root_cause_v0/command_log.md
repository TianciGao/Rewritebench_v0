# Command Log

Initial checks:
- `pwd`
- `git branch --show-current`
- `git status -sb --untracked-files=normal`
- Read project control files and required POCR audit/code/test inputs.

Static audit commands/actions:
- Parsed Track A diagnostic expansion annotation/replay/row-metrics manifests.
- Parsed Track A targeted retry decomposition, retry manifests, provider manifests, and replay outputs.
- Inspected `annotation_client.py`, `prompt_builder.py`, `checkpointed_annotation_runner.py`, `annotation_schema.py`, `stage_b_row_metrics.py`, and `pocr_aggregator.py`.
- Computed prompt-size metadata from local source/candidate/positive SQL and skills contracts without writing raw prompts.
- Produced failure taxonomy, schema/extraction reviews, safe samples, root-cause assessment, and recommended fix plan.
- Parsed audit CSVs with Python `csv.DictReader`.
- Checked audit Markdown files for non-empty content and required boundary phrases.
- Ran `python -m py_compile src/sql_rewrite_bench/pocr/annotation_client.py src/sql_rewrite_bench/pocr/prompt_builder.py src/sql_rewrite_bench/pocr/checkpointed_annotation_runner.py src/sql_rewrite_bench/pocr/annotation_schema.py src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py`.
- Ran `pytest tests/pocr -q`.
- Ran `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`.

No live API call was made. No API key was read. No bulk retry is run.

Validation commands are recorded in `validation_summary.md`.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No bulk retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists.
