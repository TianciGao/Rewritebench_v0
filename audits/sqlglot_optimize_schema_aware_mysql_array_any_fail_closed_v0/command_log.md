# Command Log

Preflight and inspection:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 3468e81e388596951bc7677465ab0d789ea3348d HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md | sed -n '1,80p'
git show origin/main:project_control/MIGRATION_STATUS.md | tail -n 40
git show origin/main:project_control/DECISION_LOG.md | rg -n "D033|D034|D035"
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md | sed -n '1,80p'
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md | tail -n 60
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md | rg -n "D033|D034|D035"
test -d audits/sqlglot_optimize_schema_aware_bounded_tri_engine_blocker_triage_v0
test -d baselines/sqlglot
git status --porcelain -- runs/user output reports results
```

Implementation inspection:

```bash
rg --files baselines/sqlglot tests/user_entry | sort
sed -n '1,260p' baselines/sqlglot/sqlglot_user_adapter.py
sed -n '1,260p' tests/user_entry/test_sqlglot_adapter.py
sed -n '260,620p' baselines/sqlglot/sqlglot_user_adapter.py
```

Validation and smoke:

```bash
pytest tests/user_entry/test_sqlglot_adapter.py -q
python -m py_compile baselines/sqlglot/sqlglot_user_adapter.py tests/user_entry/test_sqlglot_adapter.py
PYTHONPATH=src python audits/sqlglot_optimize_schema_aware_mysql_array_any_fail_closed_v0/run_bounded_smoke.py
```

Final validation commands are also recorded in `project_control/MIGRATION_RUN_LOG.md`.

Notes:

- `origin/main` did not contain D033/D034/D035 in the searched decision log; `origin/feature/case-package-v2-external-schema` did.
- Runtime artifacts were written only under `/tmp/sqlrb_sqlglot_optimize_schema_aware_mysql_array_any_fail_closed_v0/`.
