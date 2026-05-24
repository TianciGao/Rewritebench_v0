# Command Log

Commands run:

```bash
git status -sb
git branch --show-current
git log --oneline -5
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 81ec6b347c22a13ed710b548d95a9da3770ebe8d HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md | rg 'D033|D034|D035'
gh run view 26357910722 --job 77587924607 --log
sed -n '1,240p' .github/workflows/user_entry_smoke.yml
sed -n '1,260p' scripts/dev/run_user_entry_ci_smoke.py
git diff --name-only 2bc11d08352dff4c81f6bff9852795ebfa1c16a1..HEAD
python scripts/dev/run_user_entry_ci_smoke.py
sed -n '1,180p' tests/user_entry/test_user_run_outputs.py
python -m cli.main user evaluate --help
sed -n '1,260p' docs/USER_BENCHMARK_GUIDE.md
pytest tests/user_entry/test_sqlglot_adapter.py tests/user_entry/test_local_timing.py -q
pytest tests/user_entry -q
python -m py_compile baselines/sqlglot/sqlglot_user_adapter.py
git status --porcelain -- runs/user output reports results
git diff --check
git status -sb
```

Notes:

- `gh` was unavailable, so the full remote CI log could not be retrieved.
- Local reproduction used the workflow command directly.
- No full Track A 120, Common-core experiment, timing pass, verifier pass, metric computation, report/result update, retained-evidence promotion, or leaderboard output was run.
