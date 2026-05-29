# Command Log

Preflight:

```bash
git status -sb
rg -n "D034|D035" project_control/DECISION_LOG.md
test -d src/cli
test -d audits/user_cli_facade_phase2b_v0
test -d audits/user_cli_facade_phase2b_review_v0
test -d audits/user_cli_phase2c_summary_metrics_hardening_v0
test -f src/sql_rewrite_bench/user_output.py
test -f repository_spec/user_output_contract_v0_draft.md
find project_control -maxdepth 1 -type f -print | sort
```

Required reads:

```bash
sed -n '1,180p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1013,1105p' project_control/DECISION_LOG.md
tail -20 project_control/MIGRATION_STATUS.md
tail -90 project_control/MIGRATION_RUN_LOG.md
sed -n '1,240p' repository_spec/user_output_contract_v0_draft.md
sed -n '1,220p' docs/user_entry_checker_policy.md
find audits/user_output_and_cli_contract_v0 audits/user_output_writer_phase2a_v0 audits/user_cli_facade_phase2b_v0 audits/user_cli_facade_phase2b_review_v0 audits/user_cli_phase2c_summary_metrics_hardening_v0 -maxdepth 1 -type f -print | sort
```

Validation:

```bash
python - <<'PY'  # project-control readability
from pathlib import Path
for path in [
    Path('project_control/MIGRATION_MASTER_PLAN.md'),
    Path('project_control/MIGRATION_STATUS.md'),
    Path('project_control/MIGRATION_RUN_LOG.md'),
    Path('project_control/DECISION_LOG.md'),
]:
    assert path.read_text(encoding='utf-8').strip()
PY
python - <<'PY'  # Markdown sanity
from pathlib import Path
for path in sorted(Path('audits/verifier_support_output_contract_plan_v0').glob('*.md')):
    assert path.read_text(encoding='utf-8').strip()
PY
git diff --check
```
