# Protected Surface Check

Allowed committed modifications for this task:

- `audits/spark_live_two_case_smoke_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces checked:

- Source code: not modified.
- Scripts: not modified.
- Tests: not modified.
- Examples: not modified.
- Cases, manifests, SQL files, schema files, checker files, and validation files: not modified.
- `case_sets/`: not modified.
- `reports/` and `results/`: not modified.
- Denominator scaffolds: not modified.
- Paper results: not modified.
- Raw retained evidence: not modified.
- `.github/workflows/`: not modified.
- Root metadata files: not modified.
- Release tags or branches: not changed.

Local output boundary:

- `runs/user/spark_live_smoke/` was created as ignored local diagnostic output.
- `runs/user/spark_live_smoke/` is not intended to be staged or committed.

Validation note:

- `git diff --check`: passed.
- CSV/JSON parse checks for audit files: passed.
- Markdown sanity checks for audit Markdown files: passed.
- Protected-surface status check: passed. The only tracked modifications are `project_control/MIGRATION_STATUS.md` and `project_control/MIGRATION_RUN_LOG.md`; the only untracked files are under `audits/spark_live_two_case_smoke_v0/`.
- Ignored local run output check: `runs/user/spark_live_smoke/` remains ignored and is not staged.
