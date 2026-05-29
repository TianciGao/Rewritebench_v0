# Command Log

Commands run:

```bash
pwd && git branch --show-current && git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,160p' project_control/MIGRATION_STATUS.md
rg -n "D039|POCR official|POCR@planned|POCR@candidate|curated_manifest_missing" project_control/DECISION_LOG.md
tail -n 120 project_control/MIGRATION_RUN_LOG.md
find audits/pocr_official_metric_promotion_design_v0 audits/pocr_formula_dry_run_existing_diagnostics_v0 audits/pocr_minimal_stage_b_row_metrics_exporter_v0 audits/pocr_planned_candidate_aggregator_v0 audits/pocr_aggregator_smoke_existing_pg40_v0 -maxdepth 1 -type f -print | sort
find audits/pocr_candidate_sql_inventory_v0 -maxdepth 1 -type f -print | sort
find audits/pocr_paper_table_route_candidate_reconciliation_v0 -maxdepth 1 -type f -print | sort
sed -n '1,120p' case_sets/common_core_v0/cases.csv
sed -n '1,220p' audits/pocr_official_metric_promotion_design_v0/large_scale_experiment_plan.md
sed -n '1,180p' audits/pocr_official_metric_promotion_design_v0/pocr_formula_and_denominator_policy.md
sed -n '1,120p' audits/pocr_aggregator_smoke_existing_pg40_v0/smoke_summary.csv
sed -n '1,160p' audits/pocr_aggregator_smoke_existing_pg40_v0/artifact_source_review.md
for case in PERF_0006 CONS_0005 PORT_0003 LONGTAIL_0011 LONGTAIL_0022; do pool=${case%%_*}; sed -n '1,220p' cases/$pool/$case/skills.md; done
sed -n '1,220p' audits/pocr_candidate_sql_inventory_v0/candidate_root_inventory.csv
sed -n '1,220p' audits/pocr_paper_table_route_candidate_reconciliation_v0/route_candidate_root_selection.csv
sed -n '1,160p' audits/pocr_paper_table_route_candidate_reconciliation_v0/table_route_candidate_readiness.csv
sed -n '1,220p' src/sql_rewrite_bench/pocr/stage_b_row_metrics.py
sed -n '1,240p' src/sql_rewrite_bench/pocr/pocr_aggregator.py
python - <<'PY'
# Read-only readiness script:
# - counted operation_atom and semantic_guard_atom rows in skills.md
# - checked selected route-engine candidate roots
# - computed candidate SHA-256 values for existing files
# - printed proposed audit CSV contents
PY
python - <<'PY'
# Parsed all audit CSV files and confirmed pilot_row_manifest.csv has 30 rows.
PY
for f in audits/pocr_tri_engine_pilot_design_v0/*.md; do test -s "$f" || exit 1; done
for phrase in "This is not official POCR." "No route-level official POCR score is emitted." "No paper-facing metric is promoted." "POCR@planned and POCR@candidate remain D039 promotion views." "POCR@curated remains deferred until a predeclared curated manifest exists." "No live API call was made." "No annotation JSONL was generated."; do rg -F "$phrase" audits/pocr_tri_engine_pilot_design_v0 >/dev/null || exit 1; done
git diff --check
git diff --name-status -- cases case_sets inventory reports results
git diff --name-status -- runs/user
git diff --name-status -- ':(glob)**/skills.md'
git diff --name-status -- ':(glob)**/candidate_sql/**'
git diff --name-status -- output
```

No live API call was made.

No annotation JSONL was generated.

No pocr-diagnostic replay, POCR aggregation run, DB/checker/timing run, baseline rerun, or candidate SQL mutation occurred.
