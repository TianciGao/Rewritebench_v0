# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
test -f repository_spec/verifier_support_output_contract_v0_draft.md
test -d audits/verifier_support_output_contract_plan_v0
test -d src/cli
test -f src/sql_rewrite_bench/user_output.py
rg -n "D034|D035|verifier_support_output_contract_plan_v0|pending|e19af82" project_control/DECISION_LOG.md project_control/MIGRATION_RUN_LOG.md
```

Required reads:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '900,1120p' project_control/DECISION_LOG.md
tail -n 140 project_control/MIGRATION_STATUS.md
tail -n 140 project_control/MIGRATION_RUN_LOG.md
sed -n '1,260p' repository_spec/verifier_support_output_contract_v0_draft.md
sed -n '1,240p' repository_spec/user_output_contract_v0_draft.md
sed -n '1,280p' src/sql_rewrite_bench/user_output.py
sed -n '1,320p' src/cli/main.py
find audits/verifier_support_output_contract_plan_v0 -maxdepth 1 -type f -print | sort
```

Validation:

```bash
PYTHONPATH=src pytest tests/user_entry/test_verifier_support.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile \
  src/sql_rewrite_bench/verifier_support/__init__.py \
  src/sql_rewrite_bench/verifier_support/pairs.py \
  src/sql_rewrite_bench/verifier_support/verdicts.py \
  src/sql_rewrite_bench/verifier_support/summary.py \
  src/sql_rewrite_bench/verifier_support/fixtures.py
python - <<'PY'
from pathlib import Path
for path in [
    Path('project_control/MIGRATION_MASTER_PLAN.md'),
    Path('project_control/MIGRATION_STATUS.md'),
    Path('project_control/MIGRATION_RUN_LOG.md'),
    Path('project_control/DECISION_LOG.md'),
]:
    assert path.read_text(encoding='utf-8').strip()
PY
python - <<'PY'
from pathlib import Path
for path in sorted(Path('audits/verifier_support_synthetic_fixture_v1').glob('*.md')):
    assert path.read_text(encoding='utf-8').strip(), path
PY
git diff --check
```
