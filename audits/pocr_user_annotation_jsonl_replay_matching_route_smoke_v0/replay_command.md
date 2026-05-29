# Replay Command

```bash
PYTHONPATH=src python -m cli.main user pocr-diagnostic \
  --enable-pocr-diagnostic \
  --candidate-root runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql \
  --method-id direct_llm_original \
  --route-id direct_llm_original_pg40_pocr_diagnostic \
  --engine postgres \
  --run-id pocr_user_replay_direct_llm_pg40_matching_route_v0 \
  --output-root /tmp/sqlrb_pocr_user_replay_direct_llm_pg40_matching_route_v0/output \
  --annotation-jsonl audits/pocr_real_route_direct_llm_pg40_diagnostic_v0/safe_annotation_outputs.jsonl
```

The command wrote D035-style diagnostic output only under `/tmp`; repository `output/` was not created or committed.
