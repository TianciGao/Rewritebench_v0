# Command Log

Commands used for this review, with no live API, no API key read, no annotation generation, no replay rerun, and no DB/checker/timing execution:

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,240p' project_control/MIGRATION_STATUS.md
tail -n 220 project_control/DECISION_LOG.md
tail -n 260 project_control/MIGRATION_RUN_LOG.md
find output/results/pocr_annotation_direct_llm_repair1_pg40_checkpointed_full_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres -maxdepth 1 -type f -printf '%f %s\n' | sort
find /tmp/sqlrb_pocr_user_replay_direct_llm_repair1_pg40_checkpointed_full_v0/output/results/pocr_user_replay_direct_llm_repair1_pg40_checkpointed_full_v0/pocr -maxdepth 1 -type f -printf '%f %s\n' | sort
python - <<'PYGEN'
# parse existing local annotation/replay artifacts and write this audit packet
PYGEN
python - <<'PY'
# CSV parse checks for audit CSVs
PY
python - <<'PY'
# JSONL parse check for existing local safe_annotation_outputs.jsonl
PY
python - <<'PY'
# Markdown non-empty checks
PY
for phrase in "This is not official POCR." "No route-level POCR score is emitted." "No paper-facing metric is promoted." "diagnostic support only" "fail closed"; do rg -n --fixed-strings "$phrase" audits/pocr_step5_repair1_pg40_diagnostic_quality_review_v0 >/dev/null || exit 1; done
git diff --check
git diff -- cases case_sets inventory reports results runs/user output
git status --short cases case_sets inventory reports results runs/user
git status --short output
rg -n --pcre2 '(sk-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._~+/=-]{20,})' audits/pocr_step5_repair1_pg40_diagnostic_quality_review_v0 project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md || true
```

Generated at: 2026-05-26T13:35:19.987720+00:00.
