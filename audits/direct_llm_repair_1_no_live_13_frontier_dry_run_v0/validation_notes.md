# Validation Notes

Validation completed:

- `pytest tests/user_entry/test_direct_llm_repair_1_adapter.py -q`: passed, `8 passed`.
- `python -m py_compile baselines/direct_llm_repair_1/adapter.py`: passed.
- CSV parse checks: passed for `repair1_13_actionable_frontier_manifest.csv`, `unsupported_exclusion_manifest.csv`, and `repair1_dry_run_outputs.csv`.
- Markdown/text non-empty checks: passed.
- Selected actionable row count check: expected 13, observed 13.
- Unsupported exclusion count check: expected 5, observed 5.
- Repaired candidate generation check: expected 13 unless fail-closed, observed 13.
- Candidate preflight check: observed 13 passed.
- No-live check: adapter metadata recorded `provider=fake`, `live_call=false`, and `api_key_present=false` for all attempted rows.
- No DB/checker/timing/local_metrics/verifier command check: facade commands omitted DB/checker/timing flags and no prohibited tool commands were run.
- Runtime output staging check: temporary `runs/user/direct_llm_repair_1_no_live_13_frontier_dry_run_v0__*` directories were removed before staging.
- `git diff --check`: passed.
- Changed-file secret scan: passed with assignment/value-pattern scan; the literal environment variable names are documented, but no values are present.
- Protected-path review: passed; only the allowed audit packet and project-control files changed, plus two pre-existing unrelated untracked audit directories left untouched.

No official metric was computed. No paper result, denominator, case membership, raw legacy evidence, top-level reports/results, or retained evidence was changed.
