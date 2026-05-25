# Validation Notes

Validation performed or recorded:
- `pytest tests/user_entry/test_rbot_adapter.py -q`: passed, `13 passed, 5 subtests passed`.
- `python -m py_compile baselines/rbot/adapter.py`: passed.
- CSV parse checks: planned/passed for generated CSV files.
- JSON parse checks: planned/passed for `bounded_diagnostic_summary.json`.
- Markdown non-empty checks: planned/passed for generated Markdown files.
- Selected row count check: passed, 40 PostgreSQL rows.
- Live-call count check: passed, 40 selected rows had `live_call=true` metadata.
- DB/checker/timing bounded-scope check: passed from evaluate ledger; only PostgreSQL rows were selected.
- Local metrics output existence check: failed because `compute-local-metrics` exited before outputs with aggregate-run-dir stale-output guard.
- No MySQL/Spark run occurred.
- No SQLSolver or VeriEQL command occurred.
- No official R-Bot runtime, RAG index build, Chroma, or CalciteRewrite command occurred.
- No top-level reports/results update occurred.
- Runtime output staging check: passed; `runs/user/rbot_gpt54_pg40_bounded_diagnostic_v0` and `/tmp/sqlrb_rbot_gpt54_pg40_bounded_local_diagnostic_v0` were removed before staging.
- No API key value or secret value was printed or written to audit files.
- Protected-path review: planned before commit.
- `git diff --check`: planned before commit.
- Changed-file secret scan: planned before commit.

Boundary:
- This is adapted GPT-5.4 local diagnostic evidence only.
- It is not original R-Bot reproduction, not Track A 120, not official metrics, not verifier evidence, not official SER, and not paper evidence.
