# Validation Notes

Validation status:

- `pytest tests/user_entry/test_rbot_adapter.py -q`: passed, 13 passed and 5 subtests passed.
- `python -m py_compile baselines/rbot/adapter.py`: passed.
- PostgreSQL selected row count check: `40` rows.
- Live-call count check: `40` live calls, all PostgreSQL rows.
- DB/checker/timing bounded-scope check: run summary selected `40`, source execution success `40`, candidate execution success `38`, exact `37`, timed `33`.
- Single-run `compute-local-metrics` completed with `--run-id` only.
- Aggregate flags `--run-id-prefix`, `--engines`, and `--aggregate-run-id` were not used.
- local_metrics output existence check: passed for source-run and exported metrics paths.
- No MySQL/Spark run was performed.
- No SQLSolver/VeriEQL command was performed.
- No official R-Bot runtime, RAG, Chroma, or CalciteRewrite command was performed.
- No top-level reports/results update was performed.
- Runtime outputs are under `runs/user/rbot_gpt54_pg40_bounded_diagnostic_rerun_v0` and `/tmp/sqlrb_rbot_gpt54_pg40_bounded_local_diagnostic_rerun_with_metrics_v0/output`; they must not be staged or committed.
- No API key values were printed or written.
- CSV parse checks: passed for audit CSVs and local metrics CSVs.
- JSON parse checks: passed for audit summary JSON and local run/metrics JSON outputs.
- Markdown non-empty checks: passed for 10 audit Markdown/text files.
- Selected row count check: passed, 40.
- PostgreSQL-only check: passed.
- Metadata scope check: passed, 40 status files with live_call=true, provider=openai_compatible, model=gpt-5.4, official_rbot_stack=false, retrieval_used=false, rag_index_used=false, calcite_rewrite_used=false, and raw_response_saved=false.
- Top-level reports/results update check: passed.
- Changed-file secret value scan: passed.
- Protected-path review: passed.
- `git diff --check`: passed.
