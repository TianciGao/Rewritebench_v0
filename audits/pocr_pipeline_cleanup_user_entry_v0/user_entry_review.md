# User Entry Review

本任务新增 `sqlrb user pocr-aggregate`。该命令是 default-off POCR 汇总（pocr aggregation）入口，只读取已有 `pocr_stage_b_row_metrics.csv`，写本地 D035 output root。POCR 不是 official paper metric。

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.

## CLI 行为

命令形态：

```bash
sqlrb user pocr-aggregate \
  --enable-pocr-diagnostic \
  --row-metrics output/results/<replay_run_id>/pocr/stage_b/pocr_stage_b_row_metrics.csv \
  --run-id <aggregate_run_id> \
  --output-root output
```

支持重复 `--row-metrics` 或一次传入多个 paths。输出：

```text
output/results/<run_id>/pocr/aggregates/pocr_route_summary.csv
output/reports/<run_id>/pocr_route_summary.md
```

可用 `--no-report` 跳过 Markdown report。

## Default-off gate

`pocr-aggregate` 必须带 `--enable-pocr-diagnostic`。没有该 flag 时命令失败并且不运行 POCR aggregation。

## 禁止行为

`pocr-aggregate` 不会：

- call API；
- read API key；
- replay annotation；
- run DB/checker/timing；
- compute official POCR；
- promote paper metric；
- write top-level `reports/` or `results/`；
- create leaderboard。

## 边界常量

输出 summary 保持：

- `official_pocr_computed=false`
- `route_level_official_pocr_score_emitted=false`
- `paper_metric_promoted=false`
- `leaderboard_output=false`
- `pocr_curated=NA`
- `pocr_curated_status=curated_manifest_missing`

POCR@planned 和 POCR@candidate 仍然是 D039 promotion views。POCR@curated 暂缓。
