# Documentation Review

本任务按中文优先政策新增和更新 POCR 说明文档。POCR 不是 official paper metric。Track A 120 不是 leaderboard。

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.

## 新增文档

`docs/pocr_pipeline.md` 说明：

- POCR 是什么；
- POCR 不是什么；
- `source.sql` / `positive.sql` / `skills.md` / `candidate.sql` 的角色；
- Stage A 标注（Stage A annotation）；
- POCR 诊断回放（pocr-diagnostic replay）；
- Stage B 证据验证（Stage B evidence validation）；
- 逐行指标导出（row metrics export）；
- POCR 汇总（pocr aggregation）；
- POCR@planned / POCR@candidate / POCR@curated 的区别；
- 为什么 POCR@curated 暂缓；
- 为什么 SQLGlot no-op 是 candidate/control route，不是 reference；
- 为什么 POCR 不等于 correctness；
- 为什么 POCR 不等于 speed；
- 为什么不能做 global leaderboard；
- `sqlrb user pocr-diagnostic` 和 `sqlrb user pocr-aggregate` 示例；
- D035 output paths；
- 文本/Mermaid pipeline 图。

## 更新文档

`src/sql_rewrite_bench/pocr/README.md` 说明：

- package module map；
- 每个 module 的 responsibility；
- `local_metrics.py` 不应该 own POCR computation；
- `pocr_aggregator.py` owns promotion-diagnostic POCR aggregation；
- `stage_b_row_metrics.py` owns row-level export；
- `checkpointed_annotation_runner.py` owns Stage A annotation；
- `operation_evidence_policy.py` owns Stage B evidence validation；
- official metric promotion remains separately gated。

## Terminology cleanup

文档统一使用：

- Stage A 标注（Stage A annotation）
- POCR 诊断回放（pocr-diagnostic replay）
- Stage B 证据验证（Stage B evidence validation）
- 逐行指标导出（row metrics export）
- POCR 汇总（pocr aggregation）

避免把 “Stage B replay” 作为主术语；如果出现，定义为旧称。
