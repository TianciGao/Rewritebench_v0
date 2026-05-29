# Validation Notes

- CSV parse checks: passed for selected_pairs.csv and identity_guard_results.csv.
- JSONL parse check: passed for 24 verdict rows.
- JSON parse checks: passed for bounded summary and preflight summary.
- Markdown/text non-empty checks: passed for README/report/boundary/command log.
- Selected pair count check: passed (8 rows).
- Source/candidate/schema existence and hash checks: passed for all selected pairs.
- Identity guard count/gating checks: passed (3 passed, 5 failed).
- No-prohibited-command check: passed from command_log boundary statements and generated artifacts.
- Protected-path review: passed; only allowed project-control files, current audit packet, and pre-existing unrelated untracked audit dirs are present.
- Changed-file secret scan: passed over 87 files.
- git diff --check: passed before validation_notes.md write.
- No VeriEQL/local_metrics/official metrics/adapters/DB/checker/timing/LLM/Repair-1 run: passed; only SQLSolver bounded subset commands were executed.

Selected pair count: 8.

Identity guard passed pairs: 3.

Identity guard failed pairs: 5.

Actual source-candidate attempted pairs: 3.

Actual equivalent verdicts: 3.

Actual non-equivalent verdicts: 0.

`bounded_SER_if_decidable`: 1.0 over 3 decidable actual checks; local diagnostic support only, not official SER.

Boundary checks passed: no VeriEQL, no adapters, no DB execution, no checker execution, no timing collection, no LLM calls, no `compute-local-metrics`, no official metrics, no paper rendering, and no Repair-1 command.

Protected paths: only this audit packet and `project_control/MIGRATION_STATUS.md` / `project_control/MIGRATION_RUN_LOG.md` are intended for staging. Two unrelated pre-existing untracked Direct LLM audit directories remain untracked and untouched.

Secret scan: passed; no API keys, env files, private keys, or common token patterns found in changed files for this task.

`git diff --check`: passed before this note was written and will be repeated before commit.
