# Command Log

Commands run:

```bash
git status -sb
git branch --show-current
find project_control -maxdepth 1 -type f -printf '%f\n' | sort
rg -n '^## D03[45]:' project_control/DECISION_LOG.md
test -d audits/project_control_hygiene_v0 && echo OK_PROJECT_CONTROL_HYGIENE && test -d audits/final_public_layout_target_decision_v0 && echo OK_FINAL_LAYOUT_AUDIT
git log --oneline -6
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -n 90 project_control/MIGRATION_STATUS.md
tail -n 130 project_control/MIGRATION_RUN_LOG.md
sed -n '900,1120p' project_control/DECISION_LOG.md
sed -n '1,220p' docs/user_entry_checker_policy.md
sed -n '1,240p' repository_spec/timing_artifact_schema_v0_draft.md
sed -n '1,220p' audits/project_control_hygiene_v0/README.md
sed -n '1,220p' audits/final_public_layout_target_decision_v0/README.md
sed -n '1,220p' audits/final_public_layout_target_decision_v0/next_step_1_contract_adjustment.md
sed -n '1,220p' audits/local_evaluation_workbench_v0_closeout/README.md
sed -n '1,220p' audits/non_official_local_metrics_calculator_v0/README.md
sed -n '1,220p' audits/common_core_sqlglot_noop_local_metrics_projection_v0/README.md
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
from pathlib import Path
paths = sorted(Path('audits/user_output_and_cli_contract_v0').glob('*.md')) + [
    Path('repository_spec/user_output_contract_v0_draft.md'),
    Path('project_control/MIGRATION_STATUS.md'),
    Path('project_control/MIGRATION_RUN_LOG.md'),
]
for path in paths:
    text = path.read_text(encoding='utf-8')
    assert text.strip(), path
    assert any(line.startswith('#') for line in text.splitlines()), path
    print(f'OK {path}')
PY

git diff --check
git diff --name-only
python - <<'PY'
import subprocess
allowed_prefixes = ('audits/user_output_and_cli_contract_v0/',)
allowed_exact = {
    'project_control/MIGRATION_STATUS.md',
    'project_control/MIGRATION_RUN_LOG.md',
    'repository_spec/user_output_contract_v0_draft.md',
}
paths = subprocess.check_output(['git','diff','--name-only'], text=True).splitlines()
violations = [p for p in paths if not (p in allowed_exact or p.startswith(allowed_prefixes))]
if violations:
    raise SystemExit('Protected surface violations: ' + ', '.join(violations))
print('OK protected surface paths')
PY
git status --porcelain=v1 | rg '^(..|\?\?) (runs/user|output|benchmarks|src|tests|scripts|cases|case_sets|schemas|inventory|baselines|docs|examples|reports|results)/' || true
git status -sb
```

Validation result: passed at audit creation time.
