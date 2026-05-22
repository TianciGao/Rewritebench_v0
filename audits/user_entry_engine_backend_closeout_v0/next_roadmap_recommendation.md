# Next Roadmap Recommendation

Recommended next safe step: return to release/paper planning, with an optional narrow real-adapter local diagnostic evaluation only if it remains local-only and non-metric.

Rationale:

- PostgreSQL and MySQL local diagnostic backends are implemented and have current bounded rerun snapshots.
- PORT bidirectional cross-dialect controlled diagnostics are closed for the current user-entry phase.
- Spark is explicit and fail-closed, but live execution needs a separate staged implementation plan.
- Timing, official metrics, paper rendering, reports/results updates, retained-evidence promotion, release export/tagging, and leaderboard output remain out of scope.

Allowed future directions after separate authorization:

- Spark live backend planning, starting with schema/load resolver or mocked execution contract tests.
- Timing protocol design only, without implementing timing collection or speedup metrics.
- Real adapter diagnostic evaluation, clearly labeled local-only and not official metrics.
- Release/paper planning using existing audit evidence and keeping reports/results untouched unless separately authorized.

This recommendation does not authorize timing implementation, official metrics, paper table rendering, reports/results updates, retained-evidence promotion, release tag/export branch creation, or leaderboard output.
