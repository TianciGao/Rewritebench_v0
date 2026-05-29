# Command Log

Preflight:

```bash
pwd
git branch --show-current
git rev-parse HEAD
git status -sb
```

Project-control files read:

```bash
cat project_control/MIGRATION_MASTER_PLAN.md >/dev/null
cat project_control/MIGRATION_STATUS.md >/dev/null
cat project_control/DECISION_LOG.md >/dev/null
cat project_control/MIGRATION_RUN_LOG.md >/dev/null
```

Old-machine inventory and existing docs/scripts read:

```bash
sed -n '1,220p' /home/tianci_gao/baseline_runtime_inventory/00_SUMMARY.md
sed -n '1,120p' /home/tianci_gao/baseline_runtime_inventory/08_runtime_copy_reinstall_matrix.csv
sed -n '1,220p' /home/tianci_gao/baseline_runtime_inventory/09_baseline_deployment_profiles.md
sed -n '1,220p' /home/tianci_gao/baseline_runtime_inventory/10_new_machine_action_plan.md
sed -n '1,220p' scripts/setup_dev_env_ubuntu.sh
sed -n '1,220p' scripts/check_dev_env.sh
find baselines -maxdepth 2 -type f | sort
```

Validation commands:

```bash
bash -n scripts/setup_baseline_adapters.sh
bash -n scripts/check_baseline_adapters.sh
bash scripts/check_baseline_adapters.sh --profile all-safe --repo-root .
bash scripts/setup_baseline_adapters.sh --profile all-safe --repo-root . --no-install
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
python - <<'PY'
from pathlib import Path
paths=[Path('docs/baseline_deployment_en_ru.md'), *Path('audits/baseline_quick_deploy_scripts_github_v0').glob('*.md')]
missing=[str(p) for p in paths if not p.exists() or not p.read_text(encoding='utf-8').strip()]
if missing:
    raise SystemExit('empty_or_missing=' + ','.join(missing))
print(f'markdown_non_empty={len(paths)}')
PY
python - <<'PY'
from pathlib import Path
checks = {
    'docs/baseline_deployment_en_ru.md': [
        'adapter is not the same as runtime',
        'No API call is made',
        'No Track A 120 run is performed',
        'Do not commit output/',
        'адаптер не является средой выполнения',
        'API-вызовы не выполняются',
        'Track A 120 не запускается',
        'не добавляйте output/ в коммит',
    ],
    'audits/baseline_quick_deploy_scripts_github_v0/README.md': [
        'No baseline rerun occurred.',
        'No live API call occurred.',
        'No reports/results update occurred.',
        'The scripts distinguish adapters from actual runtimes.',
    ],
}
missing=[]
for path, phrases in checks.items():
    text=Path(path).read_text(encoding='utf-8')
    for phrase in phrases:
        if phrase not in text:
            missing.append(f'{path}: {phrase}')
if missing:
    raise SystemExit('missing_phrases=' + '; '.join(missing))
print('required_phrase_checks=passed')
PY
git diff --check
git status --short -- output reports results cases runs/user project_control/MIGRATION_MASTER_PLAN.md project_control/DECISION_LOG.md
git diff --cached --name-only | grep -E '^(output/|reports/|results/|cases/|runs/user/)|(^|/)skills\.md$|\.sql$|candidate_sql|project_control/MIGRATION_MASTER_PLAN\.md|project_control/DECISION_LOG\.md' || true
python - <<'PY'
import re, subprocess
from pathlib import Path
files=subprocess.check_output(['git','diff','--cached','--name-only'], text=True).splitlines()
patterns=[
    re.compile(r'sk-[A-Za-z0-9_-]{20,}'),
    re.compile(r'Bearer\s+[A-Za-z0-9._-]{20,}', re.I),
    re.compile(r'(?:API_KEY|TOKEN|SECRET|PASSWORD)=(?!<REDACTED>|<set>|<unset>|\$\{|"\$\{|\$)[^\s]+', re.I),
]
findings=[]
for file in files:
    p=Path(file)
    if not p.exists() or p.is_dir():
        continue
    text=p.read_text(encoding='utf-8', errors='ignore')
    for pat in patterns:
        for m in pat.finditer(text):
            findings.append(f'{file}: {m.group(0)[:80]}')
if findings:
    raise SystemExit('potential_secret_findings=' + '; '.join(findings[:20]))
print('staged_secret_scan=passed')
PY
```

Validation results:

- Shell syntax checks: passed.
- `check_baseline_adapters.sh --profile all-safe`: passed, `PASS=21 WARN=0 FAIL=0`.
- `setup_baseline_adapters.sh --profile all-safe --no-install`: passed, `PASS=16 WARN=1 FAIL=0`.
- `pytest tests/pocr -q`: `143 passed in 0.70s`.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`: `31 passed in 0.15s`.
- Changed Python modules: none; `py_compile` not applicable.
- Markdown non-empty: `markdown_non_empty=7`.
- Required phrase checks: passed.
- `git diff --check`: passed.
- Protected path check before staging: only untracked `output/` was present; no top-level `reports/`, `results/`, `cases/`, or `runs/user` changes.
- Staged protected-path scan: passed.
- Staged secret scan: passed.
