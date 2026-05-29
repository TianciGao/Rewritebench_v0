# Command Log

Commands run:

```bash
git status -sb
git branch --show-current
git log --oneline -8
git ls-files project_control
find project_control -maxdepth 1 -type f -print | sort
find project_control -maxdepth 1 -type d -print | sort
sed -n '1,260p' project_control/MIGRATION_MASTER_PLAN.md
tail -n 120 project_control/MIGRATION_STATUS.md
tail -n 160 project_control/MIGRATION_RUN_LOG.md
tail -n 220 project_control/DECISION_LOG.md
sed -n '1,240p' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
sed -n '1,240p' project_control/RELEASE_SURFACE_POLICY_DECISIONS.md
sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
find audits/local_evaluation_workbench_v0_closeout -maxdepth 1 -type f -print | sort
find audits/non_official_local_metrics_calculator_v0 -maxdepth 1 -type f -print | sort
find audits/local_metrics_v0_final_formula_decision_v0 -maxdepth 1 -type f -print | sort
sed -n '1,220p' audits/local_evaluation_workbench_v0_closeout/README.md
sed -n '1,220p' audits/non_official_local_metrics_calculator_v0/README.md
sed -n '1,220p' audits/local_metrics_v0_final_formula_decision_v0/README.md
sed -n '1,260p' docs/user_entry_checker_policy.md
sed -n '1,260p' repository_spec/timing_artifact_schema_v0_draft.md
mkdir -p audits/project_control_hygiene_v0/retired_project_control_docs
git mv project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md audits/project_control_hygiene_v0/retired_project_control_docs/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
git mv project_control/RELEASE_SURFACE_POLICY_DECISIONS.md audits/project_control_hygiene_v0/retired_project_control_docs/RELEASE_SURFACE_POLICY_DECISIONS.md
git mv project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md audits/project_control_hygiene_v0/retired_project_control_docs/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
git ls-files project_control
find project_control -maxdepth 1 -type f -print | sort
find project_control -maxdepth 1 -type d -print | sort
```

Validation commands are recorded after execution in the final report.

Validation commands run:

```bash
python - <<'PY'
from pathlib import Path
for path in [
    'project_control/MIGRATION_MASTER_PLAN.md',
    'project_control/MIGRATION_STATUS.md',
    'project_control/MIGRATION_RUN_LOG.md',
    'project_control/DECISION_LOG.md',
]:
    text = Path(path).read_text(encoding='utf-8')
    assert text.strip(), path
    print(f'OK {path}: {len(text.splitlines())} lines')
PY

python - <<'PY'
import csv
from pathlib import Path
for path in sorted(Path('audits/project_control_hygiene_v0').glob('*.csv')):
    with path.open(newline='', encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
        assert rows, path
        assert all(None not in row for row in rows), path
    print(f'OK {path}: {len(rows)} rows')
PY

python - <<'PY'
from pathlib import Path
mds = sorted(Path('audits/project_control_hygiene_v0').glob('*.md')) + [
    Path('project_control/DECISION_LOG.md'),
    Path('project_control/MIGRATION_STATUS.md'),
    Path('project_control/MIGRATION_RUN_LOG.md'),
]
for path in mds:
    text = path.read_text(encoding='utf-8')
    assert text.strip(), path
    assert any(line.startswith('#') for line in text.splitlines()), path
    print(f'OK {path}')
PY

git diff --check
git diff --name-only
git diff --cached --name-only
find project_control -maxdepth 1 -type f -print | sort
find project_control -maxdepth 1 -type d -print | sort
```

Validation result: passed at audit creation time.
