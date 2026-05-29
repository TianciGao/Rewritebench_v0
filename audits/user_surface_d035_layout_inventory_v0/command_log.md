# Command Log

Commands run for this packet:

```bash
git status -sb
git branch --show-current
git status --porcelain -- reports results output runs/user
rg -n "D034|D035" project_control/DECISION_LOG.md
git fetch origin main feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg --files src/cli src/sql_rewrite_bench/verifier_support baselines tests/user_entry
rg --files scripts/dev docs examples
rg -n "output/results|output/logs|output/reports|output/<run_id>|runs/user|reports/|results/" src/cli src/sql_rewrite_bench baselines tests/user_entry scripts/dev docs examples
rg -n "calcite_hep_fail_closed_adapter|calcite_hep|sqlglot_user_adapter|user_adapter|adapter.py" src/sql_rewrite_bench src/cli baselines tests/user_entry docs examples scripts/dev
git ls-files '*__pycache__*' '*.pyc'
git ls-files src/sql_rewrite_bench | rg -n "calcite|sqlglot|baseline|adapter"
git ls-files baselines
git ls-files docs examples
```

Validation commands are recorded in the run log after final validation.
