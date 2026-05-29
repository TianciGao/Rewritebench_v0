# Forbidden Manual Metric Patterns

Forbidden going forward:

- audit helper functions named like `_route_card`, `_route_card_csv_row`, `_geomean`, or `_percentile` that emit authoritative route metrics;
- route-card JSON/CSV written directly from audit `per_row_*` CSV files;
- comparison tables that consume helper route cards as metric sources;
- hand-computed `local_generation_rate`, `local_execution_coverage_rate`, `local_result_consistency_rate`, `diagnostic_gm_speedup`, or speedup percentiles outside `local_metrics.py`;
- route comparisons that label outputs as route cards before canonical local metrics exist;
- treating D035 `/tmp/output/results/<run_id>/` helper artifacts as canonical metrics when no source `runs/user/<run_id>/metrics/` exists;
- computing or implying official metrics, paper results, retained evidence, or leaderboard rankings from local diagnostic audit packets.

Allowed audit behavior:

- inspect whether canonical source-run and metrics files exist;
- validate CSV headers and row counts;
- summarize canonical `local_metrics.py` outputs without changing formulas;
- document missing canonical metrics as a gap;
- preserve raw diagnostic evidence for future reruns.
