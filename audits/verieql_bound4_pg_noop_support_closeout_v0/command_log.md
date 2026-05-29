# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin
git merge-base --is-ancestor 0695309e52acf3dac4766a065b98db12abd1c957 origin/feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg 'D032|D033|D034|D035' project_control/DECISION_LOG.md
test -d audits/verieql_finite_bound_wrapper_mode_v0
test -d audits/verieql_exact_candidate_tiny_local_pass_v0
test -d audits/verieql_one_baseline_feature_aware_subset_plan_v0
test -d audits/verieql_ddl_parameterized_type_parser_hardening_v0
test -d audits/verieql_cons0036_cons0037_two_row_exact_candidate_pass_v0
test -d audits/verieql_cons0037_bound_timeout_policy_probe_v0
test -d audits/verieql_bound4_two_row_uniform_policy_pass_v0
test -d audits/verieql_bound4_feature_aware_subset_plan_v0
test -d audits/verieql_bound4_pg_noop_all_exact_attempt_v0
test -d audits/verieql_longtail0023_non_equivalent_triage_v0
test -d audits/verieql_pg_noop_identity_guard_reclassification_v0
test -d runs/user/common_core_pg_noop_db_checker
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Closeout review:

```bash
python - <<'PY'
# Read existing summary JSON and CSV artifacts from prior VeriEQL audits.
# No new VeriEQL pairs were run.
PY
```

Validation:

```bash
python - <<'PY'
# Verified 11 Markdown files are non-empty.
# Verified verieql_pg_noop_support_summary.json parses.
# Verified verieql_pg_noop_support_summary.csv has 1 data row.
PY
git diff --check
git status -sb
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```
