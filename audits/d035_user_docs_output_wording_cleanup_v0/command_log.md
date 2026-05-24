# Command Log

Preflight and review:

```bash
git status -sb
git branch --show-current
git status --porcelain -- runs/user output reports results
test -d audits/user_surface_d035_layout_inventory_v0
rg -n "D034|D035" project_control/DECISION_LOG.md
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor d441a3fff1d260d391efc57517efe9f39b5c36a1 HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "runs/user|output/results|output/logs|output/reports|output/<run_id>|output/\\{run" README.md docs baselines examples
find docs -maxdepth 3 -type f
find examples -maxdepth 3 -type f
find baselines -maxdepth 3 -type f -name README.md -o -name "*.md"
```

Edits:

```bash
mkdir -p docs/guide docs/spec docs/templates audits/d035_user_docs_output_wording_cleanup_v0
```

Validation:

```bash
find audits/d035_user_docs_output_wording_cleanup_v0 -type f -name "*.md" -print0 | xargs -0 -I{} sh -c 'test -s "$1" || echo empty:$1' sh {}
rg -n "runs/user" README.md docs baselines examples
rg -n "output/results/<run_id>|output/logs/<run_id>|output/reports/<run_id>" README.md docs baselines examples
rg -n "output/<run_id>|output/\\{run" README.md docs baselines examples
git status --porcelain -- runs/user output reports results cases case_sets schemas inventory scripts/dev src tests
git diff --check
git status -sb
```

Validation result:

- All audit Markdown files are non-empty.
- D035 output roots are documented.
- `runs/user` mentions in user-facing docs are internal transitional staging or runner-managed staging.
- No `output/<run_id>` legacy shape remains in the reviewed user docs.
- Protected runtime/source/test/data surfaces showed no changes.
- `git diff --check` passed.
