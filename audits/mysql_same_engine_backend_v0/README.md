# MySQL Same-Engine Backend v0

Verdict: `completed_local_diagnostic_backend`.

This packet documents a bounded MySQL same-engine local diagnostic backend for user-entry runs. The backend executes a selected row's source SQL and adapter-generated candidate SQL in a local MySQL diagnostic database, writes local source/candidate result artifacts, and hands those artifacts to the existing local checker.

This is local diagnostic behavior only. It is not official metrics, not timing or speedup, not paper reproduction, not a reports/results update, not retained-evidence promotion, and not a leaderboard input.

## Implemented Behavior

- Same-engine `--engine mysql` rows now dispatch to MySQL source and candidate execution instead of the previous fail-closed stub.
- MySQL schema assets are resolved only through explicit external schema metadata for `engines.mysql`.
- Source SQL is resolved from the selected row's source SQL path.
- Candidate SQL is the adapter output captured in the per-row workspace.
- Source and candidate execute in the same temporary local MySQL diagnostic database.
- Result artifacts are written under the per-row workspace at `execution/mysql_same_engine/`.
- Existing MySQL source-reference behavior for PORT cross-dialect diagnostics is preserved under `execution/mysql_source/`.
- PostgreSQL same-engine behavior is preserved.
- Spark remains deferred and fail-closed.

## Live Smoke

Run output path: `runs/user/mysql_same_engine_smoke/`.

| Field | Count |
|---|---:|
| Selected rows | 2 |
| MySQL source executable rows | 2 |
| MySQL candidate executable rows | 2 |
| Checker attempted rows | 2 |
| Exact rows | 2 |
| Mismatch rows | 0 |

Selected live smoke cases: `PERF_0006`, `CONS_0005`.

The live smoke used the public no-op adapter, so exact rows only mean local diagnostic source-like candidate equivalence for that bounded smoke. They are not official metrics.

## Regression Checks

- PORT cross-dialect controlled regression: 5 selected rows, MySQL source-reference executable 5, PostgreSQL target-candidate executable 5, checker attempted 5, exact 5, mismatch 0.
- PostgreSQL public smoke dry-run and adapter-capture commands passed.
- Full user-entry tests passed with 102 passed and 2 skipped using the existing local pytest environment.
- Common-core v2 static case-package reference validation passed for all 40 case paths.

## Boundary

- No SQL files modified.
- No manifest files modified.
- No schema, checker, or validation files modified.
- No `case_sets/` changes.
- No reports/results updates.
- No denominator, paper result, case membership, or raw retained evidence changes.
- No timing/speedup fields introduced.
- No official metrics computed.
- No global leaderboard created.
- Local `runs/user/` outputs were used only for diagnostics and were not committed.

## Next Safe Action

Review the MySQL same-engine local diagnostic backend and audit packet. A future separately authorized task can expand live MySQL coverage beyond the bounded smoke while still keeping timing, official metrics, reports/results, paper rendering, and leaderboard work out of scope.
