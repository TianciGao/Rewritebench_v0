# Protected Surface Check

Allowed changed paths for this task:

- `src/sql_rewrite_bench/verifier_support/verieql.py`
- focused VeriEQL tests under `tests/user_entry/`
- `audits/verieql_support_layout_config_contract_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Actual expected changed paths:

- `src/sql_rewrite_bench/verifier_support/verieql.py`
- `tests/user_entry/test_verieql_support.py`
- `audits/verieql_support_layout_config_contract_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

No cases, case sets, baselines, reports/results, repository-level output, retained evidence, or `runs/user` files were modified.

Validation result before staging:

- Audit Markdown sanity: 10 Markdown files non-empty.
- `pytest tests/user_entry/test_verieql_support.py -q`: 22 passed, 3 subtests passed.
- `python -m py_compile src/sql_rewrite_bench/verifier_support/verieql.py`: passed.
- VeriEQL-specific hardcoded path scan over source/tests/scripts/docs/repository spec/workflows: no committed local VeriEQL root, Python venv, or env-var assignment to a local path found.
- `git diff --check`: passed.
- Protected path check: only the wrapper, focused VeriEQL test, audit packet, and project-control files changed.
- Third-party artifact scan: no VeriEQL support folder, external VeriEQL source tree, venv, native dependency tree, or build output found in the release repo.
- External VeriEQL source tree status: unchanged except pre-existing `M constants.py`.
- External SQLSolver source tree status: clean.

Staged validation:

- `git diff --cached --check`: passed.
- Staged path check: 14 staged paths, all under allowed paths.
- Staged external VeriEQL artifact check: no VeriEQL source tree, venv, dependency file, native library, or build output staged.
