# Command Log

Commands run, with secrets redacted by policy:

```text
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -n 140 project_control/MIGRATION_STATUS.md
tail -n 180 project_control/DECISION_LOG.md
tail -n 180 project_control/MIGRATION_RUN_LOG.md
python - <<'PY' ... verify candidate root resolves 40/40 and print case list ... PY
python - <<'PY' ... print safe live env presence booleans only ... PY
PYTHONPATH=src timeout 3600 python -m sql_rewrite_bench.pocr.checkpointed_annotation_runner --live-enabled --case-list <40 Common-core IDs> --max-live-calls 40 --timeout-seconds 60 --max-tokens 4000 --repo-root /home/tianci_gao/code/Rewritebench_v0 --output-root output --run-id pocr_annotation_direct_llm_repair1_pg40_checkpointed_full_v0 --candidate-root runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql --method-id direct_llm_repair_1 --route-id direct_llm_repair_1_pg40_pocr_diagnostic --engine postgres
sqlrb user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql --annotation-jsonl output/results/pocr_annotation_direct_llm_repair1_pg40_checkpointed_full_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres/safe_annotation_outputs.jsonl --method-id direct_llm_repair_1 --route-id direct_llm_repair_1_pg40_pocr_diagnostic --engine postgres --run-id pocr_user_replay_direct_llm_repair1_pg40_checkpointed_full_v0 --output-root /tmp/sqlrb_pocr_user_replay_direct_llm_repair1_pg40_checkpointed_full_v0/output
python - <<'PY' ... parse annotation and replay outputs ... PY
python - <<'PY' ... create full Step 5 audit packet ... PY
apply_patch ... update POCR diagnostic report wording to include "No global leaderboard is produced." ... PATCH
sqlrb user pocr-diagnostic ... rerun no-API replay to refresh /tmp report wording ...
```

No DB/checker/timing command was run. No baseline adapter command was run. No candidate SQL generation or mutation command was run.
