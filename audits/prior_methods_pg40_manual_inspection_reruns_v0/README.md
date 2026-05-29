# Prior Methods PG40 Manual-Inspection Reruns v0

This packet records manual-inspection reruns for LearnedRewrite and LLM-R2 adapted GPT-5.4 PostgreSQL-only Common-core PG40. The purpose is to preserve local per-case candidate SQL, DB execution artifacts, checker status, timing artifacts, and `local_metrics.py` outputs for SQL and timing-tail inspection.

R-Bot was not rerun because its PG40 candidate SQL was already available locally at `runs/user/rbot_gpt54_pg40_bounded_diagnostic_rerun_v0/candidate_sql/`.

## Reruns

- `learnedrewrite` / `learnedrewrite_pg40_manual_inspection_rerun_v0`: selected 40, generated 29, executable 23, exact 17, timed 17, mismatch 6, failure buckets `{'candidate_execution_failed': 6, 'mismatch': 6, 'no_candidate_sql': 11, 'none': 17}`, Generation Rate 0.725, Execution Coverage Rate 0.575, Result Consistency Rate 0.425, GM Speedup Ratio 1.0799447051682103, percentiles `{'p10': 0.6518875049288938, 'p25': 0.9734890286704523, 'p50': 0.999038713817663, 'p75': 1.69373409746415, 'p90': 1.7055378477860157}`.
- `llm_r2_gpt54_adapted` / `llm_r2_gpt54_pg40_manual_inspection_rerun_v0`: selected 40, generated 40, executable 38, exact 37, timed 32, mismatch 1, failure buckets `{'candidate_execution_failed': 2, 'mismatch': 1, 'none': 37}`, Generation Rate 1.0, Execution Coverage Rate 0.95, Result Consistency Rate 0.925, GM Speedup Ratio 0.9799978475134843, percentiles `{'p10': 0.6032068297178019, 'p25': 0.9564859607716146, 'p50': 0.9973751616775418, 'p75': 1.0290736964601923, 'p90': 1.6324207336130296}`.

## Candidate SQL Locations

- R-Bot existing root: `runs/user/rbot_gpt54_pg40_bounded_diagnostic_rerun_v0/candidate_sql/`
- LearnedRewrite rerun root: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/`
- LLM-R2 rerun root: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/`

## How To Inspect P10/P50/P90 Rows

Start with `timing_tail_case_selection.csv`, then open full SQL from each row's `source_sql_path` and `candidate_sql_path`. `source_candidate_sql_excerpt_review.md` provides short excerpts only.

## Boundary

These outputs are manual-inspection local diagnostics only. They are not paper-result replacements, not Track A 120, not retained-evidence promotion, not official metrics, and not a leaderboard.

## Next Safe Action

Use preserved local candidate SQL paths to manually inspect P10/P50/P90 and frontier examples. Update paper wording about timing variance and nontrivial rewrites without changing canonical paper-facing result tables unless a separate promotion task is authorized.
