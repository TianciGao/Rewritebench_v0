# Command Log

Preflight and context commands:

```text
pwd && git branch --show-current && git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,180p' project_control/MIGRATION_STATUS.md
tail -n 180 project_control/DECISION_LOG.md && tail -n 180 project_control/MIGRATION_RUN_LOG.md
rg --files audits/pocr_row_level_stage_b_artifact_contract_v0 audits/pocr_formula_dry_run_existing_diagnostics_v0
rg --files src/sql_rewrite_bench/pocr src/cli tests/pocr tests/user_entry
rg -n "pocr-diagnostic|pocr_diagnostic|diagnostic_rows|diagnostic_summary|Stage B|stage_b|output-root|output_root" src/sql_rewrite_bench/pocr src/cli tests/pocr tests/user_entry
```

Implementation inspection commands included reads of:

```text
src/sql_rewrite_bench/pocr/user_facade.py
src/sql_rewrite_bench/pocr/user_output_adapter.py
src/sql_rewrite_bench/pocr/diagnostic_output_schema.py
src/sql_rewrite_bench/pocr/candidate_resolver.py
src/sql_rewrite_bench/pocr/annotation_schema.py
src/sql_rewrite_bench/pocr/annotation_resolver.py
src/cli/pocr_diagnostic.py
tests/pocr/test_user_facade.py
tests/pocr/test_user_output_adapter.py
tests/user_entry/test_pocr_optional_user_run_integration.py
```

Validation commands:

```text
python -m py_compile src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/user_output_adapter.py src/sql_rewrite_bench/pocr/user_facade.py src/sql_rewrite_bench/pocr/__init__.py
pytest tests/pocr/test_stage_b_row_metrics.py tests/pocr/test_user_output_adapter.py tests/pocr/test_user_facade.py -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py::OptionalPOCRUserRunIntegrationTests::test_optional_pocr_writes_d035_outputs_under_temp_root_only -q
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
python CSV parse check for test-exported pocr_stage_b_row_metrics.csv
find audits/pocr_minimal_stage_b_row_metrics_exporter_v0 -name '*.md' -type f -print -exec test -s {} \;
python required boundary phrase check over audits/pocr_minimal_stage_b_row_metrics_exporter_v0/*.md
git diff --check
git diff --name-only -- cases ':(glob)**/skills.md' case_sets inventory reports results runs/user output
git diff --name-only | rg '(^|/)candidate_sql/|\.sql$' || true
changed-file secret scan
staged secret scan
git status -sb
git diff --name-status
```

No live API call, API key read, annotation JSONL generation, user replay rerun outside offline tests, DB/checker/timing run, baseline rerun, candidate SQL generation or mutation, official POCR computation, route-level official POCR score, paper-facing metric promotion, top-level reports/results update, retained-evidence promotion, or leaderboard output occurred.
