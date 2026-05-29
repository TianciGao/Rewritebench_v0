# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git merge-base --is-ancestor a91884b4778d3acd348026421ac59bc19c9aa838 HEAD
git merge-base --is-ancestor 39d3bb43d96a138e3446b56a4ded1ce2b0b5f111 HEAD
rg -n "D033|local_metrics_output_shape_review_v0|non_official_local_metrics_calculator_v0" \
  project_control/DECISION_LOG.md project_control/MIGRATION_RUN_LOG.md project_control/MIGRATION_STATUS.md
git log --oneline -8
```

Context read:

```bash
project_control/MIGRATION_MASTER_PLAN.md
project_control/MIGRATION_STATUS.md
project_control/MIGRATION_RUN_LOG.md
project_control/DECISION_LOG.md
project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
audits/non_official_local_metrics_calculator_v0/
audits/local_metrics_output_shape_review_v0/
audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/
audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/
src/sql_rewrite_bench/local_metrics.py
scripts/dev/compute_local_user_metrics.py
tests/user_entry/test_local_metrics.py
```

Input run discovery:

```bash
rg -n "runs/user|common_core_sqlglot_noop|after_statement" \
  audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0 \
  audits/common_core_spark_sqlglot_noop_after_statement_patch_v0 \
  audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0 \
  project_control/MIGRATION_STATUS.md
find runs/user -maxdepth 2 -name ledger.csv
```

Projection command:

```bash
PYTHONPATH=src python scripts/dev/compute_local_user_metrics.py \
  --run runs/user/common_core_sqlglot_noop_postgres_snapshot \
  --run runs/user/common_core_sqlglot_noop_mysql_snapshot \
  --run runs/user/common_core_spark_sqlglot_noop_after_statement_patch
```

Result:

- `runs/user/common_core_sqlglot_noop_postgres_snapshot/metrics/` written.
- `runs/user/common_core_sqlglot_noop_mysql_snapshot/metrics/` written.
- `runs/user/common_core_spark_sqlglot_noop_after_statement_patch/metrics/` written.

No Common-core user-run rerun, SQLGlot optimize run, or timing collection was performed.

Validation:

```bash
python - <<'PY'
# Project-control readability check.
PY
python - <<'PY'
# Audit CSV/Markdown/JSON sanity checks.
PY
git diff --check
python - <<'PY'
# Protected-surface diff check.
PY
git status -sb
```

Validation results:

- Project-control readability: passed.
- Audit CSV sanity: passed.
- Audit Markdown sanity: passed.
- `git diff --check`: passed.
- Protected-surface tracked diff check: passed.
- `runs/user/` outputs committed: no.
