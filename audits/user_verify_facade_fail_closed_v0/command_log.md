# Command Log

Preflight:

```bash
git status -sb
rg -n "D034|D035" project_control/DECISION_LOG.md
test -f src/cli/main.py
test -f src/sql_rewrite_bench/verifier_support/verieql.py
test -f src/sql_rewrite_bench/verifier_support/sqlsolver.py
test -d audits/verifier_support_fail_closed_closeout_v0
git merge-base --is-ancestor 3041c8bf467fc42626a594fa608c2bb9e95ae5ab HEAD
```

Required reads:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -n 180 project_control/MIGRATION_STATUS.md
tail -n 180 project_control/MIGRATION_RUN_LOG.md
sed -n '900,1130p' project_control/DECISION_LOG.md
sed -n '1,260p' repository_spec/verifier_support_output_contract_v0_draft.md
sed -n '1,260p' repository_spec/user_output_contract_v0_draft.md
find audits/verifier_support_output_contract_plan_v0 audits/verifier_support_synthetic_fixture_v1 audits/verieql_bounded_canary_v2 audits/sqlsolver_bounded_smoke_v3 audits/verifier_support_fail_closed_closeout_v0 -maxdepth 1 -type f -print
sed -n '1,420p' src/cli/main.py
find src/sql_rewrite_bench/verifier_support -maxdepth 1 -type f -print
sed -n '1,260p' src/sql_rewrite_bench/user_output.py
```

Validation:

```bash
PYTHONPATH=src pytest tests/user_entry/test_cli_facade.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile src/cli/main.py
tmp=$(mktemp -d) && \
  PYTHONPATH=src python -m cli.main user verify --run-id smoke_verieql --tool verieql --tool-cmd /definitely/missing/verieql --output-root "$tmp/output" && \
  PYTHONPATH=src python -m cli.main user verify --run-id smoke_sqlsolver --tool sqlsolver --tool-cmd /definitely/missing/sqlsolver --output-root "$tmp/output" && \
  find "$tmp/output" -maxdepth 4 -type f | sort && \
  rm -rf "$tmp"
python - <<'PY'  # project-control readability
...
PY
python - <<'PY'  # audit Markdown sanity
...
PY
git diff --check
python - <<'PY'  # protected-surface check
...
PY
git status --short -- runs/user output reports results
```
