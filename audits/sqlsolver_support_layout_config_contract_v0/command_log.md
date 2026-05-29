# Command Log

Key commands run:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 010c99804af9d77621670c63614742eb95680361 origin/feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "SQLRB_SQLSOLVER|sqlsolver|SQLSolver" src tests scripts docs pyproject.toml setup.cfg setup.py .github
rg -n "/home/tianci_gao/.local/share/sqlrb/sqlsolver|sqlsolver-v1.1.0.jar|SQLSolver/build/libs" src tests scripts docs repository_spec .github
find . ... SQLSolver artifact scan
```

Validation commands run:

```bash
pytest tests/user_entry/test_sqlsolver_support.py -q
python -m py_compile src/sql_rewrite_bench/verifier_support/sqlsolver.py
python - <<'PY'
# audit Markdown non-empty check
PY
rg -n "/home/tianci_gao/.local/share/sqlrb/sqlsolver|sqlsolver-v1.1.0.jar|SQLSolver/build/libs" src tests scripts docs repository_spec .github
git diff --check
git status -sb
find . ... SQLSolver artifact scan
git -C /home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver status -sb
```

Validation passed before staging. Staged validation is recorded in `protected_surface_check.md`.
