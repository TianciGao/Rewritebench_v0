# 清理摘要

本任务是 POCR pipeline cleanup、user-entry integration 和中文优先文档任务。POCR 不是 official paper metric。POCR@planned 和 POCR@candidate 仍然是 D039 promotion views。POCR@curated 暂缓。Track A 120 不是 leaderboard。

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.

## 变更范围

- `docs/pocr_pipeline.md`：新增中文优先用户说明，定义 Stage A 标注、POCR 诊断回放、Stage B 证据验证、逐行指标导出和 POCR 汇总。
- `src/sql_rewrite_bench/pocr/README.md`：中文优先重写 package boundary 和 module map。
- `src/cli/pocr_aggregate.py`：新增 default-off aggregation facade。
- `src/cli/main.py`：注册 `sqlrb user pocr-aggregate`，并清理 POCR wording。
- `src/sql_rewrite_bench/user_output.py`：将 local metrics fallback 中的 POCR wording 改为 optional diagnostic support。
- `tests/user_entry/test_cli_facade.py`：增加 pocr-aggregate user-entry tests，并更新 POCR wording expectations。

## 语义边界

没有改变 D039 metric semantics。`pocr_aggregator.py` 仍然负责 promotion-diagnostic POCR aggregation；`local_metrics.py` 不拥有 POCR computation。`stage_b_row_metrics.py` 仍然负责 row-level export。

本任务没有计算 official POCR，没有 emit route-level official POCR score，没有 promote paper metric。
