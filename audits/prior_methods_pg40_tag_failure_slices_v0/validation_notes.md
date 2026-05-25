# Validation Notes

Validation status: passed.

Checks:

- CSV parse checks: passed for 7 CSV files.
- Markdown non-empty checks: passed for 5 markdown files.
- All three methods represented: `learnedrewrite`, `rbot_gpt54_adapted`, `llm_r2_gpt54_adapted`.
- Source audit packet paths exist: passed.
- Case tag source checks: passed for all 40 Common-core cases and 185 retained taxonomy tag rows.
- Row-count sanity checks against each PG40 boundary packet: passed.
- LearnedRewrite counts: selected 40, generated 29, executable 23, exact 17, non-exact 23.
- R-Bot adapted counts: selected 40, generated 40, executable 38, exact 37, non-exact 3.
- LLM-R2 adapted counts: selected 40, generated 40, executable 39, exact 39, non-exact 1.
- Non-exact frontier row counts reconcile with boundary packets: passed.
- LONGTAIL_0011 cross-method status check: candidate_execution_failed for all three methods.
- Source-like/no-op check: LearnedRewrite `CONS_0036` and `CONS_0037`; LLM-R2 `CONS_0037`; R-Bot none.
- No-prohibited-command check: passed for exact commands recorded in `command_log.txt`.
- `git diff --check`: passed.
- Changed-file secret scan: passed.
- Staged-file secret scan: passed.
- Protected-path review: passed. Changed paths are limited to `audits/prior_methods_pg40_tag_failure_slices_v0/`, `project_control/MIGRATION_STATUS.md`, and `project_control/MIGRATION_RUN_LOG.md`.
- No top-level `reports/` or `results/` update: passed.
- No retained evidence promotion: passed.
- No runtime outputs staged: passed.

No experiment, runtime, DB/checker/timing, `compute-local-metrics`, verifier, official metrics, paper rendering, retained evidence promotion, MySQL/Spark, or Track A 120 command was run.
