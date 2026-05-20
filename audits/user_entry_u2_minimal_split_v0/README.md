# User-Entry U2 Minimal Split v0

## Purpose

This packet records the behavior-preserving U2 implementation of the user-entry module split designed in `audits/user_entry_module_split_design_v0/`.

## Implementation Summary

Added:

- `src/sql_rewrite_bench/case_package_resolver.py`
- `src/sql_rewrite_bench/adapter_runner.py`
- `src/sql_rewrite_bench/user_ledger.py`

Updated:

- `src/sql_rewrite_bench/user_run.py` now delegates package resolution, adapter invocation/candidate capture, and ledger/failure CSV writing to the new modules.
- `tests/user_entry/test_u2_module_split.py` covers resolver, adapter-runner, ledger-writer, and public smoke dry-run behavior.

`user_run.py` remains the CLI/orchestrator and still owns CLI parsing, run setup, output-root validation, config writing, selected-case CSV writing, optional PostgreSQL/checker orchestration, summary JSON construction, and report Markdown construction.

## Behavior Boundary

This was a refactor-only implementation.

- Candidate preflight implemented: no.
- Local quality report implemented: no.
- Tag slicing implemented: no.
- Timing implemented: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reports/results updated: no.
- Retained evidence parsed or promoted: no.
- Global leaderboard created: no.

## Validation Summary

- Module help: passed.
- Wrapper help: passed.
- Public smoke dry-run: passed.
- Public smoke adapter-capture: passed.
- User-entry tests: passed, 39 passed and 1 skipped.
- Required U2 smoke outputs were removed before commit.

## Next Safe Action

Run human review of the behavior-preserving split. If accepted, the next implementation phase is U3 candidate preflight v0, separately authorized and still local-diagnostic only.
