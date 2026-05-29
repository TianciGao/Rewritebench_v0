# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 0191b6425638eef72f494bdd5995d508d8de8ff4 HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
java -version
```

Focused tests:

```bash
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
```

Targeted validation:

```bash
ROOT=/tmp/sqlrb_calcite_hep_pg_identifier_quoting_fix_v0
RUN_ID=calcite_hep_pg_identifier_quoting_fix
rm -rf "$ROOT"
mkdir -p "$ROOT"
source scripts/env_postgres.local.sh
SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke \
SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep \
SQLRB_CALCITE_HEP_JAVA=/usr/bin/java \
SQLRB_CALCITE_HEP_TIMEOUT=30 \
python audits/calcite_hep_pg_identifier_quoting_fix_v0/run_targeted_quote_validation.py \
  --output-root "$ROOT" \
  --run-id "$RUN_ID" \
  --adapter-timeout-sec 40 \
  --execution-timeout-sec 40 \
  --db-schema-prefix sqlrb_calcite_quote_fix \
  > "$ROOT/run_stdout.txt" 2> "$ROOT/run_stderr.txt"
```

Final validation commands:

```bash
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
pytest tests/user_entry -q
python -m py_compile baselines/calcite_hep_fail_closed/adapter.py audits/calcite_hep_pg_identifier_quoting_fix_v0/run_targeted_quote_validation.py
python - <<'PY'  # CSV/JSON and audit non-empty sanity
...
PY
git diff --check
git status -sb
git status --porcelain -- runs/user output reports results
git diff --name-only
```
