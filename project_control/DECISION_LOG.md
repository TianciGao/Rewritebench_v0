SQL-RewriteBench 迁移决策日志

版本：v0.1
旧仓库：sql-rewrite-bench-artifact-clean
发布仓：Rewritebench_v0
状态：底层决策记录
最后更新：TBD

## D001：旧仓库定义

Decision:

旧仓库定义为：

sql-rewrite-bench-artifact-clean

Reason:

用户确认该仓库是当前 legacy source。后续所有迁移计划中，“旧仓库”均指该仓库，而不是泛称或其他路径。

Impact:

旧仓库是事实源；
不在旧仓库中继续大规模重排；
实际迁移应使用 clean worktree 或发布仓。

## D002：发布仓定义

Decision:

公开发布仓定义为：

https://github.com/TianciGao/Rewritebench_v0

Reason:

用户已建立该仓库作为 clean public release / 发布仓。ChatGPT 可以通过 GitHub 在线文件读取项目控制状态。

Impact:

project_control 三个文件应提交到该仓库；
每次 Codex 更新控制文件后应 push；
ChatGPT Project Instructions 应要求每轮先读取这些在线文件。

## D003：public release v0 范围

Decision:

public release v0 以 Common-core v0 40 cases 为主发布范围：

PERF 16；
CONS 9；
PORT 9；
LONGTAIL 6；
Track A same-engine denominator = 120 planned rows。

Reason:

论文和实验结果均围绕 Common-core v0 的 40 cases / 120 rows 展开。v0 阶段必须优先保证论文结果和复现路径稳定。

Impact:

Common-core 40 是 v0 主迁移对象；
非 Common-core cases 进入 backlog / universe index；
不把全部 197 case 混入 v0 主分母。

## D004：整体 case universe 也必须治理

Decision:

虽然 public v0 优先 Common-core 40，但全部 197 个 case-like directories 都必须纳入治理。

Reason:

第一轮审计发现 197 case-like directories，而 registry 语境曾提到 190 registered case packages。该差异必须解释，否则 public release 的 case 边界不清。

Impact:

需要 case_universe_index；
需要 registry_reconciliation_report；
非 Common-core 不进入 v0 主结果，但不能忽略。

## D005：runs/ 是 legacy retained evidence

Decision:

case-local runs/ 在迁移期定义为 legacy retained evidence surface。没有 retention mapping 前，不得删除、清空、批量移动或静默改写。

Reason:

runs/ 专项审计发现 184 个 case packages with runs/，Common-core 40 全部有 runs/。大多数 runs/ 至少可能包含 retained evidence。

Impact:

后续每个 migrated case 应有 evidence/runs_retention.yaml；
新运行输出不再写入 case-local runs/；
删除 runs/ 需要人工批准和 no-delete mapping。

## D006：目标 layout 是迁移目标，不是旧仓库事实

Decision:

公开版 layout 是目标结构。旧仓库中不存在 repository_spec/、case_sets/、scripts/user/、results/retained/ 等目录不是错误。

Reason:

迁移要基于审计结果逐步建立 clean layout，而不是把理想目录强行套在 legacy repo 上。

Impact:

不因缺目录而立即补齐所有未来目录；
先建立最小 skeleton；
每个新增目录必须说明用途和 public/backlog 边界。

## D007：先代表性 case，再批量迁移

Decision:

不直接全量迁移。先选代表性 case 做模板和 pilot，确认可行后再迁 Common-core 40。

Reason:

Common-core 40 全部需要 evidence index，且完全目标 layout 都需要 physical move。直接全量迁移风险过高。

Impact:

先做 physical pilot；
使用 copy-first；
不 bulk git mv；
不 delete；
validator 通过后再扩大。

## D008：PORT manual-review 阻塞 physical migration

Decision:

以下 PORT cases 在逐文件复核前不得进入 physical migration：

PORT_0004；
PORT_0008；
PORT_0012；
PORT_0013；
PORT_0022；
PORT_0024；
PORT_0025。

Reason:

这些 case 可能存在 Spark warehouse residue、本地路径、prompt/API/token traces、logs/stderr 或 evidence role 不清。

Impact:

必须先做只读 manual-review resolution；
复核前不删除、不移动、不清洗、不公开风险文件。

## D009：不建立 global leaderboard

Decision:

SQL-RewriteBench public release 不建立 global leaderboard。

Reason:

不同方法和路线的 role、denominator、engine scope、timing eligibility 不同。强行排名会掩盖失败边界。

Impact:

reports 和 README 不得命名 winner；
Direct LLM、Repair-1、SQLGlot no-op、SQLGlot optimize、Calcite HEP、PORT routes、verifier support 必须分开报告；
speedup 只能在 exact + timed denominator 上解释。

## D010：脚本迁移先 wrap 后 refactor

Decision:

脚本不整包复制，也不一开始全部重写。先 inventory，再决定 keep / wrap / refactor / archive / drop / manual-review。

Reason:

旧脚本可能混合 DB runner、LLM runner、本地路径、reports writer、dev scratch 和 paper renderer。直接复制会污染 public release。

Impact:

需要 script_inventory；
用户脚本优先；
deterministic 路径优先；
LLM 和 prior-system adapters 后置。

## D011：reports/results 必须 curated migration

Decision:

reports/results 不全量迁移。先区分 paper-facing retained evidence、summary tables、local run workspaces、timing outputs、logs 和 scratch。

Reason:

第一轮审计显示 reports/evaluation/common_core_v0 混合 retained evidence 与临时运行产物。直接迁移会污染 public release。

Impact:

需要 paper_evidence_freeze_map；
只迁移 curated retained evidence；
不改变论文表格数字；
scratch/logs 不进入 retained evidence。

## D012：ChatGPT 进度读取方式

Decision:

ChatGPT 不依赖本地 Codex 工作区读取进度，而是通过 Rewritebench_v0 GitHub 仓库中的 project_control 文件读取当前状态。

Reason:

Codex 能读本地文件，但 ChatGPT 不能自动读取本地 ~/code/...。GitHub 在线文件是 ChatGPT 与 Codex 之间同步项目状态的稳定方式。

Impact:

Codex 每次更新三个控制文件后必须 commit + push；
ChatGPT Project Instructions 必须写明每轮先读这三个在线文件；
如果在线文件不可用，ChatGPT 应要求用户上传或粘贴 MIGRATION_STATUS.md。

## D013：Sanitizable Spark plan evidence policy

Decision:

Public release keeps sanitized public copies for Spark plan evidence with local path traces.

Original legacy artifacts are retained through mapping and may stay in private/external archive.

Raw local path traces must not appear in public retained evidence.

PORT_0024-style stdout/stderr log references should be summarized or archived, not exposed raw by default.

Reason:

PORT manual-review audit found local-path traces in Spark plan evidence for six PORT cases.

These files are evidence, not trash.

Public release should be clean while preserving traceability.

Impact:

Draft runs_retention policy and templates.

Do not sanitize or move files until later approved migration steps.

Evidence-index normalization can proceed for all seven PORT cases using preview mappings.

Physical migration remains blocked for the six cases until sanitized public copies or archive mappings are implemented.

## D014：每轮 Codex run 必须追加 MIGRATION_RUN_LOG

Decision:

Every Codex task that modifies the release repo or produces audit outputs must append one entry to:

project_control/MIGRATION_RUN_LOG.md

The entry must record:

- task name;
- mode;
- whether legacy repo was modified;
- files created/modified;
- validation result;
- commit hash;
- push result;
- denominator/paper-result impact;
- next safe action.

Reason:

MIGRATION_STATUS.md is a current-state snapshot and should not become a long execution diary.

DECISION_LOG.md records long-term decisions, not per-run details.

A separate run log is needed for traceability and later audit/review.

Impact:

- Every future Codex prompt must include MIGRATION_RUN_LOG.md in its final writeback requirements.
- MIGRATION_STATUS.md should keep only the latest summary and point to MIGRATION_RUN_LOG.md for full history.
- ChatGPT should consult MIGRATION_RUN_LOG.md when reconstructing prior execution history.
