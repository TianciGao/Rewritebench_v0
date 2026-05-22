# Test Results

Validation commands run:

```text
PYTHONPATH=src pytest tests/user_entry/test_user_output.py -q
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/user_output.py
PYTHONPATH=src pytest tests/user_entry -q
```

Results:

- Focused output writer tests: passed, `5 passed`.
- Python compile check: passed.
- Full user-entry test suite: passed, `164 passed, 1 skipped, 12 subtests passed`.

Test coverage added:

- D035 output path construction.
- Bad run-id and top-level `reports/`/`results` root rejection.
- Run manifest local-only boundary flags.
- Boundary report local-only/non-official text.
- Ledger, quality summary, tag slices, candidates, execution, checker, timing, metrics, and verifier placeholder export.
- Failure bucket CSV derivation from existing ledger/failure artifacts.
- Optional missing artifacts producing N.A. reports instead of crashes.
- Source `runs/user/` directory non-mutation.
- Temporary output roots only.
