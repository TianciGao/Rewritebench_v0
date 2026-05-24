# Validation Notes

Validation completed:

- `pytest tests/user_entry/test_learnedrewrite_adapter.py -q`: passed,
  `14 passed, 8 subtests passed`.
- `python -m py_compile baselines/learnedrewrite/adapter.py`: passed.
- User-facade smoke selected exactly one PostgreSQL row.
- Candidate generation: 1/1.
- Source execution success: 1/1.
- Candidate execution success: 1/1.
- Checker exact: 1/1.
- Timed rows: 1/1.
- Fail-closed rows: 0.
- CSV parse checks passed for generated audit CSVs.
- Markdown non-empty checks passed for generated audit Markdown/text files.
- Run JSON artifacts parsed before cleanup.
- No `compute-local-metrics` command occurred.
- No SQLSolver, VeriEQL, R-Bot, LLM-R2, or live LLM command occurred.
- No JAR/source/runtime asset copied into the release repo.
- Runtime shutdown check passed.
- Runtime outputs were not staged.
- `git diff --check` passed.
- Changed-file secret scan passed.
- Protected-path review passed.

Boundary result:

- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
