# Command Log

This task used existing local artifacts only. No local diagnostic rerun was performed.

## Preflight

```bash
git status -sb
git branch --show-current
git log --oneline -8
```

Starting state:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
branch: feature/case-package-v2-external-schema
latest commit: 49c4aaf docs(audit): close SQLGlot noop Common-core diagnostics
```

## Required Context Reads

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -140 project_control/MIGRATION_STATUS.md
tail -160 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/DECISION_LOG.md
sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,220p' audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/README.md
sed -n '1,220p' audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/closeout_status.json
sed -n '1,120p' audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/remaining_failure_matrix.csv
sed -n '1,240p' audits/common_core_sqlglot_noop_failure_triage_v0/README.md
sed -n '1,120p' audits/common_core_sqlglot_noop_failure_triage_v0/failure_triage_matrix.csv
sed -n '1,200p' audits/common_core_sqlglot_noop_failure_triage_v0/candidate_examples.md
sed -n '1,220p' baselines/sqlglot/README.md
```

## Artifact Inspection

```bash
ls runs/user/common_core_sqlglot_noop_mysql_snapshot
head -1 runs/user/common_core_sqlglot_noop_mysql_snapshot/ledger.csv
rg -n "PERF_0062|PORT_0004|PORT_0013|PORT_0022|PORT_0024" runs/user/common_core_sqlglot_noop_mysql_snapshot/ledger.csv
find runs/user/common_core_sqlglot_noop_mysql_snapshot -maxdepth 3 -type d | sed -n '1,120p'
PYTHONPATH=src python - <<'PY'
from pathlib import Path
import csv, json
root = Path('runs/user/common_core_sqlglot_noop_mysql_snapshot')
case_ids = ['PERF_0062','PORT_0004','PORT_0013','PORT_0022','PORT_0024']
rows = {r['case_id']: r for r in csv.DictReader((root/'ledger.csv').open(newline='', encoding='utf-8'))}
def read_jsonl(path):
    p = Path(path)
    return [json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip()]
for cid in case_ids:
    r = rows[cid]
    s = read_jsonl(r['source_result_path'])
    c = read_jsonl(r['candidate_result_path'])
    print(cid, list(s[0].keys()), list(c[0].keys()), list(s[0].values()), list(c[0].values()))
PY
```

## Checker Policy Context Reads

```bash
sed -n '1,160p' cases/PERF/PERF_0062/checker/compare_config.yaml
sed -n '1,160p' cases/PERF/PERF_0062/checker/normalization.yaml
sed -n '1,160p' cases/PORT/PORT_0004/checker/compare_config.yaml
sed -n '1,160p' cases/PORT/PORT_0004/checker/normalization.yaml
sed -n '1,160p' cases/PORT/PORT_0013/checker/compare_config.yaml
sed -n '1,160p' cases/PORT/PORT_0013/checker/normalization.yaml
sed -n '1,160p' cases/PORT/PORT_0022/checker/compare_config.yaml
sed -n '1,160p' cases/PORT/PORT_0022/checker/normalization.yaml
sed -n '1,160p' cases/PORT/PORT_0024/checker/compare_config.yaml
sed -n '1,160p' cases/PORT/PORT_0024/checker/normalization.yaml
rg -n "label|column|headers|ignore|compare|positional|sort_rows|row_order" src/sql_rewrite_bench/local_result_checker.py
sed -n '1,420p' src/sql_rewrite_bench/local_result_checker.py
```

## Validation

```bash
git diff --check
PYTHONPATH=src python - <<'PY'
from pathlib import Path
files = [
    Path('project_control/MIGRATION_STATUS.md'),
    Path('project_control/MIGRATION_RUN_LOG.md'),
]
for path in files:
    text = path.read_text(encoding='utf-8')
    if not text.strip():
        raise SystemExit(f'empty file: {path}')
    if 'mysql_label_policy_triage_v0' not in text:
        raise SystemExit(f'missing task marker: {path}')
print('project-control readability: ok')
PY
PYTHONPATH=src python - <<'PY'
from pathlib import Path
import csv
root = Path('audits/mysql_label_policy_triage_v0')
for path in [root / 'label_policy_triage_matrix.csv']:
    with path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit(f'no rows: {path}')
    print(f'{path}: {len(rows)} rows')
print('csv sanity: ok')
PY
PYTHONPATH=src python - <<'PY'
from pathlib import Path
root = Path('audits/mysql_label_policy_triage_v0')
for path in sorted(root.glob('*.md')):
    text = path.read_text(encoding='utf-8')
    if not text.strip():
        raise SystemExit(f'empty markdown: {path}')
    if not text.lstrip().startswith('#'):
        raise SystemExit(f'missing top heading: {path}')
    print(f'{path}: ok')
print('markdown sanity: ok')
PY
PYTHONPATH=src python - <<'PY'
import subprocess
allowed = {
    'audits/mysql_label_policy_triage_v0/README.md',
    'audits/mysql_label_policy_triage_v0/label_policy_triage_matrix.csv',
    'audits/mysql_label_policy_triage_v0/value_vs_label_examples.md',
    'audits/mysql_label_policy_triage_v0/recommendation.md',
    'audits/mysql_label_policy_triage_v0/protected_surface_check.md',
    'audits/mysql_label_policy_triage_v0/command_log.md',
    'audits/mysql_label_policy_triage_v0/boundary_checklist.md',
    'project_control/MIGRATION_STATUS.md',
    'project_control/MIGRATION_RUN_LOG.md',
}
tracked = set(filter(None, subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()))
untracked = set(filter(None, subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], text=True).splitlines()))
changed = tracked | untracked
extra = sorted(changed - allowed)
missing = sorted(allowed - changed)
if extra:
    raise SystemExit('unexpected changed/untracked paths: ' + ', '.join(extra))
if missing:
    raise SystemExit('expected changed/untracked paths missing: ' + ', '.join(missing))
print('protected-surface status check: ok')
PY
git status -sb -- runs/user
git diff --name-only -- reports results case_sets src tests baselines cases inventory benchmark_spec repository_spec | sed -n '1,120p'
```

Results:

- `git diff --check`: passed.
- Project-control readability: passed.
- CSV sanity: passed, 5 rows.
- Markdown sanity: passed.
- Protected-surface status check: passed.
- `runs/user/` output changes: none staged or committed.
- Protected surfaces checked by path diff: no output.
