# Command Log

Commands were run from `/home/tianci_gao/code/Rewritebench_v0` unless another working directory is shown.

## Release Repo Preflight

```bash
git status -sb
git branch --show-current
```

## Raw Directory Probe

```bash
pwd
ls -la /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql
find /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql -maxdepth 2 -type f | sort | head -100
find /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql -maxdepth 4 -type d | sort
find /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged -maxdepth 3 -type f | sort | head -120
test -f /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/README.md
test -f /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/requirements.txt
test -f /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/__main__.py
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/parallel
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/benchmarks
test -f /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/README.md
test -f /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/requirements.txt
test -f /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/__main__.py
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/parallel
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/benchmarks
```

## Staged VeriEQL Source Probe

Working directory: `/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL`

```bash
python --version
git status -sb
git remote -v
git rev-parse HEAD
sed -n '1,220p' README.md
sed -n '1,160p' requirements.txt
python -m __main__ --help
python -m parallel.cli_within_timeout --help
which python
python - <<'PY'
mods = ['ujson','z3','ordered_set','lark','tqdm','pandas','yaml','prettytable','mysql.connector']
for mod in mods:
    try:
        __import__(mod)
        print(f'{mod}: ok')
    except Exception as exc:
        print(f'{mod}: missing_or_error:{type(exc).__name__}:{exc}')
PY
sed -n '1,220p' parallel/cli_within_timeout.py
sed -n '220,420p' parallel/cli_within_timeout.py
sed -n '1,120p' __main__.py
stat -c '%A,%s,%n' README.md requirements.txt __main__.py parallel/cli_within_timeout.py
find . -maxdepth 1 -type f -printf '%M,%s,%f\n' | sort
```

## Release Wrapper Inspection

```bash
sed -n '1,240p' src/sql_rewrite_bench/verifier_support/verieql.py
sed -n '220,520p' src/sql_rewrite_bench/verifier_support/verieql.py
```

## Notes Probe

```bash
sed -n '1,160p' /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/notes/inspection_summary.txt
sed -n '1,160p' /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/notes/progress_summary_v1.txt
```

## Validation

```bash
python - <<'PY'
from pathlib import Path
for path in ['project_control/MIGRATION_STATUS.md','project_control/MIGRATION_RUN_LOG.md','project_control/DECISION_LOG.md','project_control/MIGRATION_MASTER_PLAN.md']:
    assert Path(path).read_text(encoding='utf-8').strip(), path
print('project-control readability ok')
PY

python - <<'PY'
from pathlib import Path
for path in Path('audits/local_verieql_raw_directory_probe_v0').glob('*.md'):
    text = path.read_text(encoding='utf-8')
    assert text.startswith('#'), path
print('audit markdown sanity ok')
PY

git diff --check

python - <<'PY'
import subprocess
allowed_prefixes = ('audits/local_verieql_raw_directory_probe_v0/',)
allowed_files = {'project_control/MIGRATION_STATUS.md','project_control/MIGRATION_RUN_LOG.md'}
paths = [line[3:] for line in subprocess.check_output(['git','status','--porcelain'], text=True).splitlines() if line]
violations = [p for p in paths if p not in allowed_files and not p.startswith(allowed_prefixes)]
if violations:
    raise SystemExit('protected surface violation: ' + ', '.join(violations))
print('protected surface ok:', ', '.join(paths))
PY

git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
git status --porcelain | rg '^(.. )?(runs/user|output)/' || true
```

Results:

- Project-control readability: passed.
- Audit Markdown sanity: passed.
- `git diff --check`: passed.
- Protected-surface check: passed.
- Raw VeriEQL checkout status remained `M constants.py` only.
- `runs/user/` and `output/` runtime artifacts staged/committed: none.
