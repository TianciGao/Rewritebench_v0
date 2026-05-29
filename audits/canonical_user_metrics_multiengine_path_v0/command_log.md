# Command Log

Preflight and inspection:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 09e9b26872051008fbe02460bf177507706d767c HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
sed -n '1,260p' src/sql_rewrite_bench/user_output.py
sed -n '1,760p' src/sql_rewrite_bench/local_metrics.py
sed -n '1,620p' src/cli/main.py
sed -n '1,320p' tests/user_entry/test_local_metrics.py
sed -n '1,260p' tests/user_entry/test_cli_facade.py
```

Validation:

```bash
pytest tests/user_entry/test_local_metrics.py tests/user_entry/test_cli_facade.py -q
pytest tests/user_entry -q
python -m py_compile src/sql_rewrite_bench/local_metrics.py src/cli/main.py tests/user_entry/test_local_metrics.py tests/user_entry/test_cli_facade.py
```

Final validation commands are recorded in `test_coverage.md` and will be rerun before commit.
