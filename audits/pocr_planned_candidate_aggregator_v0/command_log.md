# Command Log

Preflight and context commands:

```text
pwd && git branch --show-current && git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,180p' project_control/MIGRATION_STATUS.md
tail -n 220 project_control/DECISION_LOG.md && tail -n 220 project_control/MIGRATION_RUN_LOG.md
sed -n '1,320p' src/sql_rewrite_bench/pocr/stage_b_row_metrics.py
sed -n '1,280p' tests/pocr/test_stage_b_row_metrics.py
rg -n "POCR@planned|POCR@candidate|macro|micro|curated|aggregat|route summary|pocr_stage_b_row_metrics|pocr_route_summary" audits/pocr_official_metric_promotion_design_v0 audits/pocr_formula_dry_run_existing_diagnostics_v0 audits/pocr_row_level_stage_b_artifact_contract_v0 audits/pocr_minimal_stage_b_row_metrics_exporter_v0 src/sql_rewrite_bench/pocr tests/pocr
```

Metric-definition checkpoint before implementation:

- POCR@planned is the denominator-aware route-level headline candidate for promotion diagnostics.
- POCR@candidate is the candidate-quality diagnostic view.
- POCR@curated remains NA / curated_manifest_missing.
- Macro-average over per-row OC_i is the main formula.
- Total supported atoms / total expected atoms is diagnostic micro-average only.
- This task does not compute official POCR or promote a paper metric.

Validation commands:

```text
python -m py_compile src/sql_rewrite_bench/pocr/pocr_aggregator.py src/sql_rewrite_bench/pocr/__init__.py
pytest tests/pocr/test_pocr_aggregator.py -q
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
python CSV parse check for test-exported pocr_route_summary.csv
find audits/pocr_planned_candidate_aggregator_v0 -name '*.md' -type f -print -exec test -s {} \;
python required boundary phrase check over audits/pocr_planned_candidate_aggregator_v0/*.md
git diff --check
git diff --name-only -- cases ':(glob)**/skills.md' case_sets inventory reports results runs/user output
git diff --name-only | rg '(^|/)candidate_sql/|\.sql$' || true
changed-file secret scan
staged secret scan
git status -sb
git diff --name-status
```

No live API call, API key read, annotation JSONL generation, production user replay, DB/checker/timing run, baseline rerun, candidate SQL generation or mutation, official POCR computation, paper-facing metric promotion, top-level reports/results update, retained-evidence promotion, or leaderboard output occurred.
