# User Flag Contract

Command:

```text
python -m cli.main user pocr-diagnostic \
  --enable-pocr-diagnostic \
  --candidate-root <candidate_sql_root> \
  --method-id <method_id> \
  --route-id <route_id> \
  --engine <engine> \
  --run-id <run_id> \
  --output-root <output_root> \
  [--annotation-jsonl <path>] \
  [--case-list <path>]
```

Flag behavior:
- If `--enable-pocr-diagnostic` is absent, no POCR code runs.
- If `--enable-pocr-diagnostic` is present and required inputs are missing, the command fails closed before calling the POCR facade.
- `live_enabled=false` is hard-coded for this integration task.
- API keys are not read.

Output files:
- `output/results/<run_id>/pocr/diagnostic_rows.csv`
- `output/results/<run_id>/pocr/diagnostic_summary_by_pool.csv`
- `output/logs/<run_id>/pocr/pocr_diagnostic.log`
- `output/reports/<run_id>/pocr_diagnostic.md`

Row-level constants:
- `diagnostic_only=true`
- `official_pocr_computed=false`
- `route_level_pocr_aggregated=false`
- `paper_metric_promoted=false`

Allowed summary:
- Diagnostic summary by pool with counts only.

Disallowed output:
- Route-level POCR score.
- Official Positive Operation Coverage Rate.
- Paper-facing metric promotion.
- Leaderboard row.
