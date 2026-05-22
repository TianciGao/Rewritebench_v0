# Test Results

Focused CLI tests:

```bash
PYTHONPATH=src pytest tests/user_entry/test_cli_facade.py -q
```

Result: 9 passed.

Full user-entry tests:

```bash
PYTHONPATH=src pytest tests/user_entry -q
```

Result: 172 passed, 1 skipped, 12 subtests passed.

Compile check:

```bash
PYTHONPATH=src python -m py_compile \
  src/cli/__init__.py \
  src/cli/__main__.py \
  src/cli/main.py \
  src/sql_rewrite_bench/user_output.py
```

Result: passed.

CLI schema/boundary smoke:

```bash
PYTHONPATH=src python -m cli.main user show-output-schema
PYTHONPATH=src python -m cli.main user show-boundary
```

Result: passed; both commands state the local-only, non-official boundary.
