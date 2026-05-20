# 用户入口数据流与文件位置

本文说明当前 user-entry / smoke runner 的数据流。它不是完整论文复现说明，也不定义官方 metrics、paper tables、retained evidence 或 leaderboard。

## 一句话流程

CLI 参数 -> `case_sets/common_core_v0/` -> `cases/{POOL}/{CASE_ID}/sql/source.sql` -> adapter -> `runs/user/{run_name}/candidate_sql/` -> `ledger.csv` / `summary.json` / `report.md`

## 入口文件

| 阶段 | 文件或目录 | 说明 |
|---|---|---|
| 主 CLI 入口 | `src/sql_rewrite_bench/user_run.py` | `python -m sql_rewrite_bench.user_run` 的实现入口。 |
| 薄 wrapper | `scripts/user/run_user_benchmark.py` | 从仓库根目录补充 `src/` import path 后调用同一个 CLI。 |
| 示例 adapter | `examples/user/noop_adapter.py` | 公开 smoke 示例 adapter。 |

## case 选择

| 阶段 | 文件或目录 | 说明 |
|---|---|---|
| case selection implementation | `src/sql_rewrite_bench/case_selection.py` | 从 `case_sets/common_core_v0/` 的 case-set CSV 解析选择；不通过扫描 `cases/` 目录决定 membership。 |
| case-set membership file | `case_sets/common_core_v0/cases.csv` | 定义 40 个 Common-core case package 及 package path。 |
| Track A denominator file | `case_sets/common_core_v0/denominator_same_engine_120.csv` | 定义 120 个 planned same-engine case-engine rows。 |

## case package 输入

| 阶段 | 文件或目录 | 说明 |
|---|---|---|
| case package root | `cases/{POOL}/{CASE_ID}/` | 单个 benchmark unit 的 package 根目录。 |
| source SQL | `cases/{POOL}/{CASE_ID}/sql/source.sql` | 通过 `SQLRB_SOURCE_SQL_PATH` 传给 adapter。 |
| package manifest | `cases/{POOL}/{CASE_ID}/manifest.yaml` | 记录 package manifest、provenance、SQL、schema、checker 和 validation references。 |
| schema profile | `cases/{POOL}/{CASE_ID}/schema/schema_profile.yaml` | case-facing schema summary；不是用户输出目录。 |
| external schema package | `schemas/{schema_id}/...` | PostgreSQL DDL/load 从 `schema.external_profile` 和 external profile metadata 解析；不要硬编码固定 schema 文件名。 |

## adapter 合约

Runner 会为每次 adapter 调用提供这些环境变量：

- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CANDIDATE_SQL_PATH`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_CASE_DIR`

Adapter 从 `SQLRB_SOURCE_SQL_PATH` 读取 source SQL，并把 candidate SQL 写到 `SQLRB_CANDIDATE_SQL_PATH`。Candidate 捕获优先级是 workspace `candidate.sql` 优先，stdout 次之。

## 输出目录

| 输出 | 位置 | 说明 |
|---|---|---|
| output root | `runs/user/{run_name}/` | 本地用户运行输出根目录。 |
| selected rows | `runs/user/{run_name}/selected_cases.csv` | 本次选择出的 case-engine rows。 |
| run config | `runs/user/{run_name}/config.yaml` | CLI 参数、scope 和边界标记。 |
| candidate SQL capture | `runs/user/{run_name}/candidate_sql/` | adapter 捕获到的 candidate SQL。 |
| adapter workspaces | `runs/user/{run_name}/workspaces/` | per-row adapter stdout/stderr 和 workspace 文件。 |
| local diagnostic ledger | `runs/user/{run_name}/ledger.csv` | 本地诊断 ledger，不是官方 metrics 输入。 |
| local summary | `runs/user/{run_name}/summary.json` | 本地诊断计数和边界标记。 |
| local failures | `runs/user/{run_name}/failures.csv` | 非 `none` failure bucket rows。 |
| local report | `runs/user/{run_name}/report.md` | 本地运行摘要，不是 paper table。 |
| optional PostgreSQL diagnostic helper | `src/sql_rewrite_bench/postgres_execution.py` | opt-in DB diagnostic helper；默认 smoke 不使用。 |
| optional checker helper | `src/sql_rewrite_bench/local_result_checker.py` | opt-in local checker diagnostic helper；默认 smoke 不使用。 |
| output schema / typed row model | `src/sql_rewrite_bench/user_run_schema.py` | 定义 local ledger/status 字段和值域。 |

## 可选 PostgreSQL / checker 诊断

- 默认 smoke 不执行 DB query，不运行 checker。
- `--enable-db-execution` 是 opt-in。
- `--enable-checker` 是 opt-in。
- PostgreSQL DDL/load 通过 manifest `schema.external_profile` 和 external schema metadata 解析。
- 缺 metadata 时 fail closed。
- 这些输出仍是本地 diagnostics，不是官方 metrics、paper tables、reports/results 或 leaderboard。

## 边界

- user-entry outputs are local diagnostics only。
- no official metrics。
- no paper table rendering。
- no reports/results updates。
- no retained evidence creation。
- no global leaderboard。
- no full paper reproduction claim。
