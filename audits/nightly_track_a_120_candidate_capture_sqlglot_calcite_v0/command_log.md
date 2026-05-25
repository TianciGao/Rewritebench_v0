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
sed -n '1,280p' project_control/DECISION_LOG.md
tail -n 220 project_control/MIGRATION_RUN_LOG.md
```

## Adapter Inspection

```bash
rg -n "CANDIDATE|SQLRB_.*SOURCE|candidate_sql|adapter" baselines src/cli src/sql_rewrite_bench scripts
sed -n '1,760p' baselines/sqlglot/sqlglot_user_adapter.py
sed -n '1,980p' baselines/calcite_hep_fail_closed/adapter.py
sed -n '1,280p' src/sql_rewrite_bench/adapter_runner.py
sed -n '1,620p' src/sql_rewrite_bench/user_run.py
```

## Capture

An inline Python capture helper invoked the existing adapters directly with `SQLRB_CANDIDATE_SQL_PATH` set to D035-style candidate paths under `output/results/<run_id>/candidate_sql/...` and workspaces under `output/logs/<run_id>/workspaces/...`.

The adapter commands used were:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route noop
python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware
python baselines/calcite_hep_fail_closed/adapter.py
```

No `python -m cli.main user evaluate` command was used, because the current user runner writes transitional source runs under `runs/user/`.

## Validation

```bash
python - <<'PY'
# CSV, manifest, candidate path, SHA-256, and Markdown checks
PY

git status --short -- runs/user
git diff --name-status -- runs/user cases reports results
git status --short -- cases reports results runs/user output
python - <<'PY'
# Changed-file secret scan over committed audit/project-control files
PY
git diff --check
```

After explicit staging, the staged diff was checked for secrets before commit.

No live API, API-key, annotation-generation, POCR Stage B, DB/checker/timing, local_metrics, verifier, official metrics, paper rendering, candidate SQL movement/copy/deletion, or leaderboard commands were run.
