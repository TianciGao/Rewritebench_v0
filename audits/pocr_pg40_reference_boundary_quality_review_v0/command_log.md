# Command Log

Initial confirmation:

```bash
pwd
git branch --show-current
git status -sb --untracked-files=normal
```

Required project-control reads:

```bash
sed -n '1,180p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,260p' project_control/DECISION_LOG.md
tail -220 project_control/MIGRATION_RUN_LOG.md
```

Review reads:

```bash
rg -n "positive|source|candidate|skills|operation_atom|semantic_guard|source_candidate_diff|candidate_sql_span|positive_sql_span|source_sql_span|no-op|noop|not official|Stage B|operation coverage|curated" src/sql_rewrite_bench/pocr src/cli tests/pocr
sed -n '1,260p' src/sql_rewrite_bench/pocr/prompt_builder.py
sed -n '1,300p' src/sql_rewrite_bench/pocr/operation_evidence_policy.py
sed -n '1,320p' src/sql_rewrite_bench/pocr/stage_b_row_metrics.py
sed -n '1,320p' src/sql_rewrite_bench/pocr/pocr_aggregator.py
sed -n '1,340p' src/sql_rewrite_bench/pocr/user_facade.py
sed -n '1,320p' src/sql_rewrite_bench/pocr/diagnostic_output_schema.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/candidate_resolver.py
sed -n '1,260p' src/cli/pocr_diagnostic.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/skills_parser.py
sed -n '1,260p' tests/pocr/test_evidence_validation.py
sed -n '1,260p' tests/pocr/test_prompt_builder.py
sed -n '1,280p' tests/pocr/test_pocr_aggregator.py
```

Audit packets reviewed included the PG40 pilot, tri-engine pilot retry/readiness, tri-engine pilot run, D039 promotion design, row-metrics exporter, and planned/candidate aggregator packets.

Validation commands:

```bash
python - <<'PY'
# Markdown non-empty checks, optional checklist CSV parse check, and required phrase checks.
PY
python -m py_compile src/sql_rewrite_bench/pocr/prompt_builder.py src/sql_rewrite_bench/pocr/operation_evidence_policy.py src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py src/sql_rewrite_bench/pocr/user_facade.py src/cli/pocr_diagnostic.py
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
git diff --check
git status --short cases ':(glob)**/skills.md' runs/user reports results case_sets
git diff --name-status -- cases ':(glob)**/skills.md' runs/user reports results case_sets
rg -n --hidden -S '<secret-patterns>' audits/pocr_pg40_reference_boundary_quality_review_v0 project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md
git status -sb --untracked-files=normal
git diff --name-status
```

Validation results:

- Markdown non-empty checks passed.
- `reference_boundary_checklist.csv` parse check passed with 10 rows.
- Required phrase checks passed.
- `python -m py_compile` passed for reviewed POCR modules.
- `pytest tests/pocr -q` passed with 143 tests.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q` passed with 28 tests.
- `git diff --check` passed.
- Protected-path checks found no `cases/`, `skills.md`, candidate SQL, `runs/user`, top-level `reports/`, top-level `results/`, or `case_sets/` modifications.
- Changed-file secret scan found no API key values.

Boundary phrases checked:

- This is not official POCR.
- No route-level official POCR score is emitted.
- No paper-facing metric is promoted.
- SQLGlot no-op is a candidate/control route, not a reference.
- positive SQL is reference evidence, not an atom source.
- skills.md is the only operation-atom source.
- candidate/source/positive span presence alone is not operation support.
- POCR@curated remains deferred until a predeclared curated manifest exists.
