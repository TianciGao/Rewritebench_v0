# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin
git merge-base --is-ancestor 6184616a86b33fa964763f72dfa4e1ba3ed1f951 origin/feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg 'D032|D033|D034|D035' project_control/DECISION_LOG.md
test -d audits/verieql_bound4_pg_noop_all_exact_attempt_v0
test -d runs/user/common_core_pg_noop_db_checker
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
test -x /home/tianci_gao/.venvs/sqlrb-verieql/bin/python
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Source and checker inspection:

```bash
python - <<'PY'
# Loaded LONGTAIL_0023 ledger row and compared source/candidate SQL hashes.
PY
diff -u cases/LONGTAIL/LONGTAIL_0023/sql/source.sql runs/user/common_core_pg_noop_db_checker/candidate_sql/LONGTAIL_0023__postgres.sql
sed -n '1,220p' cases/LONGTAIL/LONGTAIL_0023/sql/source.sql
sed -n '1,220p' cases/LONGTAIL/LONGTAIL_0023/checker/checker.yaml
sed -n '1,220p' cases/LONGTAIL/LONGTAIL_0023/checker/normalization.yaml
sed -n '1,220p' cases/LONGTAIL/LONGTAIL_0023/checker/compare_config.yaml
wc -l runs/user/common_core_pg_noop_db_checker/workspaces/LONGTAIL_0023/postgres/execution/source_result.jsonl runs/user/common_core_pg_noop_db_checker/workspaces/LONGTAIL_0023/postgres/execution/candidate_result.jsonl
head -5 runs/user/common_core_pg_noop_db_checker/workspaces/LONGTAIL_0023/postgres/execution/source_result.jsonl
head -5 runs/user/common_core_pg_noop_db_checker/workspaces/LONGTAIL_0023/postgres/execution/candidate_result.jsonl
```

VeriEQL rechecks:

```bash
python - <<'PY'
# Ran source-candidate at bounds 1, 2, 3, 4.
# Ran source-source at bound 4.
# Ran candidate-candidate at bound 4.
# Runtime output root:
# /tmp/sqlrb_verieql_longtail0023_non_equivalent_triage_v0/
# Wrote recheck_matrix.csv under this audit packet.
PY
```

Validation:

```bash
python - <<'PY'
# Verified 11 Markdown files are non-empty.
# Verified recheck_matrix.csv has 6 data rows.
PY
git diff --check
git status -sb
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```
