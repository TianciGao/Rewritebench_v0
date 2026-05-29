# Protected Surface Check

## Allowed Changed Surfaces

- `src/sql_rewrite_bench/user_quality_report.py`
- `src/sql_rewrite_bench/user_run.py`
- `tests/user_entry/`
- `audits/user_entry_local_quality_report_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Protected Surfaces

- `cases/`: unchanged
- manifests: unchanged
- `sql/`: unchanged
- `schema/`: unchanged
- `checker/`: unchanged
- `validation/`: unchanged
- `case_sets/`: unchanged
- `inventory/`: unchanged
- `reports/`: unchanged
- `results/`: unchanged
- `benchmark_spec/`: unchanged
- `repository_spec/`: unchanged
- denominator scaffolds: unchanged
- paper results: unchanged
- raw retained evidence: unchanged

## Boundary

No live DB/checker execution was run. No official metrics, paper tables, tag slices, timing/speedup, reports/results updates, retained-evidence parsing, or global leaderboard were created.
