# Command Log

Read/review commands:

```bash
git status -sb
git branch --show-current
rg -n "Generation Rate|Execution Coverage|Result Consistency|Semantic Equivalence|Speedup|POCR|Attribution|Cross-Engine|tag|verifier|SER" repository_spec/metrics_contract_v1.md
rg -n "generation|execution_coverage|result_consistency|semantic|speedup|pocr|cross_engine|percentile|tag|failure_bucket|verifier" src/sql_rewrite_bench/local_metrics.py
sed -n '1,330p' repository_spec/metrics_contract_v1.md
sed -n '1,980p' src/sql_rewrite_bench/local_metrics.py
sed -n '1,260p' src/sql_rewrite_bench/tag_slices.py
find src/sql_rewrite_bench/verifier_support -maxdepth 2 -type f -print
rg -n "semantic|equivalence|rate|status|unknown|timeout|unsupported|not_attempted|not_implemented|tool_error|no_verifier|decidable|verdict|summary|SER|pair" src/sql_rewrite_bench/verifier_support
sed -n '1,140p' src/sql_rewrite_bench/verifier_support/summary.py
sed -n '1,260p' src/sql_rewrite_bench/verifier_support/pairs.py
sed -n '1,220p' src/sql_rewrite_bench/verifier_support/verdicts.py
sed -n '1,90p' src/sql_rewrite_bench/verifier_support/__init__.py
rg -n "metric|Generation Rate|Execution Coverage|Result Consistency|Semantic Equivalence|SER|Speedup|POCR|Attribution|Cross-Engine|verifier|tag slice|paper" project_control/MIGRATION_MASTER_PLAN.md project_control/MIGRATION_STATUS.md project_control/DECISION_LOG.md project_control/MIGRATION_RUN_LOG.md
sed -n '369,405p' project_control/DECISION_LOG.md
sed -n '774,923p' project_control/DECISION_LOG.md
tail -n 120 project_control/MIGRATION_STATUS.md
tail -n 100 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' audits/direct_llm_original_track_a_120_canonical_user_rerun_v0/local_metrics_summary_review.md
sed -n '1,220p' audits/direct_llm_original_track_a_120_canonical_user_rerun_v0/canonical_metrics_outputs.md
sed -n '1,220p' audits/direct_llm_original_non_exact_frontier_review_v0/repair1_design_requirements.md
git diff --check
git status -sb
```

Validation helper commands parsed both audit CSV matrices, checked Markdown files for non-empty content, reviewed changed paths against the protected-surface rules, and scanned changed files for secret-shaped values.

Commands intentionally not run:

- adapters
- DB execution
- checker
- timing
- LLM calls
- SQLSolver
- VeriEQL
- `compute-local-metrics`
- official metrics
- paper table rendering
