# Replay Command

```bash
PYTHONPATH=src python -m cli.main user pocr-diagnostic \
  --enable-pocr-diagnostic \
  --candidate-root runs/user/common_core_pg_noop_db_checker/candidate_sql \
  --annotation-jsonl output/results/pocr_annotation_sqlglot_noop_pg40_sanity_control_v0/pocr/annotations/sqlglot_noop/sqlglot_noop_pg40_pocr_sanity_control/postgres/safe_annotation_outputs.jsonl \
  --method-id sqlglot_noop \
  --route-id sqlglot_noop_pg40_pocr_sanity_control \
  --engine postgres \
  --run-id pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0 \
  --output-root /tmp/sqlrb_pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0/output
```

Replay wrote local diagnostic output under `/tmp/sqlrb_pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0/output` only.

This is not official POCR.
No route-level POCR score is emitted.
No paper-facing metric is promoted.
Stage A annotation alone is not counted.
Stage B transformation-aware validation is diagnostic only.
Semantic guard atoms are not part of operation coverage numerator.
No global leaderboard is produced.
