# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 38a56dddbeb69d5668d181222873e878d09195fa HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
java -version
```

Candidate-generation run:

```bash
ROOT=/tmp/sqlrb_calcite_hep_pg_bounded_candidate_generation_v0
RUN_ID=calcite_hep_pg_candidate_generation
rm -rf "$ROOT/output" "$ROOT/run_snapshot" "runs/user/$RUN_ID"
mkdir -p "$ROOT"
SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep SQLRB_CALCITE_HEP_JAVA=/usr/bin/java SQLRB_CALCITE_HEP_TIMEOUT=30 python -m cli.main user evaluate   --case-set common_core_v0   --pool all   --engines postgres   --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py"   --output-root "$ROOT/output"   --run-id "$RUN_ID"   --adapter-timeout 40 > "$ROOT/run_stdout.txt" 2> "$ROOT/run_stderr.txt"
cp -a "runs/user/$RUN_ID" "$ROOT/run_snapshot"
rm -rf "runs/user/$RUN_ID"
```

Run stdout summary:

```text
sqlrb user evaluate complete: run_id=calcite_hep_pg_candidate_generation selected_rows=40 candidate_generated_rows=33
```

Validation:

```bash
python - <<'PY'  # audit Markdown/CSV/JSON sanity
...
PY
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
python -m py_compile baselines/calcite_hep_fail_closed/adapter.py
git diff --check
git status -sb
git status --porcelain -- runs/user output reports results
git diff --name-only
```

Validation results:

- Audit Markdown non-empty, `per_row_candidate_status.csv` has 40 data rows, and `diagnostic_summary.json` parses.
- `pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q`: 5 passed.
- `python -m py_compile baselines/calcite_hep_fail_closed/adapter.py`: passed.
- `git diff --check`: passed.
- Protected runtime surfaces showed no `runs/user`, repository-level `output`, top-level `reports`, or top-level `results` changes.
