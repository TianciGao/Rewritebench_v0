# Command Log

Preflight and inspection:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
rg -n "D033|D034|D035" project_control/DECISION_LOG.md
find audits/sqlglot_user_adapter_bounded_smoke_v0 audits/sqlglot_optimize_cons0005_triage_v0 audits/track_a_120_rerun_readiness_plan_v0 -maxdepth 1 -type d
sed -n '1,260p' baselines/sqlglot/sqlglot_user_adapter.py
sed -n '1,280p' tests/user_entry/test_sqlglot_adapter.py
sed -n '1,360p' tests/user_entry/test_local_timing.py
sed -n '1,220p' cases/CONS/CONS_0005/manifest.yaml
sed -n '1,240p' schemas/calcite_core_sql_tests_cons0005_v0/schema_profile.yaml
```

SQLGlot optimizer reproduction:

```bash
python - <<'PY'
# Reproduced context-free and schema-aware SQLGlot optimize output for CONS_0005.
PY
```

Bounded smoke:

```bash
python - <<'PY'
# Ran sqlglot_user_adapter.py --route optimize_schema_aware for
# CONS_0005, PERF_0006, and CONS_0036 across postgres/mysql/spark.
# Wrote runtime artifacts under /tmp/sqlrb_sqlglot_optimize_schema_aware_route_design_fix_v0/.
PY
```

Validation run so far:

```bash
python - <<'PY'
# Validated per_row_smoke_status.csv headers/row count and diagnostic_summary.json.
PY
find audits/sqlglot_optimize_schema_aware_route_design_fix_v0 -name '*.md' -type f -empty -print
pytest tests/user_entry/test_sqlglot_adapter.py tests/user_entry/test_local_timing.py -q
python -m py_compile baselines/sqlglot/sqlglot_user_adapter.py tests/user_entry/test_sqlglot_adapter.py tests/user_entry/test_local_timing.py
git diff --check
git status -sb
git status --porcelain -- runs/user output reports results cases case_sets schemas inventory src
```
