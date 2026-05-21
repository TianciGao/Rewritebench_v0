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

## 查看 case 和输出 schema

在运行 adapter 之前，可以先查看受控 case-set、解释本次选择，或查看本地输出 schema：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --list-cases
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --explain-selection
PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema
```

这些命令只读取 case-set metadata 或打印本地输出说明，不调用 adapter，不创建 `runs/user/...` 输出，不执行 DB/checker，也不计算官方指标。

## 用户算法适配器

- runner 通过环境变量把 source SQL 路径、case 信息和 candidate 输出路径传给 adapter。
- adapter 写出 candidate SQL，或把 candidate SQL 打印到 stdout。
- 示例 adapter 位于 `examples/user/noop_adapter.py`。
- adapter capture 只记录候选输出，不代表语义正确、性能提升或官方结果。

## 运行后看哪里

默认 smoke 会把本地诊断输出写到 `runs/user/{run_name}/`。常用文件包括：

- `selected_cases.csv`：本次选择的 case-engine rows。
- `candidate_sql/`：adapter 捕获到的 candidate SQL。
- `ledger.csv`：本地诊断 ledger，不是官方 metrics。
- `summary.json`：本地运行摘要。
- `report.md`：本地报告，不是 paper table。

更完整的数据流和文件位置见 [`docs/USER_ENTRY_DATA_FLOW.md`](docs/USER_ENTRY_DATA_FLOW.md)。

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
