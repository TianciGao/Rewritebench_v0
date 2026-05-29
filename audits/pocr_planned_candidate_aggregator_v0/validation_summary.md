# Validation Summary

Validation performed during closeout:

- `python -m py_compile` for changed Python modules.
- `pytest tests/pocr -q`.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`.
- Route summary fixture/test output parses as CSV.
- Required route summary columns are present.
- Markdown audit files are non-empty.
- Required boundary phrases are present in audit Markdown.
- `git diff --check`.
- Protected-path review.
- Changed-file secret scan.
- Staged secret scan.

The focused aggregator tests cover:

- two normal rows with correct macro average;
- macro-average distinct from diagnostic micro-average;
- POCR@planned fail-closed zero contribution;
- POCR@candidate exclusion of no-candidate rows and inclusion of candidate-bound fail-closed rows;
- no-expected-operation rows as not applicable;
- POCR@curated `NA` / `curated_manifest_missing`;
- boundary constants;
- missing required columns;
- route/candidate mismatch counts;
- all-zero no-op route output.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
