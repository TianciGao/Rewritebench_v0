# Validation Notes

Validation completed before final cleanup/staging:

- `pytest tests/user_entry/test_direct_llm_repair_1_adapter.py -q`: passed, `8 passed`.
- `python -m py_compile baselines/direct_llm_repair_1/adapter.py`: passed.
- Route assembly wrapper py_compile: passed.
- Evaluate run completed for PostgreSQL/MySQL/Spark.
- `compute-local-metrics` completed through the user facade.
- Selected planned row count: 120.
- Unsupported row count: 5.
- Repair attempted row count: 13.
- Final candidate source counts: {'original': 102, 'repaired': 13, 'unsupported_or_none': 5}.
- CSV parse checks: passed for audit CSVs and canonical metrics CSV outputs.
- JSON parse checks: passed for canonical metrics summary and verifier status placeholder JSON.
- Markdown/text non-empty checks: passed.
- Local metrics output existence checks: passed for source-run metrics and user-facing `/tmp` metrics copies.
- No SQLSolver/VeriEQL command: passed by command log review.
- No official metrics or paper rendering: passed by command log review.
- Top-level reports/results update check: passed; no tracked top-level `reports/`, `results/`, or `output/` path changed.
- Runtime output staging check: passed before explicit staging; runtime `runs/user` and `/tmp` outputs are not in the changed-file set.
- Changed-file secret scan: passed; no API key values or secret-shaped assignments were found in changed audit files or added project-control lines.
- Protected-path review: passed; only the allowed audit packet and project-control files changed.
- `git diff --check`: passed.
- Staged-file secret scan: passed after explicit staging.

Boundary: local diagnostic only; official_metric_input=false; paper_result_input=false; retained_evidence_promoted=false; leaderboard_input=false.
