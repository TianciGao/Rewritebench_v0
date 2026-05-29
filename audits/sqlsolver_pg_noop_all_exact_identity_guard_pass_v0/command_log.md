# Command Log

Key commands run:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 2d0954026bc47202f2b1c2c31a36080da0c40d02 origin/feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
java -version
git -C /home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver status -sb
git -C /home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver rev-parse HEAD
```

The SQLSolver pass was run with a local helper under the audit task. It read `runs/user/common_core_pg_noop_db_checker`, generated local-only runtime files under `/tmp/sqlrb_sqlsolver_pg_noop_all_exact_identity_guard_pass_v0/`, and wrote:

- `per_pair_verdicts.csv`
- `per_row_identity_summary.csv`
- `diagnostic_summary.json`

Validation commands are recorded in `protected_surface_check.md` after final validation.

Validation commands run:

```bash
python - <<'PY'
# audit Markdown/CSV/JSON sanity
PY
pytest tests/user_entry/test_sqlsolver_support.py -q
git diff --check
git status -sb
git -C /home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver status -sb
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Validation passed before staging. Staged validation is recorded after explicit `git add` of allowed paths only.
