# PORT Reverse Cross-Dialect MySQL Target Diagnostic v0

Verdict: `completed`.

This audit validates the reverse PORT local diagnostic route for `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`:

PostgreSQL source-reference -> MySQL target-candidate.

The controlled adapter `examples/user/port_mysql_target_reference_adapter.py` copies only the manifest-declared `local_diagnostic.engine_roles.mysql.target_reference.query` into the candidate path. It is not a user method, not a benchmark baseline, not a source oracle, and not an official metric input.

## Run Summary

- Selected rows: 4.
- Candidate generated rows: 4.
- PostgreSQL source-reference attempted/executable/failed rows: 4/4/0.
- MySQL target-candidate attempted/executable/failed rows: 4/4/0.
- Checker attempted/exact/mismatch rows: 4/4/0.
- Failure buckets: none=4.

## Interpretation

The reverse controlled diagnostic reached exact 4/4. The runner used manifest-declared target-engine-aware roles, executed PostgreSQL source-reference artifacts, executed MySQL target-candidate artifacts, and handed both artifacts to the local checker. It did not execute PostgreSQL-like `source.sql` directly in MySQL and did not use `target_reference` as a checker oracle.

Forward MySQL-source -> PostgreSQL-target regression was also checked and remained exact 5/5.

## Boundary

This is local diagnostic only. No official metrics, timing/speedup, reports/results updates, denominator changes, paper-result changes, retained-evidence promotion, raw legacy evidence changes, or leaderboard output were produced.

## Recommended Next Safe Action

Close the controlled bidirectional PORT cross-dialect local diagnostic path, or run a narrow audit-only closeout summarizing both directions. Real user adapter evaluation, timing, official metrics, reports/results updates, paper rendering, retained-evidence promotion, and leaderboard output remain out of scope.
