# Command Log

Commands run:

```bash
git status -sb
git branch --show-current
git log --oneline -8
rg --files repository_spec 2>/dev/null | sort || true
find project_control -maxdepth 1 -type f -print | sort
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -n 100 project_control/MIGRATION_STATUS.md
tail -n 140 project_control/MIGRATION_RUN_LOG.md
tail -n 180 project_control/DECISION_LOG.md
find audits/project_control_hygiene_v0 -maxdepth 2 -type f -print | sort
find audits/local_evaluation_workbench_v0_closeout -maxdepth 1 -type f -print | sort
sed -n '1,240p' repository_spec/public_release_surface_policy_v1.md
sed -n '1,240p' repository_spec/public_runner_output_policy_v1_draft.md
sed -n '1,220p' repository_spec/canonical_case_package_layout_v1.md
sed -n '1,220p' repository_spec/timing_artifact_schema_v0_draft.md
sed -n '1,180p' audits/project_control_hygiene_v0/README.md
sed -n '1,180p' audits/local_evaluation_workbench_v0_closeout/README.md
find . -maxdepth 1 -mindepth 1 -printf '%f\n' | sort
test -e audits/final_public_layout_target_decision_v0 && find audits/final_public_layout_target_decision_v0 -maxdepth 2 -print | sort || true
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
paths = sorted(Path('audits/final_public_layout_target_decision_v0').glob('*.md')) + [
    Path('project_control/DECISION_LOG.md'),
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
git status --porcelain=v1
test -d output && find output -maxdepth 3 -print | sort || true
test -d benchmarks && find benchmarks -maxdepth 3 -print | sort || true
```

Validation result: passed at audit creation time.
