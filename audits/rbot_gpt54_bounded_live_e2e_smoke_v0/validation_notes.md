# Validation Notes

Validation performed:
- `pytest tests/user_entry/test_rbot_adapter.py -q`: passed, `13 passed, 5 subtests passed`.
- `python -m py_compile baselines/rbot/adapter.py`: passed.
- CSV parse checks passed for `selected_live_e2e_rows.csv` and `live_e2e_outputs.csv`.
- Markdown/text non-empty checks passed for audit packet Markdown files and `command_log.txt`.
- Selected row count check passed: 6 selected rows.
- PostgreSQL-only scope check passed: all selected rows use `engine=postgres`.
- Live-call count check passed: 6 live calls, one per selected row.
- Candidate generation count check passed: 6 generated candidates.
- Candidate executable count check passed: 5 rows.
- Checker exact count check passed: 5 rows.
- Timed count check passed: 5 rows.
- DB/checker/timing bounded-scope check passed: execution/checker/timing was run only as part of the six-row PostgreSQL user-facade smoke.
- Runtime output staging check passed: `runs/user/rbot_gpt54_bounded_live_e2e_smoke_v0` and `/tmp/sqlrb_rbot_gpt54_bounded_live_e2e_smoke_v0` were removed before staging.
- No `compute-local-metrics` command was run.
- No SQLSolver or VeriEQL command was run.
- No official R-Bot runtime, RAG index build, Chroma, or CalciteRewrite command was run.
- No MySQL/Spark command was run.
- No official metrics, paper rendering, retained evidence promotion, leaderboard, or Track A 120 command was run.
- No API key value or secret was printed, written, staged, or committed.
- Protected-path review passed: no prohibited source, cases, schemas, inventory, top-level reports/results, retained evidence, paper result, or env/secret files were modified.
- `git diff --check`: passed.
- Changed-file secret scan: passed.

Boundary:
- This smoke is adapted GPT-5.4 local diagnostic evidence only.
- It is not original R-Bot paper reproduction.
- It is not official metrics, official SER, paper evidence, retained evidence, or leaderboard input.
