# Command Log

Commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`. Secrets were not printed.

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,180p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,140p' project_control/MIGRATION_STATUS.md
sed -n '1,180p' project_control/DECISION_LOG.md
find docs -maxdepth 3 -type f | sort
find examples -maxdepth 3 -type f | sort
find docs -maxdepth 2 -type d | sort
find examples -maxdepth 2 -type d | sort
sed -n '1,160p' README.md
sed -n '1,220p' docs/README.md
sed -n '1,220p' examples/README.md
sed -n '1,220p' docs/spec/cli_contract.md
sed -n '1,220p' docs/spec/output_contract.md
```

Final validation:

```bash
python - <<'PY'
from pathlib import Path
paths = [
    Path('docs/pocr_diagnostic.md'),
    Path('examples/pocr_diagnostic/README.md'),
    Path('audits/pocr_diagnostic_user_docs_v0/README.md'),
    Path('audits/pocr_diagnostic_user_docs_v0/docs_plan.md'),
    Path('audits/pocr_diagnostic_user_docs_v0/command_examples_review.md'),
    Path('audits/pocr_diagnostic_user_docs_v0/boundary_wording_review.md'),
    Path('audits/pocr_diagnostic_user_docs_v0/protected_path_review.md'),
    Path('audits/pocr_diagnostic_user_docs_v0/command_log.md'),
]
for p in paths:
    assert p.exists(), p
    assert p.read_text(encoding='utf-8').strip(), p
print('markdown_non_empty_passed')
PY

python - <<'PY'
from pathlib import Path
required = [
    'Positive Operation Coverage diagnostic support',
    'This is not official POCR.',
    'Stage A annotation alone is not counted.',
    'Stage B transformation-aware validation is diagnostic only.',
    'Semantic guard atoms are not part of operation coverage numerator.',
    'No route-level POCR score is emitted.',
    'No paper-facing metric is promoted.',
]
docs = [Path('docs/pocr_diagnostic.md'), Path('examples/pocr_diagnostic/README.md')]
for doc in docs:
    text = doc.read_text(encoding='utf-8')
    for phrase in required:
        assert phrase in text, (doc, phrase)
    assert '/tmp/sqlrb_pocr_user_smoke_annotation_missing_v0/output' in text
    assert '/tmp/sqlrb_pocr_user_replay_direct_llm_pg40_matching_route_v0/output' in text
    assert 'Do not commit generated `output/` artifacts.' in text
print('boundary_phrase_and_tmp_examples_passed')
PY

python - <<'PY'
from pathlib import Path
for doc in [Path('docs/pocr_diagnostic.md'), Path('examples/pocr_diagnostic/README.md')]:
    text = doc.read_text(encoding='utf-8').lower()
    assert 'this is not official pocr.' in text
    assert 'no paper-facing metric is promoted.' in text
    assert 'no route-level pocr score is emitted.' in text
    assert 'paper-facing metric' in text
print('docs_boundary_semantics_passed')
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
```

Results:

- Markdown non-empty checks passed.
- Required boundary phrase checks passed.
- `/tmp` output-root example checks passed.
- Documentation boundary semantics checks passed.
- `pytest tests/pocr -q`: 92 passed.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`: 28 passed.
- `git diff --check` passed.
- Protected-path review passed.
- Changed-file secret value scan passed.
