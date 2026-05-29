# Test Results

Focused SQLSolver tests:

```bash
PYTHONPATH=src pytest tests/user_entry/test_sqlsolver_support.py -q
```

Result: `7 passed`.

Focused verifier-support tests:

```bash
PYTHONPATH=src pytest tests/user_entry/test_verieql_support.py tests/user_entry/test_verifier_support.py tests/user_entry/test_sqlsolver_support.py -q
```

Result: `20 passed`.

Full user-entry tests:

```bash
PYTHONPATH=src pytest tests/user_entry -q
```

Result: `200 passed, 1 skipped, 12 subtests passed`.

Compile check:

```bash
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/verifier_support/sqlsolver.py src/sql_rewrite_bench/verifier_support/__init__.py
```

Result: passed.

Readability/sanity checks:

- Project-control readability: passed.
- Audit Markdown sanity: passed for 11 Markdown files.
- `git diff --check`: passed.
- Protected-surface check: passed.
- Runtime artifact check for `runs/user`, `output`, `reports`, and `results`: no staged or untracked runtime artifacts.

Bounded smoke:

- SQLSolver unavailable.
- Temp-root fail-closed smoke produced one `not_attempted` row with `semantic_equivalence_rate=None` and `na_reason=sqlsolver_unavailable`.
