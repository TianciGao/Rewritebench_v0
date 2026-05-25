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

## D020: Case package v2 target layout

Decision:

Case package v2 is the branch-adoption target on `feature/case-package-v2-external-schema`.

The v2 case package keeps only case-local case assets by default:

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- `sql/pos_01.sql`
- `sql/neg_01.sql`
- `checker/`
- `validation/`
- optional lightweight witness policy metadata
- case-local `runs/` only as legacy retained evidence

The v2 case package does not require case-local `schema/`, does not require case-local `data_profile.yaml`, does not require case-local `correct_result.csv`, and minimizes case-local `evidence/`.

Reason:

The PERF_0006 branch pilot showed that direct SQL paths and manifest references are clearer than the v1 nested SQL/schema/evidence layout, but broad conversion needs a fixed target before validators and runners are updated.

Impact:

- v1 remains compatibility context until the branch pilot and compatibility tasks are accepted.
- Future v2 case conversion prompts must not drift back to v1-only path assumptions.
- This decision does not authorize bulk case conversion, denominator changes, case-set changes, reports/results changes, official metrics, paper tables, retained-evidence deletion, or leaderboard output.

## D021: External schema strategy through schema_ref

Decision:

Schema assets move to top-level reusable schema packages:

`schemas/<SCHEMA_ID>/`

Case manifests reference schema assets through `schema_ref`. After validator and runner compatibility are implemented, `schema_ref` is the source of truth for DB/checker execution schema resolution.

Case-local `schema/` directories remain compatibility artifacts until safe removal is separately authorized.

Reason:

Many cases share source-family schemas. Repeating DDL/load files inside every case package makes package maintenance noisy and makes DB/checker compatibility harder to reason about.

Impact:

- External schema adoption is copy-first until validator and runner compatibility is proven.
- Case-local schema deletion requires explicit retention/compatibility review.
- No DB/checker execution expansion is authorized by this decision.
- Denominators, Common-core membership, paper results, reports/results, retained evidence, and leaderboard policy remain unchanged.

## D022: External evidence strategy through evidence_ref

Decision:

Heavy case evidence moves to, or is referenced through:

`evidence/cases/<POOL>/<CASE_ID>/`

Case manifests reference external evidence through `evidence_ref`.

`evidence/` is not the same as `results/retained/`. `evidence/` is not user-run output. User-run outputs remain under `runs/user/<run_id>/`.

Case-local `runs/` remains legacy retained evidence and must not be deleted without retention mapping and explicit approval.

Reason:

Case packages should stay reviewable and portable. Heavy retained controls, plans, hard-negative artifacts, package validation summaries, and retention maps need stable references without turning each case package into an output archive.

Impact:

- Future evidence externalization must be copy-first and manifest-referenced.
- `results/retained/` remains curated retained-evidence/reporting surface only after separate authorization.
- User-run outputs must not be promoted to retained evidence without a separate retained-evidence policy task.
- No reports/results migration, paper-result update, raw evidence deletion, or leaderboard output is authorized.

## D023: Validation entrypoint consolidation

Decision:

Case package v2 validation entrypoints should converge to:

- `validation/run_validation.sh`
- `validation/run_plan_collection.sh`

Case-local scripts should be thin wrappers. Shared validation and plan-collection logic should live in `scripts/` or `src/`.

Validation wrappers must resolve SQL paths, `schema_ref`, checker configuration, and `evidence_ref` through the manifest.

Existing engine-specific scripts are compatibility assets until wrapper validation is complete.

Reason:

The v1 layout has engine-specific validation scripts and case-local path assumptions. A small stable entrypoint set reduces public user confusion and gives validators one policy to enforce.

Impact:

- v2 wrappers must not write new output into case-local `runs/` by default.
- Runner/validator compatibility work must be non-destructive and manifest-driven.
- Existing compatibility scripts remain until a later cleanup task is authorized.

## D024: Runtime source-as-oracle witness policy

Decision:

For user-run DB/checker execution, the checker oracle defaults to the runtime source SQL result.

`data_profile.yaml` is optional, generated, or external. `correct_result.csv` is optional and is not required for runtime checker execution.

Retained static witness files may still exist under `evidence/` when available. Missing static witness files must not block user-run execution when source-as-oracle execution is available.

Reason:

The bounded DB/checker MVP compares source and candidate results in a local run. Requiring a static correct-result file for every case would block useful user-run diagnostics and duplicate information that can be produced by executing source SQL in the same local schema.

Impact:

- Runtime checker paths should compare `source_result` to `candidate_result`.
- Static witness assets remain useful for audits and retained controls but are not mandatory for local user-run execution.
- If source execution or checker configuration is unavailable, the runner must fail closed and report local diagnostic status, not infer correctness.
- This decision does not authorize official metrics, paper result updates, retained-evidence updates, or leaderboard output.

## D025: Case-local schema profile-only policy for v2

Decision:

Case package v2 retains case-local `schema/` only for:

- `schema/schema_profile.yaml`

Clean v2 case packages do not store executable per-engine DDL/load files under case-local `schema/`. Executable schema assets remain external under:

- `schemas/<SCHEMA_ID>/<engine>/ddl.sql`
- `schemas/<SCHEMA_ID>/<engine>/load.sql`

The case-local `schema/schema_profile.yaml` records the case-facing schema summary and linkage:

- `schema_id`
- external schema profile path
- source family
- relevant tables
- columns and types
- primary keys
- foreign keys
- dialect differences
- fixture/data notes when needed
- engine support summary

Runner and validator compatibility should resolve executable schema through the case manifest, case-local schema profile, and external `schemas/` package. Case-local per-engine DDL/load files may remain only as compatibility artifacts until a cleanup task proves safe removal.

Reason:

The prior v2 wording minimized or externalized `schema/` entirely, but writable conversion planning showed that reviewers still need a lightweight case-local schema summary. Keeping only `schema/schema_profile.yaml` preserves reviewability without duplicating executable DDL/load across cases.

Impact:

- Future v2 conversion must create or normalize `schema/schema_profile.yaml` before deleting any case-local per-engine schema files.
- External `schemas/<SCHEMA_ID>/` remains the executable schema source.
- This decision does not change denominators, `case_sets/`, reports/results, paper results, retained evidence, raw legacy evidence, official metrics, DB/checker execution authorization, or leaderboard policy.

## D026: Shared checker and validation modules for v2

Decision:

Case-local `checker/` stores configuration only:

- `checker.yaml`
- `normalization.yaml`
- `compare_config.yaml`
- `expected_rejections.yaml`

Shared checker and validation implementation belongs under `src/sql_rewrite_bench/` or shared repository scripts, not duplicated inside each case package.

Current and planned shared modules:

- `src/sql_rewrite_bench/local_result_checker.py`: existing local result comparison implementation.
- `src/sql_rewrite_bench/sql_shape_validator.py`: future shared SQL static shape validator.
- `src/sql_rewrite_bench/plan_artifact_validator.py`: future shared plan/evidence artifact validator.

Case-local `validation/run_validation.sh` and `validation/run_plan_collection.sh` are thin wrappers over shared logic. Clean v2 packages must not carry duplicated per-case implementations such as `run_engine_queries.py`, `check_results.py`, `check_sql_consistency.py`, or `check_plan_artifacts.py`; any legacy copies remain compatibility assets until shared wrappers are validated.

Reason:

The v2 conversion rulebook needs folder-ordered conversion by asset layer. Duplicating Python checker or validator implementation into each case would make conversion noisy and inconsistent, while shared modules keep execution/checking behavior auditable.

Impact:

- Future writable conversion should add or normalize case-local wrapper scripts, not copy implementation logic per case.
- Shared module creation remains separately authorized future work; this decision records the plan only.
- This decision does not authorize DB/checker execution expansion, official metrics, timing, reports/results migration, denominator changes, paper-result changes, retained-evidence updates, or leaderboard output.

## D027: Case-local runs/ reality-based v2 cleanup policy

Decision:

D005 remains valid for non-empty, uncertain, retained-evidence-present, sensitive/private, or raw-trace case-local `runs/` candidates. Those directories must not be deleted, cleared, moved, public-copied, or silently rewritten without classification, retention/archive mapping, and explicit approval.

Case package v2 cleanup may distinguish empty or placeholder-only case-local `runs/` from retained-evidence runs:

- absent `runs/` requires no cleanup;
- empty `runs/` is not retained evidence;
- placeholder-only `runs/` is not retained evidence unless the placeholder explicitly documents retained artifacts stored in that directory;
- non-empty `runs/` must be classified before deletion;
- retained-evidence-present `runs/` requires retention mapping before deletion;
- sensitive/private/local-path/raw-trace `runs/` requires private/archive mapping and must not be public-copied;
- new user-run outputs remain under top-level `runs/user/<run_id>/`, not case-local `runs/`.

Reason:

The branch-local `case_package_v2_runs_reality_audit_and_policy_update_v0` inspected 100 current case-package directories and found 99 placeholder-only case-local `runs/` directories, 1 absent `runs/` directory, and 0 retained-evidence-present, sensitive/private/raw-trace, or manual-review `runs/` directories. Treating every placeholder-only `runs/` directory as retained evidence is too broad for v2 cleanup, while D005 remains necessary for non-empty or uncertain cases.

Impact:

- A future cleanup task may delete audited empty or placeholder-only case-local `runs/` directories after policy acceptance and protected-boundary checks.
- The cleanup task must stop if any target `runs/` directory contains non-placeholder files or changes classification.
- No retained-evidence deletion, case-local evidence deletion, reports/results migration, denominator change, paper-result change, official metric computation, DB/checker execution, or leaderboard output is authorized by this decision.

## D028: Static evidence directories are not required in clean v2 public case surface

Decision:

Clean v2 case packages must not require case-local `evidence/`. Top-level `evidence/cases/<POOL>/<CASE_ID>/` is a migration-time or optional retained-artifact surface, not a required final public case surface.

If benchmark execution is runnable, evidence ledger rows should be regenerated by validation, checker, baseline, report, and result scripts under separately authorized execution/reporting tasks. The manifest should record a regeneration-first evidence policy instead of mandatory static evidence paths:

```yaml
evidence_policy:
  static_case_evidence: not_required
  regeneration_policy: regenerable_by_validation_and_report_scripts
  retained_static_artifacts: none
```

Static evidence may be omitted from the clean public release unless separately needed and explicitly authorized for paper-retained outputs. If retained static artifacts are deliberately kept, they must be represented as optional retained artifacts, not as required case-package contents.

Reason:

The v2 pilot reached clean-template-minimal case-local packages after moving through manifest, SQL, schema, checker, validation, witness, evidence, metadata, notes, runs, README/validator, and cleanup layers. The remaining top-level `evidence/cases/` package is useful as migration audit material but overstates the final public clean-template surface if treated as required. A regeneration-first policy better matches the public workbench goal: users should reproduce evidence through scripts and wrappers, while reports/results remain separately authorized paper/reporting surfaces.

Impact:

- Future validator behavior must not fail solely because `evidence_ref` is absent.
- Future clean v2 manifests should prefer `evidence_policy.static_case_evidence: not_required`.
- `evidence_ref` remains acceptable only as optional compatibility or retained-artifact metadata.
- A future writable task may update five pilot manifests/READMEs/checker/witness references and remove static evidence surfaces only after live references are removed and protected-boundary checks pass.
- This decision does not change Common-core membership, denominator values, case-set membership, reports/results authorization, paper results, official metric computation, DB/checker execution, or global leaderboard policy.

## D029: User-entry local evaluation architecture before paper reproduction

Decision:

The project will first build a modular local diagnostic user-entry harness before paper reproduction.

`src/sql_rewrite_bench/user_run.py` remains the user-entry orchestrator, not a monolithic metrics runner.

Candidate preflight, engine execution, result checking, ledger writing, quality reporting, and tag slicing are separate responsibilities.

Official metrics, paper rendering, retained-evidence updates, reports/results updates, denominator changes, paper-result changes, and leaderboard output remain unauthorized in this phase.

Reason:

The current user-entry smoke path works for non-DB adapter capture and optional PostgreSQL/checker local diagnostics, but the next practical stage needs clearer module boundaries before adding candidate preflight, local quality reports, tag-aware slices, MySQL/Spark diagnostic interfaces, or timing diagnostics.

Separating these responsibilities prevents the user-entry runner from becoming an implicit official metrics or paper reproduction path.

Impact:

- Future user-entry implementation should follow `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`.
- User-run outputs remain local diagnostics under `runs/user/{run_name}/`.
- `case_sets/common_core_v0/` remains the source of Common-core membership and denominator rows.
- Official metrics, paper table rendering, retained-evidence adapter integration, reports/results migration, denominator changes, paper-result changes, and global leaderboard creation require separate authorization.

## D030: Release-surface metadata policy decisions before skeleton implementation

Decision:

The initial public-release repository license policy is `Apache-2.0`.

Citation metadata may use safe placeholders in a future `CITATION.cff`; DOI, author order, and institutional metadata must not be invented.

Contribution policy will be conservative: external contributions may propose documentation fixes, adapter examples, and issue reports, but must not silently change Common-core membership, denominator definitions, official metrics, reports/results, retained evidence, case sets, or benchmark claims.

The current Chinese top-level README may remain on this construction branch, but an English primary README or bilingual public entrypoint is required before final VLDB/public artifact release.

Future `benchmark_spec/` skeleton files are limited to public v0 scope and must preserve Common-core v0 membership, Track A denominator, case-package benchmark unit, role-aware and denominator-aware reporting, no global leaderboard, hard-negative checker-control boundaries, no current `SpeedupTransferRate`, and verifier-support boundaries.

Future `reports/` and `results/` boundary README files may document public-release boundaries only; they must not generate, migrate, or update paper results.

No release tag or export branch is authorized yet.

Official metrics, paper rendering, retained-evidence adapter integration, reports/results updates, timing/speedup computation, and global leaderboard output remain unauthorized.

Reason:

The release-surface metadata readiness audit concluded `ready_with_policy_decisions`. Recording these decisions before skeleton implementation prevents public metadata files from silently choosing license, citation, contribution, report/result, benchmark-spec, language, or release mechanics policies.

Impact:

- A later metadata-only task may create `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `benchmark_spec/`, `reports/README.md`, and `results/README.md` only within these boundaries.
- Future citation metadata must use `TBD` or empty placeholders where final paper metadata is unavailable.
- Future contribution documentation must protect case membership, denominators, official metrics, reports/results, retained evidence, case sets, and benchmark claims from silent changes.
- Release tag/export branch creation remains deferred until final public-release closeout passes.
- This decision does not authorize metrics implementation, paper rendering, reports/results migration, denominator changes, paper-result changes, case membership changes, raw retained evidence changes, DB/checker execution, timing/speedup computation, or leaderboard creation.

## D031: PORT cross-dialect diagnostics require explicit manifest roles and fail-closed runner behavior

Decision:

PORT cross-dialect local diagnostics must be manifest-declared.

The runner must not infer source, target, or reference SQL roles from file names or SQL text.

`pos_01.sql` must not be used as a PostgreSQL source oracle unless explicitly declared by manifest metadata or a separately approved policy.

Same-engine behavior remains the default for cases without explicit cross-dialect diagnostic metadata.

MySQL source-side execution is required for MySQL-like PORT source reference diagnostics.

Spark execution remains deferred unless separately authorized.

No denominator, paper result, case membership, official metrics, reports/results, retained evidence, or leaderboard change is authorized by this decision.

Reason:

The PostgreSQL Common-core no-op local diagnostic run selected 40 rows and produced 35 exact rows, with five PORT source-execution failures: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.

The follow-up triage showed that those failures are caused by MySQL-like `sql/source.sql` files being executed directly by PostgreSQL. The failures are not schema setup failures and not rewriter-quality failures.

The current runner lacks a PORT cross-dialect diagnostic model. Silently replacing `source.sql` with `pos_01.sql` would confuse rewrite roles and could create untracked benchmark semantics. Explicit manifest roles and fail-closed behavior keep local diagnostics auditable.

Impact:

- A future manifest-role metadata design task should define the exact additive fields for PORT cross-dialect diagnostics.
- A future metadata task may add explicit PORT diagnostic role metadata only after that design is approved.
- A future runner task may consume explicit metadata only; it must not guess roles.
- A future MySQL execution backend is required before MySQL-like PORT source reference diagnostics can complete.
- Spark remains a backlog backend unless separately authorized.
- PERF, CONS, and LONGTAIL same-engine local diagnostics must remain unchanged.
- This decision does not authorize source code changes, case or manifest edits, SQL rewrites, MySQL/Spark implementation, live DB/checker execution, official metrics, timing/speedup, paper rendering, reports/results migration, denominator changes, paper-result changes, case membership changes, raw legacy evidence changes, or global leaderboard creation.

## D032: Latest paper metrics/timing phase and external skill-adapter deferral

Decision:

The project will proceed next with metrics/timing protocol alignment and performance-layer planning after completion of the user-entry local diagnostic layer.

The latest paper Table 6 is the current target for metric naming and formula alignment:

Coverage:

- Generation Rate: `|G_r| / N_S`
- Execution Coverage Rate: `|E_r| / N_S`

Correctness:

- Result Consistency Rate: `|X_r| / N_S`
- Semantic Equivalence Rate: `|V_equiv_r| / |V_equiv_r union V_non_r|`, with unknown/undecidable verifier outcomes reported separately

Performance:

- GM Speedup Ratio: `exp(|M_r|^-1 sum_{i in M_r} log s_i)`, where `s_i = t_src_i / t_rw_i`
- Speedup Ratio Percentiles: `P10`, `P25`, `P50`, `P75`, `P90` over `{s_i}_{i in M_r}`

Interpretability:

- Positive Operation Coverage Rate: `|C_r|^-1 sum_{i in C_r} (|A_hat_i| / |A_exp_i|)`

Generalization:

- Cross-Engine Execution Coverage Rate: `|E_tgt_r| / N_PORT`
- Cross-Engine Result Consistency Rate: `|X_tgt_r| / N_PORT`
- Cross-Engine GM Speedup Ratio: `exp(|M_tgt_r|^-1 sum_{i in M_tgt_r} log s_tgt_i)`

Performance metrics are exact-gated and timed-gated: speedup is only interpretable over result-consistent rows with retained paired timing.

Timing artifacts must record source/candidate paired timing in the same engine/environment/run context before metrics scripts can compute performance.

Regression@20 remains a reporting diagnostic / open question unless separately confirmed as a formal metric in the latest paper contract.

Positive Operation Coverage Rate is not implemented now. It is deferred as an external-skill-adapter integration line.

The project will wait for the collaborator's external script and operation-atom schema before creating or populating case-local `skill/` folders.

No operation atoms may be inferred from taxonomy tags, SQL text, or `positive.sql` automatically in the current phase.

No `cases/<POOL>/<CASE_ID>/skill/` directories should be created until the external script schema and integration contract are reviewed and authorized.

Future skill integration should be case-local and explicit, likely through files such as:

- `skill/operation_atoms.yaml`
- `skill/semantic_guard_atoms.yaml`
- `skill/skill_definition.md`
- `skill/positive_reference_mapping.yaml`

Exact file names and schema remain pending external-script review.

The next implementation sequence should be:

1. latest paper metrics/timing protocol alignment audit
2. timing artifact schema design
3. exact-gated local timing diagnostic implementation
4. non-official local metrics calculator for Coverage/Correctness/Performance/Generalization
5. external skill-adapter integration for POCR after collaborator script is ready
6. retained-evidence adapter / official metrics promotion
7. paper table renderer

These phases must remain separately authorized.

Reason:

User-entry local diagnostic is now sufficiently complete to support a transition toward metrics/timing planning: adapter entry, candidate capture, candidate preflight, PostgreSQL/MySQL/Spark local execution, `local_result_checker`, failure buckets, quality summary, tag slices, label-only mismatch diagnostics, and strict-label policy documentation are in place.

The latest paper metric table differs from the older repository Metrics Contract v1, especially replacing Attribution Coverage with Positive Operation Coverage Rate and replacing Speedup Retention with Cross-Engine GM Speedup Ratio.

POCR requires curated operation atoms and Stage A / Stage B evidence validation. Implementing it without the collaborator's script risks schema drift and unverifiable operation-atom definitions.

Separating timing/metrics infrastructure from POCR integration avoids blocking exact-gated performance work while protecting the interpretability metric from premature implementation.

The benchmark's core reporting policy requires role-aware and denominator-aware results, no global leaderboard, and performance interpretation only on exact + timed rows.

Impact:

- Metrics/timing protocol alignment is authorized as an audit/design next step.
- Timing implementation remains unauthorized until a separate timing artifact schema and protocol task is approved.
- Metrics computation remains unauthorized until a separate metrics implementation task is approved.
- POCR implementation is explicitly deferred.
- `skill/` folder creation/population is explicitly deferred.
- Existing user-entry local diagnostic outputs remain local-only and must not be promoted to retained evidence without a separate policy task.
- No denominator, case membership, paper result, reports/results, raw retained evidence, official metrics, leaderboard, release/export/tag, or case package layout changes are authorized by this decision.
- D018 remains historical context for the older formalized metrics contract; this decision records the latest-paper alignment direction and the need for a follow-up metrics contract delta/audit before implementation.

## D033: Local metrics v0 formula and boundary decision

Decision:

The first non-official local metrics calculator v0 may implement Coverage, Result Consistency, and Performance summaries over local diagnostic runs only. It remains local-only and must not compute official metrics, update reports/results, promote retained evidence, render paper tables, or create leaderboard output.

Regression@20 is removed from the new formal local metrics v0 implementation scope. It may remain a legacy or reporting diagnostic only.

Coverage formulas for local metrics v0 are:

- Generation Rate: `candidate_generated / selected`.
- Execution Coverage Rate: `candidate_executable / selected`.

`preflight_passed` remains a funnel diagnostic and is not part of the Generation Rate numerator.

`source_executable` remains recorded as a diagnostic/environment guard and is not a numerator condition for Execution Coverage Rate.

Correctness formula for local metrics v0:

- Result Consistency Rate: `exact / selected`.

Semantic Equivalence Rate is `N.A.` unless formal verifier evidence exists. The local result checker must not be substituted for formal semantic equivalence verification.

Performance formulas for local metrics v0 are:

- GM Speedup Ratio over strict exact + timed rows only.
- Speedup Ratio Percentiles over strict exact + timed rows only.

Under the current strict-label policy, `label_only_mismatch` remains a mismatch and remains timing-ineligible.

Cross-Engine GM Speedup Ratio replaces old Speedup Retention in the latest-paper alignment, but it is `N.A.` unless target-engine paired timing exists.

Positive Operation Coverage Rate remains deferred pending the collaborator's external skill script and stable `skill/` schema. No `skill/` folders or operation atoms should be created now.

Reason:

D032 authorized metrics/timing protocol alignment as the next project line, while keeping metrics computation and official outputs separately gated. The latest-paper alignment audit and timing schema review now provide enough local diagnostic infrastructure to define v0 local metrics formulas before implementation.

The formula decisions keep local diagnostic summaries aligned with the latest-paper direction while avoiding older or ambiguous repository contract behavior:

- Regression@20 is not part of latest Table 6 and should not enter the formal v0 local metrics calculator.
- Candidate generation should mean raw adapter candidate emission, not preflight readiness.
- Candidate execution success should drive Execution Coverage Rate, while source execution remains an environment guard.
- Result consistency stays denominator-aware over selected rows.
- Semantic equivalence requires verifier evidence and is not the same as local result consistency.
- Performance interpretation remains exact-gated and timed-gated.
- Cross-engine performance requires target-engine paired timing and must not reuse same-engine timing.
- POCR requires explicit operation atoms and remains unsafe to implement before the external skill-adapter contract is stable.

Impact:

- A future local metrics calculator v0 may be implemented for non-official local diagnostic summaries of Coverage, Result Consistency, and Performance.
- The calculator must be route-aware, method-aware, engine-aware, denominator-aware, timing-policy-aware, and local-only.
- `preflight_passed`, `source_executable`, label-only diagnostics, N.A. counts, unsupported/fail-closed counts, and failure buckets should remain visible diagnostics.
- Semantic Equivalence Rate, Cross-Engine GM Speedup Ratio, and POCR must report `N.A.` unless their required evidence exists.
- Metrics calculator implementation remains unauthorized until a separate implementation task is approved.
- Official metrics computation, reports/results updates, retained-evidence promotion, paper table rendering, leaderboard output, denominator changes, case membership changes, raw retained evidence changes, skill folders, and operation atoms remain unauthorized by this decision.

## D034: Project-control hygiene and next-phase execution order

Decision:

`project_control/` is reserved for durable control state, not one-off working plans.

Active control state should live in:

- `MIGRATION_MASTER_PLAN.md` for stable global migration rules;
- `MIGRATION_STATUS.md` for current snapshot and next safe action;
- `MIGRATION_RUN_LOG.md` for chronological execution history;
- `DECISION_LOG.md` for durable policy and roadmap decisions.

Completed or superseded planning files should be archived under audit packets, not left as active top-level `project_control/` files.

Future one-off plans should usually live under `audits/<task_name>/`, not as new top-level `project_control/` plan files.

The approved next-phase roadmap after local evaluation workbench v0 closeout is:

0. Project-control hygiene and roadmap reset.
1. Define the `output/` run-output contract and user-facing CLI/interface contract. The intended user-facing shape is:

```text
output/<run_id>/
  results/
  logs/
  reports/
```

`output/` is local/user-run output and must remain distinct from top-level `reports/` and `results/` official/paper surfaces.

2. Implement a user-facing entry facade so users do not need to call internal `src/sql_rewrite_bench/` modules directly. A thin interface may live under `src/user/` or an equivalent public CLI wrapper, while `src/sql_rewrite_bench/` remains the internal implementation package.
3. Promote failure bucket summaries and tag-slice summaries into the user output report surface:

- `output/<run_id>/results/failure_buckets.csv`
- `output/<run_id>/results/tag_slices.csv`
- `output/<run_id>/reports/failure_buckets.md`
- `output/<run_id>/reports/tag_slices.md`

4. Integrate verifier support for both VeriEQL and SQLSolver. This is a support/verifier layer, not a rewrite baseline. It should support Semantic Equivalence Rate only when formal verifier evidence exists. Without verifier evidence, Semantic Equivalence Rate remains `N.A.`. Verifier outputs should remain separate from method-generated candidate failures and hard-negative checker controls.
5. Run or prepare other baseline routes on Common-core v0 using the local workbench:

- SQLGlot noop;
- SQLGlot optimize;
- Calcite HEP fail-closed;
- Direct LLM;
- Direct LLM + Repair-1;
- portability routes such as SQLGlot Transpile and LLM Translate where applicable.

Each route must remain route-aware and denominator-aware. Routes must not be merged into a global leaderboard.

6. Broaden local exact-gated timing and non-official local metrics only after the output contract and baseline/verifier interfaces are stable.
7. Design official evidence promotion, retained-evidence integration, reports/results outputs, and paper table rendering only after local runs and verifier/baseline routes are stable.

Legacy evidence policy:

- New-repo clean evidence is preferred.
- Legacy/old-repo retained evidence is an emergency fallback only, for example if new-repo experiments cannot complete before a submission deadline.
- Legacy evidence must not be silently mixed into new official results.
- Any legacy evidence use requires retention mapping, denominator mapping, route identity mapping, environment/provenance notes, and explicit claim boundaries.

POCR and skill policy:

- Positive Operation Coverage Rate remains deferred pending the collaborator's external skill script and operation-atom schema.
- Do not create `skill/` folders now.
- Do not infer operation atoms from taxonomy tags, SQL text, or `positive.sql`.
- Future skill integration must be separately authorized.

Output/reporting boundary:

- `output/<run_id>/` is for local/user-run outputs.
- top-level `reports/` and `results/` are official/paper/release-facing surfaces and must not be updated by user-run tasks unless separately authorized.
- local metrics are not official metrics.
- local timing artifacts are not retained evidence.
- no leaderboard output is allowed.

Reason:

Local evaluation workbench v0 is closed for the current phase. The repository now has user-entry diagnostics, tri-engine local execution for supported roles, strict-label diagnostics, exact-gated local timing, and a non-official local metrics calculator. The next implementation phase needs a clean project-control surface and a durable execution order before adding user-facing output contracts, public entry points, verifier support, more baseline routes, or official evidence promotion design.

Archiving completed and superseded top-level project-control plans prevents stale working plans from competing with the active control files. Keeping the roadmap in `DECISION_LOG.md` makes the next sequence durable without modifying `MIGRATION_MASTER_PLAN.md`.

Impact:

- Top-level `project_control/` should contain only the four active control files unless a future file is explicitly justified as active.
- Completed or superseded planning files may be archived under audit packets with manifest entries.
- Step 1 output-contract design is the next safe implementation-planning step.
- VeriEQL and SQLSolver are included in the roadmap as verifier/support integrations, not rewrite baselines.
- Official metrics, timing broadening, retained-evidence promotion, reports/results updates, paper rendering, POCR, skill folders, operation atoms, leaderboard output, release/export/tag creation, denominator changes, case membership changes, paper-result changes, and raw retained evidence changes remain separately gated.

## D035: Final public repository layout target and delayed physical migration

Decision:

The team-approved final external/public repository layout target is:

```text
.github/
benchmarks/
  cases/
  case_sets/
  schemas/
  inventory/
baselines/
docs/
  guide/
  spec/
  templates/
examples/
output/
  results/
  logs/
  reports/
src/
  sql_rewrite_bench/
  cli/
  dev/
CITATION.cff
CONTRIBUTING.md
LICENSE
README.md
pyproject.toml
```

The final layout uses:

- `benchmarks/` for cases, case sets, schemas, and inventory;
- `baselines/` for baseline adapters and routes;
- `docs/guide`, `docs/spec`, and `docs/templates` for documentation;
- `examples/` for adapter examples and minimal runnable samples;
- `output/results`, `output/logs`, and `output/reports` for user-run outputs;
- `src/sql_rewrite_bench` for core implementation;
- `src/cli` for the user-facing CLI/facade;
- `src/dev` for development and validation tools.

This layout is the target external/public layout. Immediate physical migration is not authorized.

Current working paths remain valid until a separate layout migration or export-layout restructuring task is authorized.

Future output contract and CLI contract work must align with the new layout.

Future user-run output should use:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

instead of `output/<run_id>/...`.

`src/cli` is the preferred public-facing entry/facade location.

`src/sql_rewrite_bench` remains the internal implementation package.

Physical migration of `cases/`, `case_sets/`, `schemas/`, and `inventory/` into `benchmarks/` must be delayed until path resolvers, tests, validators, docs, and case-set references are ready.

No denominator, case membership, paper results, reports/results official surfaces, retained evidence, timing, metrics, or leaderboard output is changed by this decision.

Legacy retained evidence and `runs/` remain protected by existing retention rules.

Reason:

The final layout affects output and CLI contracts, so it must be recorded before Step 1 of D034 proceeds.

Moving repository directories now would risk breaking case resolution, validators, scripts, audits, and existing Common-core denominator references.

Recording the target now prevents new output and CLI work from being designed around an obsolete layout.

Impact:

- D034 remains valid, but Step 1 must use `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
- Future Step 2 should implement the public CLI facade under `src/cli`, not `src/user`.
- Later physical layout migration or export restructuring must be separately planned and validated.
- Existing local evaluation workbench v0 remains closed and unchanged.
- No physical directory migration, output writer, CLI implementation, verifier implementation, timing, metrics, reports/results update, retained-evidence promotion, paper rendering, leaderboard, denominator change, case membership change, or paper result change is authorized.

## D036: Common-core root-level skills.md is the future POCR atom contract

Decision:

The collaborator-provided Common-core POCR skill contract has arrived and is adopted as case-local root-level `skills.md` files for Common-core v0 cases:

```text
cases/<POOL>/<CASE_ID>/skills.md
```

Common-core v0 uses these root-level `skills.md` files as the official operation-atom and semantic-guard contract for future Positive Operation Coverage Rate work.

No `skill/` directory is created.

Future POCR operation atoms must come from `skills.md`, not from taxonomy labels, SQL-shape inference, positive-control inference, or ad hoc candidate analysis.

This decision records the contract and import boundary only. It does not compute Positive Operation Coverage Rate and does not promote paper-facing metrics.

Reason:

The benchmark needs an explicit, collaborator-reviewed operation-atom and semantic-guard source before any POCR parser, adapter, or user-facing facade can be implemented. Root-level `skills.md` keeps the contract case-local and easy to audit without introducing a nested `skill/` artifact surface.

Impact:

- Future no-API POCR parsing work should read `cases/<POOL>/<CASE_ID>/skills.md`.
- Operation atoms and semantic guard atoms are authoritative only when sourced from `skills.md`.
- Taxonomy tags and SQL/positive-control comparisons remain diagnostic/support context, not POCR atom sources.
- Importing `skills.md` does not change denominators, case membership, paper results, retained evidence, official metrics, or leaderboard policy.
- POCR computation, parser implementation, adapter implementation, user-facing facade integration, and paper-metric promotion remain separately gated.
