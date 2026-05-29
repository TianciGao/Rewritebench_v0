# Regression Tests

Focused tests added in `tests/user_entry/test_candidate_preflight.py`:

- `test_block_comment_semicolon_before_statement_is_single_statement`
- `test_block_comment_semicolon_after_statement_is_single_statement`
- `test_line_comment_semicolon_before_statement_is_single_statement`
- `test_string_literal_semicolon_is_single_statement`
- `test_backtick_identifier_semicolon_is_single_statement`
- `test_quoted_identifier_semicolon_is_single_statement`
- `test_with_followed_by_unsafe_second_statement_fails`
- Existing `test_multiple_statements_fail` now also asserts Spark splitter behavior.

The tests assert candidate preflight and Spark statement splitting agree on the single-statement verdict for comment and quoted-text semicolons, and that genuine two-statement SQL still splits as two statements and fails preflight.

Validation commands:

```bash
PYTHONPATH=src pytest tests/user_entry/test_candidate_preflight.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/candidate_preflight.py src/sql_rewrite_bench/spark_execution.py tests/user_entry/test_candidate_preflight.py
```

Results:

- Focused candidate preflight tests: `20 passed`.
- User-entry suite: `137 passed, 1 skipped, 12 subtests passed`.
- Python compile check: passed.
