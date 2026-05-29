# Forbidden Audit Helper Metrics

Going forward, audit packets must not hand-compute authoritative route cards or comparison tables from raw audit CSV/JSON.

Forbidden patterns:

- Computing route-card counts directly in an audit helper when canonical `metrics/local_metrics_summary.json` is absent.
- Computing Generation Rate, Execution Coverage Rate, or Result Consistency Rate outside `src/sql_rewrite_bench/local_metrics.py`.
- Computing GM speedup or speedup percentiles in an audit helper and presenting them as route metrics.
- Treating helper `route_card.json`, `route_card.csv`, or comparison tables as canonical metrics.
- Calling local diagnostic outputs official metrics, paper results, retained evidence, or leaderboard input.

Allowed audit behavior:

- Inspect canonical `metrics/local_metrics_*` outputs.
- Validate row counts and schema shape.
- Summarize canonical outputs with explicit local-only boundaries.
- Mark older helper projections as provisional diagnostic summaries.
