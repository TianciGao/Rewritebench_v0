# SQL-RewriteBench Clean Public Release 迁移总体计划

版本：v0.1
旧仓库：sql-rewrite-bench-artifact-clean
发布仓：Rewritebench_v0
状态：底层指导文件
最后更新：TBD

## 1. 迁移目标

本项目不是简单重排旧仓库目录，而是将旧仓库 `sql-rewrite-bench-artifact-clean` 中的 SQL-RewriteBench 研究原型，迁移为一个干净、可公开、可复现、可验证、与论文口径一致的 public release / benchmark workbench。

迁移目标包括：

1. 保持论文口径不变；
2. 保持 Common-core v0 分母不变；
3. 保留 retained evidence；
4. 保证 case package 可验证；
5. 建立用户和审稿人可运行的复现路径；
6. 清理内部开发痕迹、敏感路径、临时 runs；
7. 对全部 case universe 做治理，但 public release v0 优先发布 Common-core 40。

## 2. 论文口径锁定

迁移过程中不得改变以下事实：

- case package 是 benchmark unit，不是裸 SQL；
- Common-core v0 = 40 cases；
- Pool split = 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL；
- Track A same-engine denominator = 40 cases × 3 engines = 120 planned rows；
- results are role-aware and denominator-aware；
- no global leaderboard；
- performance 只能在 exact + timed rows 上解释；
- hard negatives 是 checker controls，不是 method-generated failures；
- PORT bounded evidence 不能写成 full PORT9；
- SpeedupTransferRate 当前不计算；
- verifier support 不是 rewrite-generation baseline；
- case-local runs/ 需要按内容分类；empty/placeholder-only 不是 retained evidence，non-empty/uncertain runs/ 不能无 retention/archive mapping 删除。

## 3. 已知 legacy facts

已完成的只读审计显示：

- `cases/` 下检测到 197 个 case-like directories；
- registry 语境曾提到 190 个 registered case packages，因此需要 reconciliation；
- pool 数量为 PERF 105、CONS 40、PORT 28、LONGTAIL 24；
- 所有 detected case directories 都有 manifest；
- 最新 runs/ 审计显示 184 个 case packages with runs/；
- Common-core 40 全部有 runs/；
- runs/ 分类为：
  - 162 个 retain_in_case_as_minimal_evidence；
  - 21 个 manual_review_required；
  - 14 个 regenerable_by_external_runner；
- Common-core 40 contract-fit 审计显示：
  - 28 个需要 phase_2_add_evidence_index；
  - 5 个适合 phase_3_representative_physical_pilot；
  - 7 个 defer_manual_review；
  - 0 个可 manifest-only normalization；
  - 40 个如果完全变成目标 layout 都需要 physical move。

## 4. 迁移总策略

迁移顺序：

1. 确认旧仓库和新发布仓工作区；
2. 建立项目控制文件；
3. 做必要的只读审计补齐；
4. 设计 public release layout；
5. 挑代表性 case 做模板；
6. 做 copy-first pilot；
7. 迁移 Common-core 40；
8. 对全部 197 case-like packages 建治理索引；
9. 整理用户脚本和复现脚本；
10. 从 retained evidence 重新生成论文主表；
11. 做 public hygiene；
12. 发布 public release v0；
13. post-release 再扩展 non-common-core cases。

## 5. 目标 public release layout 标记

标记说明：

- [MUST] v1 公开版必须有；
- [SHOULD] 强烈建议有；
- [OPTIONAL] 可选；
- [LOCAL] 本地运行产物，不应提交；
- [DEFER] 暂缓；
- [PRIVATE] 内部协作、AI agent、prompt、scratch，不进公开版。

目标顶层结构：

```text
sql-rewrite-bench/
  README.md                         [MUST]
  LICENSE                           [MUST]
  .gitignore                        [MUST]
  CITATION.cff                      [SHOULD]
  CONTRIBUTING.md                   [SHOULD]
  pyproject.toml                    [SHOULD]
  Makefile                          [OPTIONAL]

  benchmark_spec/                   [MUST]
  taxonomy/                         [MUST]
  inventory/                        [MUST]
  case_sets/                        [MUST]
  cases/                            [MUST]
  scripts/                          [MUST]
  docs/                             [MUST]
  reports/                          [MUST]
  results/                          [SHOULD]
  baselines/                        [SHOULD]
  tests/                            [SHOULD]
  src/                              [SHOULD]

  runs/                             [LOCAL]
  repository_spec/                  [SHOULD]
  .github/                          [SHOULD]
```

## 6. case package 目标原则

case package v1 的目标结构可以逐步靠近：

```text
cases/<POOL>/<CASE_ID>/
  README.md
  manifest.yaml
  sql/
  schema/
  data/
  checker/
  validation/
  evidence/
  metadata/
  notes/
  runs/
```

其中：

manifest.yaml 是主索引；
case-local runs/ 需要按内容分类；
empty 或 placeholder-only runs/ 不是 retained evidence；
non-empty 或不确定 runs/ 在没有 retention mapping 前继续按 legacy retained evidence 保护；
evidence/runs_retention.yaml 用于解释 retained 或 archived runs 状态；
新运行输出不再写入 case-local runs/；
Common-core membership 由 case_sets/ 控制，不通过物理目录复制 case。

## 6A. Case package v2 target addendum

case package v1 was the prior migration target and remains compatibility context. Case package v2 is the new branch-adoption target on:

`feature/case-package-v2-external-schema`

v2 is not merged to `main` until the branch pilot, validator compatibility, and runner compatibility are explicitly approved.

v2 does not change Common-core membership, denominators, paper results, reports/results, retained evidence, or no-global-leaderboard policy.

Target v2 case-local structure:

```text
cases/<POOL>/<CASE_ID>/
  README.md
  manifest.yaml
  sql/source.sql
  sql/pos_01.sql
  sql/neg_01.sql
  schema/schema_profile.yaml
  checker/
  validation/
  runs/  # optional compatibility only; empty/placeholder-only is not retained evidence
```

Case-local `schema/` remains in clean v2 only for `schema/schema_profile.yaml`. This file is a case-facing schema profile and summary, not executable DDL or load data. It records the `schema_id`, external schema profile linkage, source family, relevant tables, columns, column types, primary keys, foreign keys, dialect differences, fixture/data notes when needed, and engine support summary.

External schema structure:

```text
schemas/<SCHEMA_ID>/
  schema_profile.yaml
  postgres/ddl.sql
  postgres/load.sql
  mysql/ddl.sql
  mysql/load.sql
  spark/ddl.sql
  spark/load.sql
```

External evidence structure:

```text
evidence/cases/<POOL>/<CASE_ID>/
  package_validation_summary.json
  runs_retention.yaml
  retained_controls/
  hard_negative/
  plans/
```

Manifest reference policy:

- `schema_ref` points from a case manifest to reusable `schemas/<SCHEMA_ID>/` executable DDL/load assets and becomes the source of truth after validator and runner compatibility are implemented.
- The case manifest also references case-local `schema/schema_profile.yaml`; that profile links back to the external schema profile and executable DDL/load paths.
- `evidence_ref` points from a case manifest to external case evidence under `evidence/cases/<POOL>/<CASE_ID>/`.
- `sql.source`, `sql.positives`, and `sql.negatives` point to direct case-local SQL files under `sql/`.
- Checker paths remain case-local by default under `checker/`.
- Validation entrypoints converge to `validation/run_validation.sh` and `validation/run_plan_collection.sh`.

Folder-ordered v2 conversion sequence:

`manifest -> sql -> schema -> checker -> validation -> witness -> evidence -> metadata -> notes -> runs -> README/validator`

1. `manifest`: normalize canonical v2 references and compatibility blocks first.
2. `sql`: create direct `sql/source.sql`, `sql/pos_01.sql`, and `sql/neg_01.sql` paths.
3. `schema`: create/update case-local `schema/schema_profile.yaml` and external `schemas/<SCHEMA_ID>/<engine>/ddl.sql` and `load.sql` references.
4. `checker`: retain case-local checker configuration only.
5. `validation`: add thin `run_validation.sh` and `run_plan_collection.sh` wrappers.
6. `witness`: record source-as-oracle and optional/generated witness policy.
7. `evidence`: add copy-first `evidence_ref` plans without deleting retained evidence.
8. `metadata`: merge stable governance metadata into manifest or compatibility blocks.
9. `notes`: classify notes for README, manifest notes, or external evidence notes.
10. `runs`: classify case-local runs as legacy retained evidence; never write new outputs there.
11. `README/validator`: update package documentation and run static validator checks after the structural layers are stable.

Runtime witness/source-as-oracle policy:

- User-run DB/checker execution should default to comparing runtime source SQL results against candidate SQL results.
- `data_profile.yaml` is optional, generated, or external.
- `correct_result.csv` is optional and not required for runtime checker execution when source-as-oracle execution is available.
- Missing static witness files must fail closed only when source execution or checker configuration is unavailable.

Artifact boundary policy:

- `runs/user/<run_id>/` is local user-run output only. It is not retained paper evidence, not `results/retained/`, and not a leaderboard input.
- case-local `runs/` must be classified by content. Empty or placeholder-only case-local `runs/` is not retained evidence; non-empty, uncertain, retained-evidence-present, sensitive/private, or raw-trace `runs/` remains protected and must not receive new user-run output.
- `results/retained/` is a curated retained-evidence/reporting surface only after separate authorization.
- `evidence/cases/` is retained case evidence/reference material, not user-run output and not paper table output.

Branch-only adoption roadmap:

1. Record v2 master plan and repository specs on `feature/case-package-v2-external-schema`.
2. Implement non-destructive validator and runner compatibility for `schema_ref` and `evidence_ref`.
3. Recheck `PERF_0006` without modifying additional cases.
4. Expand branch-only pilot to `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` if authorized.
5. Plan Common-core 40 conversion only after validator/runner compatibility and pilot review pass.
6. Externalize evidence copy-first and keep compatibility mappings.
7. Clean up case-local compatibility assets only after explicit retention mapping and approval.
8. Align the clean public export surface after v2 package boundaries are stable.

## 7. runs/ 政策

case-local runs/ 在迁移期必须按内容分类，而不是自动视为 retained evidence。

当前 v2 branch reality audit 显示：current release branch 中大多数 case-local runs/ 只是 README placeholder，未包含 retained evidence payload。因此 v2 cleanup policy 区分：

- absent runs/: 无需 cleanup；
- empty runs/: 不是 retained evidence；
- placeholder-only runs/: 不是 retained evidence，除非 placeholder 明确说明 retained artifacts 存在于该目录内；
- non-empty runs/: 删除前必须分类；
- retained-evidence-present runs/: 删除前必须有 retention mapping；
- sensitive/private/local-path/raw-trace runs/: 不得 public-copy，需要 private/archive mapping；
- manual-review runs/: 人工复核前不得删除。

D005 仍适用于 non-empty、uncertain、retained-evidence-present、sensitive/private/raw-trace runs candidates。

没有 retention mapping 前，不允许：

删除 non-empty/uncertain retained-evidence runs/；
清空 non-empty/uncertain retained-evidence runs/；
批量移动 non-empty/uncertain retained-evidence runs/；
全部外迁 non-empty/uncertain retained-evidence runs/；
静默改写 non-empty/uncertain retained-evidence runs/；
隐藏 failed / unsupported / mismatch / timing-missing evidence。

每个迁移后的 case 应逐步增加：

evidence/runs_retention.yaml

用于记录：

retained control evidence；
retained plan evidence；
hard-negative evidence；
method/baseline output；
regenerable run output；
manual-review risk；
do-not-delete files。

## 8. 代表性 case 策略

先做代表性 case，不直接全量迁移。

建议 physical pilot：

PERF_0006；
CONS_0005；
PORT_0003；
LONGTAIL_0011；
LONGTAIL_0022。

建议 evidence-index 对照样本：

PERF_0007；
CONS_0007；
PORT_0005。

暂缓 manual-review PORT cases：

PORT_0004；
PORT_0008；
PORT_0012；
PORT_0013；
PORT_0022；
PORT_0024；
PORT_0025。

## 9. 迁移阶段

| Phase | 名称 | 目标 |
|---|---|---|
| 0 | 确认旧仓库与发布仓工作区 | 确认路径、分支、remote、status |
| 1 | 整体情况审计 | 审计顶层、case universe、scripts、reports |
| 2 | 代表性 case 选择与模板设计 | 选模板 case，定义 case package v1 |
| 3 | case package template v1 | 确定 required / optional / legacy-allowed |
| 4 | pilot migration | copy-first 试迁代表性 case |
| 5 | Common-core 40 migration | 迁移 public v0 主分母 |
| 6 | whole-case universe governance | 对 197 case-like packages 建索引和 backlog |
| 7 | script and reproduction path | 建用户脚本、复现脚本、metrics 脚本 |
| 8 | results and metrics closure | 从 retained evidence 重新生成论文主表 |
| 9 | public hygiene | 清理敏感痕迹和内部残留 |
| 10 | release v0 | 发布干净 public release |
| 11 | post-release backlog | 扩展 non-common-core cases 和更多功能 |

## 10. 执行纪律

不在旧仓库做大规模重排；
所有实际迁移在 clean worktree 或发布仓完成；
不使用 git add .；
不删除 runs/；
不改变 denominator；
不改变论文结果；
不合并 route；
不建立 global leaderboard；
Codex 每次写操作前必须说明将修改哪些文件；
Codex 每次完成后必须输出 git status 和 git diff 摘要。
