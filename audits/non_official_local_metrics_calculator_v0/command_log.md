# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git log --oneline -8
git merge-base --is-ancestor 2990340ec5a0d4682288e125606caf85d146d558 HEAD
rg -n "D033|local_metrics_v0_final_formula_decision_v0|Commit hash:|Push result:" project_control/DECISION_LOG.md project_control/MIGRATION_RUN_LOG.md project_control/MIGRATION_STATUS.md
```

Context read:

```bash
project_control/MIGRATION_MASTER_PLAN.md
project_control/MIGRATION_STATUS.md
project_control/MIGRATION_RUN_LOG.md
project_control/DECISION_LOG.md
project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
repository_spec/timing_artifact_schema_v0_draft.md
docs/user_entry_checker_policy.md
audits/local_metrics_v0_final_formula_decision_v0/
audits/exact_gated_local_timing_artifact_review_v0/
audits/exact_gated_local_timing_diagnostic_v0/
audits/timing_schema_open_questions_resolution_v0/
```

Implementation and validation:

```bash
PYTHONPATH=src pytest tests/user_entry/test_local_metrics.py -q
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/local_metrics.py scripts/dev/compute_local_user_metrics.py
PYTHONPATH=src python scripts/dev/compute_local_user_metrics.py \
  --run runs/user/timing_sqlglot_noop_postgres_smoke \
  --run runs/user/timing_sqlglot_noop_mysql_smoke \
  --run runs/user/timing_sqlglot_noop_spark_smoke
PYTHONPATH=src pytest tests/user_entry -q
```

Final validation:

```bash
PYTHONPATH=src pytest tests/user_entry/test_local_metrics.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/local_metrics.py scripts/dev/compute_local_user_metrics.py
python - <<'PY'
from pathlib import Path
for path in [
    Path("project_control/MIGRATION_MASTER_PLAN.md"),
    Path("project_control/MIGRATION_STATUS.md"),
    Path("project_control/MIGRATION_RUN_LOG.md"),
    Path("project_control/DECISION_LOG.md"),
]:
    assert path.read_text(encoding="utf-8").strip(), path
PY
git diff --check
git diff --name-only
git ls-files --others --exclude-standard
```

Results:

- Focused local metrics tests: passed, 6 tests.
- Full user-entry tests: passed, 159 tests, 1 skipped, 12 subtests passed.
- Python compile: passed.
- Bounded local metrics smoke output sanity: passed.
- Project-control readability: passed.
- Audit Markdown/CSV/JSON sanity: passed.
- Protected-surface check: passed.
- `runs/user/` committed output check: passed.
