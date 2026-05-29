# Validation Summary

Validation commands are recorded in `command_log.md`. The required checks include CSV parsing, JSONL parsing, row metrics parsing, aggregator summary parsing, Markdown non-empty checks, required boundary phrase checks, pytest, protected-path review, secret scans, `git diff --check`, final status, and final diff name-status.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula.

## Completed Checks

- Audit CSV parse checks: passed.
- Selected pilot row count: 30.
- Generated annotation JSONL parse checks: passed for 6 files / 30 rows.
- Row metrics CSV parse checks: passed for 6 files / 30 rows.
- Aggregator summary CSV parse and required-column checks: passed.
- Markdown non-empty checks: passed.
- Required boundary phrase checks: passed.
- Boundary constants in row metrics and aggregate summary: passed.
- `python -m py_compile` for POCR/replay modules: passed.
- `pytest tests/pocr -q`: 143 passed.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`: 28 passed.
- `git diff --cached --check`: passed.
- Changed-file and staged secret scans: passed for staged additions/changes; no API key values were found.
- Protected-path staged check: passed; no `output/`, `cases/`, `case_sets/`, `reports/`, `results/`, or `runs/user` paths are staged.
- `output/` remains local and uncommitted.
