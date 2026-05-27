# Command Log

Metric-definition checkpoint: this task follows D039. POCR@planned and POCR@candidate remain promotion-diagnostic views. POCR@curated remains NA / curated_manifest_missing until a predeclared curated manifest exists. Macro-average over per-row OC_i is the formula. Diagnostic micro-average is not the paper formula. Expected atoms come only from operation_atom entries in case-local root-level skills.md. semantic_guard_atom is excluded from numerator and denominator. Implemented atoms come only from Stage-B transformation-supported operation atoms. Stage A annotation alone is not counted. candidate/source/positive span presence alone is not enough. source-to-candidate transformation evidence is required. This task does not compute official POCR and does not promote a paper metric.

Initial commands:

```bash
pwd
git branch --show-current
git status -sb --untracked-files=normal
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,260p' project_control/DECISION_LOG.md
tail -n 160 project_control/MIGRATION_RUN_LOG.md
```

Reusable replay commands:

```bash
python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql --annotation-jsonl audits/pocr_real_route_direct_llm_pg40_diagnostic_v0/safe_annotation_outputs.jsonl --method-id direct_llm_original --route-id direct_llm_original_pg40_pocr_diagnostic --engine postgres --run-id pocr_user_replay_pg40_direct_llm_original_pilot_v0 --output-root output
python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql --annotation-jsonl output/results/pocr_annotation_direct_llm_repair1_pg40_targeted_retry_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres/merged_safe_annotation_outputs.jsonl --method-id direct_llm_repair_1 --route-id direct_llm_repair_1_pg40_pocr_diagnostic --engine postgres --run-id pocr_user_replay_pg40_direct_llm_repair1_pilot_v0 --output-root output
python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/common_core_pg_noop_db_checker/candidate_sql --annotation-jsonl output/results/pocr_annotation_sqlglot_noop_pg40_sanity_control_v0/pocr/annotations/sqlglot_noop/sqlglot_noop_pg40_pocr_sanity_control/postgres/safe_annotation_outputs.jsonl --method-id sqlglot_noop --route-id sqlglot_noop_pg40_pocr_sanity_control --engine postgres --run-id pocr_user_replay_pg40_sqlglot_noop_pilot_v0 --output-root output
```

SQLGlot optimize annotation and replay:

```bash
python -m sql_rewrite_bench.pocr.checkpointed_annotation_runner --live-enabled --repo-root . --output-root output --run-id pocr_annotation_pg40_sqlglot_optimize_pilot_v0 --candidate-root runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__postgres/candidate_sql --method-id sqlglot_optimize_schema_aware --route-id sqlglot_optimize_schema_aware_pg40_pocr_diagnostic --engine postgres --case-list <34 candidate-present cases> --max-live-calls 34 --timeout-seconds 90 --max-tokens 4000
python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0__postgres/candidate_sql --annotation-jsonl output/results/pocr_annotation_pg40_sqlglot_optimize_pilot_v0/pocr/annotations/sqlglot_optimize_schema_aware/sqlglot_optimize_schema_aware_pg40_pocr_diagnostic/postgres/safe_annotation_outputs.jsonl --method-id sqlglot_optimize_schema_aware --route-id sqlglot_optimize_schema_aware_pg40_pocr_diagnostic --engine postgres --run-id pocr_user_replay_pg40_sqlglot_optimize_pilot_v0 --output-root output
```

Aggregation:

```bash
python helper using sql_rewrite_bench.pocr.pocr_aggregator over four pocr_stage_b_row_metrics.csv files
```

Results:

- Live SQLGlot optimize calls: 34.
- SQLGlot optimize annotation rows: 34, schema-valid 29, fail-closed 5.
- Replays emitted 40 rows per route.
- Aggregator wrote `output/results/pocr_aggregate_pg40_official_pilot_v0/pocr/aggregates/pocr_route_summary.csv`.

Validation commands:

```bash
python - <<'PY'
# CSV parse checks for audit CSVs, JSONL parse check for generated SQLGlot optimize annotations,
# row metrics CSV parse checks, aggregator summary CSV parse check, Markdown non-empty checks,
# and required phrase checks.
PY
python -m py_compile src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py src/sql_rewrite_bench/pocr/checkpointed_annotation_runner.py src/cli/pocr_diagnostic.py
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
git diff --check
git status --short cases ':(glob)**/skills.md' runs/user reports results case_sets
git diff --name-status -- cases ':(glob)**/skills.md' runs/user reports results case_sets
rg -n --hidden -S '<secret-patterns>' audits/pocr_pg40_official_pilot_annotation_replay_aggregation_v0 project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md
git status -sb --untracked-files=normal
git diff --name-status
```

Validation results:

- Audit CSV parse checks passed.
- Generated SQLGlot optimize annotation JSONL parsed with 34 rows.
- Four local row metrics CSVs parsed with 40 rows each.
- Local aggregator summary parsed with four route rows.
- Markdown non-empty checks and required phrase checks passed.
- `python -m py_compile` passed.
- `pytest tests/pocr -q` passed with 143 tests.
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q` passed with 28 tests.
- `git diff --check` passed.
- Protected-path checks found no `cases/`, `skills.md`, candidate SQL, `runs/user`, top-level `reports/`, top-level `results/`, or `case_sets/` modifications.
- Changed-file secret scan found no API key values.
- Staged protected-path and staged secret scans found no forbidden paths or API key values.
