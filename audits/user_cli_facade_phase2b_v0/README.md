# user_cli_facade_phase2b_v0

Verdict: completed.

This audit records Phase 2B of the local evaluation workbench user surface: a thin `src/cli` facade for local user-evaluation commands. The facade delegates to existing `src/sql_rewrite_bench` internals and the Phase 2A output exporter; it does not implement verifier integration, official metrics, paper reporting, retained-evidence promotion, physical layout migration, or leaderboard output.

Implemented command group:

- `sqlrb user evaluate`
- `sqlrb user list-cases`
- `sqlrb user explain-selection`
- `sqlrb user show-output-schema`
- `sqlrb user show-boundary`
- `sqlrb user compute-local-metrics`
- `sqlrb user summarize`

The bounded CLI smoke used SQLGlot noop over PostgreSQL only with the deterministic smoke subset `PERF_0006` and `CONS_0005`. It selected 2 rows, generated 2 candidates, executed source/candidate successfully for 2 rows, checked 2 rows, and produced 2 exact / 0 mismatch. Runtime outputs were written only to `runs/user/` plus a temporary `/tmp` output root during the smoke and were removed before commit.

Boundary:

- Local diagnostic only.
- No full Common-core run.
- No SQLGlot optimize run.
- No timing collection.
- No official metrics.
- No top-level `reports/` or `results/` update.
- No retained-evidence promotion.
- No leaderboard output.

Next safe action: implement Phase 2C summary/local-metrics facade hardening or run a narrow user-facing CLI review before expanding beyond bounded smoke.
