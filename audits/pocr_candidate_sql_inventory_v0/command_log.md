# Command Log

Commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`.

Preflight and project-control review:

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
tail -n 220 project_control/DECISION_LOG.md
tail -n 160 project_control/MIGRATION_RUN_LOG.md
```

Read-only candidate SQL discovery:

```bash
find runs/user -type d -name candidate_sql | sort
sed -n '1,120p' case_sets/common_core_v0/cases.csv
find runs/user -maxdepth 3 -type d | sort | sed -n '1,240p'
find runs/user -type f -path '*/candidate_sql/*' | sed -n '1,80p'
```

Audit CSV generation:

```bash
python - <<'PY'
# Inline read-only inventory generator:
# - scanned runs/user/**/candidate_sql roots
# - parsed CASE_ID__engine.sql filenames
# - resolved Common-core case membership from case_sets/common_core_v0/cases.csv
# - computed SHA-256 digests read-only
# - wrote candidate_root_inventory.csv, candidate_file_inventory.csv, and candidate_sha256_manifest.csv
PY
```

Inventory review:

```bash
python - <<'PY'
# Summarized roots, files, PG40-complete roots, Track-A-family-complete roots, and ambiguous roots.
PY
wc -l audits/pocr_candidate_sql_inventory_v0/*.csv
du -h audits/pocr_candidate_sql_inventory_v0/*.csv
sed -n '1,12p' audits/pocr_candidate_sql_inventory_v0/candidate_root_inventory.csv
sed -n '1,12p' audits/pocr_candidate_sql_inventory_v0/candidate_file_inventory.csv
python - <<'PY'
# Rewrote generated CSVs with LF line endings after git diff --check flagged CRLF from csv.writer defaults.
PY
```

Final validation:

```bash
python - <<'PY'
import csv
from pathlib import Path
files = [
    Path('audits/pocr_candidate_sql_inventory_v0/candidate_root_inventory.csv'),
    Path('audits/pocr_candidate_sql_inventory_v0/candidate_file_inventory.csv'),
    Path('audits/pocr_candidate_sql_inventory_v0/candidate_sha256_manifest.csv'),
]
for path in files:
    rows = list(csv.DictReader(path.open(newline='', encoding='utf-8')))
    assert rows, path
    print(f'{path}: rows={len(rows)} columns={len(rows[0])}')
root_rows = list(csv.DictReader(files[0].open(newline='', encoding='utf-8')))
file_rows = list(csv.DictReader(files[1].open(newline='', encoding='utf-8')))
assert len(root_rows) == 1660, len(root_rows)
assert len(file_rows) == 2377, len(file_rows)
assert sum(r['pg40_complete'] == 'yes' for r in root_rows) == 5
assert sum(r['track_a_120_complete'] == 'yes' for r in root_rows) == 6
print('csv_parse_and_inventory_count_checks_passed')
PY

python - <<'PY'
from pathlib import Path
paths = [
    Path('audits/pocr_candidate_sql_inventory_v0/README.md'),
    Path('audits/pocr_candidate_sql_inventory_v0/route_mapping_review.md'),
    Path('audits/pocr_candidate_sql_inventory_v0/preservation_risk_review.md'),
    Path('audits/pocr_candidate_sql_inventory_v0/recommended_next_routes.md'),
    Path('audits/pocr_candidate_sql_inventory_v0/protected_path_review.md'),
    Path('audits/pocr_candidate_sql_inventory_v0/command_log.md'),
]
for p in paths:
    assert p.exists(), p
    assert p.read_text(encoding='utf-8').strip(), p
print('markdown_non_empty_passed')
PY

git diff --name-only | rg '^(cases/|output/|reports/|results/|runs/)|/skills\.md$|/skill/' || true
git status --short runs/user | sed -n '1,40p'
git diff --name-status -- runs/user cases output reports results || true
test ! -e output && echo 'repo_output_absent' || { echo 'repo_output_exists'; find output -maxdepth 3 -type f | head -20; }
git diff --check
git diff --cached --check

python - <<'PY'
import csv
from pathlib import Path
for path in [
    Path('audits/pocr_candidate_sql_inventory_v0/candidate_root_inventory.csv'),
    Path('audits/pocr_candidate_sql_inventory_v0/candidate_file_inventory.csv'),
    Path('audits/pocr_candidate_sql_inventory_v0/candidate_sha256_manifest.csv'),
]:
    rows = list(csv.DictReader(path.open(newline='', encoding='utf-8')))
    assert rows, path
print('csv_parse_after_lf_normalization_passed')
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

- CSV parse checks passed for all three audit CSV files.
- Inventory count checks passed: 1,660 candidate roots, 2,377 candidate files, 5 PG40-complete PostgreSQL roots, and 6 Track-A-120-complete route-family component roots.
- Markdown non-empty checks passed.
- Candidate inventory was read-only: no `runs/user` or `runs/user/**/candidate_sql` diff/status changes were present.
- Repository `output/` was absent.
- Protected-path review passed: no `cases/`, `skills.md`, `skill/`, `output/`, top-level `reports/`, top-level `results/`, or `runs/` files were modified.
- `git diff --check` passed after CSV LF normalization and Markdown trailing-space cleanup.
- `git diff --cached --check` passed.
- CSV parse checks passed after LF normalization.
- Changed-file secret value scan passed.
- Staged protected-path review passed.
- Staged secret value scan passed.
