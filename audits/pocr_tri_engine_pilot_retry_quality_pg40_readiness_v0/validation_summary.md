# Validation Summary

Validation completed before staging:

- CSV parse checks for all audit CSVs: passed.
- Retry/merged annotation JSONL parse checks: passed.
- Row metrics CSV parse checks for six retry replay runs: passed.
- Aggregator summary CSV parse check: passed.
- Markdown non-empty checks: passed.
- Required boundary phrase checks: passed.
- `python -m py_compile src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py src/sql_rewrite_bench/pocr/checkpointed_annotation_runner.py`: passed.
- `pytest tests/pocr -q`: passed, 143 tests.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`: passed, 28 tests.
- `git diff --check`: passed.
- Protected path pre-staging check: only `project_control/` modifications plus the new audit packet are intended; `output/` remains untracked.
- Changed-file secret scan: passed for the new audit packet and modified project-control files.
- Staged secret scan: passed.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@curated remains deferred until a predeclared curated manifest exists.
