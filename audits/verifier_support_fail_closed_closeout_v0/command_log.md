# Command Log

Preflight:

```bash
git status -sb
rg -n "D034|D035" project_control/DECISION_LOG.md
test -f repository_spec/verifier_support_output_contract_v0_draft.md
test -f src/sql_rewrite_bench/verifier_support/verieql.py
test -f src/sql_rewrite_bench/verifier_support/sqlsolver.py
test -d audits/verifier_support_synthetic_fixture_v1
test -d audits/verieql_bounded_canary_v2
test -d audits/sqlsolver_bounded_smoke_v3
git merge-base --is-ancestor a39d3ff91895e51283cf7024227d7f1b8f9da209 HEAD
```

Required reads:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -n 220 project_control/MIGRATION_STATUS.md
tail -n 220 project_control/MIGRATION_RUN_LOG.md
sed -n '900,1130p' project_control/DECISION_LOG.md
sed -n '1,260p' repository_spec/verifier_support_output_contract_v0_draft.md
find src/sql_rewrite_bench/verifier_support -maxdepth 1 -type f -print
sed -n '1,320p' src/sql_rewrite_bench/verifier_support/verieql.py
sed -n '1,340p' src/sql_rewrite_bench/verifier_support/sqlsolver.py
sed -n '1,260p' src/cli/main.py
for d in audits/verifier_support_output_contract_plan_v0 audits/verifier_support_synthetic_fixture_v1 audits/verieql_bounded_canary_v2 audits/sqlsolver_bounded_smoke_v3; do sed -n '1,160p' "$d/README.md"; done
```

Validation:

```bash
python - <<'PY'  # project-control readability
...
PY
python - <<'PY'  # audit Markdown sanity
...
PY
python - <<'PY'  # audit CSV sanity
...
PY
git diff --check
python - <<'PY'  # protected-surface check
...
PY
git status --short -- runs/user output reports results
```

No real VeriEQL or SQLSolver command was run.
