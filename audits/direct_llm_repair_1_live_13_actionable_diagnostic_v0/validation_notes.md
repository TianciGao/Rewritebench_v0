# Validation Notes

Validation completed:

- `pytest tests/user_entry/test_direct_llm_repair_1_adapter.py -q`: passed, `8 passed`.
- `python -m py_compile baselines/direct_llm_repair_1/adapter.py`: passed.
- CSV parse checks for generated CSVs: passed.
- JSON parse check for `live_13_diagnostic_summary.json`: passed.
- Markdown/text non-empty checks: passed.
- Selected row count check: expected 13, observed 13.
- Unsupported exclusion count check: expected 5, observed 5.
- Live-call count check: observed 13; all were selected rows.
- DB/checker/timing bounded-scope check: observed source/candidate DB and checker only for selected rows; exact rows timed 9/13 and mismatch rows were timing-ineligible.
- No `compute-local-metrics` command was run.
- No SQLSolver/VeriEQL command was run.
- Runtime output staging check: temporary `runs/user/direct_llm_repair_1_live_13_actionable_diagnostic_v0__*` directories were removed before staging.
- Changed-file secret scan: passed; no API key values or secret-shaped assignments were found in changed audit files or added project-control lines.
- Staged-file secret scan: passed after explicit staging.
- Protected-path review: passed; only the allowed audit packet and project-control files were changed/staged.
- `git diff --check`: passed.

Observed runtime summary before source-run removal:

- selected rows: 13
- unsupported excluded rows: 5
- live calls: 13
- generated candidates: 13
- candidate executable rows: 13
- exact rows: 9
- mismatch rows: 4
- candidate execution failed rows: 0
- timed rows: 9
- fail-closed rows: 0

No official metric, official SER, paper result, denominator change, case membership change, raw legacy evidence change, or retained-evidence promotion occurred.
