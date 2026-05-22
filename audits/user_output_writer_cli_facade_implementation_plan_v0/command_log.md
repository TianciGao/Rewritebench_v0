# Command Log

Commands run:

```text
git status -sb
git branch --show-current
find project_control -maxdepth 1 -type f -printf '%f\n' | sort
find project_control -maxdepth 1 -type d -printf '%f\n' | sort
rg -n '^## D03[45]:' project_control/DECISION_LOG.md
test -d audits/user_output_and_cli_contract_v0 && echo OK_AUDIT
test -f repository_spec/user_output_contract_v0_draft.md && echo OK_SPEC
git merge-base --is-ancestor 9b12239 HEAD && echo OK_9b12239_OR_LATER
git show -s --oneline 9b12239
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -90 project_control/MIGRATION_STATUS.md
tail -140 project_control/MIGRATION_RUN_LOG.md
sed -n '900,1120p' project_control/DECISION_LOG.md
sed -n '1,260p' repository_spec/user_output_contract_v0_draft.md
find audits/user_output_and_cli_contract_v0 -maxdepth 1 -type f -print | sort
sed -n '1,220p' audits/project_control_hygiene_v0/README.md
sed -n '1,220p' audits/final_public_layout_target_decision_v0/README.md
sed -n '1,220p' audits/final_public_layout_target_decision_v0/next_step_1_contract_adjustment.md
sed -n '1,220p' audits/local_evaluation_workbench_v0_closeout/README.md
sed -n '1,220p' audits/non_official_local_metrics_calculator_v0/README.md
sed -n '1,220p' audits/common_core_sqlglot_noop_local_metrics_projection_v0/README.md
sed -n '1,260p' src/sql_rewrite_bench/user_run.py
sed -n '720,1040p' src/sql_rewrite_bench/user_run.py
sed -n '1,260p' src/sql_rewrite_bench/user_ledger.py
sed -n '1,260p' src/sql_rewrite_bench/user_quality_report.py
sed -n '260,620p' src/sql_rewrite_bench/user_quality_report.py
sed -n '1,260p' src/sql_rewrite_bench/local_metrics.py
sed -n '260,620p' src/sql_rewrite_bench/local_metrics.py
sed -n '1,260p' scripts/dev/compute_local_user_metrics.py
rg -n 'user_output_and_cli_contract_v0|commit hash|push result' project_control/MIGRATION_RUN_LOG.md project_control/MIGRATION_STATUS.md
```

Validation commands are recorded after validation in the task closeout.

Validation commands run:

```text
git diff --check
python - <<'PY'
from pathlib import Path
files = [Path('project_control/MIGRATION_MASTER_PLAN.md'), Path('project_control/MIGRATION_STATUS.md'), Path('project_control/MIGRATION_RUN_LOG.md'), Path('project_control/DECISION_LOG.md')]
for path in files:
    text = path.read_text(encoding='utf-8')
    assert text.strip(), path
print('project-control readability: ok')
PY
python - <<'PY'
from pathlib import Path
root = Path('audits/user_output_writer_cli_facade_implementation_plan_v0')
required = {
    'README.md', 'current_output_inventory.md', 'output_writer_plan.md', 'cli_facade_plan.md',
    'phase2_implementation_slices.md', 'transition_strategy_runs_user_to_output.md',
    'test_plan.md', 'risk_assessment.md', 'protected_surface_check.md', 'command_log.md',
    'boundary_checklist.md'
}
seen = {p.name for p in root.glob('*.md')}
missing = required - seen
assert not missing, f'missing: {sorted(missing)}'
for path in sorted(root.glob('*.md')):
    text = path.read_text(encoding='utf-8')
    assert text.strip(), path
    assert text.lstrip().startswith('#'), path
print('audit markdown sanity: ok')
PY
python - <<'PY'
from pathlib import Path
allowed_prefixes = ('audits/user_output_writer_cli_facade_implementation_plan_v0/',)
allowed_exact = {'project_control/MIGRATION_STATUS.md', 'project_control/MIGRATION_RUN_LOG.md'}
changed = []
import subprocess
tracked = subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()
untracked = [line[3:] for line in subprocess.check_output(['git', 'status', '--short'], text=True).splitlines() if line.startswith('?? ')]
for path in tracked + untracked:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    changed.append(path)
assert not changed, 'unexpected changed paths: ' + ', '.join(changed)
print('protected-surface diff check: ok')
PY
git status --short
git status --short -- src tests scripts cases case_sets schemas inventory baselines docs examples reports results output benchmarks repository_spec runs/user
git diff --name-only
perl -0pi -e 's/\n+\z/\n/' audits/user_output_writer_cli_facade_implementation_plan_v0/*.md
git add audits/user_output_writer_cli_facade_implementation_plan_v0
git diff --cached --check
python - <<'PY'
import subprocess
allowed_prefixes = ('audits/user_output_writer_cli_facade_implementation_plan_v0/',)
allowed_exact = {'project_control/MIGRATION_STATUS.md', 'project_control/MIGRATION_RUN_LOG.md'}
paths = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()
unexpected = [p for p in paths if p not in allowed_exact and not p.startswith(allowed_prefixes)]
assert not unexpected, unexpected
print('staged protected-surface check: ok')
PY
```

Validation result:

- `git diff --check`: passed.
- Project-control readability: passed.
- Audit Markdown sanity: passed.
- Protected-surface diff check: passed.
- Staged `git diff --cached --check`: passed after mechanical EOF whitespace cleanup.
- Staged protected-surface check: passed.
- No `src/`, `tests/`, `scripts/`, `cases/`, `case_sets/`, `schemas/`, `inventory/`, `baselines/`, `docs/`, `examples/`, `reports/`, `results/`, `output/`, `benchmarks/`, `repository_spec/`, or `runs/user/` changes were present.
