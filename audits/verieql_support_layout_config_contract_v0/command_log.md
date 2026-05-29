# Command Log

Key commands run:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 0ede25f50b8a566afdb7c84debc71f59cd951d4c origin/feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
rg -n "SQLRB_VERIEQL|VERIEQL_ROOT|verieql|VeriEQL" src tests scripts docs repository_spec .github pyproject.toml setup.cfg setup.py
rg -n "/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql|/home/tianci_gao/.venvs/sqlrb-verieql" src tests scripts docs repository_spec .github
find . ... VeriEQL artifact scan
```

Validation commands run:

```bash
pytest tests/user_entry/test_verieql_support.py -q
python -m py_compile src/sql_rewrite_bench/verifier_support/verieql.py
python - <<'PY'
# audit Markdown non-empty check
PY
rg -n "/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql|/home/tianci_gao/.venvs/sqlrb-verieql" src tests scripts docs repository_spec .github
git diff --check
git status -sb
find . ... VeriEQL artifact scan
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Validation passed before staging. Staged validation is recorded in `protected_surface_check.md`.
