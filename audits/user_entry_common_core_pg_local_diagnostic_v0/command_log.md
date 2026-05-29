# Command Log

Commands run before execution:

```bash
git status -sb
git branch --show-current
git log --oneline -10
```

Context read:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md` tail
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- current user-entry execution/checker/report/tag modules
- `examples/user/noop_adapter.py`

Environment checks:

```bash
command -v psql
psql --version
psql -X -v ON_ERROR_STOP=1 -q -Atc 'select 1'
```

Run command:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run   --case-set common_core_v0   --engine postgres   --adapter-command "python examples/user/noop_adapter.py"   --out runs/user/common_core_pg_noop_db_checker   --enable-db-execution   --enable-checker
```

Observed result:

- Command exited 0.
- `selected_rows=40`.
- `candidate_generated_rows=40`.
- Local run outputs were written under `runs/user/common_core_pg_noop_db_checker/`.
- Local run outputs remain ignored local diagnostics and were not staged.

Final validation result: passed.

Final validation included:

- `git diff --check`.
- CSV/JSON parse checks for the audit files.
- Markdown sanity checks for the audit Markdown files.
- Protected-surface diff check.
- Confirmation that `runs/user/common_core_pg_noop_db_checker/` is ignored local output and not staged.
