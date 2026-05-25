# Replay Command

```bash
PYTHONPATH=src python -m cli.main user pocr-diagnostic \
  --enable-pocr-diagnostic \
  --candidate-root runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql \
  --method-id direct_llm_original \
  --route-id direct_llm_original_pg40_user_replay \
  --engine postgres \
  --run-id pocr_user_replay_direct_llm_pg40_v0 \
  --output-root /tmp/sqlrb_pocr_user_replay_direct_llm_pg40_v0/output \
  --annotation-jsonl audits/pocr_real_route_direct_llm_pg40_diagnostic_v0/safe_annotation_outputs.jsonl
```

The command used a temp output root and did not call live APIs, read API keys, run DB/checker/timing, or rerun a baseline.
