# Test Results

Focused VeriEQL/verifier-support tests:

```bash
PYTHONPATH=src pytest tests/user_entry/test_verieql_support.py tests/user_entry/test_verifier_support.py -q
```

Result:

```text
13 passed
```

Full user-entry test result is recorded in `command_log.md`.

Full user-entry tests:

```bash
PYTHONPATH=src pytest tests/user_entry -q
```

Result:

```text
193 passed, 1 skipped, 12 subtests passed
```

Coverage:

- unavailable VeriEQL fail-closed behavior
- detection without installing tools
- equivalent output normalization
- non-equivalent/refutation output normalization
- unknown, unsupported, timeout, and tool-error handling
- fake-command bounded local summary path
- nonzero counterexample output preserved as `non_equivalent`
- local result-checker exactness not used as verifier evidence
- output contract path shape
- local-only boundary flags
- no winner/rank/best-method fields
