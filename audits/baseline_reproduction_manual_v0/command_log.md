# Command Log

Commands used for inspection and validation, with no secrets printed:

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
sed -n '1,260p' project_control/DECISION_LOG.md
tail -n 180 project_control/MIGRATION_RUN_LOG.md
sed -n '1,240p' README.md
sed -n '1,260p' docs/README.md
sed -n '1,260p' docs/guide/user_quickstart.md
sed -n '1,280p' docs/USER_BENCHMARK_GUIDE.md
sed -n '1,280p' docs/spec/cli_contract.md
sed -n '1,260p' docs/candidate_sql_outputs.md
sed -n '1,220p' docs/pocr_diagnostic.md
rg -n "compute-local-metrics|run-id-prefix|aggregate-run-id|timing-repetitions|collect-timing|sqlglot_user_adapter|optimize_schema" src/cli src/sql_rewrite_bench baselines docs tests -g '*.py' -g '*.md'
ls -R baselines
sed -n '1,430p' src/cli/main.py
sed -n '1,140p' baselines/sqlglot/README.md
sed -n '1,180p' baselines/calcite_hep_fail_closed/README.md
sed -n '1,160p' baselines/direct_llm_original/README.md
sed -n '1,160p' baselines/direct_llm_repair_1/README.md
sed -n '1,220p' baselines/rbot/README.md
sed -n '1,220p' baselines/llm_r2/README.md
sed -n '1,240p' baselines/learnedrewrite/README.md
sed -n '1,180p' examples/README.md
rg -F "local diagnostic reproduction" docs/baseline_reproduction.md
rg -F "No paper-facing metric is promoted" docs/baseline_reproduction.md
rg -F "No global leaderboard is produced" docs/baseline_reproduction.md
rg -F "Performance is interpreted only over exact+timed rows" docs/baseline_reproduction.md
rg -F "PG40 cannot fill Track A 120" docs/baseline_reproduction.md
rg -F "Do not fabricate missing candidates" docs/baseline_reproduction.md
rg -F "Do not commit output/" docs/baseline_reproduction.md
rg -F "docs/baseline_reproduction.md" README.md
rg -F "baseline_reproduction.md" docs/README.md
python - <<'PY'
import csv
from pathlib import Path
for path in [Path('audits/baseline_reproduction_manual_v0/baseline_command_index.csv'), Path('audits/baseline_reproduction_manual_v0/environment_requirement_index.csv')]:
    with path.open(newline='', encoding='utf-8') as fh:
        rows=list(csv.DictReader(fh))
    if not rows:
        raise SystemExit(f'{path} has no rows')
PY
find docs examples/baseline_reproduction audits/baseline_reproduction_manual_v0 -type f \( -name '*.md' -o -name '*.csv' \) -print0 | xargs -0 -I{} sh -c 'test -s "$1" || exit 1' sh {}
git diff --name-status -- cases '**/skills.md' output reports results runs/user
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
```

Closeout validation commands are recorded in the project-control run log.
