# Artifact Source Review

Existing durable `pocr_stage_b_row_metrics.csv` files for these historical PG40 replays were not present in the repository output tree because those replay runs predated the exporter.

The smoke therefore produced row metrics from existing replay artifacts only:
- Repair-1 source: `/tmp/sqlrb_pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/output/results/pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/pocr/diagnostic_rows.csv`.
- SQLGlot no-op source: `/tmp/sqlrb_pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0/output/results/pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0/pocr/diagnostic_rows.csv`.

Generated local smoke outputs:
- `/tmp/sqlrb_pocr_aggregator_smoke_existing_pg40_v0/output/results/pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/pocr/stage_b/pocr_stage_b_row_metrics.csv`.
- `/tmp/sqlrb_pocr_aggregator_smoke_existing_pg40_v0/output/results/pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0/pocr/stage_b/pocr_stage_b_row_metrics.csv`.
- `/tmp/sqlrb_pocr_aggregator_smoke_existing_pg40_v0/output/results/pocr_aggregator_smoke_existing_pg40_v0/pocr/aggregates/pocr_route_summary.csv`.

The `/tmp` tree was used only as local smoke output. No `/tmp` artifact was staged or committed.

The existing repository `output/` tree was inspected read-only for existing row metrics. No repository `output/` file was modified, staged, or committed by this task.

This smoke did not read API keys, call a live API, generate annotation JSONL, rerun user replay, run DB/checker/timing, rerun baselines, or mutate candidate SQL.
