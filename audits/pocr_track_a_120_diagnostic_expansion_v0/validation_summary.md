# Validation Summary

Validation completed during closeout.

Checks passed:
- CSV parse checks for all audit CSVs.
- JSONL parse checks for generated annotation JSONL.
- Row metrics CSV parse checks for 12 `pocr_stage_b_row_metrics.csv` files.
- Aggregator summary CSV parse check.
- Markdown non-empty checks.
- Required phrase checks.
- `python -m py_compile` for POCR replay/export/aggregation modules.
- `pytest tests/pocr -q`: 143 passed.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`: 28 passed.
- `git diff --check`: passed.
- Protected-path checks found no modified `cases/`, `skills.md`, candidate SQL, `runs/user`, or top-level `reports/` / `results/` paths.
- No `output/` or `/tmp` paths were staged.
- Changed-file secret scan over the new audit packet found no key-shaped values.
- Staged diff secret scan found no key-shaped values.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula.
