# Command Log

Preflight:

```bash
git status -sb
find project_control -maxdepth 1 -type f -print | sort
rg -n "D034|D035" project_control/DECISION_LOG.md
test -d audits/final_public_layout_target_decision_v0
```

Required reads and layout inspection:

```bash
rg -n "layout|public|repository|cases/|case_sets/|scripts/|output/|reports/|results/|benchmarks|src/cli|src/dev" project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1013,1105p' project_control/DECISION_LOG.md
find audits/final_public_layout_target_decision_v0 audits/project_control_hygiene_v0 -maxdepth 1 -type f -print | sort
sed -n '1,180p' repository_spec/user_output_contract_v0_draft.md
```

Validation:

```bash
python - <<'PY'  # project-control readability
from pathlib import Path
for path in [
    Path('project_control/MIGRATION_MASTER_PLAN.md'),
    Path('project_control/MIGRATION_STATUS.md'),
    Path('project_control/MIGRATION_RUN_LOG.md'),
    Path('project_control/DECISION_LOG.md'),
]:
    assert path.read_text(encoding='utf-8').strip()
PY
python - <<'PY'  # audit Markdown sanity
from pathlib import Path
for path in sorted(Path('audits/migration_master_plan_d035_layout_sync_v0').glob('*.md')):
    assert path.read_text(encoding='utf-8').strip()
PY
git diff --check
python - <<'PY'  # protected surface check
import subprocess
allowed = (
    ' M project_control/MIGRATION_MASTER_PLAN.md',
    ' M project_control/MIGRATION_RUN_LOG.md',
    ' M project_control/MIGRATION_STATUS.md',
    '?? audits/migration_master_plan_d035_layout_sync_v0/',
)
for line in subprocess.check_output(['git','status','--short','--untracked-files=all'], text=True).splitlines():
    assert line.startswith(allowed), line
PY
find output -maxdepth 3 -type f -print
```
