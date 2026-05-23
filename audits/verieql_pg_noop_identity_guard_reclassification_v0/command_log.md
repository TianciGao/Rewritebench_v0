# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin
git merge-base --is-ancestor 84e918c5faf3d0c1f3e908d39308cb50e6b3b149 origin/feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg 'D032|D033|D034|D035' project_control/DECISION_LOG.md
test -d audits/verieql_bound4_pg_noop_all_exact_attempt_v0
test -d audits/verieql_longtail0023_non_equivalent_triage_v0
test -d runs/user/common_core_pg_noop_db_checker
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
test -x /home/tianci_gao/.venvs/sqlrb-verieql/bin/python
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Identity checks and reclassification:

```bash
python - <<'PY'
# Loaded prior per-row source-vs-candidate verdicts.
# Ran 35 source-vs-source identity checks in one VeriEQL finite-bound batch.
# Ran 35 candidate-vs-candidate identity checks in one VeriEQL finite-bound batch.
# Wrote:
#   per_row_identity_recheck.csv
#   reclassified_verdicts.csv
#   reclassified_summary.json
# Runtime output root:
#   /tmp/sqlrb_verieql_pg_noop_identity_guard_reclassification_v0/
PY
```

Review:

```bash
python - <<'PY'
# Reviewed identity guard counts, corrected verdict counts, and summary JSON.
PY
```

Validation:

```bash
python - <<'PY'
# Verified 9 Markdown files are non-empty.
# Verified per_row_identity_recheck.csv has 70 data rows.
# Verified reclassified_verdicts.csv has 40 data rows.
# Verified reclassified_summary.json parses with identity_checked_rows=35 and corrected_decidable_count=4.
PY
git diff --check
git status -sb
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```
