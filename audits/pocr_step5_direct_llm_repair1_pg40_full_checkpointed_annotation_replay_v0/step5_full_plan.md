# Step 5 Full Plan

Selected baseline: Direct LLM Repair-1 PostgreSQL PG40.

- method_id: `direct_llm_repair_1`
- route_id: `direct_llm_repair_1_pg40_pocr_diagnostic`
- engine: `postgres`
- case_set_id: `common_core_v0`
- denominator_scope: `pg40_postgres_only`
- annotation_run_id: `pocr_annotation_direct_llm_repair1_pg40_checkpointed_full_v0`
- replay_run_id: `pocr_user_replay_direct_llm_repair1_pg40_checkpointed_full_v0`

Plan executed:

1. Resolve the existing candidate root read-only against 40 Common-core PostgreSQL cases.
2. Run the checkpointed Stage A live annotation runner with `--live-enabled` and `--max-live-calls 40`.
3. Preserve per-row checkpoint manifests and safe JSONL under D035-style local `output/` paths.
4. Replay the generated annotation JSONL through `sqlrb user pocr-diagnostic` into a `/tmp` output root.
5. Commit only this audit packet and project-control updates.

No prior 2-row checkpointed outputs were reused; the full run used a fresh run id and regenerated all 40 annotation rows with 40 new provider calls.
