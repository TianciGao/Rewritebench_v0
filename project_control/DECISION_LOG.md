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

## D015：Canonical case package layout policy

Decision:

Public release case packages should converge to the canonical layout defined in:

repository_spec/canonical_case_package_layout_v1.md

The layout is a target, not legacy current fact.

Legacy-compatible pilots may exist, but they do not redefine the target layout.

`runs/` remains legacy retained evidence and must be mapped through `evidence/runs_retention.yaml`.

New run outputs must not be written into case-local `runs/`.

`case_sets/` defines release membership and denominators.

Reason:

We need to prevent drift during subsequent Codex migrations.

`PORT_0004` proved copy-first migration can work, but its legacy-compatible layout is not the final canonical structure.

`PORT_0008` or another later pilot should test canonical layout explicitly.

Impact:

Future full-case migration prompts must reference `canonical_case_package_layout_v1.md`.

Validator full-case mode should later be extended to check canonical layout conformance.

No immediate case movement is authorized by this decision.

## D016：Redevelopment-led public workbench phase after Common-core 40 canonical migration

Decision:

After completing Common-core 40 canonical case-package migration and membership/denominator scaffolding, the project shifts from migration-first work to redevelopment-led public workbench construction.

The public workbench should be built around:

- canonical case packages;
- evidence ledger schema;
- metrics contract;
- runner/output policy;
- retained evidence adapter;
- reproduction/report renderer;
- user-facing candidate runner.

Legacy scripts, reports, and results should be treated as retained evidence sources, reference implementations, or adapter inputs, not as the architecture to copy wholesale.

Reason:

Legacy scripts and reports/results mix DB runners, LLM runners, local paths, scratch outputs, logs, timing artifacts, and paper renderers. Copying them wholesale would preserve legacy complexity and make future metric adjustments harder.

Impact:

- Future scripts should be designed against canonical case packages and evidence ledger.
- Legacy reports/results should be mapped into a new ledger, not blindly copied.
- User-facing outputs must not write into case-local `runs/`.
- Final metric changes must be confirmed by maintainer/team before implementing the unified reproduction interface.
- Common-core 40 remains the public v0 benchmark line; non-common-core cases remain governed backlog/universe, not v0 denominator.

## D017: Clean public release export strategy

Decision:

`Rewritebench_v0` is treated as a release construction and migration work repository. The final public v0 artifact should be produced through a clean public export branch or clean public release repository rather than assuming that the current construction history and all audit scaffolding are the final public surface.

Reason:

During migration and redevelopment, the repository intentionally contains project-control files, audit reports, planning previews, future prompts, temporary strategy files, and draft specifications. These are useful for safety and coordination but can make the final public repository unnecessarily noisy. A clean export step allows the project to preserve construction traceability while publishing a minimal reviewer/user-facing artifact.

Impact:

- Do not delete current audits during active redevelopment.
- Before release tag, run a public release surface pruning / clean-export task.
- Classify files as `PUBLIC_FINAL`, `PUBLIC_SUPPORT`, `MAINTAINER_ARCHIVE`, `DROP_BEFORE_V0`, or `PRIVATE_ONLY`.
- The clean release surface should retain canonical case packages, case sets, inventory, benchmark specs, user docs, curated reports/results, scripts, source package code, tests, and CI as appropriate.
- Migration logs, future prompts, intermediate audits, scratch files, and internal coordination artifacts should not be assumed to belong in the final public surface.
- If history cleanliness is required, create a clean export branch or clean public release repository from selected files.

## D018: Metrics contract v1 formalized from maintainer/team-approved paper scope

Decision:

The SQL-RewriteBench public workbench metric contract is formalized in `repository_spec/metrics_contract_v1.md` from the maintainer/team-approved paper scope.

The primary metric suite is:

- Coverage: Generation Rate; Execution Coverage Rate.
- Correctness: Result Consistency Rate; Semantic Equivalence Rate.
- Performance: GM_Speedup; Speedup Ratio Percentiles.
- Explainability: Attribution Coverage.
- Generalization: Cross-Engine Execution; Cross-Engine Consistency; Speedup Retention.

The older draft contract remains only as historical alignment context. Metrics implementation, retained-evidence adapter implementation, reproduction interface implementation, public runner implementation, paper table rendering, reports/results migration, denominator changes, paper-result changes, and case membership changes are not authorized by this decision.

Reason:

The maintainer/team-approved paper scope resolves the previous metric-decision packet. Candidate Failure Rate is removed as a primary metric, Regression@20 is demoted to optional legacy diagnostic/comparison status, broad Observability/PlanFrontier framing is replaced in the main suite by Attribution Coverage, and the independent Support Layer is folded into correctness and semantic-equivalence support.

Impact:

- Future metrics code and report rendering must use `repository_spec/metrics_contract_v1.md` as the governing metric contract.
- Public wording should use `Generation Rate`, `Result Consistency Rate`, `Speedup Ratio Percentiles`, and `Description` where applicable.
- Generation Rate means candidate SQL emission over planned cases; extraction/readiness remains diagnostic or optional support.
- Semantic Equivalence Rate is limited to verifier-decidable result-consistent cases, with unknown or undecidable cases reported separately.
- GM_Speedup and Speedup Ratio Percentiles are limited to result-consistent timed cases.
- Speedup Retention is `N.A.` unless paired source-engine and target-engine timing exists.
- Attribution Coverage is the main explainability metric, while atom-based rewrite opportunity observability and PlanFrontier remain support/diagnostic unless separately approved.
- No global leaderboard is allowed.

## D019: Case package v2 external-schema branch adoption

Decision:

Freeze further B-line user-entry and DB/checker expansion while case package v2 external-schema adoption is piloted on a dedicated branch:

`feature/case-package-v2-external-schema`

Adopt the colleague-proposed simplified case package direction for branch pilots:

- SQL files live directly under `sql/`: `source.sql`, `pos_01.sql`, and `neg_01.sql`.
- `witness/` holds data profile and expected/correct result material where safely retained or derivable.
- `checker/` holds comparison configuration, normalization rules, and expected rejection rules.
- `validation/` holds reproducible validation and plan-collection entrypoints.
- Case-local `runs/` is retained only as legacy retained evidence and is not a default output root for new runs.
- Schema assets move out of case packages into reusable external `schemas/<SCHEMA_ID>/` packages.
- Case manifests reference external schema assets through `schema_ref`.

No denominator, `case_sets/`, paper results, retained evidence, reports/results, official metrics, paper tables, raw legacy evidence, or leaderboard changes are authorized by this decision.

External schema adoption requires branch-pilot validation before any Common-core bulk conversion or main-branch merge.

Reason:

The user-entry and DB/checker MVPs proved local execution can work, but the current v1 package layout still embeds schema assets in each case package and uses nested positive/negative SQL directories. Before expanding execution, the repository should pilot the simpler v2 package shape and reusable schema references in a controlled branch so runner and validator compatibility risks are visible before broader conversion.

Impact:

- Further B-line user-entry/DB-checker expansion is frozen until the v2 branch pilot is reviewed.
- `PERF_0006` is the only case authorized for the first v2 external-schema pilot.
- Copy-first external schema adoption is allowed; destructive deletion of case-local schema or retained runs is not required and is not authorized by this decision.
- Existing denominators, Common-core membership, reports/results, paper results, retained evidence, and no-global-leaderboard boundaries remain unchanged.
