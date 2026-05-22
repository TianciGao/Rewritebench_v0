# Command Log

This task was design/audit only. No local diagnostic rerun was performed.

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
latest commit: 7ecec26 docs(audit): triage MySQL label policy
```

## Required Reads

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -120 project_control/MIGRATION_STATUS.md
tail -140 project_control/MIGRATION_RUN_LOG.md
sed -n '1,240p' project_control/DECISION_LOG.md
sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,220p' audits/mysql_label_policy_triage_v0/README.md
sed -n '1,80p' audits/mysql_label_policy_triage_v0/label_policy_triage_matrix.csv
sed -n '1,220p' audits/mysql_label_policy_triage_v0/value_vs_label_examples.md
sed -n '1,180p' audits/mysql_label_policy_triage_v0/recommendation.md
sed -n '1,220p' audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/README.md
sed -n '1,200p' audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/closeout_status.json
sed -n '1,120p' audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/remaining_failure_matrix.csv
sed -n '1,180p' audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/recommendation.md
sed -n '1,420p' src/sql_rewrite_bench/local_result_checker.py
```

## Checker Config Reads

```bash
sed -n '1,180p' cases/PERF/PERF_0062/checker/checker.yaml
sed -n '1,180p' cases/PERF/PERF_0062/checker/compare_config.yaml
sed -n '1,180p' cases/PERF/PERF_0062/checker/normalization.yaml
sed -n '1,180p' cases/PORT/PORT_0004/checker/checker.yaml
sed -n '1,180p' cases/PORT/PORT_0004/checker/compare_config.yaml
sed -n '1,180p' cases/PORT/PORT_0004/checker/normalization.yaml
sed -n '1,180p' cases/PORT/PORT_0013/checker/checker.yaml
sed -n '1,180p' cases/PORT/PORT_0013/checker/compare_config.yaml
sed -n '1,180p' cases/PORT/PORT_0013/checker/normalization.yaml
sed -n '1,180p' cases/PORT/PORT_0022/checker/checker.yaml
sed -n '1,180p' cases/PORT/PORT_0022/checker/compare_config.yaml
sed -n '1,180p' cases/PORT/PORT_0022/checker/normalization.yaml
sed -n '1,180p' cases/PORT/PORT_0024/checker/checker.yaml
sed -n '1,180p' cases/PORT/PORT_0024/checker/compare_config.yaml
sed -n '1,180p' cases/PORT/PORT_0024/checker/normalization.yaml
rg -n "enable_cross_dialect_normalization|enable_mixed_numeric_equivalence|run_local_checker|diagnostic_mode|source_reference|target_candidate" src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/user_run_schema.py src/sql_rewrite_bench/user_ledger.py
sed -n '420,510p' src/sql_rewrite_bench/user_run.py
```

## Validation

```bash
git diff --check
PYTHONPATH=src python - <<'PY'
from pathlib import Path
files = [Path('project_control/MIGRATION_STATUS.md'), Path('project_control/MIGRATION_RUN_LOG.md')]
for path in files:
    text = path.read_text(encoding='utf-8')
    if not text.strip():
        raise SystemExit(f'empty file: {path}')
    if 'checker_label_policy_design_v0' not in text:
        raise SystemExit(f'missing task marker: {path}')
print('project-control readability: ok')
PY
PYTHONPATH=src python - <<'PY'
from pathlib import Path
root = Path('audits/checker_label_policy_design_v0')
expected = {
    'README.md', 'current_behavior.md', 'inspected_examples.md', 'proposed_policy.md',
    'patch_options.md', 'regression_plan.md', 'risk_assessment.md',
    'protected_surface_check.md', 'command_log.md', 'boundary_checklist.md',
}
seen = {p.name for p in root.glob('*.md')}
if seen != expected:
    raise SystemExit(f'unexpected markdown set: {sorted(seen)}')
for path in sorted(root.glob('*.md')):
    text = path.read_text(encoding='utf-8')
    if not text.strip() or not text.lstrip().startswith('#'):
        raise SystemExit(f'markdown sanity failed: {path}')
print('markdown sanity: ok')
PY
PYTHONPATH=src python - <<'PY'
import subprocess
allowed = {
    'audits/checker_label_policy_design_v0/README.md',
    'audits/checker_label_policy_design_v0/current_behavior.md',
    'audits/checker_label_policy_design_v0/inspected_examples.md',
    'audits/checker_label_policy_design_v0/proposed_policy.md',
    'audits/checker_label_policy_design_v0/patch_options.md',
    'audits/checker_label_policy_design_v0/regression_plan.md',
    'audits/checker_label_policy_design_v0/risk_assessment.md',
    'audits/checker_label_policy_design_v0/protected_surface_check.md',
    'audits/checker_label_policy_design_v0/command_log.md',
    'audits/checker_label_policy_design_v0/boundary_checklist.md',
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
git diff --name-only -- src tests cases baselines case_sets reports results inventory benchmark_spec repository_spec | sed -n '1,120p'
```

Results:

- `git diff --check`: passed.
- Project-control readability: passed.
- Markdown sanity: passed.
- Protected-surface status check: passed.
- `runs/user/` output changes: none staged or committed.
- Protected surfaces checked by path diff: no output.
