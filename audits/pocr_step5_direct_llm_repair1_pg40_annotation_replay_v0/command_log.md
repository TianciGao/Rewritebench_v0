# Command Log

Commands run, with secrets redacted by policy:

```text
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
sed -n '1,280p' project_control/DECISION_LOG.md
tail -n 260 project_control/MIGRATION_RUN_LOG.md
python - <<'PY' ... verify Repair-1 candidate root resolves 40/40 ... PY
python - <<'PY' ... print safe live env presence booleans only ... PY
python - <<'PY' ... bounded live annotation generation attempt ... PY
kill <annotation-subprocess-pid>
find output/results/pocr_annotation_direct_llm_repair1_pg40_v0 output/logs/pocr_annotation_direct_llm_repair1_pg40_v0 output/reports/pocr_annotation_direct_llm_repair1_pg40_v0 -maxdepth 6 -type f -print
python - <<'PY' ... create fail-closed audit packet ... PY
python - <<'PY' ... CSV parse checks for audit CSVs ... PY
python - <<'PY' ... Markdown non-empty checks ... PY
python - <<'PY' ... report boundary wording checks ... PY
test -f output/results/pocr_annotation_direct_llm_repair1_pg40_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres/safe_annotation_outputs.jsonl
git status --short -- cases ':(glob)cases/**/skills.md' output reports results runs/user
git diff --name-only -- cases output reports results runs/user
git diff --name-only -- ':(glob)runs/user/**/candidate_sql/**'
find output/results/pocr_annotation_direct_llm_repair1_pg40_v0 output/logs/pocr_annotation_direct_llm_repair1_pg40_v0 output/reports/pocr_annotation_direct_llm_repair1_pg40_v0 /tmp/sqlrb_pocr_user_replay_direct_llm_repair1_pg40_v0 -maxdepth 7 -type f -print
```

No command printed API key values. No DB/checker/timing command was run. No baseline adapter was run.
