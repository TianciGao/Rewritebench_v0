# Command Log

Preflight and source inspection:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 23ec34242fc98dc98b6c5dff73f6ee1f65301cfe HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "D034|D035" project_control/DECISION_LOG.md
source scripts/env_postgres.local.sh && python scripts/dev/check_local_engine_env.py
java -version
git status --porcelain -- runs/user output reports results
```

Timing inspection and execution:

```bash
rg -n "timing|warmup|repetition|median|speedup|collect_timing|Timing" src scripts tests
sed -n '1,240p' src/sql_rewrite_bench/local_timing.py
sed -n '240,700p' src/sql_rewrite_bench/local_timing.py
sed -n '1,260p' src/sql_rewrite_bench/postgres_execution.py
python audits/calcite_hep_pg_exact_timing_diagnostic_v0/run_pg_exact_timing_from_execution_audit.py
python -m json.tool audits/calcite_hep_pg_exact_timing_diagnostic_v0/diagnostic_summary.json
wc -l audits/calcite_hep_pg_exact_timing_diagnostic_v0/per_row_timing.csv
```

Validation:

```bash
python - <<'PY'
import csv, json
from pathlib import Path
md=list(Path('audits/calcite_hep_pg_exact_timing_diagnostic_v0').glob('*.md'))
empty=[p.name for p in md if not p.read_text(encoding='utf-8').strip()]
rows=list(csv.DictReader(Path('audits/calcite_hep_pg_exact_timing_diagnostic_v0/per_row_timing.csv').open()))
summary=json.loads(Path('audits/calcite_hep_pg_exact_timing_diagnostic_v0/diagnostic_summary.json').read_text())
assert not empty
assert len(rows) == 40
assert summary['timed_rows'] == 20
assert summary['timing_failed_rows'] == 0
PY
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
python -m py_compile baselines/calcite_hep_fail_closed/adapter.py audits/calcite_hep_pg_exact_timing_diagnostic_v0/run_pg_exact_timing_from_execution_audit.py
git diff --check
git status --porcelain -- runs/user output reports results
git status -sb
```

Validation result: passed.
