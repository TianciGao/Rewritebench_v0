# Command Log

Commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`.

Preflight and read-only review:

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
tail -n 120 project_control/MIGRATION_RUN_LOG.md
rg --files src/sql_rewrite_bench/pocr tests/pocr src/cli | sort
sed -n '1,260p' src/sql_rewrite_bench/pocr/__init__.py
sed -n '1,60p' src/sql_rewrite_bench/pocr/live_smoke.py
sed -n '1,60p' src/sql_rewrite_bench/pocr/calibration_runner.py
sed -n '1,60p' src/sql_rewrite_bench/pocr/real_route_diagnostic_runner.py
sed -n '1,60p' src/sql_rewrite_bench/pocr/stage_b_static_runner.py
sed -n '1,60p' src/sql_rewrite_bench/pocr/draft_runner.py
sed -n '1,60p' src/sql_rewrite_bench/pocr/pocr_row.py
sed -n '1,220p' src/cli/pocr_diagnostic.py
sed -n '1,180p' src/cli/main.py
```

Final validation:

```bash
python - <<'PY'
from pathlib import Path
paths = [
    Path('src/sql_rewrite_bench/pocr/README.md'),
    Path('audits/pocr_package_boundary_cleanup_v0/README.md'),
    Path('audits/pocr_package_boundary_cleanup_v0/public_internal_boundary.md'),
    Path('audits/pocr_package_boundary_cleanup_v0/audit_only_helpers_review.md'),
    Path('audits/pocr_package_boundary_cleanup_v0/init_export_review.md'),
    Path('audits/pocr_package_boundary_cleanup_v0/protected_path_review.md'),
    Path('audits/pocr_package_boundary_cleanup_v0/command_log.md'),
]
for p in paths:
    assert p.exists(), p
    assert p.read_text(encoding='utf-8').strip(), p
print('markdown_non_empty_passed')
PY

python - <<'PY'
import csv
from pathlib import Path
path = Path('audits/pocr_package_boundary_cleanup_v0/package_map.csv')
rows = list(csv.DictReader(path.open(newline='', encoding='utf-8')))
expected = ['module','category','public_or_internal','short_purpose','safe_for_user_entry','audit_only','notes']
assert rows, 'empty package map'
assert list(rows[0].keys()) == expected, rows[0].keys()
assert any(r['module'] == 'src/cli/pocr_diagnostic.py' for r in rows)
assert any(r['audit_only'] == 'yes' for r in rows)
print(f'package_map_csv_parse_passed rows={len(rows)}')
PY

python - <<'PY'
from pathlib import Path
text = Path('src/sql_rewrite_bench/pocr/README.md').read_text(encoding='utf-8')
phrases = [
    'This is not official POCR.',
    'No route-level POCR score is emitted.',
    'No paper-facing metric is promoted.',
    'Stage A annotation alone is not counted.',
    'Stage B transformation-aware validation is diagnostic only.',
    'Semantic guard atoms are not part of operation coverage numerator.',
    'No global leaderboard is produced.',
]
missing = [p for p in phrases if p not in text]
assert not missing, missing
print('required_boundary_phrases_passed')
PY

python - <<'PY'
import subprocess
changed = subprocess.check_output(['git','diff','--name-only'], text=True).splitlines()
touched_py = [p for p in changed if p.endswith('.py')]
if touched_py:
    raise SystemExit('unexpected touched Python files: ' + ', '.join(touched_py))
print('py_compile_touched_python_not_applicable_no_touched_py_files')
PY

PYTHONPATH=src pytest tests/pocr -q
PYTHONPATH=src pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
git diff --check

python - <<'PY'
import subprocess
names = subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()
blocked = []
for name in names:
    if name.startswith(('cases/', 'output/', 'reports/', 'results/', 'runs/', 'retained_evidence/')) or name.endswith('/skills.md') or '/skill/' in name:
        blocked.append(name)
if blocked:
    print('\n'.join(blocked))
    raise SystemExit(1)
print('protected_path_review_passed')
PY

python - <<'PY'
import re, subprocess, sys
files = subprocess.check_output(['git','diff','--name-only'], text=True).splitlines()
patterns = [
    re.compile(r'sk-[A-Za-z0-9_-]{20,}'),
    re.compile(r'Bearer\s+[A-Za-z0-9._-]{20,}', re.I),
    re.compile(r'(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*["\']?[A-Za-z0-9_./+=-]{20,}'),
]
hits=[]
for name in files:
    try:
        text=open(name, encoding='utf-8').read()
    except Exception:
        continue
    for i,line in enumerate(text.splitlines(),1):
        for pat in patterns:
            if pat.search(line):
                hits.append(f'{name}:{i}:{line[:160]}')
if hits:
    print('\n'.join(hits))
    sys.exit(1)
print('changed_file_secret_value_scan_passed')
PY

git diff --cached --check
python - <<'PY'
import subprocess
names = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()
blocked = []
for name in names:
    if name.startswith(('cases/', 'output/', 'reports/', 'results/', 'runs/', 'retained_evidence/')) or name.endswith('/skills.md') or '/skill/' in name:
        blocked.append(name)
if blocked:
    print('\n'.join(blocked))
    raise SystemExit(1)
print('staged_protected_path_review_passed')
PY
python - <<'PY'
import re, subprocess, sys
files = subprocess.check_output(['git','diff','--cached','--name-only'], text=True).splitlines()
patterns = [
    re.compile(r'sk-[A-Za-z0-9_-]{20,}'),
    re.compile(r'Bearer\s+[A-Za-z0-9._-]{20,}', re.I),
    re.compile(r'(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*["\']?[A-Za-z0-9_./+=-]{20,}'),
]
hits=[]
for name in files:
    try:
        blob = subprocess.check_output(['git','show',f':{name}'], text=True, stderr=subprocess.DEVNULL)
    except Exception:
        continue
    for i,line in enumerate(blob.splitlines(),1):
        for pat in patterns:
            if pat.search(line):
                hits.append(f'{name}:{i}:{line[:160]}')
if hits:
    print('\n'.join(hits))
    sys.exit(1)
print('staged_secret_value_scan_passed')
PY
```

Results:

- Markdown non-empty checks passed.
- `package_map.csv` parsed with 25 rows.
- Required package README boundary phrases passed.
- Python compile for touched Python files: not applicable; no Python files were touched.
- `pytest tests/pocr -q`: 92 passed.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`: 28 passed.
- `git diff --check` passed.
- Protected-path review passed.
- Changed-file secret value scan passed.
- Staged `git diff --cached --check` passed.
- Staged protected-path review passed.
- Staged secret value scan passed.
