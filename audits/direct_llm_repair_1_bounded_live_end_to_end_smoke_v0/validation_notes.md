# Validation Notes

Validation completed:

- `pytest tests/user_entry/test_direct_llm_repair_1_adapter.py -q`: passed, `8 passed`.
- `python -m py_compile baselines/direct_llm_repair_1/adapter.py`: passed.
- CSV parse checks for `selected_live_e2e_rows.csv` and `live_e2e_outputs.csv`: passed.
- Markdown/text non-empty checks: passed.
- Selected row count check: expected 3-6, observed 3.
- Unsupported-engine exclusion check: expected 0 attempted, observed 0.
- Live-call count check: observed 3, all selected rows.
- DB/checker/timing bounded-scope check: observed source/candidate DB, checker, and timing only for selected rows.
- No `compute-local-metrics` command was run.
- No SQLSolver/VeriEQL command was run.
- Runtime output staging check: temporary `runs/user/direct_llm_repair_1_bounded_live_end_to_end_smoke_v0__*` directories were removed before staging.
- Changed-file secret scan: passed; no secret values in changed files.
- Protected-path review: passed; only the allowed audit packet and project-control files changed, plus two pre-existing unrelated untracked Direct LLM original audit directories left untouched.
- `git diff --check`: passed.
- Staged-file secret scan: passed.

Observed runtime summary before source-run removal:

- selected rows: 3
- live calls: 3
- generated candidates: 3
- candidate executable rows: 3
- exact rows: 3
- timed rows: 3
- fail-closed rows: 0

No official metric, official SER, paper result, denominator change, case membership change, raw legacy evidence change, or retained-evidence promotion occurred.
