# Rerun Plan

Recommended future sequence:

1. Keep current audit diagnostics as readiness evidence only.
2. Implement the missing user-facing exact-candidate verifier pair scope.
3. Rerun the selected candidate run through `sqlrb user verify --pair-scope run-candidates`.
4. Require identity guard for every attempted exact candidate row.
5. Emit canonical verifier outputs under `output/results|logs|reports/<run_id>/`.
6. Review coverage, identity failures, unknowns, timeouts, and non-equivalent rows.
7. Seek separate authorization before any paper-facing Semantic Equivalence Rate row is produced.

Suggested first rerun target after implementation:

- Tool: SQLSolver.
- Source candidate run: `runs/user/common_core_pg_noop_db_checker` or its future user-facing exported equivalent.
- Method/route: SQLGlot noop / `noop`.
- Engine: PostgreSQL.
- Scope: exact/result-consistent rows only.

VeriEQL should not be the first paper-facing rerun candidate because current corrected coverage is 4/35.
