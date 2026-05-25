# Command Log

Commands are recorded with secrets redacted. No DB/checker/timing, baseline rerun, `compute-local-metrics`, verifier, user-output integration, official metric, paper rendering, or leaderboard command was run.

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
tail -n 140 project_control/DECISION_LOG.md
find runs/user -type d -name candidate_sql -print
PYTHONPATH=src python -m sql_rewrite_bench.pocr.real_route_diagnostic_runner --live-enabled --output-dir audits/pocr_real_route_direct_llm_pg40_diagnostic_v0
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/pocr/real_route_diagnostic_runner.py
PYTHONPATH=src pytest tests/pocr -q
git diff --check
```
