# Protected Surface Check

Allowed release-repo modifications:

- `audits/calcite_hep_pg_execution_checker_diagnostic_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces expected unchanged:

- `src/`
- `tests/`
- `baselines/calcite_hep_fail_closed/adapter.py`
- `cases/`
- `case_sets/`
- top-level `reports/`
- top-level `results/`
- retained evidence
- repository-level `output/`
- `runs/user/`
- Calcite source/JAR/class/build outputs
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

Validation result:

- Audit Markdown files are non-empty.
- `per_row_execution_checker_status.csv` has the expected header and 40 data rows.
- `diagnostic_summary.json` parses and records 40 selected rows, 33 generated candidates, 7 no-candidate rows, and 20 exact rows.
- `pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q`: 5 passed.
- `python -m py_compile baselines/calcite_hep_fail_closed/adapter.py audits/calcite_hep_pg_execution_checker_diagnostic_v0/run_pg_execution_checker_from_prior_candidates.py`: passed.
- `git diff --check`: passed.
- `git status --porcelain -- runs/user output reports results`: no output.
- Tracked Calcite artifact scan found no Calcite JAR/class/build artifacts.
- Changed release-repo paths are limited to this audit packet and project-control writeback files.
