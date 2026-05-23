# Calcite HEP PostgreSQL Identifier Quoting Fix

Task: `calcite_hep_pg_identifier_quoting_fix_v0`

Branch: `feature/case-package-v2-external-schema`

Scope: local-only PostgreSQL diagnostic fix for the Calcite HEP fail-closed route at `baselines/calcite_hep_fail_closed/adapter.py`.

The fix is a narrow PostgreSQL-only candidate postprocess. It unquotes and lowercases simple Calcite-emitted quoted identifiers only when the lowercase identifier is present as an unquoted table or column name in the resolved PostgreSQL DDL. This targets generated candidates such as `"DEPT"` against PostgreSQL schemas loaded as `dept`.

Targeted validation used the 9 identifier-quoting rows from `audits/calcite_hep_pg_frontier_blocker_triage_v0/frontier_inventory.csv`:

- `PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`
- `CONS_0036`, `CONS_0037`
- `LONGTAIL_0011`, `LONGTAIL_0012`, `LONGTAIL_0013`

Validation result:

- Target rows: 9
- Candidate generated after fix: 5
- Candidate executable after fix: 5
- Exact/result-consistent after fix: 1 (`CONS_0037`)
- Improved to candidate executable but checker mismatch: 4 (`CONS_0036`, `LONGTAIL_0011`, `LONGTAIL_0012`, `LONGTAIL_0013`)
- Unchanged no-candidate parse rows: 4 (`PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`)
- Regressions: 0

No timing, verifier pass, official metrics, paper result, retained evidence promotion, leaderboard output, MySQL/Spark run, or full Track-A run was performed.
