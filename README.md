# SQL-RewriteBench

SQL-RewriteBench 是一个面向 statement-level SQL rewrite 的 benchmark / workbench。它评估的是方法最终输出的完整 SQL 语句，而不是优化器内部 AST、规则 trace，或仅 parser-level 的转换结果。

## 当前公开范围

- 当前主公开分母是 `Common-core v0`。
- `Common-core v0` 包含 40 个 `case package`。
- Pool split: 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL。
- `Track A` same-engine evaluation 展开到 `PostgreSQL` / `MySQL` / `Spark SQL`，共 120 planned rows。
- `case package` 是 benchmark unit。
- 结果解释必须 role-aware 和 denominator-aware。

## 快速 smoke run

这是安全的用户入口 smoke。默认是 non-DB 路径，使用 `--smoke` 选择一个很小的确定性子集，调用 `examples/user/noop_adapter.py`，并把输出写入 `runs/user/...`。该 smoke 不执行 DB query，不运行 checker，不计算官方指标，不更新 paper results，也不生成 leaderboard。

Dry-run smoke:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/smoke_dry_run \
  --dry-run
```

Adapter-capture smoke:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/smoke_dummy_adapter
```

## 用户算法适配器

- runner 通过环境变量把 source SQL 路径、case 信息和 candidate 输出路径传给 adapter。
- adapter 写出 candidate SQL，或把 candidate SQL 打印到 stdout。
- 示例 adapter 位于 `examples/user/noop_adapter.py`。
- adapter capture 只记录候选输出，不代表语义正确、性能提升或官方结果。

## 用户入口数据流与文件位置

```text
CLI -> case_sets/common_core_v0 -> cases/<POOL>/<CASE_ID>/sql/source.sql -> adapter -> runs/user/<run_name>/candidate_sql -> ledger/summary/report
```

| 阶段 | 文件或目录 | 作用 |
|---|---|---|
| 主 CLI 入口 | `src/sql_rewrite_bench/user_run.py` | `python -m sql_rewrite_bench.user_run` 的实现入口。 |
| 薄 wrapper | `scripts/user/run_user_benchmark.py` | 从仓库根目录补充 `src/` import path 后调用同一个 CLI。 |
| case selection implementation | `src/sql_rewrite_bench/case_selection.py` | 从 metadata 解析 `Common-core v0` 选择，不通过扫描目录决定 membership。 |
| case-set metadata | `case_sets/common_core_v0/cases.csv` | 定义 40 个 Common-core case package 及 package path。 |
| Track A denominator metadata | `case_sets/common_core_v0/denominator_same_engine_120.csv` | 定义 120 个 planned same-engine case-engine rows。 |
| case package root | `cases/<POOL>/<CASE_ID>/` | 单个 benchmark unit 的 package 根目录。 |
| source SQL passed to adapter | `cases/<POOL>/<CASE_ID>/sql/source.sql` | 通过 `SQLRB_SOURCE_SQL_PATH` 传给 adapter。 |
| package manifest | `cases/<POOL>/<CASE_ID>/manifest.yaml` | 记录 package manifest、provenance、SQL、schema、checker 和 validation references。 |
| schema profile | `cases/<POOL>/<CASE_ID>/schema/schema_profile.yaml` | case-facing schema summary；不是用户输出目录。 |
| external schema package | `schemas/<schema_id>/...` | PostgreSQL DDL/load 从 `schema.external_profile` 和 external profile metadata 解析；不要硬编码固定 schema 文件名。 |
| public example adapter | `examples/user/noop_adapter.py` | 公开 smoke 示例；读取 source SQL 并写出相同 candidate SQL。 |
| adapter environment | `SQLRB_SOURCE_SQL_PATH`, `SQLRB_CANDIDATE_SQL_PATH`, `SQLRB_WORKSPACE_DIR` | adapter 从 source path 读取 SQL，把 candidate 写到 candidate path，并可使用 per-row workspace。 |
| output root | `runs/user/<run_name>/` | 当前用户运行的本地输出根目录。 |
| selected rows | `runs/user/<run_name>/selected_cases.csv` | 记录本次选择出的 case-engine rows。 |
| run config | `runs/user/<run_name>/config.yaml` | 记录 CLI 参数、scope 和边界标记。 |
| candidate SQL capture | `runs/user/<run_name>/candidate_sql/` | 保存 adapter 捕获到的 candidate SQL。 |
| adapter workspaces | `runs/user/<run_name>/workspaces/` | 保存 per-row adapter stdout/stderr 和 workspace 文件。 |
| local diagnostic ledger | `runs/user/<run_name>/ledger.csv` | 本地诊断 ledger；不是官方 metrics 输入。 |
| local summary | `runs/user/<run_name>/summary.json` | 本地诊断计数和边界标记。 |
| local failures | `runs/user/<run_name>/failures.csv` | 记录非 `none` failure bucket rows。 |
| local report | `runs/user/<run_name>/report.md` | 本地运行摘要；不是 paper table。 |
| optional PostgreSQL diagnostic helper | `src/sql_rewrite_bench/postgres_execution.py` | opt-in DB diagnostic helper；默认 smoke 不使用。 |
| optional checker helper | `src/sql_rewrite_bench/local_result_checker.py` | opt-in local checker diagnostic helper；默认 smoke 不使用。 |
| output schema / typed row model | `src/sql_rewrite_bench/user_run_schema.py` | 定义 local ledger/status 字段和值域。 |

`runs/user/<run_name>/...` 输出只是本地 diagnostics：不是官方 metrics，不是 paper tables，不更新 `reports/` 或 `results/`，不是 retained evidence，也不会创建 leaderboard。默认 smoke 不执行 DB queries，也不运行 checkers；PostgreSQL/checker diagnostics 必须显式 opt-in，且仍然只是本地诊断。

## 可选本地 PostgreSQL 诊断

- 可选 DB/checker diagnostics 是 opt-in。
- 使用 `--enable-db-execution` 和可选 `--enable-checker`。
- 当前路径是 external-schema aware：PostgreSQL DDL/load 通过 `manifest.yaml` 中的 `schema.external_profile` 解析。
- 这是本地诊断，不是完整论文复现，不是官方 metrics，不写 `reports/` 或 `results/`。

## 如何阅读一个 case package

一个 `case package` 通常包含：

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- `sql/pos_01.sql`
- `sql/neg_01.sql` when declared
- `schema/schema_profile.yaml`
- `checker/`
- `validation/`

`manifest.yaml` 是 package manifest，记录 source-family、provenance、taxonomy、SQL 路径、schema profile、checker、validation entrypoint 和证据策略等信息。`Common-core v0` membership 由 `case_sets/` 管理，而不是由物理目录或 case README 单独定义。

## 仓库主要目录

- `cases/`: case packages。
- `case_sets/`: 受控 case membership、denominator 和 control scaffolds。
- `schemas/`: external schema profiles 与 engine-specific DDL/load assets。
- `src/`: Python package implementation。
- `scripts/`: developer/user entry scripts。
- `examples/`: public examples, including user adapter smoke examples。
- `docs/`: user-facing and maintainer-facing documentation。
- `audits/`: release-construction audit packets and planning records。
- `project_control/`: release construction status and decision control files。
- `runs/`: local/user output or retained legacy evidence depending on location and policy。

新的用户运行输出应写入顶层 `runs/user/...`。除非有明确文档说明，不要提交本地 run outputs。

## 重要边界

- `Common-core v0` 是受控覆盖面，不是生产 SQL 频率样本。
- hard negatives 是 checker controls，不是 method-generated candidates。
- performance 只能在 exact + timed rows 上解释。
- PORT bounded evidence 不能写成 full PORT9 closure。
- `SpeedupTransferRate` 当前不计算。
- verifier support 不是 rewrite-generation baseline。
- 本仓库不提供全局 leaderboard。
- user smoke outputs 只是本地 diagnostics。
- `PERF_0077` 和 `PERF_0082` 保留 nonblocking source-path provenance uncertainty；不要声称恢复了 exact JOB source paths。

## 更多文档

- [User benchmark guide](docs/USER_BENCHMARK_GUIDE.md)
- [Common-core v0 case set](case_sets/common_core_v0/)
- [Project control](project_control/)
