# Validation Notes

## Artifact Checks

- CSV parse checks: passed for `local_candidate_sql_availability_before_rerun.csv`, `rerun_candidate_sql_manifest.csv`, and `timing_tail_case_selection.csv`.
- Markdown/text non-empty checks: passed for all packet Markdown/text files.
- LearnedRewrite selected rows: 40.
- LearnedRewrite generated candidates: 29.
- LearnedRewrite generated candidate paths existing locally: 29.
- LearnedRewrite exact rows: 17.
- LearnedRewrite timed rows: 17.
- LearnedRewrite failure buckets: `{'mismatch': 6, 'no_candidate_sql': 11, 'none': 17, 'candidate_execution_failed': 6}`.
- LLM-R2 selected rows: 40.
- LLM-R2 generated candidates: 40.
- LLM-R2 generated candidate paths existing locally: 40.
- LLM-R2 exact rows: 37.
- LLM-R2 timed rows: 32.
- LLM-R2 failure buckets: `{'none': 37, 'mismatch': 1, 'candidate_execution_failed': 2}`.
- local_metrics output existence: passed for both reruns under `runs/user/<run_id>/metrics/`.
- Candidate SQL path existence checks: passed for generated candidates.
- LearnedRewrite source-like rows from rerun ledger: 2.
- LLM-R2 source-like rows from rerun ledger: 0.
- Timing-tail/source-like selection rows: 38.

## Runtime Boundary Checks

- R-Bot rerun: no.
- MySQL/Spark: no commands run.
- Track A 120: no command run.
- Verifier: no SQLSolver/VeriEQL command run. User evaluate emitted verifier placeholder status files only; no verifier runtime was invoked.
- Official metrics or paper rendering: no.
- Top-level reports/results update: no.
- Retained evidence promotion: no.
- API key exposure: no key values printed, written, staged, or committed.
- LearnedRewrite runtime stopped: port 6336 check returned no listener after shutdown.

## Protected Path Review

- Allowed local runtime outputs created and preserved: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/` and `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/`.
- These `runs/user` directories are intentionally not staged or committed.
- No tracked files under `src/`, `cases/`, `schemas/`, `case_sets/`, `inventory/`, top-level `reports/`, top-level `results/`, retained evidence, paper result files, env files, API keys, or secrets were modified by this task.
- `MIGRATION_MASTER_PLAN.md` was read only and not modified.

## Final Validation Commands

- CSV/Markdown parse checks: passed.
- `git diff --check`: passed.
- changed-file secret scan: passed with high-signal key/token patterns.
- protected-path review: passed; `git diff --name-status` showed only project-control modifications before explicit staging, and the audit packet is the only task-created untracked tree intended for staging.
