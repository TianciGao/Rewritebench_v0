
# Replay Command

```bash
python -m cli.main user pocr-diagnostic \
  --enable-pocr-diagnostic \
  --candidate-root runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql \
  --annotation-jsonl output/results/pocr_annotation_direct_llm_repair1_pg40_targeted_retry_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres/merged_safe_annotation_outputs.jsonl \
  --method-id direct_llm_repair_1 \
  --route-id direct_llm_repair_1_pg40_pocr_diagnostic \
  --engine postgres \
  --run-id pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0 \
  --output-root /tmp/sqlrb_pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/output
```

The replay used the user-facing POCR diagnostic path and wrote only to `/tmp` output. It did not compute official POCR, aggregate a route-level POCR score, or promote a paper-facing metric.
