# Command Log

Preflight and repository checks:
- `git status -sb`
- `git branch --show-current`
- `git fetch origin`
- `git merge-base --is-ancestor 0c53cc7d492bc14cf4bf9d97506ce86e002b4976 origin/feature/case-package-v2-external-schema`
- `git show origin/main:project_control/MIGRATION_MASTER_PLAN.md`
- `git show origin/main:project_control/MIGRATION_STATUS.md`
- `git show origin/main:project_control/DECISION_LOG.md`
- `git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md`
- `git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md`
- `git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md`

Workflow inspection:
- `sed -n '1,220p' .github/workflows/user_entry_smoke.yml`
- `sed -n '1,220p' .github/workflows/ledger-fixture-smoke.yml`
- `python - <<'PY' ... yaml.safe_load(...) ... PY`
- `git show --stat --oneline 0c53cc7d492bc14cf4bf9d97506ce86e002b4976 -- .github/workflows`
- `git ls-tree -r --name-only 0c53cc7d492bc14cf4bf9d97506ce86e002b4976 .github/workflows`
- `find . -maxdepth 3 -name .gitmodules -print`
- `git config --get-regexp '^submodule\.'`
- `find . -maxdepth 2 -name .gitattributes -print`

GitHub API inspection:
- Queried `user_entry_smoke.yml` workflow runs for branch `feature/case-package-v2-external-schema`.
- Queried jobs for `user-entry-smoke` run ids `26329489901` and `26329490534`.
- Queried `ledger-fixture-smoke.yml` workflow runs for the same branch.
- Queried jobs for ledger run id `26329489902`.

Validation:
- `python -m pip install -e .`
- `python -m pip install pytest PyYAML`
- `python scripts/dev/run_user_entry_ci_smoke.py`
- `python scripts/dev/smoke_ledger_fixtures.py`

Cleanup of validation-only generated files:
- `git restore audits/ledger_fixture_dev_smoke/ledger_fixture_dev_smoke_report.md`
- `rm -rf src/sql_rewrite_bench.egg-info`

Final validation:
- `python - <<'PY' ... check audit Markdown files are non-empty ... PY`
- `git diff --check`
- `git status --short runs/user output reports results cases case_sets baselines src tests scripts .github/workflows`
- `git status -sb`
- `git status --short`
- `python - <<'PY' ... protected-surface status parser ... PY`
