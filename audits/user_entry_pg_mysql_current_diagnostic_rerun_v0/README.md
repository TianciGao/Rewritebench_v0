# PostgreSQL and MySQL Current Local Diagnostic Rerun v0

Verdict: `completed_with_expected_noop_cross_dialect_target_failures`.

This audit summarizes the bounded PostgreSQL and MySQL Common-core v0 local diagnostic rerun after target-engine-aware PORT role mapping, bidirectional PORT controlled closeout, MySQL same-engine backend implementation, and opt-in cross-dialect checker normalization.

This is local diagnostic output only. It is not a paper result, not Track A official metric output, not timing or speedup, not a reports/results update, not retained-evidence promotion, not a leaderboard, and not a release/export tag.

## Run Summary

- PostgreSQL run output: `runs/user/bounded_pg_noop_db_checker_current/`.
- MySQL run output: `runs/user/bounded_mysql_noop_db_checker_current/`.
- Adapter: `python examples/user/noop_adapter.py`.
- PostgreSQL selected rows: 40; exact local diagnostic rows: 35; mismatch rows: 0; failure buckets: `none=35`, `candidate_execution_failed=5`.
- MySQL selected rows: 40; exact local diagnostic rows: 36; mismatch rows: 0; failure buckets: `none=36`, `candidate_execution_failed=4`.
- PostgreSQL source-reference executable rows: 40/40.
- MySQL source-reference executable rows: 40/40.

## Interpretation

The current rerun confirms that source-reference execution now reaches all selected PostgreSQL and MySQL rows. The remaining failures are target-candidate execution failures in PORT cross-dialect rows where the no-op adapter copied source-like SQL into the selected target engine.

For PostgreSQL, the five failures are `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`: MySQL source-reference executed, but the no-op target candidate remained MySQL-like and failed in PostgreSQL.

For MySQL, the four failures are `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`: PostgreSQL source-reference executed, but the no-op target candidate remained PostgreSQL-like and failed in MySQL.

This is expected no-op behavior for cross-dialect PORT routes. Controlled target-reference diagnostics already validated the target-side path separately: forward exact 5/5 and reverse exact 4/4. The no-op adapter is not a PORT target candidate for cross-dialect exactness.

## Boundary

- Official metrics computed: no.
- Timing/speedup computed: no.
- Reports/results updated: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local run outputs committed: no.

## Recommended Next Safe Action

Treat this as the current local diagnostic snapshot for PostgreSQL and MySQL user-entry behavior. If further work is authorized, keep it separate: either evaluate real adapters under local-only boundaries, design Spark fail-closed/live execution, or return to release/paper planning. Do not start timing or official metrics from this rerun.
