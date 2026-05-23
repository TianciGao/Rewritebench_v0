# Source Run Review

Source run inspected: `runs/user/common_core_pg_noop_db_checker`.

The run is the existing SQLGlot-noop PostgreSQL local diagnostic run. It contains 40 selected Common-core rows. The exact/result-consistency gate identified 35 rows eligible for SQLSolver verifier execution and five PostgreSQL PORT rows as ineligible because source execution failed in the source run.

Counts:

- Selected rows: 40.
- Exact/result-consistent rows: 35.
- Not-attempted ineligible rows: 5.
- Method id: `sqlglot_noop`.
- Route id: `noop`.
- Engine: `postgres`.

The five ineligible rows were retained in `per_row_identity_summary.csv` as `not_attempted_ineligible`, not silently dropped.
