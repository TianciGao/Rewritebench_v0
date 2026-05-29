# Source Run Review

Source run:
- `runs/user/common_core_pg_noop_db_checker`

Relevant artifacts:
- Ledger: `runs/user/common_core_pg_noop_db_checker/ledger.csv`
- Quality summary: `runs/user/common_core_pg_noop_db_checker/quality_summary.json`
- Candidate SQL: `runs/user/common_core_pg_noop_db_checker/candidate_sql/`

Run shape:
- Baseline route/method: SQLGlot noop.
- Engine: PostgreSQL.
- Selected rows: 40.
- Exact/result-consistent rows: 35.
- Non-exact rows: 5.

Non-exact verifier-ineligible rows:

| case_id | pool | reason |
| --- | --- | --- |
| PORT_0004 | PORT | source execution failed |
| PORT_0013 | PORT | source execution failed |
| PORT_0022 | PORT | source execution failed |
| PORT_0024 | PORT | source execution failed |
| PORT_0025 | PORT | source execution failed |

This plan does not rerun the source run and does not modify `runs/user/`.

