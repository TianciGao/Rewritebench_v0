# PORT Cross-Dialect Runner Metadata Consumption

Verdict: `completed`.

P3 updated local user-entry diagnostics and static validation so the repository understands the additive `local_diagnostic` manifest role metadata added to all 9 Common-core PORT manifests in P2.

Implemented scope:

- Static v2 case-package validation now accepts and validates the top-level `local_diagnostic` block.
- `case_package_resolver.py` exposes explicit diagnostic mode, source-reference engine/query, target-candidate engine, target-reference path/role, and boundary flags.
- The engine router consumes `diagnostic_mode`.
- Declared cross-dialect PORT rows fail closed with `cross_dialect_backend_missing` while the MySQL source-reference backend remains unimplemented.
- The PostgreSQL executor is not invoked for declared cross-dialect PORT source-reference SQL.

Boundary:

- Local diagnostic only.
- No live MySQL execution implemented.
- No live Spark execution implemented.
- No SQL edits.
- No manifest edits.
- No official metrics.
- No timing or speedup.
- No reports/results updates.
- No leaderboard.

Next safe action: authorize a separate P4/P5 design or implementation task for MySQL source-side local diagnostic execution only if the maintainer accepts the fail-closed P3 behavior.
