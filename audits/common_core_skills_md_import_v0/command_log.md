# Command Log

Required pre-edit confirmation:

```bash
pwd
git branch --show-current
git status -sb
ls -lh /home/tianci_gao/code/Rewritebench_v0/cases.zip
sed -n '1,180p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
```

Membership and zip inspection:

```bash
sed -n '1,80p' case_sets/common_core_v0/cases.csv
find cases -maxdepth 2 -type d | head -80
find cases -path '*/skills.md' -type f | sort | head -50
python - <<'PY'
import zipfile
from pathlib import Path
zp=Path('/home/tianci_gao/code/Rewritebench_v0/cases.zip')
with zipfile.ZipFile(zp) as z:
    names=z.namelist()
print('zip_entries', len(names))
for name in names[:40]:
    print(name)
PY
```

Structured zip safety and Common-core exact-match check:

```bash
python - <<'PY'
import csv, zipfile, posixpath
from pathlib import Path
from collections import Counter
zip_path=Path('/home/tianci_gao/code/Rewritebench_v0/cases.zip')
cc=[]
with Path('case_sets/common_core_v0/cases.csv').open(newline='') as f:
    for row in csv.DictReader(f):
        cc.append((row['pool'], row['case_id'], row['case_path']))
cc_set={(p,c) for p,c,_ in cc}
with zipfile.ZipFile(zip_path) as z:
    names=z.namelist()
    bad=[]
    skills=[]
    for name in names:
        n=name.replace('\\','/')
        parts=[p for p in n.split('/') if p not in ('', '.')]
        if n.startswith('/') or any(p == '..' for p in parts):
            bad.append(name)
        if len(parts)==4 and parts[0]=='cases' and parts[1] in {'PERF','CONS','PORT','LONGTAIL'} and parts[3]=='skills.md':
            skills.append((name, parts[1], parts[2], '/'.join(parts)))
print('zip_entries', len(names))
print('path_traversal_issues', len(bad))
print('root_level_skills', len(skills))
print('pool_split', dict(Counter(p for _,p,_,_ in skills)))
zip_set={(p,c) for _,p,c,_ in skills}
print('common_core_count', len(cc_set))
print('zip_skills_match_common_core', zip_set == cc_set)
print('missing_from_zip', sorted(cc_set-zip_set))
print('extra_in_zip', sorted(zip_set-cc_set)[:20], 'extra_count', len(zip_set-cc_set))
print('duplicates', [item for item,count in Counter((p,c) for _,p,c,_ in skills).items() if count>1])
print('sample_skills', skills[:5])
PY
```

Sample content inspection and pre-copy validation/conflict check:

```bash
python - <<'PY'
import zipfile
from pathlib import Path
with zipfile.ZipFile('/home/tianci_gao/code/Rewritebench_v0/cases.zip') as z:
    data=z.read('cases/CONS/CONS_0005/skills.md').decode('utf-8-sig')
print(data[:2000])
PY
python - <<'PY'
import csv, zipfile
from pathlib import Path
zip_path=Path('/home/tianci_gao/code/Rewritebench_v0/cases.zip')
with Path('case_sets/common_core_v0/cases.csv').open(newline='') as f:
    cc={(row['pool'], row['case_id']): row for row in csv.DictReader(f)}
errors=[]
existing=[]
with zipfile.ZipFile(zip_path) as z:
    for name in z.namelist():
        parts=[p for p in name.replace('\\','/').split('/') if p not in ('', '.')]
        if len(parts)==4 and parts[0]=='cases' and parts[1] in {'PERF','CONS','PORT','LONGTAIL'} and parts[3]=='skills.md':
            pool, case_id=parts[1], parts[2]
            data=z.read(name)
            text=data.decode('utf-8-sig')
            checks={
                'case_id': f'case_id: `{case_id}`' in text or f'case_id: {case_id}' in text,
                'pool': f'pool: `{pool}`' in text or f'pool: {pool}' in text,
                'Atom Protocol': 'Atom Protocol' in text,
                'operation_atom': 'operation_atom' in text,
                'semantic_guard_atom': 'semantic_guard_atom' in text,
                'Required Candidate Annotation Shape': 'Required Candidate Annotation Shape' in text,
                'Review Boundaries': 'Review Boundaries' in text,
            }
            for k,v in checks.items():
                if not v:
                    errors.append((case_id,k,'missing'))
            dest=Path('cases')/pool/case_id/'skills.md'
            if dest.exists():
                existing.append((case_id, data == dest.read_bytes()))
print('validation_errors', errors[:20], 'count', len(errors))
print('existing_destinations', existing[:20], 'count', len(existing))
if errors:
    raise SystemExit(1)
if any(not same for _,same in existing):
    raise SystemExit('conflicting existing skills.md')
PY
```

Controlled import and audit CSV generation:

```bash
python - <<'PY'
# Structured zipfile import copied only validated cases/<POOL>/<CASE_ID>/skills.md
# and wrote zip_inventory.csv, imported_skills_inventory.csv, and
# skills_contract_validation.csv under audits/common_core_skills_md_import_v0/.
PY
python - <<'PY'
# Normalized generated CSV files and imported skills.md files to repository LF style
# after the initial staged git diff --check reported CRLF/trailing blank-line artifacts.
PY
```

Validation commands:

```bash
python - <<'PY'
import csv
from pathlib import Path
for p in ['audits/common_core_skills_md_import_v0/zip_inventory.csv','audits/common_core_skills_md_import_v0/imported_skills_inventory.csv','audits/common_core_skills_md_import_v0/skills_contract_validation.csv']:
    with Path(p).open(newline='') as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=40:
        raise SystemExit(f'{p}: expected 40 rows, got {len(rows)}')
    print('csv_ok', p, len(rows))
PY
python - <<'PY'
import csv
from pathlib import Path
from collections import Counter
rows=list(csv.DictReader(Path('audits/common_core_skills_md_import_v0/imported_skills_inventory.csv').open()))
counts=Counter(r['pool'] for r in rows)
expected={'PERF':16,'CONS':9,'PORT':9,'LONGTAIL':6}
if dict(counts)!=expected:
    raise SystemExit(f'pool split mismatch: {dict(counts)}')
print('import_count_and_pool_split_ok', len(rows), dict(counts))
PY
python - <<'PY'
import csv
from pathlib import Path
with Path('case_sets/common_core_v0/cases.csv').open(newline='') as f:
    cc={(r['pool'],r['case_id']) for r in csv.DictReader(f)}
with Path('audits/common_core_skills_md_import_v0/zip_inventory.csv').open(newline='') as f:
    zset={(r['pool'],r['case_id']) for r in csv.DictReader(f)}
if cc != zset:
    raise SystemExit('membership mismatch')
print('common_core_membership_exact_match_ok', len(cc))
PY
python - <<'PY'
import csv
from pathlib import Path
rows=list(csv.DictReader(Path('audits/common_core_skills_md_import_v0/skills_contract_validation.csv').open()))
required_bool=['utf8_sig_readable','case_id_matches_directory','pool_matches_directory','contains_atom_protocol','contains_operation_atom','contains_semantic_guard_atom','contains_required_candidate_annotation_shape','contains_review_boundaries']
for r in rows:
    for col in required_bool:
        if r[col] != 'true':
            raise SystemExit(f'{r["case_id"]} failed {col}')
    if int(r['operation_atom_count']) < 1 or int(r['semantic_guard_atom_count']) < 1:
        raise SystemExit(f'{r["case_id"]} atom count failed')
print('skills_contract_validation_ok', len(rows))
PY
find cases -path '*/skill' -type d | wc -l
find cases -path '*/skills.md' -type f | wc -l
python - <<'PY'
import subprocess
names=subprocess.check_output(['git','status','--short'], text=True).splitlines()
case_lines=[line[3:] for line in names if line.startswith('?? cases/') or line.startswith(' A cases/') or line.startswith('A  cases/') or line.startswith(' M cases/') or line.startswith('M  cases/')]
non_skills=[p for p in case_lines if not p.endswith('/skills.md')]
if non_skills:
    raise SystemExit('non-skills case paths changed: '+', '.join(non_skills[:20]))
print('protected_case_path_review_ok', len(case_lines))
PY
git diff --check
rg -n --pcre2 "(?i)(sk-[A-Za-z0-9_-]{20,}|api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{20,}|bearer\s+[A-Za-z0-9_./+=-]{20,}|gptsapi[_-]?key\s*[:=])" audits/common_core_skills_md_import_v0 project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md project_control/DECISION_LOG.md cases/*/*/skills.md || true
git diff --name-status
git status -sb
```

No live API call, DB/checker/timing run, baseline rerun, POCR computation, official metrics, paper rendering, retained-evidence promotion, or leaderboard command was run.
