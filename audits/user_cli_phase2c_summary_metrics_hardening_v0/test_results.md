# Test Results

Focused CLI tests:

```bash
PYTHONPATH=src pytest tests/user_entry/test_cli_facade.py -q
```

Result: 16 passed.

Full user-entry tests:

```bash
PYTHONPATH=src pytest tests/user_entry -q
```

Result: 180 passed, 1 skipped, 12 subtests passed.

Compile check:

```bash
PYTHONPATH=src python -m py_compile src/cli/__init__.py src/cli/__main__.py src/cli/main.py
```

Result: passed.

Additional validation:

- Project-control readability: passed.
- Audit Markdown sanity: passed.
- `git diff --check`: passed.
- Protected-surface check: passed.
