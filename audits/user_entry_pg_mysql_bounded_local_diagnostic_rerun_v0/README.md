# PostgreSQL and MySQL Bounded Local Diagnostic Rerun v0

Verdict: `completed_with_failures`.

This packet summarizes a bounded Common-core v0 rerun for PostgreSQL and MySQL using the public no-op adapter after PORT target-engine-aware role mapping and bidirectional controlled closeout.

This is local diagnostic output only. It is not official metrics, not Track A paper output, not timing or speedup, not reports/results migration, not retained-evidence promotion, and not a leaderboard input.

## PostgreSQL Run

- Output path: `runs/user/bounded_pg_noop_db_checker_current/`.
- Selected rows: 40.
- Candidate generated rows: 40.
- Source executable rows: 40.
- Candidate executable rows: 35.
- Checker attempted rows: 35.
- Exact rows: 35.
- Mismatch rows: 0.
- Failure buckets: candidate_execution_failed=5, none=35.

The five PostgreSQL failures are target-candidate execution failures on PORT cross-dialect rows where the no-op adapter emits source-like MySQL SQL. MySQL source-reference execution succeeded for those rows before PostgreSQL target-candidate execution failed.

## MySQL Run

- Output path: `runs/user/bounded_mysql_noop_db_checker_current/`.
- Selected rows: 40.
- Candidate generated rows: 40.
- Source executable rows: 40.
- Candidate executable rows: 36.
- Checker attempted rows: 36.
- Exact rows: 36.
- Mismatch rows: 0.
- Failure buckets: candidate_execution_failed=4, none=36.

The four MySQL failures are target-candidate execution failures on reverse PORT cross-dialect rows where the no-op adapter emits source-like PostgreSQL SQL. PostgreSQL source-reference execution succeeded for those rows before MySQL target-candidate execution failed.

## Interpretation

The no-op adapter is source-like. It validates adapter capture, routing, DB execution, checker handoff, quality summary, quality report, and tag-slice production, but it is not a PORT target-generating adapter for cross-dialect exactness. Controlled target-reference diagnostics remain the evidence for bidirectional PORT route validation: forward exact 5/5 and reverse exact 4/4.

## Recommended Next Safe Action

Use this packet as the current PostgreSQL/MySQL no-op local diagnostic snapshot. Any real adapter evaluation, Spark live execution, timing design or implementation, official metrics, paper rendering, reports/results updates, retained-evidence promotion, leaderboard output, or release export requires separate authorization.
