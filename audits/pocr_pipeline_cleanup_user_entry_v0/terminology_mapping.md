# Terminology Mapping

本文档记录本任务采用的 POCR 术语映射。POCR 不是 official paper metric。POCR@planned 和 POCR@candidate 仍然是 D039 promotion views。POCR@curated 暂缓。

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.

| 中文优先术语 | English / code term | 说明 |
| --- | --- | --- |
| Stage A 标注 | Stage A annotation | LLM 读取 source / positive / candidate / skills.md 后提出 atom-level JSON annotation；只有显式 live mode 才可调用 API。 |
| POCR 诊断回放 | pocr-diagnostic replay | 读取已有 Stage A annotation JSONL，执行 Stage B 证据验证并导出 diagnostic rows；无 API。 |
| Stage B 证据验证 | Stage B evidence validation | 检查 atom support 是否有 source-to-candidate transformation evidence；span presence alone 不够。 |
| 逐行指标导出 | row metrics export | 写 `pocr_stage_b_row_metrics.csv`；由 `stage_b_row_metrics.py` 负责。 |
| POCR 汇总 | pocr aggregation | 读 row metrics，写 `pocr_route_summary.csv`；由 `pocr_aggregator.py` 负责。 |
| 失败闭合 | fail-closed | no candidate、schema invalid、route mismatch 等状态保留为显式零贡献或状态行，不静默删除。 |
| candidate/control route | candidate/control route | SQLGlot no-op 是 candidate/control route，不是 reference。 |

补充边界：

- POCR 不等于 correctness。
- POCR 不等于 speed。
- Track A 120 不是 leaderboard。
- positive SQL 是 reference evidence，不是 atom source。
- `skills.md` 是唯一 operation-atom source。
