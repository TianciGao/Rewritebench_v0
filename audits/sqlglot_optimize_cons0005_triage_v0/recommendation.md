# Recommendation

Recommended action: keep the current `sqlglot_optimize` route fail-visible for now.

Rationale:

- The current adapter route is explicitly context-free: it reads source SQL, parses by selected engine dialect, calls SQLGlot `optimize(expression)`, and emits candidate SQL.
- The observed failure is clear local diagnostic behavior: `CONS_0005` candidate generation succeeds, preflight passes, source execution succeeds, candidate execution fails, and checker is not attempted.
- The failure is reproducible outside `user_run` with a minimal SQLGlot snippet.
- The no-op route remains valid for the same case and engines, so the backend/checker path is not the immediate cause.
- A schema-aware optimizer experiment avoids the invalid reference, but it changes route semantics and may emit dialect constructs needing separate validation.

Future options:

- Add a documentation warning that `sqlglot_optimize` is context-free and may emit invalid qualification for correlated subqueries.
- Design a separately named schema-aware SQLGlot route in a future authorized task, using case schema metadata through the runner/adapter contract and preserving route comparability.
- Keep `CONS_0005` as a bounded fail-visible regression case for any future SQLGlot optimize-route change.

Not recommended in this task:

- Do not patch `baselines/sqlglot/sqlglot_user_adapter.py`.
- Do not silently change `--route optimize` to inject schema.
- Do not broaden the optimize route trial.
- Do not convert these local diagnostic failures into official metrics, timing, paper results, retained evidence, reports/results, or leaderboard outputs.
