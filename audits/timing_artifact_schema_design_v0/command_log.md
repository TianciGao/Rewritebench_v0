# Command Log

Commands run for this task:

```bash
git status -sb
git branch --show-current
git log --oneline -5
rg -n "latest_paper_metrics_timing_protocol_alignment_v0|D032|Timing|metrics_timing_skill_adapter" project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md project_control/DECISION_LOG.md
ls -1 audits/latest_paper_metrics_timing_protocol_alignment_v0
ls -1 audits/metrics_timing_skill_adapter_decision_record_v0
ls -1 repository_spec | sort
tail -n 120 project_control/MIGRATION_STATUS.md
tail -n 120 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' audits/latest_paper_metrics_timing_protocol_alignment_v0/proposed_timing_artifact_schema.md
sed -n '1,220p' audits/latest_paper_metrics_timing_protocol_alignment_v0/timing_protocol_alignment.md
sed -n '1,220p' audits/latest_paper_metrics_timing_protocol_alignment_v0/proposed_metrics_input_schema.md
sed -n '1,220p' audits/latest_paper_metrics_timing_protocol_alignment_v0/open_questions_for_human.md
mkdir -p audits/timing_artifact_schema_design_v0
```

Validation commands:

```bash
git diff --check
python - <<'PY'
from pathlib import Path
files = [
    Path('project_control/MIGRATION_STATUS.md'),
    Path('project_control/MIGRATION_RUN_LOG.md'),
    Path('project_control/DECISION_LOG.md'),
]
for path in files:
    text = path.read_text(encoding='utf-8')
    assert text.strip(), path
    print(f'OK {path} lines={len(text.splitlines())}')
PY
python - <<'PY'
from pathlib import Path
paths = sorted(Path('audits/timing_artifact_schema_design_v0').glob('*.md')) + [Path('repository_spec/timing_artifact_schema_v0_draft.md')]
for path in paths:
    text = path.read_text(encoding='utf-8')
    assert text.startswith('#'), f'{path} missing top-level heading'
    assert '\t' not in text, f'{path} contains tab'
    print(f'OK {path} lines={len(text.splitlines())}')
PY
python - <<'PY'
import subprocess
allowed_prefixes = (
    'audits/timing_artifact_schema_design_v0/',
    'project_control/MIGRATION_STATUS.md',
    'project_control/MIGRATION_RUN_LOG.md',
    'repository_spec/timing_artifact_schema_v0_draft.md',
)
changed = subprocess.check_output(['git','diff','--name-only'], text=True).splitlines()
for path in changed:
    if not any(path == p or path.startswith(p) for p in allowed_prefixes):
        raise SystemExit(f'protected surface changed: {path}')
print('OK protected surface changed files:')
for path in changed:
    print(path)
PY
git status -sb
python - <<'PY'
import subprocess
allowed_prefixes = (
    'audits/timing_artifact_schema_design_v0/',
    'project_control/MIGRATION_STATUS.md',
    'project_control/MIGRATION_RUN_LOG.md',
    'repository_spec/timing_artifact_schema_v0_draft.md',
)
changed = set(subprocess.check_output(['git','diff','--name-only'], text=True).splitlines())
status = subprocess.check_output(['git','status','--porcelain'], text=True).splitlines()
for line in status:
    path = line[3:] if line.startswith('?? ') else line[3:]
    changed.add(path)
for path in sorted(changed):
    if not any(path == p or path.startswith(p) for p in allowed_prefixes):
        raise SystemExit(f'protected surface changed: {path}')
print('OK protected surface including untracked:')
for path in sorted(changed):
    print(path)
PY
git status --porcelain -- runs/user
```

Validation result:

- `git diff --check`: passed.
- Project-control readability check: passed.
- Audit Markdown and draft spec sanity check: passed.
- Protected-surface check including untracked files: passed.
- `runs/user/` committed-output check: passed with no output.
- `git status -sb` showed only intended modified project-control files and intended untracked audit/spec files before staging.
