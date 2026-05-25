# Command Log

Pre-edit confirmation and project-control reads:

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,160p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
```

Format and convention inspection:

```bash
sed -n '1,180p' cases/CONS/CONS_0005/skills.md
sed -n '1,220p' pyproject.toml
find src/sql_rewrite_bench -maxdepth 2 -type f | sort | sed -n '1,120p'
find tests -maxdepth 3 -type f | sort | sed -n '1,160p'
rg -n "csv.DictReader|dataclass|Path\\(" src/sql_rewrite_bench tests | head -80
```

Implementation and parse-only validation:

```bash
mkdir -p src/sql_rewrite_bench/pocr tests/pocr
python -m py_compile src/sql_rewrite_bench/pocr/__init__.py src/sql_rewrite_bench/pocr/models.py src/sql_rewrite_bench/pocr/skills_parser.py src/sql_rewrite_bench/pocr/validation.py src/sql_rewrite_bench/pocr/inventory.py
pytest tests/pocr/test_skills_parser.py tests/pocr/test_skills_inventory.py -q
python - <<'PY'
from pathlib import Path
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory, write_parse_only_report
repo=Path.cwd()
out=repo/'audits/pocr_no_api_parser_adapter_v0'
out.mkdir(parents=True, exist_ok=True)
inv=build_common_core_inventory(repo)
write_parse_only_report(inv, out)
print('parsed_count', inv.parsed_count)
print('valid_count', inv.valid_count)
print('pool_split', inv.pool_split)
print('atom_count', inv.atom_count)
print('operation_atom_count', inv.operation_atom_count)
print('semantic_guard_atom_count', inv.semantic_guard_atom_count)
print('issues_count', inv.issues_count)
PY
head -5 audits/pocr_no_api_parser_adapter_v0/parsed_skills_inventory.csv
head -5 audits/pocr_no_api_parser_adapter_v0/atom_inventory.csv
cat audits/pocr_no_api_parser_adapter_v0/validation_issues.csv
```

Validation commands:

```bash
python -m py_compile src/sql_rewrite_bench/pocr/__init__.py src/sql_rewrite_bench/pocr/models.py src/sql_rewrite_bench/pocr/skills_parser.py src/sql_rewrite_bench/pocr/validation.py src/sql_rewrite_bench/pocr/inventory.py
pytest tests/pocr/test_skills_parser.py tests/pocr/test_skills_inventory.py -q
python - <<'PY'
from pathlib import Path
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory, EXPECTED_COMMON_CORE_SPLIT
inv=build_common_core_inventory(Path.cwd())
if inv.parsed_count != 40 or inv.valid_count != 40:
    raise SystemExit(f'bad counts parsed={inv.parsed_count} valid={inv.valid_count}')
if inv.pool_split != EXPECTED_COMMON_CORE_SPLIT:
    raise SystemExit(f'bad split {inv.pool_split}')
if inv.operation_atom_count < 40 or inv.semantic_guard_atom_count < 40:
    raise SystemExit('missing atom category entries')
if inv.issues_count:
    raise SystemExit(f'issues present {inv.issues_count}')
print('parse_only_inventory_ok', inv.parsed_count, inv.pool_split, inv.atom_count, inv.operation_atom_count, inv.semantic_guard_atom_count)
PY
python - <<'PY'
import csv
from pathlib import Path
base=Path('audits/pocr_no_api_parser_adapter_v0')
for name in ['parsed_skills_inventory.csv','atom_inventory.csv','validation_issues.csv']:
    path=base/name
    with path.open(newline='', encoding='utf-8') as handle:
        rows=list(csv.DictReader(handle))
    if name != 'validation_issues.csv' and not rows:
        raise SystemExit(f'empty csv: {path}')
    print('csv_ok', path, len(rows))
PY
python - <<'PY'
from pathlib import Path
for path in Path('audits/pocr_no_api_parser_adapter_v0').glob('*.md'):
    if not path.read_text(encoding='utf-8').strip():
        raise SystemExit(f'empty markdown: {path}')
    print('md_ok', path)
PY
python - <<'PY'
import subprocess
changed=subprocess.check_output(['git','status','--short'], text=True).splitlines()
case_changes=[line for line in changed if line[3:].startswith('cases/')]
for line in case_changes:
    raise SystemExit('case package modified unexpectedly: '+line)
for line in changed:
    path=line[3:]
    if path.startswith(('reports/','results/','output/','runs/')) or '/runs/' in path:
        raise SystemExit('protected output path modified: '+line)
print('protected_path_review_ok')
PY
rg -n --pcre2 "(?i)(sk-[A-Za-z0-9_-]{20,}|api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{20,}|bearer\s+[A-Za-z0-9_./+=-]{20,}|gptsapi[_-]?key\s*[:=])" src/sql_rewrite_bench/pocr tests/pocr audits/pocr_no_api_parser_adapter_v0 project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md || true
git diff --check
git diff --name-status
git status -sb
```

No live API call, DB/checker/timing run, baseline rerun, Stage A annotation, Stage B validation, Positive Operation Coverage Rate computation, official metrics, paper rendering, retained-evidence promotion, or leaderboard command was run.
