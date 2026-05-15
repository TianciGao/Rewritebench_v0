SQL-RewriteBench 迁移当前状态

版本：v0.1
旧仓库：sql-rewrite-bench-artifact-clean
发布仓：Rewritebench_v0
状态：当前进度表
最后更新：2026-05-15

## 1. 当前总状态

当前处于：

post-bootstrap planning stage

尚未进入大规模 case 物理迁移。

当前最重要的判断：

旧仓库是 sql-rewrite-bench-artifact-clean；
新发布仓是 Rewritebench_v0；
public release layout 是迁移目标，不是旧仓库当前事实；
已经完成若干只读审计；
control-layer bootstrap 已完成；
三个 project_control 文件已创建、提交并 push 到 GitHub；
project_control/MIGRATION_RUN_LOG.md now exists as the execution ledger；
full execution history should be recorded in MIGRATION_RUN_LOG.md, while this file remains a current status snapshot；
runs/ 不能直接删除；
Common-core 40 是 public v0 主范围；
全部 197 case-like packages 需要治理索引；
本地发布仓 clone 已确认；
latest completed run is PORT_0008 formal sanitized evidence mapping pilot；
当前下一步安全动作是 review PORT_0008 pilot slice, then either apply the same evidence-mapping-only pattern to another simple PORT case or continue with approved pilot planning。

## 2. 仓库 / 工作区状态

### 2.1 旧仓库

sql-rewrite-bench-artifact-clean

状态：用户确认这是旧仓库；control-layer bootstrap 未修改该仓库。

本地路径：

/home/tianci_gao/code/sql-rewrite-bench-artifact-clean

分支：

artifact/case-package-contract-alignment-clean

当前已知状态：

behind origin by 7；
已有 dirty files under reports/evaluation/common_core_v0/...；
bootstrap 未修改旧仓库。

迁移 caution：

在从 legacy repo 迁移任何文件前，必须先决定如何处理 behind-by-7 与 dirty reports/evaluation/common_core_v0 状态；不得在该状态下直接做大规模迁移或复制 evidence。

### 2.2 新发布仓

https://github.com/TianciGao/Rewritebench_v0

用途：public release repository；用于保存 project_control 文件和后续 clean release 迁移内容。

### 2.3 本地发布仓 clone

状态：已确认并完成 control-layer bootstrap。

本地路径：

/home/tianci_gao/code/Rewritebench_v0

分支：

main

remote：

git@github.com:TianciGao/Rewritebench_v0.git

bootstrap 后 final status：

## main...origin/main

已创建并 push 的 control files：

project_control/MIGRATION_MASTER_PLAN.md；
project_control/MIGRATION_STATUS.md；
project_control/DECISION_LOG.md；
project_control/MIGRATION_RUN_LOG.md。

bootstrap commit：

1b7fab1 project: add migration control files

Execution history:

Use `project_control/MIGRATION_RUN_LOG.md` for the chronological Codex execution ledger. `MIGRATION_STATUS.md` should stay focused on current state, blockers, and next safe action.

### 2.4 clean worktree

状态：待 Codex 检查并填写。

如果需要，可使用：

~/code/sql-rewrite-bench_public_migration_worktree

但当前优先使用新发布仓 Rewritebench_v0 作为控制文件和发布仓。

## 3. 已完成审计

### 3.1 第一轮：整体初步审计

状态：已完成只读审计。

主要发现：

cases/ 下检测到 197 个 case-like directories；
registry 语境曾提到 190 个 registered case packages；
pool 数量为 PERF 105、CONS 40、PORT 28、LONGTAIL 24；
所有 detected case directories 都有 manifest；
第一轮发现 183 个 case directories 有 runs/；
reports/evaluation/common_core_v0 混合 retained evidence、run workspaces、logs、timing outputs；
脚本不应整包复制；
static hygiene scan 发现 AI-agent、本地路径、prompt、API-keyword 等风险。

结论：接受为只读审计结果；需要后续正式做 case universe reconciliation、script inventory 和 reports/results audit。

### 3.2 第二轮：runs/ 专项审计

状态：已完成只读审计。

主要发现：

197 rows in runs package matrix；
184 with runs/；
Common-core 40 全部有 runs/；
162 个 retain_in_case_as_minimal_evidence；
21 个 manual_review_required；
14 个 regenerable_by_external_runner。

结论：

以 184 with runs 为当前准数；
runs/ 是 legacy retained evidence surface；
不得直接删除；
后续应通过 evidence/runs_retention.yaml 索引。

### 3.3 第三轮：Common-core 40 contract-fit 审计

状态：已完成只读审计。

扫描范围：

PERF 16；
CONS 9；
PORT 9；
LONGTAIL 6。

结果：

28 个 phase_2_add_evidence_index；
5 个 phase_3_representative_physical_pilot；
7 个 defer_manual_review；
0 个 phase_1_manifest_only。

结论：

Common-core 40 不能只靠 manifest-only normalization；
每个 case 至少需要 evidence index；
物理迁移需要先做 pilot；
PORT 7 个 manual-review case 是当前 blocker。

## 4. 当前 blockers

### B001：本地发布仓 / worktree 状态未确认

状态：resolved。

影响：

本 blocker 已解除；本地发布仓 clone、branch、remote、status 均已确认，三个 control files 已提交并 push。

下一步：

后续迁移优先在 `/home/tianci_gao/code/Rewritebench_v0` 中推进 control-layer 和 clean public release 内容；不得修改旧仓库 case/evidence 文件。

新增 caution：

在从 legacy repo 迁移任何文件前，必须先决定如何处理旧仓库 behind-by-7 与 dirty `reports/evaluation/common_core_v0/...` 状态。

### B002：PORT manual-review 风险

涉及 case：

PORT_0004；
PORT_0008；
PORT_0012；
PORT_0013；
PORT_0022；
PORT_0024；
PORT_0025。

风险：

Spark warehouse residue；
parquet / crc / _SUCCESS 文件角色不清；
local path / WSL / localhost；
prompt / API / token / assistant traces；
logs / stderr / debug residue；
evidence role 不明。

下一步：

做只读逐文件检查；
先分类，不删除、不移动、不清洗。

### B003：reports/evaluation/common_core_v0 混合 retained evidence 与 scratch

影响：

不能直接全量迁移 reports；
需要 curated retained evidence map。

下一步：

做 reports/results audit；
建立 paper_evidence_freeze_map。

### B004：script inventory 尚未正式化

影响：

不能直接复制 scripts/；
不知道哪些脚本是 user-facing、dev、internal、scratch。

下一步：

做 script inventory；
每个脚本标记 reuse_decision。

## 5. 当前建议 first batch

Physical pilot candidates：

PERF_0006；
CONS_0005；
PORT_0003；
LONGTAIL_0011；
LONGTAIL_0022。

Evidence-index 对照样本：

PERF_0007；
CONS_0007；
PORT_0005。

暂缓：

PORT_0004；
PORT_0008；
PORT_0012；
PORT_0013；
PORT_0022；
PORT_0024；
PORT_0025。

## Last Codex run：PORT_0008 formal sanitized evidence mapping pilot

Date：2026-05-15

Task name：PORT_0008 formal sanitized evidence mapping pilot

Mode：release-repo formal evidence-mapping pilot；legacy read-only

Legacy repo modified：no

Actual legacy evidence sanitized/moved/deleted/copied：no

Formal public sanitized copies created：yes

Case-local `evidence/runs_retention.yaml` created for PORT_0008：yes

Full case package migrated：no

Denominator changed：no

Paper results changed：no

Validation summary：

- YAML validation：passed；`cases/PORT/PORT_0008/evidence/runs_retention.yaml` parsed successfully.
- SHA256 match：passed；both formal sanitized plan copies match the corresponding Route B trial artifacts.
- Sanitized output scan：passed；formal public pilot files do not expose maintainer-local paths, local URI traces, host endpoints, platform traces, or credential-keyword traces covered by the required scan.
- Raw legacy Spark plan copied into public retained evidence：no；formal retained plan files were copied from validated sanitized trial outputs only.

Next safe action：review the committed PORT_0008 pilot slice, then use the same evidence-mapping-only pattern for the next approved PORT manual-review case.

## 6. Phase progress

| Phase | 名称 | 状态 | 当前判断 | 下一步 |
|---|---|---|---|---|
| 0 | 确认旧仓库与发布仓工作区 | completed | release repo clone、branch、remote、status 已确认；control files 已 push | 进入 PORT manual-review read-only resolution |
| 1 | 整体情况审计 | partial done | 已有初步审计 | 整理正式 summary |
| 2 | 代表性 case 选择与模板设计 | pending | 已有建议 batch | 先设计模板 |
| 3 | case package template v1 | pending | 目标结构已有草案 | 起草 contract |
| 4 | pilot migration | not started | 不应直接开始 | 等 contract + worktree |
| 5 | Common-core 40 migration | not started | 40 个都需要 evidence index | 先 pilot |
| 6 | 整体 case universe 治理 | partial | 197 vs 190 差异已知 | 做 reconciliation |
| 7 | 脚本与复现路径整理 | pending | 需 script inventory | 做脚本台账 |
| 8 | 结果与论文表格闭环 | pending | reports 混合 | 做 retained evidence map |
| 9 | public hygiene | pending | 风险已知 | 后期扫描 |
| 10 | public release v0 | not started | 前序未完成 | 等 smoke pass |

## 7. 当前不能做的事

当前不应：

直接重排全部 cases；
删除或外迁 runs/；
清空 reports；
批量复制 scripts；
合并 different routes；
改 Common-core 分母；
把 non-common-core 加进 public v0 主分母；
建 global leaderboard；
在旧仓库 dirty 状态下做大规模迁移。

## 8. 当前安全下一步

根据 2026-05-15 Spark plan sanitization trial，当前安全下一步是：

1. 人工审阅 Route B trial sanitized artifacts，重点确认 Spark plan structure 是否保持证据含义、local path redaction 是否足够、PORT_0024 result-check summary 是否满足 public evidence 要求。
2. 若人工批准，选择一个受影响 PORT case 将 trial mapping 转化为正式 case-local `evidence/runs_retention.yaml` 和 public retained evidence path 设计；仍不要修改 legacy repo。
3. 在批准前，不要把 trial outputs 当作 final retained evidence，也不要删除、移动、清洗或替换 legacy originals。

## 9. Last Codex run

- task name: PORT manual-review read-only resolution
- date: 2026-05-15
- mode: read-only legacy inspection, release-repo audit outputs
- legacy repo modified: no
- release repo modified: yes, audit outputs and `MIGRATION_STATUS.md` only
- outputs created:
  - `audits/port_manual_review_resolution/port_case_clearance_summary.md`
  - `audits/port_manual_review_resolution/port_manual_review_resolution.csv`
  - `audits/port_manual_review_resolution/port_file_review_matrix.csv`
  - `audits/port_manual_review_resolution/port_public_release_risk_table.md`
  - `audits/port_manual_review_resolution/port_sanitize_or_archive_plan.md`
  - `audits/port_manual_review_resolution/port_no_delete_list.txt`
  - `audits/port_manual_review_resolution/port_static_reference_map.csv`
  - `audits/port_manual_review_resolution/port_followup_questions.md`
- cases inspected:
  - PORT_0004
  - PORT_0008
  - PORT_0012
  - PORT_0013
  - PORT_0022
  - PORT_0024
  - PORT_0025
- cases cleared for evidence-index normalization:
  - PORT_0004
  - PORT_0008
  - PORT_0012
  - PORT_0013
  - PORT_0022
  - PORT_0024
  - PORT_0025
- cases cleared for physical pilot:
  - PORT_0004
- cases still blocked for physical pilot:
  - PORT_0008
  - PORT_0012
  - PORT_0013
  - PORT_0022
  - PORT_0024
  - PORT_0025
- cases needing human approval:
  - PORT_0008
  - PORT_0012
  - PORT_0013
  - PORT_0022
  - PORT_0024
  - PORT_0025
- next safe action: resolve the sanitized-copy vs private/archive decision for the six blocked PORT cases, then draft evidence-index / `runs_retention.yaml` templates without moving case files.

## 10. Last Codex run

- task name: runs-retention policy and PORT sanitization template design
- date: 2026-05-15
- mode: policy/template design in release repo; no legacy evidence edits
- legacy repo modified: no
- release repo modified: yes, policy docs, templates, PORT preview mappings, `DECISION_LOG.md`, and `MIGRATION_STATUS.md`
- actual evidence sanitized/moved/deleted/copied: no
- D013 added: yes, `Sanitizable Spark plan evidence policy`
- outputs created:
  - `repository_spec/runs_retention_policy_v1.md`
  - `repository_spec/case_package_contract_v1.md`
  - `templates/runs_retention_template.yaml`
  - `templates/port_sanitized_plan_mapping_template.yaml`
  - `audits/port_manual_review_resolution/previews/PORT_0004_runs_retention_preview.yaml`
  - `audits/port_manual_review_resolution/previews/PORT_0008_runs_retention_preview.yaml`
  - `audits/port_manual_review_resolution/previews/PORT_0012_runs_retention_preview.yaml`
  - `audits/port_manual_review_resolution/previews/PORT_0013_runs_retention_preview.yaml`
  - `audits/port_manual_review_resolution/previews/PORT_0022_runs_retention_preview.yaml`
  - `audits/port_manual_review_resolution/previews/PORT_0024_runs_retention_preview.yaml`
  - `audits/port_manual_review_resolution/previews/PORT_0025_runs_retention_preview.yaml`
  - `audits/port_manual_review_resolution/port_runs_retention_preview_summary.md`
- cases with proposed runs-retention previews:
  - PORT_0004
  - PORT_0008
  - PORT_0012
  - PORT_0013
  - PORT_0022
  - PORT_0024
  - PORT_0025
- evidence-index normalization status: all seven PORT cases have preview mappings and can proceed to evidence-index normalization design.
- physical pilot status:
  - PORT_0004 remains clear for copy-first physical pilot with runs-retention mapping.
  - PORT_0008, PORT_0012, PORT_0013, PORT_0022, PORT_0024, and PORT_0025 remain blocked for physical pilot until sanitized public copies and/or private archive mappings are implemented.
- next safe action: pick the first copy-first pilot package and implement case-local `evidence/runs_retention.yaml` plus sanitized/archive path mapping without changing denominators, paper results, or raw legacy evidence.

## 11. Last Codex run

- task name: Spark plan sanitization trial for six blocked PORT cases
- date: 2026-05-15
- mode: release-repo sanitized trial; legacy read-only
- legacy repo modified: no
- release repo modified: yes, sanitized trial outputs and `MIGRATION_STATUS.md`
- actual legacy evidence sanitized/moved/deleted/copied: no
- sanitized trial copies created: yes
- cases covered:
  - PORT_0008
  - PORT_0012
  - PORT_0013
  - PORT_0022
  - PORT_0024
  - PORT_0025
- outputs created:
  - `audits/port_manual_review_resolution/sanitized_trial/README.md`
  - `audits/port_manual_review_resolution/sanitized_trial/redaction_manifest.csv`
  - `audits/port_manual_review_resolution/sanitized_trial/redaction_validation.csv`
  - `audits/port_manual_review_resolution/sanitized_trial/original_to_sanitized_mapping.csv`
  - `audits/port_manual_review_resolution/sanitized_trial/case_clearance_after_sanitization_trial.md`
  - `audits/port_manual_review_resolution/sanitized_trial/PORT_0008/`
  - `audits/port_manual_review_resolution/sanitized_trial/PORT_0012/`
  - `audits/port_manual_review_resolution/sanitized_trial/PORT_0013/`
  - `audits/port_manual_review_resolution/sanitized_trial/PORT_0022/`
  - `audits/port_manual_review_resolution/sanitized_trial/PORT_0024/`
  - `audits/port_manual_review_resolution/sanitized_trial/PORT_0025/`
- validation result summary:
  - 12 Spark plan sanitized trial files created and validated with no raw local path remaining.
  - 1 PORT_0024 Spark result-check sanitized summary created and validated with stdout/stderr log references replaced by placeholders.
  - YAML validation passed for all six per-case `mapping.yaml` files.
  - Broad whole-tree substring scan has a known schema-label caveat because `redaction_validation.csv` is required to include a host-name validation column; artifact-content validation passed.
- remaining blockers:
  - human approval is still required before trial artifacts become final public retained evidence.
  - original legacy artifacts remain do-not-delete and must stay mapped.
  - this does not authorize physical case migration by itself.
- next safe action: human review of Route B trial artifacts, then approve one formal sanitized evidence mapping pilot without modifying the legacy repository.
