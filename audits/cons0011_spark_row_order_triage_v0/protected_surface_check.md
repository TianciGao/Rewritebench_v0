# Protected Surface Check

Allowed changed surfaces for this triage:

- `audits/cons0011_spark_row_order_triage_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces not to change:

- source code;
- scripts;
- tests;
- docs outside the audit packet and project-control files;
- examples;
- cases, manifests, SQL files, schema files, checker config files, and validation files;
- `case_sets/`;
- `reports/`;
- `results/`;
- denominator scaffolds;
- paper results;
- raw retained evidence;
- root metadata files;
- release tags or branches.

Validation result: passed.

Checks performed:

- `git diff --check`: passed with no output.
- Audit CSV parse checks: passed for `cons0011_result_shape.csv` and `checker_config_review.csv`.
- Local JSON artifact parse checks: passed for `checker_result.json`, `mismatch_summary.json`, and `spark_execution_metadata.json`.
- Audit Markdown sanity checks: passed for 5 Markdown files.
- Protected-surface status check: only `audits/cons0011_spark_row_order_triage_v0/*`, `project_control/MIGRATION_STATUS.md`, and `project_control/MIGRATION_RUN_LOG.md` changed.

Local run outputs:

- Existing local artifacts used: `runs/user/common_core_spark_noop_db_checker/`
- `CONS_0011` rerun output created: no.
- Local run outputs staged or committed: no.
