# Command Log

Preflight:

```text
git status -sb
git branch --show-current
test -d audits/verieql_one_baseline_feature_aware_subset_plan_v0
rg CONS_0037 audits/verieql_one_baseline_feature_aware_subset_plan_v0
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 2a6b9881b19833bd515773010f3aafd301de4c69 HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg D032/D033/D034/D035 project_control/DECISION_LOG.md
```

Focused validation:

```text
pytest tests/user_entry/test_verieql_support.py -q
python -m py_compile src/sql_rewrite_bench/verifier_support/verieql.py
```

CONS_0037 schema-only smoke:

```text
rm -rf /tmp/sqlrb_verieql_ddl_parameterized_type_parser_hardening_v0
mkdir -p /tmp/sqlrb_verieql_ddl_parameterized_type_parser_hardening_v0
PYTHONPATH=src python - <<'PY'
# Wrote a source_vs_candidate VeriEQL JSONL pair for CONS_0037 only.
# Did not invoke VeriEQL.
# Confirmed NAME -> VARCHAR(32) in schema metadata.
PY
```

Final validation commands are recorded in the task final report.

