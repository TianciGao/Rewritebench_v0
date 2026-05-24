# Boundary

This review is local diagnostic only.

Not performed:

- candidate generation
- SQL execution/checker rerun
- timing rerun
- SQLSolver or VeriEQL verifier pass
- official metrics computation
- official Semantic Equivalence Rate
- formal Regression@20
- POCR
- paper table rendering
- top-level `reports/` update
- top-level `results/` update
- retained-evidence promotion
- leaderboard output
- denominator change
- case membership change

The reviewed metrics are canonical local diagnostics because they were produced by `src/sql_rewrite_bench/local_metrics.py`. They are still not official or paper-facing.
