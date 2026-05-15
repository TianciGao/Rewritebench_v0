SQL-RewriteBench 迁移当前状态

版本：v0.1
旧仓库：sql-rewrite-bench-artifact-clean
发布仓：Rewritebench_v0
状态：当前进度表
最后更新：TBD

## 1. 当前总状态

当前处于：

control-layer bootstrap / planning stage

尚未进入大规模 case 物理迁移。

当前最重要的判断：

旧仓库是 sql-rewrite-bench-artifact-clean；
新发布仓是 Rewritebench_v0；
public release layout 是迁移目标，不是旧仓库当前事实；
已经完成若干只读审计；
runs/ 不能直接删除；
Common-core 40 是 public v0 主范围；
全部 197 case-like packages 需要治理索引；
需要确认本地 clean worktree / 发布仓 clone；
下一步应先创建项目控制文件和确认工作区，再做代表性 case 模板。

## 2. 仓库 / 工作区状态

### 2.1 旧仓库

sql-rewrite-bench-artifact-clean

状态：用户确认这是旧仓库。

### 2.2 新发布仓

https://github.com/TianciGao/Rewritebench_v0

用途：public release repository；用于保存 project_control 文件和后续 clean release 迁移内容。

### 2.3 本地发布仓 clone

状态：待 Codex 检查并填写。

建议本地路径：

~/code/Rewritebench_v0

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

影响：

不能确定在哪里做后续实际迁移；
不能直接在旧仓库大规模重排。

下一步：

Codex 检查 pwd、branch、remote、git status、worktree list；
确认或 clone Rewritebench_v0。

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

## 6. Phase progress

| Phase | 名称 | 状态 | 当前判断 | 下一步 |
|---|---|---|---|---|
| 0 | 确认旧仓库与发布仓工作区 | active | 旧仓库和发布仓已由用户说明，本地状态待查 | Codex 检查并 clone/pull |
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

在 Rewritebench_v0 中创建三个控制文件；
commit 并 push 到 GitHub；
更新 ChatGPT Project Instructions，使其每轮先读 GitHub 上这三个文件；
之后再做 PORT 7 个 manual-review read-only resolution；
再起草 case package template v1。
