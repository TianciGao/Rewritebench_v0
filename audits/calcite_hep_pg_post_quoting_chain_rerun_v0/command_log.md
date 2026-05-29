# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor a429bd300137483d504d25b9a6e6d7e5d9fdc14f HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "D033|D034|D035" project_control/DECISION_LOG.md
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py --engine postgres
```

Rerun command:

```bash
ROOT=/tmp/sqlrb_calcite_hep_pg_post_quoting_chain_rerun_v0
RUN_ID=calcite_hep_pg_post_quoting_chain
rm -rf "$ROOT"
mkdir -p "$ROOT"
source scripts/env_postgres.local.sh
SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke \
SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep \
SQLRB_CALCITE_HEP_JAVA=/usr/bin/java \
SQLRB_CALCITE_HEP_TIMEOUT=30 \
python audits/calcite_hep_pg_post_quoting_chain_rerun_v0/run_post_quoting_chain.py \
  --output-root "$ROOT" \
  --run-id "$RUN_ID" \
  --adapter-timeout-sec 40 \
  --execution-timeout-sec 40 \
  --timing-timeout-sec 30 \
  --db-schema-prefix sqlrb_calcite_post_quote \
  > "$ROOT/run_stdout.txt" 2> "$ROOT/run_stderr.txt"
```

Validation:

```bash
python - <<'PY'  # CSV/JSON/Markdown sanity
...
PY
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
python -m py_compile baselines/calcite_hep_fail_closed/adapter.py audits/calcite_hep_pg_post_quoting_chain_rerun_v0/run_post_quoting_chain.py
git diff --check
git status -sb
git status --porcelain -- runs/user output reports results
```
