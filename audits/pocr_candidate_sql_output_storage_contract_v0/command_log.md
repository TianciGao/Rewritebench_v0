# Command Log

Commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`.

## Preflight

```bash
pwd
git branch --show-current
git status -sb
```

## Project-Control Reads

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,260p' project_control/DECISION_LOG.md
tail -n 180 project_control/MIGRATION_RUN_LOG.md
```

## Docs Inspection

```bash
find docs -maxdepth 2 -type f | sort | sed -n '1,120p'
sed -n '1,220p' docs/README.md
sed -n '1,240p' docs/pocr_diagnostic.md
```

## Validation

```bash
python -m pytest tests/pocr -q
python -m pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
git diff --check
git status -sb
git diff --name-status
```

No live API, API-key, annotation-generation, DB/checker/timing, baseline, verifier, official metrics, paper rendering, output creation, candidate SQL movement/copy/deletion, or leaderboard commands were run.
