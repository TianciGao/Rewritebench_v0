# Protected Surface Check

Allowed changed paths for this task:

- `src/sql_rewrite_bench/verifier_support/sqlsolver.py`
- `tests/user_entry/test_sqlsolver_support.py`
- `audits/sqlsolver_support_layout_config_contract_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Actual expected changed paths:

- `tests/user_entry/test_sqlsolver_support.py`
- `audits/sqlsolver_support_layout_config_contract_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

No wrapper source change was needed.

Validation result before staging:

- Audit Markdown sanity: 10 Markdown files non-empty.
- `pytest tests/user_entry/test_sqlsolver_support.py -q`: 11 passed.
- `python -m py_compile src/sql_rewrite_bench/verifier_support/sqlsolver.py`: passed.
- SQLSolver-specific hardcoded path scan over source/tests/scripts/docs/repository spec/workflows: no committed local SQLSolver root, JAR, or library path found.
- `git diff --check`: passed.
- Protected path check: only the audit packet, `tests/user_entry/test_sqlsolver_support.py`, and project-control files changed.
- Third-party artifact scan: no SQLSolver support folders, SQLSolver source tree, JAR, native library, ANTLR library, Gradle cache, or build output found in the release repo.
- External SQLSolver source tree status: clean at commit `dcc2a91d8971a4c4d30b055f99d7d8428a1b754b`.

Staged validation:

- `git diff --cached --check`: passed.
- Staged path check: 13 staged paths, all under allowed paths.
- Staged third-party artifact check: no SQLSolver source, JAR, native library, ANTLR library, Gradle cache, or build output staged.
