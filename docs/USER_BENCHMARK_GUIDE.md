# SQL-RewriteBench 用户基准测试指南

本指南覆盖当前 B 线用户入口界面。当前受支持的公开 smoke/default 路径是一个非数据库的 adapter-capture runner：它允许用户在选定的 Common-core v0 case-engine 行上运行 SQL rewrite adapter，并将本地实验输出保存到 `runs/user/<run_id>/` 下。可选的 PostgreSQL 诊断在下文单独说明。

默认公开路径不会对完整 benchmark run 进行打分。它不会执行 SQL、运行 checkers、收集计时、计算官方指标、更新论文结果、更新 retained evidence，也不会创建 leaderboard。

## 安装与导入

本地开发时，请使用仓库根目录作为工作目录。

使用可编辑安装：

```bash
python -m pip install -e .
python -m sql_rewrite_bench.user_run --help
```

不安装时：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --help
```

也可以使用轻量 wrapper：

```bash
python scripts/user/run_user_benchmark.py --help
```

## 最小命令

创建一个包含 Common-core case id 的文本文件，例如：

```text
PERF_0006
PERF_0007
```

在这些选定行上运行一个 adapter：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/demo_run
```

等价的 wrapper 命令：

```bash
python scripts/user/run_user_benchmark.py \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/demo_run
```

## Dry-run 示例

Dry-run 会解析选定行并写入本地运行文件，但不会调用 adapter：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python my_rewriter.py" \
  --out runs/user/demo_dry_run \
  --dry-run
```

Dry-run 的 ledger 行使用：

- `adapter_invoked=false`
- `candidate_generated=false`
- `extraction_status=skipped_dry_run`
- `execution_status=not_run_non_db_mvp`
- `checker_status=not_run_non_db_mvp`
- `exact_status=not_evaluated_non_db_mvp`
- `timed_status=not_timed_non_db_mvp`
- `failure_bucket=none`

## 公开 Smoke 示例

使用 `--smoke` 可以进行确定性的小型 Common-core 选择。它会为请求的 engine 选择 `PERF_0006` 和 `CONS_0005`，且不需要 case-list 文件。

Dry-run smoke 不会调用 adapter：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/smoke_dry_run \
  --dry-run
```

Adapter-capture smoke 会调用公开的 no-op 示例 adapter：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/smoke_dummy_adapter
```

示例 adapter 会把 source SQL 复制到 candidate 路径。这些 smoke 输出仍然只是本地诊断。

## 可读性与检查命令

以下命令用于运行前检查和解释。它们不会调用 adapter，不会创建 `runs/user/...` 输出，不会执行 DB/checker，不会计算官方指标，不会更新 `reports/` 或 `results/`，也不会创建 leaderboard。

列出 `Common-core v0` case packages：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --list-cases
```

按 pool 过滤：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --list-cases
```

解释 smoke 选择：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --explain-selection
```

查看本地 user-run 输出 schema：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema
```

这些 schema 是本地诊断输出说明，不是 official metrics、paper tables、retained evidence、reports/results updates 或 leaderboard input。

## Adapter 示例

公开的 no-op 示例 adapter 会把确定性的 candidate SQL 写入 runner 提供的路径：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/demo_noop_adapter
```

Adapter 可以通过以下两种方式之一生成 candidate SQL：

- 将 candidate SQL 写入 `SQLRB_CANDIDATE_SQL_PATH` 指定的文件路径。
- 将 candidate SQL 打印到 stdout。

如果两者都存在，则 workspace 中的 `candidate.sql` 优先于 stdout。

## 可选 SQLGlot Adapter 示例

仓库包含可选的 SQLGlot 用户入口 adapter，仅用于 candidate generation。它们不会执行 SQL、运行 checkers、收集计时、计算官方指标、更新论文结果、更新 retained evidence，也不会创建 leaderboard。

Dry-run 不需要 SQLGlot，因为 adapter 不会被调用：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/sqlglot_noop_dry_run \
  --dry-run
```

在运行真实 adapter 路线之前，请安装可选 SQLGlot 支持：

```bash
python -m pip install -e ".[sqlglot]"
```

SQLGlot no-op 路线：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/sqlglot_noop_demo
```

SQLGlot optimize 路线：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list path/to/case_ids.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize" \
  --out runs/user/sqlglot_optimize_demo
```

两个路线都会把 candidate SQL 写入由 `SQLRB_CANDIDATE_SQL_PATH` 提供的逐行 user-run workspace 路径。如果 SQLGlot 不可用或解析失败，adapter 会以非零状态退出，而不是静默回退到原始 source SQL。

## 可选本地 PostgreSQL 诊断

Runner 也提供可选的 PostgreSQL DB/checker 诊断：

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/postgres_local_diagnostic \
  --enable-db-execution \
  --enable-checker
```

该模式仅作为本地诊断支持。它会通过每个 case manifest 的 `schema.external_profile` 和 `schemas/` 下的外部 schema package 来解析 PostgreSQL DDL/load 文件。如果外部 schema profile 或 PostgreSQL DDL/load 路径缺失，它会 fail closed。它需要通过 `SQLRB_POSTGRES_DSN` 或标准 libpq 环境变量配置本地 PostgreSQL，并且需要 `psql` CLI。

DB/checker 诊断输出仍保存在 `runs/user/<run_id>/` 下。它们不是官方指标、retained evidence、reports、results、paper outputs 或 leaderboard rows。

## Adapter 环境变量

Runner 会为每次 adapter 调用提供这些变量：

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

Adapter 命令会使用 `shlex.split` 并以 `shell=False` 的方式调用。子进程工作目录为仓库根目录。

## 输出目录规则

输出根目录必须位于：

```text
runs/user/<run_id>/
```

Runner 会拒绝 case-local 路径、`reports/`、`results/`、绝对路径，以及类似 `../demo` 的父级相对路径。

User-run 输出只是本地实验输出。它们不是 retained paper evidence，也不应提交到仓库。

## 输出文件

每次运行会写入：

- `config.yaml`：命令参数、选定 scope、输出策略标志，以及 no-leaderboard/no-paper 边界标志。
- `selected_cases.csv`：元数据解析后的选定 Common-core case-engine 行。
- `candidate_sql/`：捕获到的用户生成 candidate SQL，如果有生成。
- `workspaces/`：逐行 adapter stdout/stderr 诊断和 workspace 文件。
- `ledger.csv`：每个选定 case-engine 行对应一条本地诊断行。
- `summary.json`：本地诊断计数和边界标志。
- `failures.csv`：`failure_bucket` 不为 `none` 的行。
- `report.md`：本地报告，包含 selected scope、diagnostic funnel、failure buckets、artifact links 和 warnings。
- `quality_summary.json`：从 `ledger.csv` 汇总出的本地 denominator-aware diagnostic funnel。
- `quality_report.md`：`quality_summary.json` 的人类可读本地诊断报告，不是 paper table。
- `tag_slices.csv`：基于 retained manifest/taxonomy tags 的本地 diagnostic slices，不是 tag score 或 ranking。

## 当前限制

- 默认公开 smoke 和 adapter-capture 命令不会执行数据库查询。
- 默认公开 smoke 和 adapter-capture 命令不会运行 checkers。
- 不收集计时。
- 没有官方 benchmark metrics。
- 不渲染论文表格。
- 不更新论文结果。
- 不更新 retained evidence。
- 没有 leaderboard。
- SQLGlot adapters 仅用于 candidate generation，且是可选的。
- 没有 Calcite 或 R-Bot baseline adapter 实现。
- 没有论文复现 CLI。
- MVP 中不支持非 Common-core 选择。

可选的本地 PostgreSQL 诊断不是完整的论文复现，也不会改变任何官方 benchmark result。

User-run 输出不得写入 `cases/`、case-local `runs/`、`case_sets/`、`inventory/`、`reports/` 或 `results/`。
