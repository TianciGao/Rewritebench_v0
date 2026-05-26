# Validation Summary

Initial smoke generation completed successfully:
- Repair-1 row metrics rows: 40.
- SQLGlot no-op row metrics rows: 40.
- Aggregator route summary rows: 2.
- Repair-1 POCR@planned and POCR@candidate matched prior dry-run values exactly.
- SQLGlot no-op POCR@planned and POCR@candidate matched prior dry-run values exactly.

Validation commands are recorded in `command_log.md`.

Completed validation:
- `python -m py_compile src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py` passed.
- `pytest tests/pocr -q` passed with 143 tests.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q` passed with 28 tests.
- `smoke_summary.csv` parsed as CSV with 2 data rows.
- The local `/tmp` aggregator `pocr_route_summary.csv` parsed as CSV with 2 data rows and all required route-summary columns.
- Audit Markdown files are non-empty.
- Required boundary phrase checks passed.
- `git diff --check` passed.

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

POCR@curated remains deferred until a predeclared curated manifest exists.

Micro-average is diagnostic only and not the paper formula.
