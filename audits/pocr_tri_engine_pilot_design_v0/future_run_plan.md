# Future Run Plan

This file defines future run IDs and output locations only. It does not run annotation, replay, aggregation, DB/checker/timing, or baselines.

## Route Metadata

Direct LLM Repair-1:
- `method_id`: `direct_llm_repair_1`
- `route_id`: `direct_llm_repair_1_tri_engine_pocr_pilot_v0`

SQLGlot no-op:
- `method_id`: `sqlglot_noop`
- `route_id`: `sqlglot_noop_tri_engine_pocr_sanity_control_v0`

Common metadata:
- `case_set_id`: `common_core_v0`
- `denominator_scope`: `tri_engine_5case_pocr_pilot_v0`
- engines: `postgres`, `mysql`, `spark`

## Future Run IDs

Annotation run IDs:
- `pocr_annotation_direct_llm_repair1_tri_engine_pilot_postgres_v0`
- `pocr_annotation_direct_llm_repair1_tri_engine_pilot_mysql_v0`
- `pocr_annotation_direct_llm_repair1_tri_engine_pilot_spark_v0`
- `pocr_annotation_sqlglot_noop_tri_engine_pilot_postgres_v0`
- `pocr_annotation_sqlglot_noop_tri_engine_pilot_mysql_v0`
- `pocr_annotation_sqlglot_noop_tri_engine_pilot_spark_v0`

Replay run IDs:
- `pocr_user_replay_direct_llm_repair1_tri_engine_pilot_postgres_v0`
- `pocr_user_replay_direct_llm_repair1_tri_engine_pilot_mysql_v0`
- `pocr_user_replay_direct_llm_repair1_tri_engine_pilot_spark_v0`
- `pocr_user_replay_sqlglot_noop_tri_engine_pilot_postgres_v0`
- `pocr_user_replay_sqlglot_noop_tri_engine_pilot_mysql_v0`
- `pocr_user_replay_sqlglot_noop_tri_engine_pilot_spark_v0`

Aggregator run ID:
- `pocr_aggregate_tri_engine_pilot_v0`

## Output Locations

Future annotation outputs should use:

```text
output/results/<annotation_run_id>/pocr/annotations/<method_id>/<route_id>/<engine>/
output/logs/<annotation_run_id>/pocr/
output/reports/<annotation_run_id>/
```

Future replay outputs should use:

```text
output/results/<replay_run_id>/pocr/
output/results/<replay_run_id>/pocr/stage_b/pocr_stage_b_row_metrics.csv
output/logs/<replay_run_id>/pocr/
output/reports/<replay_run_id>/
```

Future aggregation output should use:

```text
output/results/pocr_aggregate_tri_engine_pilot_v0/pocr/aggregates/pocr_route_summary.csv
output/reports/pocr_aggregate_tri_engine_pilot_v0/pocr_route_summary.md
```

## Future Pipeline

The future pipeline is:

```text
annotation JSONL
-> pocr-diagnostic replay
-> pocr_stage_b_row_metrics.csv
-> pocr_aggregator.py
-> pocr_route_summary.csv
```

Live API policy for a future run:
- only after explicit authorization;
- maximum live calls equals candidate-bound pilot rows;
- current candidate-bound pilot rows: 30 total, 15 per route;
- checkpointed and resumable annotation is required;
- API keys must come from environment only and must not be printed, written, staged, or committed.

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.
