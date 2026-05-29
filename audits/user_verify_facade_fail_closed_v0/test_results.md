# Test Results

Focused CLI tests:

```bash
PYTHONPATH=src pytest tests/user_entry/test_cli_facade.py -q
```

Result: `20 passed`.

Full user-entry tests:

```bash
PYTHONPATH=src pytest tests/user_entry -q
```

Result: `204 passed, 1 skipped, 12 subtests passed`.

Compile check:

```bash
PYTHONPATH=src python -m py_compile src/cli/main.py
```

Result: passed.

Temp-root CLI smoke:

```bash
PYTHONPATH=src python -m cli.main user verify --run-id smoke_verieql --tool verieql --tool-cmd /definitely/missing/verieql --output-root "$tmp/output"
PYTHONPATH=src python -m cli.main user verify --run-id smoke_sqlsolver --tool sqlsolver --tool-cmd /definitely/missing/sqlsolver --output-root "$tmp/output"
```

Result:

- VeriEQL: fail-closed `semantic_equivalence_rate=N.A.`
- SQLSolver: fail-closed `semantic_equivalence_rate=N.A.`
- Outputs were written only under the temporary output root.
- Temporary output root was removed after smoke.

Additional validation:

- Project-control readability: passed.
- Audit Markdown sanity: passed for 10 Markdown files.
- Audit CSV/JSON sanity: no audit CSV or JSON files created.
- `git diff --check`: passed.
- Protected-surface check: passed.
- Runtime artifact check for `runs/user`, `output`, `reports`, and `results`: no staged or untracked runtime artifacts.
