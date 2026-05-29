# Replay Command

```bash
sqlrb user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql --annotation-jsonl output/results/pocr_annotation_direct_llm_repair1_pg40_checkpointed_full_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres/safe_annotation_outputs.jsonl --method-id direct_llm_repair_1 --route-id direct_llm_repair_1_pg40_pocr_diagnostic --engine postgres --run-id pocr_user_replay_direct_llm_repair1_pg40_checkpointed_full_v0 --output-root /tmp/sqlrb_pocr_user_replay_direct_llm_repair1_pg40_checkpointed_full_v0/output
```

The replay mode did not call a live API and did not read API keys. It consumed the route-bound annotation JSONL produced by the checkpointed full annotation run.
