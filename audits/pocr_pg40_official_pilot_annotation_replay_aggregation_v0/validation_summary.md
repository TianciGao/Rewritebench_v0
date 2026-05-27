# Validation Summary

Validation completed for this audit packet and the local PG40 pilot outputs.

- Audit CSV parse checks: passed.
- SQLGlot optimize generated annotation JSONL parse check: passed with 34 rows.
- Row metrics CSV parse checks: passed for four PG40 replay outputs, 40 rows each.
- Aggregator summary CSV parse check: passed with four route rows.
- Markdown non-empty checks: passed.
- Required boundary phrase checks: passed.
- `python -m py_compile` for POCR replay/export/aggregate modules: passed.
- `pytest tests/pocr -q`: passed, 143 tests.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`: passed, 28 tests.
- `git diff --check`: passed.
- Protected-path review: passed.
- Changed-file secret scan: passed.
- Staged protected-path check: passed.
- Staged secret scan: passed.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula. PG40 is not Track A 120.
