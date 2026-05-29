# Command Log

Preflight and context commands:

```text
git status -sb
find project_control -maxdepth 1 -type f -printf '%f\n' | sort
rg -n '^## D03[45]:' project_control/DECISION_LOG.md
test -d audits/user_output_and_cli_contract_v0 && echo OK_AUDIT
test -f repository_spec/user_output_contract_v0_draft.md && echo OK_SPEC
git merge-base --is-ancestor 9b12239 HEAD && echo OK_9b12239_OR_LATER
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -120 project_control/MIGRATION_STATUS.md
tail -160 project_control/MIGRATION_RUN_LOG.md
sed -n '900,1100p' project_control/DECISION_LOG.md
sed -n '1,260p' repository_spec/user_output_contract_v0_draft.md
find audits/user_output_and_cli_contract_v0 -maxdepth 1 -type f -print | sort
find audits/user_output_writer_cli_facade_implementation_plan_v0 -maxdepth 1 -type f -print | sort
sed -n '1,220p' audits/local_evaluation_workbench_v0_closeout/README.md
sed -n '1,220p' audits/user_output_and_cli_contract_v0/run_manifest_schema.md
sed -n '1,220p' audits/user_output_and_cli_contract_v0/result_artifact_contract.md
sed -n '1,220p' audits/user_output_and_cli_contract_v0/log_artifact_contract.md
sed -n '1,220p' audits/user_output_and_cli_contract_v0/report_artifact_contract.md
sed -n '1,260p' audits/user_output_writer_cli_facade_implementation_plan_v0/output_writer_plan.md
sed -n '1,180p' audits/user_output_writer_cli_facade_implementation_plan_v0/phase2_implementation_slices.md
sed -n '1,180p' audits/user_output_writer_cli_facade_implementation_plan_v0/test_plan.md
sed -n '1,180p' audits/user_output_writer_cli_facade_implementation_plan_v0/transition_strategy_runs_user_to_output.md
sed -n '1,260p' src/sql_rewrite_bench/user_run.py
sed -n '720,1040p' src/sql_rewrite_bench/user_run.py
sed -n '1,280p' src/sql_rewrite_bench/user_ledger.py
sed -n '1,320p' src/sql_rewrite_bench/user_quality_report.py
sed -n '1,360p' src/sql_rewrite_bench/local_metrics.py
rg --files tests/user_entry | sort
sed -n '1,220p' tests/user_entry/test_local_metrics.py
sed -n '1,280p' tests/user_entry/test_user_run_outputs.py
find runs/user/timing_sqlglot_noop_postgres_smoke -maxdepth 3 -type f | sort | head -80
find runs/user/timing_sqlglot_noop_postgres_smoke/workspaces -maxdepth 5 -type f | sort | head -120
```

Implementation and validation commands:

```text
PYTHONPATH=src pytest tests/user_entry/test_user_output.py -q
tmpdir=$(mktemp -d) && PYTHONPATH=src python - <<'PY' "$tmpdir"
import json
import sys
from pathlib import Path
from sql_rewrite_bench.user_output import export_run_to_output
root = Path(sys.argv[1])
run_dir = Path('runs/user/timing_sqlglot_noop_postgres_smoke')
exported = export_run_to_output(run_dir, root / 'output', repo_root=Path.cwd())
manifest = json.loads(exported.run_manifest_path.read_text(encoding='utf-8'))
print('smoke_output_root=' + (root / 'output').as_posix())
print('run_id=' + exported.run_id)
print('result_root_exists=' + str(exported.paths.result_root.exists()).lower())
print('log_root_exists=' + str(exported.paths.log_root.exists()).lower())
print('report_root_exists=' + str(exported.paths.report_root.exists()).lower())
print('manifest_boundary=' + str(manifest['local_diagnostic_only']).lower() + '/' + str(manifest['official_metric_input']).lower() + '/' + str(manifest['paper_result_input']).lower())
print('selected_case_count=' + str(manifest['selected_case_count']))
print('route_id=' + str(manifest['route_id']))
PY
rm -rf "$tmpdir"
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/user_output.py
PYTHONPATH=src pytest tests/user_entry -q
git diff --check
python - <<'PY'
from pathlib import Path
for path in ['project_control/MIGRATION_MASTER_PLAN.md','project_control/MIGRATION_STATUS.md','project_control/MIGRATION_RUN_LOG.md','project_control/DECISION_LOG.md']:
    assert Path(path).read_text(encoding='utf-8').strip(), path
print('project-control readability: ok')
PY
python - <<'PY'
from pathlib import Path
root = Path('audits/user_output_writer_phase2a_v0')
for path in root.glob('*.md'):
    text = path.read_text(encoding='utf-8')
    assert text.strip(), path
    assert text.lstrip().startswith('#'), path
print('audit markdown sanity: ok')
PY
python - <<'PY'
import subprocess
allowed = {
    'src/sql_rewrite_bench/user_output.py',
    'tests/user_entry/test_user_output.py',
    'project_control/MIGRATION_STATUS.md',
    'project_control/MIGRATION_RUN_LOG.md',
}
allowed_prefixes = ('audits/user_output_writer_phase2a_v0/',)
tracked = subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()
untracked = [line[3:] for line in subprocess.check_output(['git', 'status', '--short'], text=True).splitlines() if line.startswith('?? ')]
unexpected = [p for p in tracked + untracked if p not in allowed and not p.startswith(allowed_prefixes)]
assert not unexpected, 'unexpected changed paths: ' + ', '.join(unexpected)
print('protected-surface diff check: ok')
PY
git status --short -- reports results output runs/user cases case_sets baselines scripts repository_spec src/cli benchmarks
```

Validation result:

- Focused tests passed.
- Bounded export smoke passed and used a temporary output root only.
- Python compile passed.
- Full user-entry tests passed.
- `git diff --check` passed before audit writeback.
- Project-control readability check passed.
- Audit Markdown sanity check passed.
- Protected-surface diff check passed.
- No repository-level `output/`, top-level `reports/`/`results`, `runs/user/`, case/case_set/baseline/script/repository_spec/`src/cli`/`benchmarks` changes were present.
