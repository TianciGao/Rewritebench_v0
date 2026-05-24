# Canonical Metrics Review

Canonical local metrics command:
- Not run.

Reason:
- The intended live-provider smoke did not reach a live provider call.
- No candidates were generated.
- There were no candidate execution/checker results to summarize as meaningful local diagnostics.

Policy:
- No metrics were computed manually in this audit.
- No `python -m cli.main user compute-local-metrics` command was run.
- No official metrics, Semantic Equivalence Rate, formal Regression@20, paper result, retained evidence promotion, or leaderboard output was created.

Future condition:
- If a live-provider smoke succeeds and produces standard user-run output, local metrics may be computed only through `src/sql_rewrite_bench/local_metrics.py` via `python -m cli.main user compute-local-metrics`.
