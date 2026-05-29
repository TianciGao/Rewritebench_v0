# Run Scope

## Selected Scope

- case set: `common_core_v0`
- planned cases: 40
- engines: `postgres`, `mysql`, `spark`
- planned rows: 120
- selected rows: 120
- route: `sqlglot_optimize_schema_aware`
- method: `sqlglot`

## Enabled

- candidate generation and capture;
- adapter preflight / fail-closed handling;
- source execution where the current local checker path can run it;
- candidate execution when an executable candidate exists;
- local result checker when source and candidate both execute.

The audit helper also recorded MySQL source-only execution for explicit MySQL fail-closed rows, matching the precedent from the post-ARRAY_ANY bounded rerun.

## Disabled

- timing;
- SQLSolver and VeriEQL;
- official metrics;
- official Semantic Equivalence Rate;
- formal Regression@20;
- POCR;
- paper report/result updates;
- retained evidence promotion;
- leaderboard output.

## Runtime Boundary

Runtime artifacts were written under:

`/tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/`

The committed repository contains only this audit packet and project-control writeback.
