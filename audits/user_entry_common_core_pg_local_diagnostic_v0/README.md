# User-Entry Common-core PostgreSQL Local Diagnostic v0

Verdict: local diagnostic trial completed with exposed PostgreSQL source-execution failures.

This packet summarizes a bounded PostgreSQL-only Common-core v0 local diagnostic run using the public no-op adapter. The run exercised case selection, adapter capture, candidate preflight, PostgreSQL local execution, local checker comparison, ledger/failure accounting, quality summary/report generation, and tag slices.

This is local diagnostic output only. It is not official metrics, not paper reproduction, not timing or speedup, not reports/results migration, and not a leaderboard.

## Run Summary

- Run output: `runs/user/common_core_pg_noop_db_checker/`
- PostgreSQL environment ready: yes
- Selected rows: 40
- Candidate generated rows: 40
- Candidate preflight passed rows: 40
- DB execution enabled rows: 40
- DB execution attempted rows: 35 by current quality-summary derivation; the five source-execution failures did enter the PostgreSQL execution path but failed before candidate execution.
- Source executable rows: 35
- Candidate executable rows: 35
- Checker attempted rows: 35
- Exact rows: 35
- Mismatch rows: 0
- Source-like rows: 40

## Failure Summary

- `none`: 35
- `source_execution_failed`: 5

Failed cases: PORT_0004, PORT_0013, PORT_0022, PORT_0024, PORT_0025.

The five failures are PORT cases whose PostgreSQL source execution failed on backtick-quoted dialect SQL. Candidate execution and checker comparison were not attempted for those rows.

## Tag Slices

`tag_slices.csv` was generated with 57 local diagnostic tag rows across axes: portability_risk=21, rewrite_opportunity=10, sql_feature=26.

Tag slices are loaded from retained manifest taxonomy metadata and are not a tag score, ranking, official metric, paper result, or leaderboard input.

## Boundaries

- No official metrics computed.
- No timing or speedup computed.
- No paper tables rendered.
- No reports/results updated.
- No denominator, paper result, case membership, or raw legacy evidence changed.
- No MySQL or Spark run was attempted.
