# Command Log

Commands run for this packet:

```bash
git status -sb
git branch --show-current
git status --porcelain -- runs/user output reports results
test -d audits/calcite_hep_pg_post_quoting_chain_rerun_v0
test -f baselines/sqlglot/sqlglot_user_adapter.py
rg -n "D033|D034|D035" project_control/DECISION_LOG.md
git fetch origin main feature/case-package-v2-external-schema
source scripts/env_postgres.local.sh && python scripts/dev/check_local_engine_env.py --engine postgres
git merge-base --is-ancestor b261ee0bde85856ae57bc4e310eadb0fcbdc6cf2 HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
source scripts/env_postgres.local.sh && python audits/sqlglot_noop_pg_current_route_card_refresh_v0/run_sqlglot_noop_pg_route_card.py --output-root /tmp/sqlrb_sqlglot_noop_pg_current_route_card_refresh_v0
python - <<'PY'
# audit Markdown/CSV/JSON sanity check
PY
python -m py_compile audits/sqlglot_noop_pg_current_route_card_refresh_v0/run_sqlglot_noop_pg_route_card.py
git diff --check
git status --porcelain -- runs/user output reports results
git status -sb
```

The `py_compile` command created an audit-local `__pycache__` directory during validation; it was removed before staging.
