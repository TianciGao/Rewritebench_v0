# Test Results

Focused verifier-support tests:

```bash
PYTHONPATH=src pytest tests/user_entry/test_verifier_support.py -q
```

Result:

```text
7 passed
```

Coverage:

- equivalent normalization
- non-equivalent normalization
- unknown normalization
- timeout normalization
- unsupported normalization
- tool-error normalization
- not-attempted normalization
- unrecognized raw verdict fail-visible policy
- Semantic Equivalence Rate over decidable outcomes only
- N.A. Semantic Equivalence Rate when no decidable outcomes exist
- separate unknown/timeout/unsupported/tool-error/not-attempted counts
- local-only boundary flags
- contract field validation
- no winner/rank/best-method fields
- result-checker exactness not used as verifier evidence

Full user-entry test result is recorded in `command_log.md`.

Full user-entry tests:

```bash
PYTHONPATH=src pytest tests/user_entry -q
```

Result:

```text
187 passed, 1 skipped, 12 subtests passed
```
