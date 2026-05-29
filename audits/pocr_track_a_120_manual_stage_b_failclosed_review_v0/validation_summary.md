# Validation Summary

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.

Validation completed:
- CSV parse checks passed for `remaining_fail_closed_review.csv` and `review_summary_by_route_engine.csv`.
- Markdown non-empty checks passed for all audit Markdown files.
- Required boundary phrase checks passed, including `SQLGlot no-op remains a candidate/control route, not a reference.`
- `python -m py_compile src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py src/sql_rewrite_bench/pocr/operation_evidence_policy.py` passed.
- `pytest tests/pocr -q` passed: 143 passed.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q` passed: 28 passed.
- `git diff --check` passed.
- Protected-path checks found no tracked changes under `cases/`, `skills.md`, candidate SQL, `runs/user`, top-level `reports/`, or top-level `results/`.
- No `output/` or `/tmp` output is intended to be staged or committed.

No live API call was made. No API key was read. No retry run, annotation generation, replay rerun, aggregation rerun, DB/checker/timing run, baseline rerun, candidate SQL generation, or candidate SQL mutation occurred.
