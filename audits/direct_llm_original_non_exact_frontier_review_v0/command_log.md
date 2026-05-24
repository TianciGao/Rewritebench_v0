# Command Log

Commands run for this audit-only task:

```bash
git status -sb
git branch --show-current
git merge-base --is-ancestor 68613d1 HEAD
ls runs/user/direct_llm_original_track_a_120_canonical_v0/metrics
ls audits/direct_llm_original_track_a_120_canonical_user_rerun_v0
python - <<'PY'
# Parsed the existing per_row_metadata.csv frontier rows for review only.
PY
python - <<'PY'
# Read the existing local_metrics_summary.json for review only.
PY
mkdir -p audits/direct_llm_original_non_exact_frontier_review_v0
git diff --check
git status -sb
```

Validation helper commands parsed `frontier_table.csv`, parsed `frontier_summary.json`, checked non-empty Markdown files, and scanned changed files for secret-shaped values.

Commands intentionally not run:

- Repair-1 execution
- live LLM calls
- benchmark evaluation
- `compute-local-metrics`
- official metrics
- official SER
- formal Regression@20
- POCR
- report/result promotion
