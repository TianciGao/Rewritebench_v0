# Smoke Command

Executed command:

```text
PYTHONPATH=src python -m cli.main user pocr-diagnostic \
  --enable-pocr-diagnostic \
  --candidate-root runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql \
  --method-id direct_llm_original \
  --route-id direct_llm_original_pg40_user_smoke \
  --engine postgres \
  --run-id pocr_user_smoke_annotation_missing_v0 \
  --output-root /tmp/sqlrb_pocr_user_smoke_annotation_missing_v0/output
```

No `--annotation-jsonl` argument was supplied.

Observed stdout:

```text
sqlrb user pocr-diagnostic complete: run_id=pocr_user_smoke_annotation_missing_v0 rows=40 results=/tmp/sqlrb_pocr_user_smoke_annotation_missing_v0/output/results/pocr_user_smoke_annotation_missing_v0/pocr reports=/tmp/sqlrb_pocr_user_smoke_annotation_missing_v0/output/reports/pocr_user_smoke_annotation_missing_v0
boundary: Positive Operation Coverage diagnostic support only; official_pocr_computed=false; route_level_pocr_aggregated=false; paper_metric_promoted=false; leaderboard_input=false
```

Expected temp outputs were present:
- `diagnostic_rows.csv`
- `diagnostic_summary_by_pool.csv`
- `pocr_diagnostic.log`
- `pocr_diagnostic.md`
