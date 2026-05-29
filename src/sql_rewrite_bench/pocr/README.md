# POCR package 边界和模块地图

本文档用中文优先说明 `src/sql_rewrite_bench/pocr/` package。文件名、Python symbol、CLI command、CSV column name 保持英文。

POCR 不是 official paper metric。POCR@planned 和 POCR@candidate 仍然是 D039 promotion views。POCR@curated 暂缓，直到存在预先声明并冻结的 curated denominator manifest。Track A 120 不是 leaderboard。

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.

## package 目的

本 package 实现 optional Positive Operation Coverage diagnostic support。它负责：

- 解析 case-local root-level `skills.md`；
- 支持 Stage A 标注（Stage A annotation）；
- 执行 Stage B 证据验证（Stage B evidence validation）；
- 导出逐行指标（row metrics export）；
- 汇总 promotion-diagnostic POCR@planned / POCR@candidate。

它不负责 official metric promotion、paper-facing reports/results、retained evidence promotion、leaderboard output、DB/checker/timing 或 baseline rerun。

## 用户入口

普通用户应通过 `sqlrb user` facade 进入：

```bash
sqlrb user pocr-diagnostic ...
sqlrb user pocr-aggregate ...
```

- `pocr-diagnostic`：POCR 诊断回放，读取已有 Stage A annotation JSONL，执行 Stage B 证据验证，写逐行指标。
- `pocr-aggregate`：POCR 汇总，读取 `pocr_stage_b_row_metrics.csv`，写 `pocr_route_summary.csv`。

这两个命令都必须显式使用 `--enable-pocr-diagnostic`，默认关闭。它们不自动调用 API。

## 模块职责

### contract / parsing

- `models.py`：`skills.md` contract 的 dataclass 和 validation issue 类型。
- `skills_parser.py`：解析 case-local root-level `skills.md`。
- `validation.py`：校验 skill contract 与 case directory metadata / required sections。
- `inventory.py`：Common-core inventory scanning 和 parse-only audit helper。

expected operation atoms 只能来自 `skills.md` 中的 `operation_atom`。不得从 taxonomy、SQL shape、positive SQL、source SQL、candidate SQL、retained evidence 或 ad hoc analysis 推断 atoms。

### candidate / annotation

- `candidate_resolver.py`：只读解析 existing route-labeled candidate roots。
- `annotation_schema.py`：Stage A candidate annotation schema 和 validator。
- `prompt_builder.py`：基于 `skills.md`、source SQL、candidate SQL、positive SQL 构造 deterministic prompt。
- `annotation_client.py`：fake/offline 和 fail-closed live client 接口。live API 必须显式授权。
- `json_output_guard.py`：provider response JSON parse guard。
- `annotation_resolver.py`：只读 annotation JSONL replay resolver。
- `checkpointed_annotation_runner.py`：Stage A 标注（Stage A annotation）runner，负责 checkpoint、resume、safe JSONL、fail-closed provider rows。

Stage A annotation alone is not counted。Stage A 只是结构化声明，不能直接进入 POCR numerator。

### Stage B evidence validation

- `evidence_validation.py`：早期 schema / synthetic evidence validation interface。
- `static_evidence.py`：explicit static evidence reference checks。
- `transformation_evidence.py`：SQL normalization 和 source/candidate comparison helper。
- `operation_evidence_policy.py`：Stage B 证据验证的核心策略。

`operation_evidence_policy.py` owns Stage B evidence validation。operation support 必须有 source-to-candidate transformation evidence。`candidate_sql_span` / `source_sql_span` / `positive_sql_span` alone is not operation support。

`semantic_guard_atom` 可以单独验证和计数，但排除在 operation coverage numerator 和 denominator 之外。

### diagnostic replay / output

- `diagnostic_output_schema.py`：diagnostic row / pool summary / CSV / Markdown schema。
- `user_facade.py`：组合 candidate resolver、annotation resolver、Stage B diagnostics 和 output writing 的内部 facade。
- `user_output_adapter.py`：写 D035-style diagnostic output。
- `stage_b_row_metrics.py`：owns row-level export，写 `pocr_stage_b_row_metrics.csv`。

`stage_b_row_metrics.py` 只导出 aggregator input。它不计算 route-level POCR，不 promotion paper metric。

### aggregation

- `pocr_aggregator.py`：owns promotion-diagnostic POCR aggregation。

`pocr_aggregator.py` 读取一个或多个 `pocr_stage_b_row_metrics.csv`，计算 macro-average POCR@planned / POCR@candidate，并输出 `pocr_route_summary.csv`。它必须保持：

- `official_pocr_computed=false`
- `route_level_official_pocr_score_emitted=false`
- `paper_metric_promoted=false`
- `leaderboard_output=false`
- `pocr_curated=NA`
- `pocr_curated_status=curated_manifest_missing`

Diagnostic micro-average 只能作为 separately labeled diagnostic，不是 paper formula。

## 不应该走的 shortcut

- 不要让 `local_metrics.py` own POCR computation。`local_metrics.py` 负责 generation / execution / exact / timing local metrics，不负责 POCR aggregation。
- 不要从 candidate SQL、positive SQL、source SQL 或 taxonomy 直接生成 operation atoms。
- 不要把 SQLGlot no-op 当 reference。SQLGlot no-op 是 candidate/control route，不是 reference。
- 不要把 positive SQL 当 atom source。positive SQL 是 reference evidence，不是 atom source。
- 不要把 Stage A annotation alone 计入 implemented atoms。
- 不要把 span presence alone 计入 operation support。
- 不要从 `output/` 推广到 top-level `reports/` / `results/`，除非有单独授权。

## internal audit helpers

以下模块主要用于历史 audit、calibration 或 release-v0 traceability，不是稳定公共 API：

- `draft_runner.py`
- `pocr_row.py`
- `stage_b_static_runner.py`
- `live_smoke.py`
- `calibration_runner.py`
- `real_route_diagnostic_runner.py`
- `manual_review.py`
- `retry_planner.py`
- `evidence_ref_linter.py`

这些模块不得作为 shortcut 来绕开 `pocr-diagnostic` / `stage_b_row_metrics.py` / `pocr_aggregator.py` 的边界。

## official promotion gate

official metric promotion remains separately gated。当前 package 可以支持 promotion review，但不能自行完成：

- official POCR computation；
- route-level official POCR score emission；
- paper-facing metric promotion；
- retained-evidence promotion；
- top-level reports/results update；
- denominator change；
- case membership change；
- global leaderboard。

POCR 不等于 correctness。POCR 不等于 speed。Track A 120 不是 leaderboard。
