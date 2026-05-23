# Command Log

Commands run in the release repository unless otherwise noted.

Preflight and context:

```bash
git status -sb
git branch --show-current
git fetch origin
git merge-base --is-ancestor 6e36d5eb211eb7288552c627902462c4c864564a origin/feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg 'D032|D033|D034|D035' project_control/DECISION_LOG.md
test -d audits/verieql_one_baseline_feature_aware_subset_plan_v0
test -d audits/verieql_ddl_parameterized_type_parser_hardening_v0
test -d audits/verieql_cons0037_bound_timeout_policy_probe_v0
test -d audits/verieql_bound4_two_row_uniform_policy_pass_v0
test -d runs/user/common_core_pg_noop_db_checker
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Inventory and review:

```bash
python - <<'PY'
# Rebuilt exact-row inventory, refreshed feature eligibility matrix,
# and proposed bound4 subset CSVs under this audit packet.
PY
head -5 audits/verieql_bound4_feature_aware_subset_plan_v0/exact_row_inventory.csv
head -8 audits/verieql_bound4_feature_aware_subset_plan_v0/updated_feature_eligibility_matrix.csv
cat audits/verieql_bound4_feature_aware_subset_plan_v0/proposed_bound4_subset.csv
wc -l audits/verieql_bound4_feature_aware_subset_plan_v0/*.csv
rg '^CONS_0036|^CONS_0037' audits/verieql_bound4_feature_aware_subset_plan_v0/*.csv
```

Validation:

```bash
python - <<'PY'
# Verified 11 Markdown files are non-empty.
# Verified CSV row counts:
# exact_row_inventory.csv: 35 rows
# updated_feature_eligibility_matrix.csv: 35 rows
# proposed_bound4_subset.csv: 2 rows
PY
git diff --check
git status --short
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
perl -pi -e 's/\r$//' audits/verieql_bound4_feature_aware_subset_plan_v0/*.csv
git diff --cached --check
```
