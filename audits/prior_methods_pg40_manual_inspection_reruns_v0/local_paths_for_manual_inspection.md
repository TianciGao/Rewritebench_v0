# Local Paths For Manual Inspection

These paths are intentionally local and are not staged or committed.

## Candidate SQL Roots

- R-Bot existing PG40 candidate SQL root, not rerun: `runs/user/rbot_gpt54_pg40_bounded_diagnostic_rerun_v0/candidate_sql/`
- LearnedRewrite manual-inspection rerun candidate SQL root: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/`
- LLM-R2 adapted GPT-5.4 manual-inspection rerun candidate SQL root: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/`

## LearnedRewrite Manual-Inspection Rerun

- Run root: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/`
- Ledger: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/ledger.csv`
- Metrics summary: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/metrics/local_metrics_summary.json`
- Timing speedup rows: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/metrics/local_timing_speedup_rows.csv`
- Timing artifacts: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/timing/rows/`
- Temporary user-facing output mirror: `/tmp/sqlrb_learnedrewrite_pg40_manual_inspection_rerun_v0/output/`

## LLM-R2 Adapted GPT-5.4 Manual-Inspection Rerun

- Run root: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/`
- Ledger: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/ledger.csv`
- Metrics summary: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/metrics/local_metrics_summary.json`
- Timing speedup rows: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/metrics/local_timing_speedup_rows.csv`
- Timing artifacts: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/timing/rows/`
- Temporary user-facing output mirror: `/tmp/sqlrb_llm_r2_gpt54_pg40_manual_inspection_rerun_v0/output/`

## Manual Inspection Guidance

Use `timing_tail_case_selection.csv` to identify min, P10-near, P50-near, P90-near, max, frontier, and source-like rows. Use `source_candidate_sql_excerpt_review.md` only as a short excerpt map; inspect full SQL at the candidate/source paths above.
