# Command Log

Commands run were read-only inspection and validation commands. They did not invoke adapters, DB execution, checker execution, timing collection, LLM calls, SQLSolver, VeriEQL, `compute-local-metrics`, official metrics, or paper rendering.

Representative commands:

```bash
git status -sb
git branch --show-current
rg -n "Track A|metric|Semantic Equivalence|POCR|tag_slices|local metrics|official|leaderboard|reports/results|D032|D033|D034" project_control/MIGRATION_MASTER_PLAN.md project_control/MIGRATION_STATUS.md project_control/DECISION_LOG.md project_control/MIGRATION_RUN_LOG.md repository_spec/metrics_contract_v1.md
rg -n "local_metrics_summary|generation_rate|result_consistency_rate|failure_bucket|tag_slices|semantic_equivalence|verifier|pocr|cross_engine|candidate_sql" src/sql_rewrite_bench/local_metrics.py src/sql_rewrite_bench/tag_slices.py src/sql_rewrite_bench/verifier_support
ls -1 runs/user/<run_id>/metrics
ls -1 audits/<canonical_audit_packet>/
wc -l runs/user/<run_id>/ledger.csv
find runs/user/<run_id> -maxdepth 2 -type f
find runs/user/<run_id> runs/user/<run_id>__* -path '*verifier*' -print
```

Python snippets were used only to parse existing JSON/CSV artifacts and validate/copy existing values into the inventory. No metric recomputation or benchmark execution was performed.
