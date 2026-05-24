# User Metrics Source Of Truth Alignment

Task: `user_metrics_source_of_truth_alignment_v0`

Verdict: the canonical local diagnostic metric source of truth is `src/sql_rewrite_bench/local_metrics.py`, reached through `compute_and_write_local_metrics(run_dir)` or the CLI facade command `python -m cli.main user compute-local-metrics`.

The reviewed route-card and comparison audit packets are not canonical local metrics outputs. They are useful local diagnostic evidence, but their route cards, comparison tables, and speedup/rate summaries were assembled by audit helpers or manual audit aggregation rather than by `local_metrics.py`.

Immediate correction:

- Stop creating route-card or comparison metric outputs from audit helper formulas.
- Treat existing `route_card.json`, `route_card.csv`, `comparison_table.csv`, and helper-computed diagnostic summaries as audit-only provisional summaries.
- Replace the previous `sqlglot_optimize_schema_aware` route-card projection plan with a canonical user-facade run or re-run that produces a standard source run, followed by `sqlrb user compute-local-metrics`.

No experiments, metrics computation, verifier pass, paper output, retained-evidence promotion, or leaderboard output were run in this task.
