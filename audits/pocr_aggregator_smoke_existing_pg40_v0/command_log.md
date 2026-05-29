# Command Log

Commands run:

```bash
pwd && git branch --show-current && git status -sb
sed -n '1,260p' project_control/MIGRATION_STATUS.md
sed -n '1,260p' project_control/DECISION_LOG.md
tail -n 140 project_control/MIGRATION_RUN_LOG.md
rg -n "D039|POCR@planned|POCR@candidate|curated_manifest_missing" project_control/DECISION_LOG.md
find audits/pocr_formula_dry_run_existing_diagnostics_v0 -maxdepth 1 -type f -print | sort
find audits/pocr_minimal_stage_b_row_metrics_exporter_v0 -maxdepth 1 -type f -print | sort
find audits/pocr_planned_candidate_aggregator_v0 -maxdepth 1 -type f -print | sort
sed -n '1,260p' src/sql_rewrite_bench/pocr/stage_b_row_metrics.py
sed -n '1,720p' src/sql_rewrite_bench/pocr/pocr_aggregator.py
sed -n '1,260p' tests/pocr/test_stage_b_row_metrics.py
sed -n '1,320p' tests/pocr/test_pocr_aggregator.py
sed -n '1,120p' audits/pocr_formula_dry_run_existing_diagnostics_v0/route_level_dry_run_summary.csv
sed -n '1,120p' audits/pocr_formula_dry_run_existing_diagnostics_v0/input_artifact_inventory.csv
sed -n '1,80p' audits/pocr_formula_dry_run_existing_diagnostics_v0/repair1_pg40_formula_dry_run.csv
sed -n '1,80p' audits/pocr_formula_dry_run_existing_diagnostics_v0/sqlglot_noop_pg40_formula_dry_run.csv
sed -n '1,240p' src/sql_rewrite_bench/pocr/diagnostic_output_schema.py
find /tmp -path '*pocr_stage_b_row_metrics.csv' -print | sort | head -n 50
find output -path '*pocr_stage_b_row_metrics.csv' -print | sort | head -n 50
sed -n '1,3p' /tmp/sqlrb_pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/output/results/pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/pocr/diagnostic_rows.csv
sed -n '1,3p' /tmp/sqlrb_pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0/output/results/pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0/pocr/diagnostic_rows.csv
python - <<'PY'
# Converted existing replay diagnostic rows to temporary pocr_stage_b_row_metrics.csv
# files under /tmp/sqlrb_pocr_aggregator_smoke_existing_pg40_v0/output and ran
# aggregate_pocr_rows/write_pocr_aggregate_outputs over those row metrics.
PY
sed -n '1,10p' /tmp/sqlrb_pocr_aggregator_smoke_existing_pg40_v0/output/results/pocr_aggregator_smoke_existing_pg40_v0/pocr/aggregates/pocr_route_summary.csv
wc -l /tmp/sqlrb_pocr_aggregator_smoke_existing_pg40_v0/output/results/pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/pocr/stage_b/pocr_stage_b_row_metrics.csv /tmp/sqlrb_pocr_aggregator_smoke_existing_pg40_v0/output/results/pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0/pocr/stage_b/pocr_stage_b_row_metrics.csv /tmp/sqlrb_pocr_aggregator_smoke_existing_pg40_v0/output/results/pocr_aggregator_smoke_existing_pg40_v0/pocr/aggregates/pocr_route_summary.csv
python -m py_compile src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py
python - <<'PY'
# Parsed smoke_summary.csv and local /tmp pocr_route_summary.csv;
# verified route-summary required columns.
PY
for f in audits/pocr_aggregator_smoke_existing_pg40_v0/*.md; do test -s "$f" || exit 1; done
for phrase in "This is not official POCR." "No route-level official POCR score is emitted." "No paper-facing metric is promoted." "POCR@curated remains deferred until a predeclared curated manifest exists." "Micro-average is diagnostic only and not the paper formula."; do rg -F "$phrase" audits/pocr_aggregator_smoke_existing_pg40_v0 >/dev/null || exit 1; done
git diff --check
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
```

The broad `/tmp` search reported permission-denied messages for unrelated system-private temporary directories; it still confirmed no relevant historical durable row-metrics output for these two route replays beyond test scratch files.

No command read API keys, called a live API, generated annotation JSONL, ran DB/checker/timing, reran a baseline, or mutated candidate SQL.
