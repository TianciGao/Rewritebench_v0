# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 32eee7278857894cf76207973c0a58a5ab928fad origin/feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "D034|D035" project_control/DECISION_LOG.md
sed -n '1,220p' .github/workflows/user_entry_smoke.yml
sed -n '1,260p' scripts/dev/run_user_entry_ci_smoke.py
sed -n '1,220p' tests/user_entry/test_calcite_hep_fail_closed_route.py
sed -n '1,220p' baselines/calcite_hep_fail_closed/adapter.py
```

Diagnosis:

```bash
command -v gh && gh run view 488 --repo TianciGao/Rewritebench_v0 --log
git archive HEAD | tar -x -C /tmp/sqlrb_ci_calcite_repro
PYTHONPATH=/tmp/sqlrb_ci_calcite_repro/src PYTHONDONTWRITEBYTECODE=1 \
  pytest /tmp/sqlrb_ci_calcite_repro/tests/user_entry/test_calcite_hep_fail_closed_route.py -q
```

Validation:

```bash
PYTHONPATH=/tmp/sqlrb_ci_calcite_fixed_repro/src PYTHONDONTWRITEBYTECODE=1 \
  pytest /tmp/sqlrb_ci_calcite_fixed_repro/tests/user_entry/test_calcite_hep_fail_closed_route.py -q
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
python scripts/dev/run_user_entry_ci_smoke.py
pytest tests/user_entry -q
python -m py_compile baselines/calcite_hep_fail_closed/adapter.py
git diff --check
git status -sb
git status --short -- reports results output runs/user
```
