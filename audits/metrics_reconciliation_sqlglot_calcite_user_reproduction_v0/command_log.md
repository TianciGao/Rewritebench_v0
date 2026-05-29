# Command Log

Read/inspection commands only; no DB/checker/timing rerun and no baseline rerun.

- `pwd && git branch --show-current && git status -sb`
- `sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md`
- `sed -n '1,180p' project_control/MIGRATION_STATUS.md`
- `sed -n '1,260p' project_control/DECISION_LOG.md`
- `tail -140 project_control/MIGRATION_RUN_LOG.md`
- `find audits -maxdepth 3 -type f ...`
- `find output/results/... -maxdepth 4 -type f ...`
- `rg -n "sqlglot_noop|sqlglot_optimize|calcite_hep|GM Speedup|gm_speedup|Result Consistency|timed" ...`
- Python CSV/JSON parsing scripts to compare existing metrics, timing rows, failure buckets, and runtime traceability.

No command printed API keys or secrets.
