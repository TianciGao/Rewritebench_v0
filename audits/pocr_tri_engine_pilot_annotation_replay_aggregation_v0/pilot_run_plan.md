# Pilot Run Plan

The run followed the pilot design in `audits/pocr_tri_engine_pilot_design_v0/`: five cases, three engines, and two routes.

Selected cases: `PERF_0006`, `CONS_0005`, `PORT_0003`, `LONGTAIL_0011`, and `LONGTAIL_0022`.

Routes and engines:
- Direct LLM Repair-1: PostgreSQL, MySQL, Spark.
- SQLGlot no-op sanity/control: PostgreSQL, MySQL, Spark.

For each route-engine combination, the checkpointed annotation runner used exactly the selected five case IDs and the read-only candidate root from the design audit. The replay command used `sqlrb user pocr-diagnostic` with `--case-list /tmp/sqlrb_pocr_tri_engine_pilot_cases.txt`. The aggregator consumed the six `pocr_stage_b_row_metrics.csv` files and wrote a local diagnostic route summary.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula.
