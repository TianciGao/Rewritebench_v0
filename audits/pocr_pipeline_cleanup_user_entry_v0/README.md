# POCR pipeline cleanup user-entry v0

本任务只清理 POCR pipeline 文档和 user entry。POCR 不是 official paper metric。POCR@planned 和 POCR@candidate 仍然是 D039 promotion views。POCR@curated 暂缓，直到存在预先声明的 curated manifest。Track A 120 不是 leaderboard。

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.

本任务完成：

- 新增中文优先文档 `docs/pocr_pipeline.md`。
- 将 `src/sql_rewrite_bench/pocr/README.md` 改为中文优先 package/module map。
- 新增 `sqlrb user pocr-aggregate` 薄 CLI facade。
- 清理主 CLI 中 POCR wording，不再把 POCR 简化描述为 `deferred`。
- 增加 user-entry tests，覆盖 `pocr-aggregate` default-off、输出路径、边界常量和 help wording。

本任务未执行：

- 无 live API call。
- 无 API key read。
- 无 annotation JSONL generation。
- 无 retry。
- 无 pocr-diagnostic replay run。
- 无 POCR aggregation production run；只有 tiny offline tests。
- 无 DB/checker/timing run。
- 无 baseline rerun。
- 无 candidate SQL generation 或 mutation。
- 无 official POCR computation。
- 无 paper-facing metric promotion。
- 无 top-level reports/results update。
- 无 retained-evidence promotion。
- 无 leaderboard。
