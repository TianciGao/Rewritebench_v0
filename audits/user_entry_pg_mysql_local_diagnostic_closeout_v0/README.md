# PostgreSQL and MySQL Local Diagnostic Closeout v0

Verdict: `pg_mysql_local_diagnostic_ready_with_deferred_items`.

This audit closes the current PostgreSQL/MySQL user-entry local diagnostic capability review after the bidirectional PORT cross-dialect closeout. It consolidates evidence from the user-entry U0-U7 closeout, the PostgreSQL Common-core local diagnostic trial, the MySQL same-engine backend implementation, the MySQL Common-core local diagnostic trial, the MySQL source-failure triage, target-engine-aware PORT role mapping, and bidirectional PORT controlled diagnostics.

This is local diagnostic closeout only. It does not compute official metrics, run timing, compute speedup, render paper tables, update reports/results, promote retained evidence, create a leaderboard, change denominators, change paper results, change case membership, or create a release tag/export branch.

## Supported Capabilities

- The user-entry harness can select Common-core rows, capture adapter output, run candidate preflight, execute optional local DB diagnostics, run the local checker, write ledger/failure files, produce local quality summaries, and write tag slices.
- PostgreSQL same-engine local diagnostics are implemented and live validated.
- MySQL same-engine local diagnostics are implemented and live smoke validated on `PERF_0006` and `CONS_0005`.
- MySQL Common-core no-op local diagnostics executed 31 same-engine rows exactly, with remaining PORT findings now explained by role mapping and cross-dialect routing.
- PORT forward controlled diagnostics are validated: MySQL source-reference to PostgreSQL target-candidate, exact 5/5.
- PORT reverse controlled diagnostics are validated: PostgreSQL source-reference to MySQL target-candidate, exact 4/4.
- Target-engine-aware PORT metadata and runner consumption prevent wrong-engine source execution in both directions.
- Local quality reports and tag slices remain local diagnostic artifacts, not official metrics or leaderboard inputs.

## Remaining Gaps

Spark live execution remains deferred/fail-closed. Real user PORT adapter evaluation remains future work. Timing/speedup, official metrics, paper rendering, retained evidence integration, reports/results migration, release/export tagging, and leaderboard output remain deferred or forbidden for this phase.

## Interpretation

PostgreSQL and MySQL local diagnostics are ready for broader bounded local reruns, provided the run is treated as diagnostic only and not as `40 x 2` official metric output. Controlled target-reference adapters validate routing and checker handoff, but they are not user methods or benchmark baselines. The no-op adapter validates source-like local behavior, not PORT cross-dialect target generation quality.

## Recommended Next Safe Action

Run a bounded PostgreSQL+MySQL local diagnostic rerun as a diagnostic closeout only, with no timing, no official metrics, no paper rendering, no reports/results update, no retained-evidence promotion, and no leaderboard. If broader engine work is prioritized instead, Spark should remain a design-only task until explicitly authorized.
