# Command Log

Preflight and source review:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 0d60f06765c0ab4eca4d7af9558453a4000183af HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
scripts/dev/check_local_engine_env.py
```

Timing run:

```bash
rm -rf /tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0
PYTHONPATH=src python audits/sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/run_track_a_120_exact_timing.py
```

Validation:

```bash
python -m py_compile audits/sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/run_track_a_120_exact_timing.py
wc -l audits/sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/per_row_timing.csv
head -1 audits/sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/per_row_timing.csv
python -m json.tool audits/sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/diagnostic_summary.json
pytest tests/user_entry/test_local_timing.py -q
pytest tests/user_entry/test_sqlglot_adapter.py -q
git diff --check
git status -sb
git status --porcelain -- runs/user output reports results src tests baselines cases case_sets schemas inventory
```

Observed validation results:

- CSV row count: 120 data rows plus header.
- Timing attempted/timed/failed: 66 / 66 / 0.
- Summary JSON parsed.
- `pytest tests/user_entry/test_local_timing.py -q`: 7 passed.
- `pytest tests/user_entry/test_sqlglot_adapter.py -q`: 14 passed, 1 skipped.
- CSV/JSON invariant validation passed.
- `git diff --check`: passed.
- Protected-path status check for `runs/user`, repository-level `output`, top-level `reports`, top-level `results`, `src`, `tests`, `baselines`, `cases`, `case_sets`, `schemas`, and `inventory`: no output.
