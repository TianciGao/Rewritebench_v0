# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 6cdd552aa39b449b158b992cbc1df3e8582c8f85 origin/feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "D034|D035" project_control/DECISION_LOG.md
find baselines -maxdepth 4 -type f -print
rg -n "calcite_hep_fail_closed|calcite_hep_fail_closed_adapter|SQLRB_CALCITE_HEP|CALCITE_HEP" src tests baselines audits/calcite_hep_fail_closed_user_route_scaffold_v0 pyproject.toml docs scripts repository_spec .github
```

Validation:

```bash
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
pytest tests/user_entry -q
python -m py_compile baselines/calcite_hep_fail_closed/adapter.py src/sql_rewrite_bench/local_timing.py
python -m cli.main user evaluate --case-set common_core_v0 --pool all --engines postgres --case-list /tmp/sqlrb_calcite_hep_baseline_layout_contract_v0/case_list.txt --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" --output-root /tmp/sqlrb_calcite_hep_baseline_layout_contract_v0/d035_output --run-id calcite_hep_layout_smoke --adapter-timeout 10
```

Final checks:

```bash
git diff --check
git status -sb
git status --short -- reports results output runs/user
```
