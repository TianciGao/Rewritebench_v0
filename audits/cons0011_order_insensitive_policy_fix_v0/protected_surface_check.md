# Protected Surface Check

Allowed tracked changes for this task:

- `cases/CONS/CONS_0011/checker/normalization.yaml`
- `audits/cons0011_order_insensitive_policy_fix_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Observed tracked changes are limited to those surfaces.

Protected surfaces confirmed unchanged:

- SQL files: unchanged.
- Manifest files: unchanged.
- Global checker/source code: unchanged.
- Other case checker configs: unchanged.
- Schema files: unchanged.
- Validation files: unchanged.
- `case_sets/`: unchanged.
- `reports/`: unchanged.
- `results/`: unchanged.
- Denominator scaffolds: unchanged.
- Paper results: unchanged.
- Raw retained evidence: unchanged.
- Root metadata files: unchanged.
- Release tags/branches: unchanged.

Local run outputs:

- `runs/user/cons0011_spark_order_fix/`
- `runs/user/spark_two_case_regression_after_cons0011_fix/`
- `runs/user/common_core_spark_after_cons0011_order_fix/`

These are ignored local diagnostic outputs and are not staged or committed.

Validation:

- `git diff --check`: passed.
- YAML parse check for modified normalization config: passed.
- Audit CSV parse checks: passed for `before_after_outcome_summary.csv` and `regression_check_summary.csv`.
- Audit Markdown sanity checks: passed for 4 Markdown files.
- Protected-surface scripted check: passed; only allowed tracked paths changed.
