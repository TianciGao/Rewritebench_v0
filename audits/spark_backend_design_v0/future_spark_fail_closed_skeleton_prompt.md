# Future Prompt: Spark Fail-Closed Skeleton and Environment Detector

Task title: Implement Spark fail-closed environment detector for user-entry local diagnostics

Purpose: Add a narrow Spark local diagnostic skeleton that reports explicit Spark readiness/fail-closed statuses without executing Spark SQL.

Allowed scope:

- Update `src/sql_rewrite_bench/spark_execution.py` to add environment/config detection only.
- Update status constants only if needed for transparent local diagnostic statuses.
- Add mocked tests under `tests/user_entry/`.
- Add an audit packet under `audits/spark_fail_closed_skeleton_v0/`.
- Update project-control status and run log.

Requirements:

- Do not start Spark sessions.
- Do not execute Spark SQL.
- Do not modify SQL, manifests, schemas, checker configs, validation files, or case_sets.
- Do not compute timing, speedup, official metrics, paper tables, reports/results, retained evidence, or leaderboard output.
- Fail closed when Spark local diagnostics are not explicitly enabled.
- Report whether `pyspark` is importable and whether minimal local Spark env variables are present, without printing secrets or full environment dumps.
- Preserve PostgreSQL/MySQL behavior and bidirectional PORT controlled routes.

Validation:

- `git diff --check`.
- Python compile for modified files.
- User-entry tests using mocks; no live Spark required.
- Help/readability commands.
- Protected-surface check.

Next phases beyond this skeleton require separate authorization.
