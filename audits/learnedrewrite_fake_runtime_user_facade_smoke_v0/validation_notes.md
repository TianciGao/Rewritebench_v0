# Validation Notes

## Command Validation

- `pytest tests/user_entry/test_learnedrewrite_adapter.py -q`: passed, `12 passed, 8 subtests passed`.
- `python -m py_compile baselines/learnedrewrite/adapter.py`: passed.
- `python -m cli.main user evaluate ...`: passed for 2 PostgreSQL rows in fake mode.

## Facade Smoke Checks

- Selected row count: 2.
- Selected rows: `PERF_0006/postgres`, `CONS_0036/postgres`.
- Candidate generated count: 2.
- Candidate preflight passed count: 2.
- Candidate SQL shape: one `SELECT` statement per row.
- DB execution: not enabled.
- Checker execution: not enabled.
- Timing: not requested.
- Local metrics: not run.
- Verifier: not run.

## Fail-Closed Checks

Temporary adapter-level checks passed for:

- missing fake response -> `fake_runtime_missing_response`;
- multiple statements -> `multiple_sql_statements`;
- prose-only response -> `response_not_sql`;
- unsupported engine -> `unsupported_engine`.

## CSV And Markdown Checks

- `adapter_output_review.csv` parses with 2 rows.
- All Markdown files in this packet are non-empty.

## Runtime And Source Hygiene

- Fake runtime only: passed.
- No `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1`: passed.
- No Java runtime command occurred: passed by command log review.
- No DB/checker/timing/local_metrics/verifier command occurred: passed by command log review.
- No upstream source, JAR, dependency JAR, checkpoint, dataset, generated output, or request log copied: passed by changed-file review.
- Runtime outputs under `runs/user/` and `/tmp` are not intended for staging or commit.

## Secret And Protected-Path Review

- No API key was required.
- Metadata scan found no secret-like fields.
- Changed-file secret scan: passed for secret-shaped values in this audit packet and project-control writeback.
- Staged-file secret scan: passed after explicit staging.
- Protected-path review: passed; intended staged paths are this audit packet and project-control writeback only. Two unrelated pre-existing untracked Direct LLM audit directories were left untouched.
- `git diff --check`: passed.
