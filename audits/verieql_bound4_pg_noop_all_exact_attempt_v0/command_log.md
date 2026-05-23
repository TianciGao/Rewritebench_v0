# Command Log

Preflight and source review:

```bash
git status -sb
git branch --show-current
git fetch origin
git merge-base --is-ancestor 2e5af2613d6d4e6729962f4023edb19dac21c604 origin/feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg 'D032|D033|D034|D035' project_control/DECISION_LOG.md
test -d audits/verieql_finite_bound_wrapper_mode_v0
test -d audits/verieql_ddl_parameterized_type_parser_hardening_v0
test -d audits/verieql_cons0037_bound_timeout_policy_probe_v0
test -d audits/verieql_bound4_two_row_uniform_policy_pass_v0
test -d audits/verieql_bound4_feature_aware_subset_plan_v0
test -d runs/user/common_core_pg_noop_db_checker
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
test -x /home/tianci_gao/.venvs/sqlrb-verieql/bin/python
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

Verifier attempt:

```bash
python - <<'PY'
# Loaded runs/user/common_core_pg_noop_db_checker/ledger.csv.
# Loaded audits/verieql_bound4_feature_aware_subset_plan_v0/exact_row_inventory.csv.
# Attempted VeriEQL finite-bound mode one exact row at a time under:
#   bound_size=4, timeout_seconds=30, cores=1.
# Wrote runtime artifacts only under:
#   /tmp/sqlrb_verieql_bound4_pg_noop_all_exact_attempt_v0/
# Wrote audit outputs:
#   per_row_verdicts.csv
#   diagnostic_summary.json
PY
```

Review:

```bash
python - <<'PY'
# Reviewed per-row verdict counts and diagnostic summary.
PY
```

Validation:

```bash
python - <<'PY'
# Verified 11 Markdown files are non-empty.
# Verified per_row_verdicts.csv has 40 data rows and required headers.
# Verified diagnostic_summary.json parses and has selected_rows=40, exact_candidate_rows=35.
PY
git diff --cached --check
python - <<'PY'
# Confirmed cached changed paths are limited to this audit packet and project-control status/log files.
PY
git diff --cached --name-only | rg '^(runs/user/|output/)' || true
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```
