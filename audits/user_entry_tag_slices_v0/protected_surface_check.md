# Protected Surface Check

## Allowed Changed Surfaces

- `src/sql_rewrite_bench/tag_slices.py`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/user_quality_report.py`
- `tests/user_entry/`
- `audits/user_entry_tag_slices_v0/`
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

No live DB/checker execution was run. No timing/speedup, official metrics, paper
tables, reports/results updates, retained-evidence parsing, tag score/ranking,
or global leaderboard were created.
